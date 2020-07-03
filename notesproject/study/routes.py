from flask import render_template, request, Blueprint, Response, jsonify
from flask_login import current_user
from notesproject.models import *
from sqlalchemy.sql import text
import json
from notesproject.study import utils

study = Blueprint('study', __name__)


@study.route("/practice/<id>")
def practice(id):
    try:
        id = int(id)
    except ValueError:
        return render_template('errors/404.html'), 404
    if id is None or id <= 0:
        return render_template('errors/404.html'), 404
    flash_card = FlashCard.query.get(id)
    if flash_card.user_id != current_user.id:
        return render_template('errors/404.html'), 404
    return render_template('practice.html', flash_card=flash_card, card_set=id)



@study.route("/review/<id>")
def review_list(id):
    try:
        id = int(id)
    except ValueError:
        return render_template('errors/404.html'), 404
    if id is None or id <= 0:
        return render_template('errors/404.html'), 404
    flash_card = FlashCard.query.get(id)
    if flash_card.user_id != current_user.id:
        return render_template('errors/404.html'), 404
    return render_template('review.html', flash_card=flash_card)

@study.route("/api/flashcard", methods=['POST'])
def mark_answer():
    jsonData = request.get_json()
    card_set_id = jsonData['card_set']
    flash_card_id = jsonData['flashcard']
    correct = jsonData['correct']

    card_set = FlashCard.query.get(1)
    if card_set.user_id != current_user.id:
        js = json.dumps({'error': 'Authentication Error'})
        resp = Response(js, status=401, mimetype='application/json')
        return resp

    flash_card_score = FlashCardScores(
        flash_card_data_id=flash_card_id,
        title="",
        is_correct_answer=correct,
        answer=""
    )
    db.session.add(flash_card_score)
    db.session.commit()

    js = json.dumps({'success': 'Data Recorded', 'correct': 1})
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@study.route('/checkstuff')
def checkstuff():
    fcs = FlashCardScores.query.all()
    print(vars(fcs[2]))
    return "Check Console"

@study.route('/results')
def see_data():
    statement = text("""
        SELECT
            fcs.id, 
            fcs.flash_card_data_id,
            fcs.is_correct_answer,
            fc.title,
            fc.category_name  
        FROM flash_card_scores fcs
            LEFT JOIN flash_card_data fcd ON fcd.id = fcs.flash_card_data_id
            LEFT JOIN flash_card fc ON fc.id = fcd.flash_card_id
        WHERE
            fc.user_id = :current_user_id
    """)
    query_data = db.session.query(FlashCardScores).from_statement(statement).params(current_user_id=current_user.id).all()
    titles = utils.get_titles(query_data)
    data = {
        "total_count": len(query_data),
        "total_right": utils.get_total_right(query_data),
        "total_wrong": utils.get_total_wrong(query_data),
        "scores": json.dumps(utils.get_scores(query_data)),
        "titles": titles,
        "json_titles": json.dumps(titles)
    }

    return render_template('results.html', data=data)
