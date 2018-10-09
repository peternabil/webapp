from blog0.models import User,Post,Team
from flask import render_template, url_for, flash, redirect
from blog0.form0 import RegForm,LoginForm
from blog0 import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required


@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():
    # return render_template('home.html')
    return render_template('mainpage.html')

# @app.route('/link')
# def link():
#     return render_template('link1.html')


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for {}!'.format(form.username.data),'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/current_user.username')
def account():
    return render_template('account.html',title='Account')



@app.route('/score')
def score():
    # paths = {"acmilan","ahly","ajax","arsenal","asmonaco","athelieticomadrid","barcelona","bayernmunich","brussiadortmund","brightonalbion","bournemouth","bunlry","chelsea","everton","fulham","huddersfield","intermilan","juventus","leicestercity","liverpool","mancity","manunited","napoli","newcastle","zamalek","pyramids","rcdespanyol","realmadrid","realsociedad","roma","tottenham","valencia","watford","westbromwich","westhamunited"}
    return render_template('scoring.html')
