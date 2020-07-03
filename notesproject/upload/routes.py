import os, json
from flask import Flask, request, Blueprint, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import current_user
from notesproject import db
from notesproject.models import *
from notesproject.upload import util

upload = Blueprint('upload', __name__)

# get current app directory
dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/data/'

# upload.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@upload.route("/upload", methods=['GET', 'POST'])
def main_form():

	if request.method == 'POST':
		# request.file <class 'werkzeug.datastructures.FileStorage'>
		# request.url is http://127.0.0.1:5000/
		# check if the post request has the file part
		if 'file' not in request.files:
			log = 'no file field in request.'
			return render_template(
				'upload.html',
				filename='',
				size=0,
				column_names=json.dumps([]),
				data_part=json.dumps([]),
				log=log
			);
		# print(request.files['file'])
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			# This part should use flash to output information
			log = 'Empty filename.'
			return render_template(
				'upload.html',
				filename='',
				size=0,
				column_names=json.dumps([]),
				data_part=json.dumps([]),
				log=log
			);
		if not util.allowed_file(file.filename):
			log = 'Wrong Filetype.'
			return render_template(
				'upload.html',
				filename='',
				size=0,
				column_names=json.dumps([]),
				data_part=json.dumps([]),
				log=log
			);
		if file and util.allowed_file(file.filename):
			# get filename in a safe way
			filename = secure_filename(file.filename)
			file_and_path = os.path.join(UPLOAD_FOLDER, filename)
			file.save(file_and_path)
			column_names, data_part = util.preview_csv(UPLOAD_FOLDER + filename)

			category = request.form['Category']
			title = request.form['Title']
			fc = FlashCard(title=title, category_name=category, user_id=current_user.id)
			db.session.add(fc)
			db.session.commit()
			for row in data_part:
				fcd = FlashCardData(
					flash_card_id=fc.id,
					question=row[0],
					answer=row[1]
				)
				db.session.add(fcd)
			db.session.commit()

			return render_template(
				'upload.html',
				filename=file.filename,
				size=os.stat(file_and_path).st_size,
				column_names=json.dumps(column_names),
				data_part=json.dumps(data_part),
				log='',
				msg="CSV file loaded for -",
				msgC="Catgeory: ",
				msgT="Title: ",
				catg=category,
				tle=title,
				link=fc.id
			)
	elif request.method == 'GET':
		return render_template('upload.html')

