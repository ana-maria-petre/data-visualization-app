# Data Visualization and Classification App

**A Python desktop application for interactive data exploration, visualization, and unsupervised classification using K-Means clustering.**  
This tool allows users to load CSV datasets, inspect and filter tabular data, visualize individual or multiple features, analyze variable correlations, and apply clustering techniques — all through a user-friendly graphical interface built with Tkinter.

Built on top of core data science libraries such as Matplotlib, Seaborn, NumPy, and Scikit-learn, this application is designed for data analysts, students, and researchers who need a quick and lightweight environment for exploratory data analysis (EDA) and pattern discovery.

---

## ✨ Features

- 📁 **CSV Import**: Load any CSV file with headers and preview the data in a scrollable table.
- 📊 **Data Visualization**: Plot line graphs for selected columns to analyze trends over rows.
- 📈 **Histogram Generator**: Create histograms for any numeric column to understand value distributions.
- 🔗 **Correlation Matrix**: Generate a heatmap of Pearson correlation coefficients between numeric features.
- 🧠 **K-Means Clustering**: Select multiple numeric columns and apply unsupervised classification with an adjustable number of clusters (K).
- 🖱️ **GUI Interface**: Everything runs through a Tkinter-based interface — no coding required.

---

## 📂 File Requirements

- Input files must be in **CSV** format.
- The CSV file should have a **header row**.
- For best results in clustering and visualization, ensure numeric columns have **consistent, parseable values**.

---

## 📦 Requirements

- **Python 3.x**
- Libraries:
  - `tkinter`
  - `matplotlib`
  - `numpy`
  - `seaborn`
  - `scikit-learn`

---

## 🚀 Usage

1. **Load CSV**: Click on "Load CSV" to open a file dialog and load a CSV file into the app.
2. **View Data**: The dataset will be displayed in an interactive table where you can inspect the contents.
3. **Data Analysis**:
   - Click on "Correlation Matrix" to generate a correlation heatmap of numeric columns.
   - Use the "Histogram" button to create a histogram of a selected column.
   - "Data Visualization" will plot selected columns over the row index.
4. **K-Means Clustering**:
   - Select columns for classification from the list.
   - Specify the number of clusters (K) and click "K-Means Classification" to perform clustering and visualize the results.

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/ana-maria-petre/data-visualization-app.git
cd data-visualization-app
pip install -r requirements.txt
python main.py

