from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from notesproject import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# This is the flash card set.  It has the id of the card set or set of notes.
class FlashCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    category_name = db.Column(db.String(255))
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    flash_card_data = db.relationship('FlashCardData', lazy=True)


# These are the individual note cards. It holds one individual flash card or note card.
class FlashCardData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flash_card_id = db.Column(
        db.Integer,
        db.ForeignKey('flash_card.id'),
        nullable=False
    )
    title = db.Column(db.String())
    question = db.Column(db.Text())
    answer = db.Column(db.Text())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


# These are individual answers reported.
class FlashCardScores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flash_card_data_id = db.Column(
        db.Integer,
        db.ForeignKey('flash_card_data.id'),
        nullable=False
    )
    title = db.Column(db.String())
    is_correct_answer = db.Column(db.Boolean())
    answer = db.Column(db.Text())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

