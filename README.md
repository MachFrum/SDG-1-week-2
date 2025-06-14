# Predicting Economic Poverty with Machine Learning

![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.6.1%2B-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-green.svg)
![Numpy](https://img.shields.io/badge/Numpy-1.23.5%2B-purple.svg)

An interactive web application that uses machine learning to predict the extreme poverty rate of a country based on key economic indicators. The app features both a live mode, which fetches data from the World Bank API, and a manual mode for "what-if" scenario analysis.

## Live Demo

[Live Demo of the App](https://sdg-1-week-2-mous5x6bgcjskr8rhreiik.streamlit.app/)  
*A live demonstration of the app's dual-mode prediction capabilities.*

## Blog

[A blog on the App's_Findings](https://machfrum.github.io/SDG-1-week-2/)  
*A blog on the app's dual-mode prediction capabilities and how inflation is a hidden tax to humanity.*

## Key Features

- **Dual Prediction Modes:**
  - **Live API Mode:** Fetches the latest available annual economic data for a selected country directly from the World Bank API.
  - **Manual Scenario Builder:** Allows users to input hypothetical economic figures to explore their potential impact on poverty.
- **Side-by-Side Model Comparison:** Deploys two distinct machine learning models—a simple Linear Regression and a more complex Random Forest—and displays their predictions simultaneously for comparison.
- **Model Transparency:** Includes a detailed section explaining the performance metrics (R-squared, MAE) and the feature importances, so users can understand *how* the models make their predictions and which economic factors are most influential.
- **Interactive UI:** Built with Streamlit for a clean, responsive, and user-friendly experience.

## Project Workflow & Code Explanation

This project was developed in two main phases: an analysis/modeling phase and a deployment phase.

### 1. Analysis and Modeling (`SDG 1.ipynb`)

The initial work was performed in a Jupyter Notebook (`SDG 1.ipynb`) and followed a standard data science workflow:

- **Data Collection:** Two separate datasets were used: one on historical poverty rates (`share-of-population-living-in-extreme-poverty.csv`) and another on national economic indicators (`Economic Indicators And Inflation.csv`).
- **Data Cleaning & Merging:** The core challenge was that the datasets were misaligned. The code performs extensive cleaning by:
    - Standardizing country names (e.g., "USA" to "United States").
    - Filtering out non-country aggregate data (e.g., "World", "Europe and Central Asia (PIP)").
    - Aligning the data temporally to a common timeframe (2010 onwards).
    - Merging the two datasets into a single, analysis-ready DataFrame.
- **Exploratory Data Analysis (EDA):** Visualizations like a correlation heatmap revealed that there was no simple, linear relationship between inflation and poverty. This insight was crucial for model selection.
- **Model Training:** Two models were trained on the cleaned data:
    1.  **Linear Regression:** A baseline model to test for simple linear patterns.
    2.  **Random Forest Regressor:** A more powerful, tree-based model capable of capturing complex, non-linear relationships.
- **Model Persistence:** The trained models, performance metrics, and feature lists were saved into a single file (`poverty_predictor_assets.joblib`) using `joblib` for easy loading in the web app.

### 2. Deployment (`webapp.py`)

The trained models were deployed as an interactive web application using Streamlit.

- **Loading Assets:** The app starts by loading the `poverty_predictor_assets.joblib` file, which contains all the necessary pre-trained objects.
- **User Interface (UI):** The app uses `st.tabs` to create a clean separation between the "Live API" and "Manual Scenario" modes.
- **API Integration:** The "Live API" tab uses the `requests` library to call the World Bank API. It includes functions to:
    - Build the correct API URL based on user-selected country and year.
    - Fetch and parse the JSON response.
    - Perform robust error handling in case the API call fails or data is missing.
- **Prediction Logic:** User inputs (either from the API or manual sliders) are formatted into a pandas DataFrame that matches the structure the models were trained on. The `.predict()` method is then called on both models to generate the poverty rate predictions.

## How to Install and Run Locally

To run this application on your local machine, please follow these steps:

**1. Prerequisites:**
- Python 3.9 or higher
- `git` for cloning the repository

**2. Clone the Repository:**
```bash
git clone https://github.com/MachFrum/SDG-1-week-2.git
cd MachFrum
```

**3. Create a Virtual Environment (Recommended):**
- **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **On Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

**4. Install Dependencies:**
Create a file named `requirements.txt` with the following content, and then run the installation command.

```
# requirements.txt
streamlit
pandas
scikit-learn
requests
matplotlib
seaborn
joblib
```

Now, install the packages:
```bash
pip install -r requirements.txt
```

**5. Run the Streamlit App:**
```bash
streamlit run webapp.py
```
Your web browser should open a new tab with the application running.

## How to Interpret the Results

The application provides three key pieces of information:

1.  **The Predictions:**
    - **Random Forest Prediction:** This is the primary and more reliable prediction. This model is sophisticated enough to understand complex interactions between economic factors.
    - **Linear Regression Prediction:** This is a baseline. If its prediction is wildly different from the Random Forest's, it confirms that simple linear assumptions are not sufficient for this problem.

2.  **Model Performance Metrics (in the expandable section):**
    - **R-squared (R²):** Represents the percentage of the variation in the poverty rate that the model can explain. A score of `0.40` means the model explains 40% of the variance. Higher is better (max is 1.0).
    - **Mean Absolute Error (MAE):** The average error of the model's predictions. An MAE of `1.85` means the model's predictions are, on average, off by 1.85 percentage points (e.g., predicting 10.85% when the real value is 9.00%). Lower is better.

3.  **Feature Importance Chart:**
    This is the most insightful part of the analysis. It breaks down which factors the Random Forest model found most important when making its predictions. A higher importance score means that the feature has a greater impact on the final poverty rate prediction. This chart directly answers the question: **"What are the biggest drivers of poverty in this model?"**

## Future Improvements

- **Add More Features:** Incorporate other influential data, such as education levels, political stability indices, or infrastructure quality.
- **Expand Country Coverage:** Integrate additional poverty and economic datasets to increase the number of countries the model can predict for.
- **Advanced Modeling:** Experiment with more advanced algorithms like Gradient Boosting (XGBoost, LightGBM) or time-series models (like VAR) for potentially higher accuracy.
- **Caching API Results:** Implement `st.cache_data` to cache results from the World Bank API, making the app faster and reducing redundant calls.

---

## License.
- **This is for learning purposes** Tweak, improve, change. Have fun!

---
