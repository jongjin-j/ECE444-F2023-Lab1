from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, StopValidation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret key'
bootstrap = Bootstrap(app)
moment = Moment(app)

def email_check(form, field):
    if not '@' in field.data:
        error_message = "Please include an '@' in the email address. '{}' is missing an '@'.".format(field.data)
        raise StopValidation(error_message)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), email_check])
    submit = SubmitField('Submit')
    
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data

        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['email'] = form.email.data

        return redirect(url_for('index'))
    
    uoft_email = True

    if not 'utoronto' in session['email']:
        uoft_email = False

    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), uoft_email=uoft_email)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)