# PipelineX AI 🚀

> **Intelligent ML Automation Platform** — Automate the complete machine learning lifecycle from data ingestion and preprocessing to model training, evaluation, and export.

---

## 📸 Preview

![PipelineX AI Homepage](https://via.placeholder.com/900x400/0f172a/38bdf8?text=PipelineX+AI)

---

## 📌 About the Project

PipelineX AI is a web-based machine learning automation platform built as an **Industrial Training Project**. It provides a clean, modern interface for data scientists and ML practitioners to manage their entire ML workflow without writing repetitive boilerplate code.

---

## ✨ Features

| Module | Description |
|---|---|
| 🧹 **Data Cleaning** | Automated duplicate removal, null handling, and structured data correction |
| 📊 **EDA Module** | Interactive visualizations, correlation heatmaps, and statistical summaries |
| ⚙️ **Auto-Preprocessing** | Feature scaling, label encoding, and missing value imputation |
| 🤖 **Model Training** | Train classification/regression models with auto hyperparameter tuning |
| 📈 **Model Evaluation** | Accuracy, confusion matrix, ROC curves, and performance metrics |
| 💾 **Model Export** | Save and download production-ready models in `.pkl` or `.joblib` format |

---

## 🛠️ Tech Stack

- **Backend** — Python, Flask, Flask-SQLAlchemy
- **Database** — SQLite (via SQLAlchemy ORM)
- **Frontend** — HTML5, CSS3 (Glassmorphism UI), Jinja2 Templating
- **Auth** — Werkzeug password hashing (`generate_password_hash` / `check_password_hash`)
- **Session Management** — Flask Sessions & Flash Messages

---

## 📁 Project Structure

```
PipelineX_AI/
│
├── app.py                  # Main Flask application & route definitions
│
├── templates/              # Jinja2 HTML templates
│   ├── index.html          # Landing / Home page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   └── dashboard.html      # User dashboard (protected route)
│
├── static/                 # Static assets served by Flask
│   └── style.css           # Global stylesheet (glassmorphism theme)
│
├── instance/
│   └── users.db            # SQLite database (auto-generated on first run)
│
├── .gitignore              # Files and folders excluded from Git
└── README.md               # Project documentation (you are here)
```

---

## ⚙️ Getting Started

### Prerequisites

Make sure you have **Python 3.8+** installed.

```bash
python --version
```

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/PipelineX_AI.git
cd PipelineX_AI
```

### 2. Create a Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask flask-sqlalchemy werkzeug
```

### 4. Run the Application

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

---

## 🔐 Authentication Flow

```
/             →  Home / Landing Page
/register     →  Create a new account (name, email, password)
/login        →  Sign in with existing credentials
/dashboard    →  Protected page (requires active session)
/logout       →  Clears session and redirects to home
```

**Password Rules enforced at registration:**
- Minimum 8 characters
- Must contain at least one letter
- Must contain at least one number
- Must contain at least one special character

---

## 🗄️ Database

The project uses **SQLite** with SQLAlchemy ORM. The database file (`users.db`) is auto-created inside the `instance/` folder on the first run — no manual setup needed.

**User Model:**

| Column | Type | Details |
|---|---|---|
| `id` | Integer | Primary Key, Auto-increment |
| `name` | String(100) | User's full name |
| `email` | String(100) | Unique, used for login |
| `password` | String(200) | Stored as a secure hash |

---

## 🚧 Roadmap

- [x] User Registration & Login
- [x] Session Management & Flash Messages
- [x] Protected Dashboard Route
- [ ] CSV File Upload for Datasets
- [ ] Data Cleaning Module
- [ ] EDA Visualizations
- [ ] Auto-Preprocessing Pipeline
- [ ] ML Model Training Interface
- [ ] Model Evaluation Dashboard
- [ ] Model Export & Download

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo, create a feature branch, and open a pull request.

```bash
git checkout -b feature/your-feature-name
git commit -m "Add your feature"
git push origin feature/your-feature-name
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Shivang Verma**
- GitHub: [@Shivangverma7](https://github.com/Shivangverma7)

---

> *Built as part of an Industrial Training Project*
