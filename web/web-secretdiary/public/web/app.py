import os
import string
from time import time, sleep
from datetime import datetime

from flask import Flask, render_template, flash, request, redirect, url_for, Response, make_response
from flask_login import login_user, UserMixin, login_required, logout_user, current_user, login_manager, LoginManager
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue
from wtforms import StringField, validators
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect

from visitor import visit_user_page

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db.init_app(app)
CSRFProtect(app)
my_login_manager = LoginManager()
my_login_manager.init_app(app)
chars = string.ascii_letters
admin_password = ''.join(chars[os.urandom(1)[0] % len(chars)] for i in range(16))
FLAG = os.environ.get("CHALLENGE_FLAG") or "flag{default}"

q = Queue(connection=Redis(host="redis"))
last_visit = {}
VISIT_COOLDOWN = 20


class User(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    is_active = db.Column(db.Boolean, default=True)
    password = db.Column(db.String(32))
    aboutme = db.Column(db.String(256))

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    text = db.Column(db.Text, default="")
    date = db.Column(db.String(256))
    img_src = db.Column(db.String(256))
    img_type = db.Column(db.String(256), default="")

class UserSession(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        return self.user.username

    def is_active(self):
        return self.user.is_active


def current_date():
    return datetime.now().strftime("%H:%M on %b %d, %Y")


def contains_illegal_char(list_items):
    blocked = ["&", ">" "<", "'", '"']
    for item in list_items:
        for block in blocked:
            if block in item:
                return True
    return False


@app.login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User, user_id)
    return UserSession(user) if user else None


class LoginForm(FlaskForm):
    username = StringField(validators=[validators.Length(min=2, max=64)])
    password = StringField(validators=[validators.Length(min=2, max=64)])


class RegisterForm(LoginForm):
    aboutme = StringField(validators=[validators.Length(min=2, max=256)])


class DiaryEntryForm(FlaskForm):
    text = StringField(validators=[validators.Length(min=2, max=2048)])
    img_src = StringField(validators=[validators.Length(min=2, max=256)])
    img_type = StringField(validators=[validators.Length(min=0, max=256)])


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/tryharder')
def tryharder():
    return render_template('tryharder.html')

@app.route('/healthcheck')
def healthcheck():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def do_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.get(User, form.username.data)
        if user and user.password == form.password.data:
            login_user(UserSession(user))
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Wrong username or password', 'warning')
            return render_template('login.html')
    else:
        flash(f'Invalid log in: {form.errors}', 'error')
        return render_template('login.html')


@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return url_for('index')
    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def do_register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = db.session.get(User, form.username.data)
        if existing:
            flash(f'User {form.username.data} already exists', 'danger')
            return redirect(url_for('register'))
        else:
            db.session.add(User(username=form.username.data, password=form.password.data, aboutme=form.aboutme.data))
            db.session.commit()
            flash('Signed up successfully, redirecting to log in page', 'success')
            return redirect(url_for('login'))
    else:
        flash(f'Invalid sign up data: {form.errors}', 'danger')
        return redirect(url_for('register'))


@app.route('/visit/', methods=['POST'])
@login_required
def do_visit():
    ip = request.remote_addr
    last_timestamp = last_visit.get(ip)
    current_timestamp = time()
    if last_timestamp and (current_timestamp - last_timestamp < VISIT_COOLDOWN):
        flash(f"You have recently asked for a visit, please wait at least {VISIT_COOLDOWN} seconds between visits", 'warning')
        app.logger.info(f"Rejected enqueue {ip}, current: {current_timestamp}, last {last_timestamp}")
    else:
        last_visit[ip] = current_timestamp
        visit_url = f"http://secretdiary:8080/profile/?username={current_user.get_id()}"
        q.enqueue(visit_user_page, visit_url, admin_password)
        flash("Enqueued successfully, Santa Claus will review your diary soon. Ho Ho Ho!", 'success')
        app.logger.info(f"Enqueued visit from {ip} to {visit_url}, santaclaus pw: {admin_password}")

    return redirect(url_for('profile'))


@app.route('/profile/', methods=['GET'])
@login_required
def profile():
    username = request.args.get("username")
    if username and current_user.get_id() == "santaclaus":
        # Santa can check if any user has been a good boy or girl
        target_user = db.session.get(User, username)
        if target_user:
            return render_profile(target_user)
        else:
            flash(f"User {username} not found", 'danger')
    elif username:
        flash("Only Santa Claus can visit other users. Naughty Hacker...", 'danger')

    return render_profile(current_user.user)


def render_profile(user):
    entries = (db.session
               .query(DiaryEntry)
               .filter(DiaryEntry.username == user.username)
               .all())
    return render_template("profile.html", user=user, entries=entries)


@app.route('/profile/', methods=['POST'])
@login_required
def add_entry():
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(32))
    # text = db.Column(db.Text, default="")
    # date = db.Column(db.String(256))
    # img_src = db.Column(db.String(256))
    # img_type = db.Column(db.String(256), default="")
    form = DiaryEntryForm()
    if form.validate_on_submit():
        if contains_illegal_char([form.text.data, form.img_src.data, form.img_type.data]):
            return redirect(url_for('tryharder'))

        user = db.session.get(User, current_user.get_id())
        db.session.add(DiaryEntry(
            username=user.username,
            text=form.text.data,
            date=current_date(),
            img_src=form.img_src.data,
            img_type=form.img_type.data
        ))
        db.session.commit()
        flash(f'Added new entry to diary', 'success')
    else:
        flash(f'Invalid diary entry: {form.errors}', 'danger')

    return redirect(url_for('profile'))


@app.login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


with app.app_context():
    print("Waiting 10 seconds before initializing DB...")
    sleep(10)
    db.create_all()
    print("DB initialized")
    santaclaus = db.session.get(User, "santaclaus")
    if not santaclaus:
        db.session.add(User(
            username="santaclaus",
            password=admin_password,
            aboutme="The man, the myth, the legend"
        ))
        db.session.add(DiaryEntry(
            username="santaclaus",
            text=f"Ho ho ho, I'm Santa Claus. Today, I found Pere Fouettard had dismembered a child. I have decided to take him under my service. Naughty children no more. Ho ho ho. {FLAG}",
            date=current_date(),
            img_src="/static/santaclaus.png",
            img_type="sensitive"
        ))
        db.session.commit()
        print(f"Santa Claus password: {admin_password}")
    else:
        print(f"Santa Claus password: {santaclaus.password}")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
