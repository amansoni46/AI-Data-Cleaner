# 🧹 AI Data Cleaner

### Smart Data Cleaning • Quality Analysis • Cleaning History

An interactive data-cleaning application built with **Python and Streamlit** that helps users identify data quality issues, clean CSV and Excel files, analyze datasets, and download cleaned data with ease.

<p align="center">
  <a href="https://uri-infotech-ai-data-cleaner.streamlit.app/">
    <strong>🚀 Live Demo</strong>
  </a>
  &nbsp; • &nbsp;
  <a href="https://github.com/amansoni46/AI-Data-Cleaner">
    <strong>💻 GitHub Repository</strong>
  </a>
</p>

---

## 📌 Overview

Working with raw datasets often involves duplicate records, missing values, inconsistent formatting, and unnecessary data. These issues can affect the accuracy of analysis and decision-making.

**AI Data Cleaner** is designed to simplify this process through an interactive web application that analyzes uploaded datasets, identifies common data quality issues, applies cleaning operations, and generates downloadable cleaned files.

The application also integrates Supabase for storing cleaning history and supports user authentication.

## ✨ Key Features

* **📂 CSV & Excel Upload** — Upload datasets in supported CSV and Excel formats.
* **📊 Data Quality Analysis** — Examine dataset dimensions, missing values, duplicate records, and other data quality issues.
* **🧹 Automated Data Cleaning** — Remove duplicate rows and handle empty rows, empty columns, and unnecessary blank values.
* **✨ Text & Column Name Cleaning** — Clean unwanted whitespace in text values and column names.
* **📈 Dataset Insights** — Review dataset statistics and cleaning results through an interactive interface.
* **📥 Download Cleaned Data** — Export and download the processed dataset.
* **🗂️ Cleaning History** — Store and review previous cleaning records using Supabase.
* **🔐 User Authentication** — Access the application through its supported login and signup options.
* **🌐 Web-Based Interface** — Use the application through a browser without installing a desktop application.

## 🛠️ Tech Stack

| Technology                | Purpose                                       |
| ------------------------- | --------------------------------------------- |
| Python                    | Core application logic and data processing    |
| Streamlit                 | Interactive web interface                     |
| Pandas                    | Data manipulation, analysis, and cleaning     |
| NumPy                     | Numerical and data-processing operations      |
| Plotly                    | Interactive visualizations, where implemented |
| OpenPyXL                  | Excel file processing                         |
| Supabase                  | Backend database and cleaning history         |
| Git & GitHub              | Version control and source code management    |
| Streamlit Community Cloud | Application deployment                        |

## ⚙️ How It Works

1. **Upload:** Import a CSV or Excel dataset.
2. **Analyze:** Inspect the dataset and identify potential data quality problems.
3. **Clean:** Apply the available cleaning operations.
4. **Review:** Compare the original and cleaned dataset statistics.
5. **Download:** Export the cleaned dataset for further analysis.
6. **Track:** Save and review cleaning history through the integrated backend.

## 🚀 Live Application

Try the deployed application:

**[Open AI Data Cleaner →](https://uri-infotech-ai-data-cleaner.streamlit.app/)**

> Note: Authentication and database-backed features depend on the application's deployment configuration and backend availability.

## 💻 Run Locally

Follow these steps to run the project on your computer.

### 1. Clone the Repository

```bash
git clone https://github.com/amansoni46/AI-Data-Cleaner.git
```

### 2. Open the Project Folder

```bash
cd AI-Data-Cleaner
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate.bat
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Secrets

The application uses Supabase for backend functionality.

Create a `.streamlit/secrets.toml` file in the project directory and configure the required credentials:

```toml
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_PUBLISHABLE_KEY = "YOUR_SUPABASE_PUBLISHABLE_KEY"
APP_URL = "YOUR_APPLICATION_URL"
```

Use the actual variable names expected by the application's current configuration. If the application supports `SUPABASE_ANON_KEY` as an alternative, configure the appropriate key instead.

**Security:** Never commit actual secret keys, passwords, or private credentials to GitHub. Keep `secrets.toml` out of version control.

### 6. Start the Application

```bash
python -m streamlit run app.py
```

Open the local address displayed in the terminal, usually:

```text
http://localhost:8501
```

## 📁 Project Structure

```text
AI-Data-Cleaner/
│
├── app.py                  # Main Streamlit application
├── supabase_client.py      # Supabase client configuration
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── .gitignore              # Git exclusion rules
│
└── modules/
    ├── __init__.py
    ├── analyzer.py         # Dataset quality analysis
    ├── cleaner.py          # Data cleaning operations
    └── report.py           # Cleaning reports and results
```

## 🔒 Security & Data Handling

* Backend access depends on the configured Supabase credentials and database permissions.
* Authentication and database operations require the appropriate backend configuration.
* Never expose service-role keys or other privileged credentials in client-facing code.
* Configure database access policies appropriately before deploying the application.
* Review your deployment and data-handling requirements before uploading sensitive datasets.

## 🎯 Use Cases

* Preparing datasets for data analysis.
* Removing duplicate records from CSV and Excel files.
* Identifying missing or incomplete data.
* Standardizing text and column names.
* Preparing structured datasets for reporting and visualization.
* Reviewing historical data-cleaning activity.

## 🔮 Future Improvements

Potential enhancements for future versions include:

* Advanced missing-value imputation.
* Custom data-cleaning rules.
* Before-and-after data quality reports.
* Additional file format support.
* More advanced visual analytics.
* AI-assisted cleaning recommendations.
* Exportable cleaning summaries.

## 👨‍💻 Developer

**Aman Soni**

BCA Student | Aspiring Data Analyst | Python Developer

* **GitHub:** [@amansoni46](https://github.com/amansoni46)
* **Project Repository:** [AI Data Cleaner](https://github.com/amansoni46/AI-Data-Cleaner)
* **Live Demo:** [Launch Application](https://uri-infotech-ai-data-cleaner.streamlit.app/)

---

<p align="center">
  <strong>Built to make data cleaning simpler, faster, and more accessible.</strong>
  <br>
  ⭐ If you find this project useful, consider giving the repository a star!
</p>
