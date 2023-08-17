from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from weather import main as get_weather
from forms import RegisterForm, LoginForm
from models import User
from main import app
from main import db
from flask_login import login_user, logout_user


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
