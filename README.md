# PipelineX AI 🚀

> **Intelligent ML Automation Platform** — Automate the complete machine learning lifecycle from data ingestion and preprocessing to model training, evaluation, and export.

---

## 📸 Preview

![PipelineX AI Homepage](/Homepage.png)

---

## 📌 About the Project

PipelineX AI is a web-based machine learning automation platform built as an **Industrial Training Project**. It provides a clean, modern interface for data scientists and ML practitioners to manage their entire ML workflow without writing repetitive boilerplate code.

The platform guides users through a structured 8-module pipeline — from raw file upload to a downloadable trained model — entirely in the browser. No Jupyter notebooks. No local pip installs.

---

## ✨ Features

| Module | Status | Description |
|---|---|---|
| 📂 **File Upload & Parsing** | ✅ Complete | Upload CSV, Excel, JSON, XML, or HTML — auto-parsed into a pandas DataFrame |
| 📋 **Data Summary** | ✅ Complete | Row/column counts, dtypes, missing value analysis, descriptive statistics |
| 📊 **EDA Visualizations** | ✅ Complete | Histograms with KDE, categorical bar charts, correlation heatmap |
| 🧹 **Data Cleaning** | ✅ Complete | Mean/median/mode imputation, IQR outlier detection & handling, duplicate removal, string normalization |
| ⚙️ **Feature Engineering** | ✅ Complete | LabelEncoder for categoricals, StandardScaler for numerics, per-column selection |
| 🎯 **Problem Selection** | ✅ Complete | Classification, Regression, or Clustering — target column picker |
| 🤖 **Model Training** | ✅ Complete | scikit-learn training with 80/20 split, 5 algorithms across 3 problem types |
| 📈 **Model Evaluation** | ✅ Complete | Accuracy, R², RMSE, Silhouette Score — colour-coded results |
| 💾 **Model Export** | ✅ Complete | Download trained model as `.pkl` via `joblib.dump()` |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, Flask 3.1 |
| **Database** | SQLite via Flask-SQLAlchemy ORM |
| **Frontend** | HTML5, CSS3 (custom dark UI), Jinja2 Templating |
| **Auth** | Werkzeug (`generate_password_hash` / `check_password_hash`) |
| **Data** | pandas 2.2, NumPy |
| **Visualization** | matplotlib 3.10, seaborn 0.13 |
| **ML** | scikit-learn 1.6, joblib |
| **Sessions** | Flask Sessions & Flash Messages |

---

## 📁 Project Structure

```
PipelineX_AI/
│
├── app.py                          # Main Flask application & all route definitions
│
├── modules/                        # Business logic — one file per pipeline stage
│   ├── data_loader.py              # Module 3   — File parsing & extension validation
│   ├── data_summary.py             # Module 4   — Shape, dtypes, missing values, describe()
│   ├── eda.py                      # Module 5   — Histograms, bar charts, heatmap (Base64)
│   ├── cleaning.py                 # Module 6–8 — Imputation, outlier handling, deduplication
│   ├── feature_engineering.py      # Module 9   — LabelEncoder & StandardScaler
│   └── model_training.py           # Module 12–13 — Training & evaluation logic
│
├── templates/                      # Jinja2 HTML templates
│   ├── index.html                  # Landing / Home page
│   ├── login.html                  # Login form
│   ├── register.html               # Registration form
│   ├── dashboard.html              # User dashboard (protected)
│   ├── upload.html                 # Dataset upload form
│   ├── summary.html                # Data summary report
│   ├── eda.html                    # EDA visualizations page
│   ├── cleaning.html               # Data cleaning controls
│   ├── feature_engineering.html    # Feature transformation controls
│   ├── problem_select.html         # Problem type & target column selection
│   ├── train.html                  # Model training & results
│   └── export.html                 # Model export / download
│
├── static/
│   └── style.css                   # Global stylesheet
│
├── uploads/                        # Temporary file storage (gitignored)
│
├── instance/
│   └── users.db                    # SQLite database (auto-generated on first run)
│
├── .gitignore
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites

Python 3.8 or higher is required.

```bash
python --version
```

### 1. Clone the Repository

```bash
git clone https://github.com/Shivangverma7/PipelineX_AI.git
cd PipelineX_AI
```

### 2. Create a Virtual Environment

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask flask-sqlalchemy werkzeug pandas numpy matplotlib seaborn scikit-learn joblib openpyxl lxml
```

