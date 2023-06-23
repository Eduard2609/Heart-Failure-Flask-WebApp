from flask import Flask, render_template, flash, redirect, url_for
from forms import  SendToHeartApiForm, RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'cheie_secreta'


@app.route('/')

@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SendToHeartApiForm()
    if form.validate_on_submit():
        return render_template('home.html', form=form, response = form.response.data)
    return render_template('home.html', form = form)

@app.route('/history')
def history():
    return render_template('history.html', title='History')

@app.route('/about')
def about():
    return render_template('about.html', title='About')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)