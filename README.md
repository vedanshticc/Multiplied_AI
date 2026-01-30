# 🚧 Near Miss Data Analysis Dashboard

An interactive web-based dashboard for analyzing *Near Miss incidents* in a construction or industrial environment.
The application processes raw JSON data and provides meaningful visual insights to help identify safety risks, trends, and high-risk areas.

---

## 📌 What is a Near Miss?

A *Near Miss* is an unplanned event that could have resulted in an accident, injury, or damage but did not, either due to chance or timely intervention.

*Examples:*

* A worker slips but regains balance
* A tool falls from height but misses workers
* A vehicle stops just before a collision

Analyzing near misses helps organizations *prevent future accidents* and improve safety standards.

---

## 🎯 Objective of the Project

The objective of this project is to:

* Work with real-world JSON datasets
* Perform robust data preprocessing and cleaning
* Build a stable and interactive dashboard
* Visualize safety trends and risk patterns
* Handle missing or inconsistent data gracefully

---

## 🚀 Key Features

* Upload raw *Near Miss JSON* data
* Automatic flattening of nested JSON structures
* Intelligent detection of relevant columns
* Robust handling of missing and inconsistent values
* Interactive sidebar filters (Category, Region)
* Key Safety Metrics (KPIs)
* *10+ visualizations*, including:

  * Near Misses by Category
  * Severity Distribution
  * Monthly Trend Analysis
  * Year-wise Comparison
  * Region-wise Distribution
  * Unsafe Condition vs Unsafe Behavior
  * Severity vs Category Heatmap
  * High-Severity Analysis
  * Top Sub-Categories
  * Pareto (80/20) Analysis
* Clean, responsive UI built with Streamlit

---

## 🛠 Tech Stack

* *Python*
* *Streamlit* – Web application framework
* *Pandas* – Data processing and transformation
* *Plotly* – Interactive data visualizations

---

## 📂 Project Structure

near-miss-dashboard/
├── app.py               – Main Streamlit dashboard
├── utils.py             – Utility functions (JSON to DataFrame)
├── requirements.txt     – Python dependencies
├── README.md            – Project documentation
└── sample_data/         – (Optional) Sample JSON file


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
bash
git clone https://github.com/your-username/near-miss-dashboard.git
cd near-miss-dashboard


### 2️⃣ Create a Virtual Environment (Optional but Recommended)
bash
python -m venv env
source env/bin/activate      # macOS / Linux
env\Scripts\activate         # Windows


### 3️⃣ Install Dependencies
bash
pip install -r requirements.txt


### 4️⃣ Run the Application
bash
streamlit run app.py


---

## 📤 Using the Dashboard

1. Launch the Streamlit application
2. Upload a *Near Miss JSON* file
3. Apply filters from the sidebar
4. Explore trends, distributions, and risk insights using interactive charts

---

## 📊 Data Handling & Processing

* JSON files are flattened using pandas.json_normalize
* Column names are standardized (lowercase, underscore format)
* Missing categorical values are normalized and labeled as *"Unknown"*
* Severity values are coerced to numeric format
* Incident timestamps are assumed to be in *epoch milliseconds*
* All time-based analysis (month and year) is derived *only from timestamps*

---

## 📈 Time-Series Logic

* *Monthly trends* are generated using a derived year_month feature
* *Year-wise comparisons* are derived from the incident timestamp year
* Raw year fields in the dataset are intentionally ignored to avoid misleading trends

---

## ⚠️ Assumptions

* Input JSON contains structured Near Miss records
* At least one timestamp or date field exists
* Timestamp values are stored in epoch milliseconds
* Severity follows an ordinal numeric scale
* Dataset size is suitable for in-memory processing

---

## 🚫 Limitations

* No authentication or role-based access control
* Very large JSON files may take longer to load
* Dashboard is designed for exploratory analysis, not real-time monitoring
* Assumes consistent timestamp format across records

---

## ✅ Stability & Performance

* Graceful handling of missing or empty data
* Safe fallbacks when expected columns are not found
* Protection against crashes due to invalid filters
* Cached data loading for improved performance

---

## ❤️ Credits

Made with ❤️ by *Vedansh Kadre*

---

## 📌 Submission Note

This project was developed as part of a technical evaluation to demonstrate:

* Data handling and correctness
* Quality and relevance of visualizations
* Application stability and performance
* Code clarity and structure
* User experience design

---
