from flask import render_template, request, Blueprint
from flask_login import current_user
from notesproject import db
from notesproject.models import *


view = Blueprint('view', __name__)


@view.route("/list")
def main_form():
    fc = FlashCard.query.filter_by(user_id=current_user.id)
    return render_template('view.html', flash_cards=fc)
def search():
    if request.method == "POST":
        #fc = FlashCard.query.filter_by(user_id=current_user.id)
        statement = text("""
        SELECT
            *
        FROM flash_card_data
        WHERE
            question like '%s%' or answer like '%s%'
    """, request.form['search'], request.form['search'])
        fc = db.session.query(flash_card_data).from_statement(statement).params(current_user_id=current_user.id).all()
    else:
        fc = FlashCard.query.filter_by(user_id=current_user.id)

    return render_template('view.html', flash_cards=fc)



@view.route("/create")
def create_post():
    return render_template('create.html')

@view.route("/practice/<id>")
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


@view.route("/review/<id>")
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

@view.route("/test_database")
def check_queries():
    users = User.query.all()
    fc = FlashCard.query.all()
    print(vars(users[0]))
    return "Check Console Output"

@view.route("/edit")
def sample():
    fc = FlashCard(title="Sample List", category_name="General", user_id=current_user.id)
    db.session.add(fc)
    db.session.commit()
    fcd_1 = FlashCardData(
        flash_card_id=fc.id,
        question="What is your favorite ice cream?",
        answer="Moose Tracks"
    )
    fcd_2 = FlashCardData(
        flash_card_id=fc.id,
        question="Who is the best clean comedian?",
        answer="Michael Jr."
    )
    fcd_3 = FlashCardData(
        flash_card_id=fc.id,
        question="Is this enough for a list?",
        answer="Yes I think so."
    )
    db.session.add(fcd_1)
    db.session.add(fcd_2)
    db.session.add(fcd_3)
    db.session.commit()
    print(fc.id)

                 