Or if a `requirements.txt` is present:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 🔁 Application Routes

| Route | Method | Access | Description |
|---|---|---|---|
| `/` | GET | Public | Home / Landing page |
| `/register` | GET, POST | Public | Create a new account |
| `/login` | GET, POST | Public | Sign in with existing credentials |
| `/logout` | GET | Authenticated | Clears session, redirects to home |
| `/dashboard` | GET | Authenticated | User dashboard |
| `/upload` | GET, POST | Authenticated | Upload dataset file |
| `/summary` | GET | Authenticated | View data summary report |
| `/eda` | GET | Authenticated | View EDA visualizations |
| `/cleaning` | GET, POST | Authenticated | Apply data cleaning operations |
| `/feature_engineering` | GET, POST | Authenticated | Apply feature transformations |
| `/problem_select` | GET, POST | Authenticated | Select problem type and target column |
| `/train` | GET, POST | Authenticated | Train model and view evaluation metrics |
| `/export` | GET | Authenticated | Download trained model as `.pkl` |

---

## 🔐 Authentication

**Password rules enforced at registration:**
- Minimum 8 characters
- Must contain at least one letter
- Must contain at least one number
- Must contain at least one special character

Passwords are stored as salted hashes using Werkzeug's `generate_password_hash()`. Plaintext passwords are never persisted.

---

## 📤 File Upload — `modules/data_loader.py` (Module 3)

**Supported formats:** `.csv`, `.xlsx`, `.xls`, `.json`, `.xml`, `.html`, `.htm`

**Max file size:** 50 MB

| Function | Description |
|---|---|
| `allowed_file(filename)` | Validates the file extension against the allowed set |
| `load_dataframe(filepath)` | Reads the file and returns a parsed pandas DataFrame |

Uploaded files are saved to `uploads/`, parsed with the appropriate pandas reader (`read_csv`, `read_excel`, `read_json`, `read_xml`, `read_html`), and held in a module-level in-memory store for the duration of the session.

---

## 📋 Data Summary — `modules/data_summary.py` (Module 4)

| Function | Description |
|---|---|
| `get_summary(df)` | Returns a dict of all summary data needed to render `summary.html` |

**Keys returned by `get_summary()`:**

| Key | Type | Contents |
|---|---|---|
| `rows` | int | Total row count |
| `cols` | int | Total column count |
| `columns_info` | list of dicts | Per-column name, dtype, missing count, missing percentage |
| `stats` | dict of dicts | `df.describe()` output for all numeric columns (rounded to 3dp) |
| `preview_cols` | list | Column names for the table header |
| `preview_rows` | list of lists | First 5 rows as raw values |

---

## 📊 EDA Visualizations — `modules/eda.py` (Module 5)

| Function | Description |
|---|---|
| `generate_visualizations(df)` | Generates all plots and returns them as a `{name: base64}` dict |
| `get_base64_plot()` | Internal helper — saves current figure to a BytesIO buffer and Base64-encodes it |

**Plots generated:**

| Plot | Columns Used | Details |
|---|---|---|
| Histograms | Up to 6 numeric columns | `sns.histplot` with KDE, dark background, `#6c63ff` fill |
| Bar charts | Up to 4 categorical columns | Top-10 value counts, `mako` palette, rotated x-labels |
| Correlation heatmap | All numeric columns | `sns.heatmap`, `coolwarm` palette, annotated with 2dp values |

All plots use matplotlib's `Agg` backend (non-interactive, required for Flask) and are Base64-encoded for direct embedding in HTML — no external image hosting or temp files.

---

## 🧹 Data Cleaning — `modules/cleaning.py` (Modules 6, 7, 8)

