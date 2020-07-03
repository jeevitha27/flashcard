import os, json
from flask import Flask, request, Blueprint, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import current_user
from notesproject import db
from notesproject.models import *

create = Blueprint('create', __name__)


@create.route('/create',methods=['POST'])
def main_form():
    if request.method == 'POST':
        return redirect(url_for('main.sample'))
    else:
        return render_template('create.html')


@create.route('/sample', methods=['POST'])
def sample():
    category = request.form['Category']
    title = request.form['Title']
    term1 = request.form['term1']
    def1 = request.form['def1']
    term2 = request.form['term2']
    def2 = request.form['def2']
    term3 = request.form['term3']
    def3 = request.form['def3']
    term4 = request.form['term4']
    def4 = request.form['def4']
    term5 = request.form['term5']
    def5 = request.form['def5']
    
    fc = FlashCard(title=title, category_name=category, user_id=current_user.id)
    db.session.add(fc)
    db.session.commit()
    fcd = FlashCardData(
        flash_card_id=fc.id,
        question=term1,
        answer=def1,
    )
    db.session.add(fcd)
    db.session.commit()
    fcd = FlashCardData(
        flash_card_id=fc.id,           
        question=term2,
        answer=def2
    )
    db.session.add(fcd)
    db.session.commit()
    return render_template(
        'create.html',
        msg="The FlashCard is created with-",
        msgC="Catgeory: ",
        msgT="Title: ",
        catg=category,
        tle=title,
        link=fc.id
)
    
