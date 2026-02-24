from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

with app.app_context():
    db.create_all()

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not name or len(name.strip()) < 2:
            flash('Name must be at least 2 characters long.', 'error')
            return redirect(url_for('register'))

        if not email or '@' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('register'))

        if (len(password) < 8 or
                not any(c.isdigit() for c in password) or
                not any(c.isalpha() for c in password) or
                not any(not c.isalnum() for c in password)):
            flash('Password must be at least 8 characters and contain letters, numbers, and special characters.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email.strip()).first():
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name.strip(), email=email.strip(), password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email.strip()).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful! Welcome back.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['user_name'])


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
