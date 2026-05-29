# Netflix Content Analytics Dashboard

## Synent Technologies Internship – Task 4: CSV to Dashboard

### Live Demo
https://synent-task04-csvtodahboard-aeleesbhuva.streamlit.app/

---

## Problem Statement

Organizations often work with large CSV datasets that are difficult to analyze manually. The objective of this project is to build an interactive dashboard that allows users to upload a dataset, explore data visually, apply filters, and generate insights through dynamic charts.

As part of Task 4 of the Synent Technologies Data Science Internship, an interactive dashboard was developed using Streamlit and the Netflix Movies & TV Shows dataset.

---

## Dataset Details

### Dataset Name
Netflix Movies and TV Shows Dataset

### Dataset Source
Netflix Dataset (Kaggle)

### Dataset Description

The dataset contains information about movies and TV shows available on Netflix, including:

- Title
- Type (Movie / TV Show)
- Director
- Cast
- Country
- Date Added
- Release Year
- Rating
- Duration
- Genre
- Description

### Key Columns

| Column | Description |
|----------|-------------|
| show_id | Unique identifier |
| type | Movie or TV Show |
| title | Content title |
| country | Production country |
| date_added | Date added to Netflix |
| release_year | Release year |
| rating | Content rating |
| duration | Duration of content |
| listed_in | Genre categories |

---

## Approach

The project follows a standard Data Science workflow:

### 1. Data Loading
- Load dataset using Pandas
- Support CSV upload through Streamlit

### 2. Data Preprocessing
- Handle missing values
- Convert date columns
- Create derived features:
  - year_added
  - month_added
  - decade
  - region

### 3. Dashboard Development

Built using Streamlit with four interactive sections:

#### Overview Dashboard
- Total Titles
- Total Movies
- Total TV Shows
- Total Countries
- Genre Distribution
- Rating Analysis
- Duration Analysis

#### Trends Dashboard
- Content Added Per Year
- Monthly Upload Trends
- Decade-wise Analysis

#### Geographic Dashboard
- Country-wise Content Distribution
- Regional Analysis
- Content Type by Region

#### Data Explorer
- Search Functionality
- Dynamic Filtering
- Missing Value Analysis
- Interactive Data Table

### 4. Visualization

Libraries Used:

- Plotly Express
- Streamlit Charts
- Pandas

---

## Results

The dashboard successfully provides:

### Key Insights

- Movies dominate the Netflix catalog compared to TV Shows.
- Significant growth in content additions occurred after 2015.
- The United States contributes the highest amount of content.
- Drama and International categories are among the most popular genres.
- Most content was added between 2018 and 2020.

### Dashboard Features Achieved

✔ CSV Upload Support

✔ Dynamic Filtering

✔ Interactive Charts

✔ Trend Analysis

✔ Geographic Analysis

✔ Data Exploration

✔ Missing Value Reporting

✔ Responsive Streamlit Interface

---

## Tools & Technologies

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

---

## Installation

```bash
git clone https://github.com/Aelees0807/synent-task4-csvtodashboard-aeleesbhuva.git

cd synent-task4-csvtodashboard-aeleesbhuva

pip install -r requirements.txt

streamlit run netflix_dashboard.py
