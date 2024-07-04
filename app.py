from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from forms import LoginForm, RegistrationForm, EditProfileForm  # Импортируем новую форму

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# In-memory user storage (for demonstration purposes)
users = {}

class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
@login_required
def home():
    return f'Hello, {current_user.username}! <a href="/logout">Logout</a> <a href="/edit_profile">Edit Profile</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        for user in users.values():
            if user.username == username and user.password == password:
                login_user(user)
                return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user_id = str(len(users) + 1)
        users[user_id] = User(user_id, username, email, password)
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.password = form.password.data
        flash('Profile updated successfully.')
        return redirect(url_for('home'))
    form.username.data = current_user.username  # Pre-fill the form with current username
    form.email.data = current_user.email  # Pre-fill the form with current email
    return render_template('edit_profile.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
