
import os
import pandas as pd
from flask import (Flask, render_template, request,
                   redirect, url_for, flash, session)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from modules.data_loader import load_dataframe, allowed_file
from modules.data_summary import get_summary
from modules.eda import generate_visualizations

# ── App config ───────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = 'mlreadyai_secret_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Folder where uploaded files are stored temporarily
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024   # 50 MB limit

# ── Database ─────────────────────────────────────────────────
db = SQLAlchemy(app)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100))
    email    = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

with app.app_context():
    db.create_all()

# ── In-memory DataFrame store ────────────────────────────────
_store = {}

def get_df():
    """Return the currently loaded DataFrame (or None)."""
    return _store.get('df')

def set_df(df):
    """Save a DataFrame into the in-memory store."""
    _store['df'] = df

# ── Auth guard helper ─────────────────────────────────────────
def login_required():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    return None

# =============================================================
# AUTH ROUTES
# =============================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name             = request.form['name']
        email            = request.form['email']
        password         = request.form['password']
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
        email    = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email.strip()).first()
        if user and check_password_hash(user.password, password):
            session['user_id']   = user.id
            session['user_name'] = user.name
            flash('Login successful! Welcome back.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


# =============================================================
# MODULE 1 — Home
# =============================================================

@app.route('/')
def home():
    return render_template('index.html')


# =============================================================
# Dashboard (protected)
# =============================================================

@app.route('/dashboard')
def dashboard():
    guard = login_required()
    if guard:
        return guard
    return render_template('dashboard.html', name=session['user_name'])


# =============================================================
# MODULE 2 & 3 — Upload + Parse
# =============================================================

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    GET  -> show the upload form
    POST -> receive the file, parse it into a DataFrame, store it
    """
    guard = login_required()
    if guard:
        return guard

    if request.method == 'POST':
        # 1. Check a file was included in the form
        if 'dataset' not in request.files:
            flash('No file part in the request.', 'error')
            return redirect(url_for('upload'))

        file = request.files['dataset']

        # 2. Check the user actually selected a file
        if file.filename == '':
            flash('Please select a file before uploading.', 'error')
            return redirect(url_for('upload'))

        # 3. Validate extension
        if not allowed_file(file.filename):
            flash('Unsupported file format. Please upload CSV, Excel, JSON, XML or HTML.', 'error')
            return redirect(url_for('upload'))

        # 4. Save the file safely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # 5. Parse the file into a DataFrame (MODULE 3)
        try:
            df = load_dataframe(filepath)
        except Exception as e:
            flash(f'Could not read file: {e}', 'error')
            return redirect(url_for('upload'))

        # 6. Store in memory and remember the filename in session
        set_df(df)
        session['filename'] = filename

        flash(f'"{filename}" uploaded successfully - {df.shape[0]} rows x {df.shape[1]} columns.', 'success')
        return redirect(url_for('summary'))    # -> Module 4

    # GET request -> just show the upload form
    return render_template('upload.html')


# =============================================================
# MODULE 4 — Data Summary
# =============================================================

@app.route('/summary')
def summary():
    """
    Shows:
      - Key metrics (rows, cols, missing cols, numeric cols)
      - Per-column info table (name, dtype, missing count/pct)
      - Descriptive statistics for numeric columns
      - First 5 rows preview
    """
    guard = login_required()
    if guard:
        return guard

    df = get_df()
    if df is None:
        flash('Please upload a dataset first.', 'error')
        return redirect(url_for('upload'))

    summary_data = get_summary(df)
    filename     = session.get('filename', 'dataset')
    return render_template('summary.html', summary=summary_data, filename=filename)


# =============================================================
# MODULE 5 — EDA Visualizations
# =============================================================

@app.route('/eda')
def eda():
    """
    Generates and displays:
      - Histograms for numeric columns
      - Bar charts for categorical columns
      - Correlation Heatmap
    Uses Base64 encoding to embed plots directly in HTML.
    """
    guard = login_required()
    if guard:
        return guard

    df = get_df()
    if df is None:
        flash('Please upload a dataset first.', 'error')
        return redirect(url_for('upload'))

    plots    = generate_visualizations(df)
    filename = session.get('filename', 'dataset')
    return render_template('eda.html', plots=plots, filename=filename)


# ── PLACEHOLDER routes (will be filled in future modules) ────

# ── Run ──────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
