from flask import render_template, request, Blueprint
from flask_login import current_user
from notesproject import db
from notesproject.models import *
import json

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/home2")
def home2():
    return render_template("home2.html")


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/setup_database")
def make_new():
    db.create_all()
    print("got this far")
    return "Database Should have been created!"


@main.route("/test_database")
def check_queries():
    users = User.query.all()
    fc = FlashCard.query.all()
    print(vars(users[0]))
    return "Check Console Output"


@main.route("/addsampledata")
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
    fc = FlashCard(title="Other Sample List", category_name="General", user_id=current_user.id)
    db.session.add(fc)
    db.session.commit()
    fcd_1 = FlashCardData(
        flash_card_id=fc.id,
        question="Do you have good notes?",
        answer="I'm not telling!"
    )
    fcd_2 = FlashCardData(
        flash_card_id=fc.id,
        question="How has your ECU experience been so far?",
        answer="It depends on my grade in this class!"
    )
    fcd_3 = FlashCardData(
        flash_card_id=fc.id,
        question="Is this enough for a second list?",
        answer="Maybe we should one more."
    )
    fcd_4 = FlashCardData(
        flash_card_id=fc.id,
        question="Well what should the last question say?",
        answer="Don't be smart, just put something."
    )
    db.session.add(fcd_1)
    db.session.add(fcd_2)
    db.session.add(fcd_3)
    db.session.add(fcd_4)
    db.session.commit()
    return "Check Console output"


@main.route('/viewflashcards')
def view_sample():
    fc = FlashCard.query.all()

    return render_template('sample.html', flash_cards=fc)


@main.route('/cleardata')
def delete_flashcards():
    for value in db.session.query(FlashCardData.id).distinct():
        fcd = FlashCardData.query.get(value[0])
        db.session.delete(fcd)
    db.session.commit()
    for value in db.session.query(FlashCard.id).distinct():
        fc = FlashCard.query.get(value[0])
        db.session.delete(fc)
    db.session.commit()
    return "Rows Deleted"


@main.route("/edit/<id>")
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
    return render_template('edit.html', flash_card=flash_card)


@main.route("/edit_question/<id>", methods=["PUT"])
def update_question(id):
    fcd = FlashCardData.query.filter_by(id=id).first()
    json_data = request.get_json()
    fcd.question = json_data.get('text')
    db.session.commit()

    return "Success"


@main.route("/edit_answer/<id>", methods=["PUT"])
def update_answer(id):
    fcd = FlashCardData.query.filter_by(id=id).first()
    json_data = request.get_json()
    fcd.question = json_data.get('text')
    db.session.commit()

    return "Success"

@main.route("/edit_category/<id>", methods=["PUT"])
def update_category(id):
    print(id)
    fc = FlashCard.query.filter_by(id=id).first()
    print(fc)
    json_data = request.get_json()
    fc.category_name = json_data.get('text')
    db.session.commit()

    return "Success"


@main.route("/edit_title/<id>", methods=["PUT"])
def update_title(id):

    fc = FlashCard.query.filter_by(id=id).first()
    json_data = request.get_json()
    fc.title = json_data.get('text')
    db.session.commit()

    return "Success"