| Function | Signature | Description |
|---|---|---|
| `handle_missing_values` | `(df, strategy='auto')` | `'auto'` → mean/mode; `'median'` → median/mode |
| `get_missing_stats` | `(df)` | Returns `{column: missing_count}` for columns with nulls |
| `detect_outliers` | `(df)` | IQR method — returns `{column: outlier_count}` for numeric columns |
| `handle_outliers` | `(df, strategy='remove')` | `'remove'` drops outlier rows; `'cap'` clips to IQR bounds (Winsorization) |
| `remove_duplicates` | `(df)` | Drops exact duplicate rows via `df.drop_duplicates()` |
| `fix_inconsistencies` | `(df)` | Strips leading/trailing whitespace from all string (object) columns |

---

## ⚙️ Feature Engineering — `modules/feature_engineering.py` (Module 9)

| Function | Signature | Description |
|---|---|---|
| `apply_label_encoding` | `(df, columns)` | Applies `sklearn.LabelEncoder` — converts strings to integers |
| `apply_standard_scaling` | `(df, columns)` | Applies `sklearn.StandardScaler` (mean=0, std=1) to numeric columns |
| `get_feature_info` | `(df)` | Returns `{'categorical': [...], 'numeric': [...]}` for UI column selection |

Transformations are applied to a copy of the DataFrame; the original is never mutated. Only columns that exist in the DataFrame are processed.

---

## 🤖 Model Training & Evaluation — `modules/model_training.py` (Modules 12, 13)

| Function | Signature | Description |
|---|---|---|
| `train_model_logic` | `(df, problem_type, algorithm, target_col)` | Trains the selected model and returns the model object, metrics dict, and test split |

**Supported algorithms:**

| Problem Type | Algorithm | `algorithm` key |
|---|---|---|
| Classification | Logistic Regression (`max_iter=1000`) | `logistic_regression` |
| Classification | Random Forest (100 estimators) | `random_forest` |
| Regression | Linear Regression | `linear_regression` |
| Regression | Decision Tree Regressor | `decision_tree` |
| Clustering | K-Means (k=3, `n_init='auto'`) | `kmeans` |

**Evaluation metrics by problem type:**

| Problem Type | Metric | Function |
|---|---|---|
| Classification | Accuracy | `accuracy_score()` |
| Regression | R² Score | `r2_score()` |
| Regression | RMSE | `sqrt(mean_squared_error())` |
| Clustering | Silhouette Score | `silhouette_score()` |

All supervised models use an 80/20 train-test split with `random_state=42`. Clustering runs on the full dataset; Silhouette Score is only calculated when more than one cluster label is present.

---

## 🗄️ Database

The project uses **SQLite** with SQLAlchemy ORM. `users.db` is auto-created inside `instance/` on the first run — no manual setup needed.

**User Model:**

| Column | Type | Details |
|---|---|---|
| `id` | Integer | Primary Key, auto-increment |
| `name` | String(100) | User's full name |
| `email` | String(100) | Unique, used for login |
| `password` | String(200) | Werkzeug salted hash — never plaintext |

---

## 🚧 Roadmap

- [x] User Registration & Login
- [x] Session Management & Flash Messages
- [x] Protected Dashboard Route
- [x] Multi-format Dataset Upload — CSV, Excel, JSON, XML, HTML (Module 3)
- [x] Data Summary Report — shape, dtypes, missing values, describe() (Module 4)
- [x] EDA Visualizations — Histograms, Bar Charts, Correlation Heatmap (Module 5)
- [x] Data Cleaning — Imputation, Outlier Handling, Deduplication, String Normalization (Modules 6–8)
- [x] Feature Engineering — LabelEncoder, StandardScaler, per-column selection (Module 9)
- [x] Problem Selection — Classification / Regression / Clustering + target column (Module 10)
- [x] Model Training — 5 algorithms, 80/20 split (Modules 11–12)
- [x] Model Evaluation — Accuracy, R², RMSE, Silhouette Score (Module 13)
- [x] Model Export — `.pkl` via `joblib.dump()`, served as file download (Module 14)

---

## 🤝 Contributing

Contributions are welcome. Fork the repo, create a feature branch, and open a pull request.

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

**Utkarsh Verma**
- GitHub: [@utkarsh0928](https://github.com/utkarsh0928)

**Shivang Verma**
- GitHub: [@Shivangverma7](https://github.com/Shivangverma7)

---

> *Built as part of an Industrial Training Project · 2026*
