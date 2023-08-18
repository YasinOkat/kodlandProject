from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from weather import main as get_weather
from forms import RegisterForm, LoginForm
from models import User, ExamScore
from main import app
from main import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/', methods=['GET', 'POST'])
def home_page():
    data_1 = None
    data_2 = None
    data_3 = None
    day1_name = None
    day2_name = None
    day3_name = None
    if request.method == 'POST':
        city = request.form['cityName']
        data_1, data_2, data_3, day1_name, day2_name, day3_name = get_weather(city)
    return render_template('index.html', day1_data=data_1, day2_data=data_2, day3_data=data_3,
                           day1_name=day1_name, day2_name=day2_name, day3_name=day3_name)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        return redirect(url_for('home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Kullanıcı oluşturulurken hata oluştu: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Başarılı! Hoşgeldin {attempted_user.username}')
            return redirect(url_for('home_page'))
        else:
            flash('Hatalı kullanıcı adı veya parola', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Çıkış yapıldı", category='info')
    return redirect(url_for('home_page'))


@app.route('/exam')
def exam_page():
    return render_template('exam.html')


@app.route('/submit_exam', methods=['POST', 'GET'])
@login_required
def submit_exam():
    user_score = calculate_user_score(request.form)

    print("User ID:", current_user.id)
    print("User Score:", user_score)

    existing_score = ExamScore.query.filter_by(user_id=current_user.id).first()
    if existing_score:
        existing_score.score = user_score
    else:
        exam_score = ExamScore(user_id=current_user.id, score=user_score)
        db.session.add(exam_score)

    db.session.commit()

    return redirect(url_for('exam_leadership_page'))


@app.route('/exam-leadership')
def exam_leadership_page():
    exam_scores = ExamScore.query.order_by(ExamScore.score.desc()).all()
    print(exam_scores)
    return render_template('exam-leadership.html', exam_scores=exam_scores)


def calculate_user_score(user_answers):
    correct_answers = {
        'q1': 'b',
        'q2': 'b',
        'q3': 'b',
        'q4': 'a',
        'q5': 'b'
    }

    print("Correct Answers:", correct_answers)
    print("User Answers:", user_answers)

    user_score = 0
    for question, user_answer in user_answers.items():
        if question in correct_answers and user_answer == correct_answers[question]:
            user_score += 20

    return user_score


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
