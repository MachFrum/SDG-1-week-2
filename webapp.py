import streamlit as st
import joblib
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Load the Saved Assets  ---
try:
    app_data = joblib.load('poverty_predictor_assets.joblib')
    models = app_data['models']
    metrics = app_data['metrics']
    features = app_data['features']
    feature_importance_df = app_data['feature_importance']
    
    lr_model = models['Linear Regression']
    rf_model = models['Random Forest']

except FileNotFoundError:
    st.error("Error: The 'poverty_predictor_assets.joblib' file was not found. Please ensure it's in the same folder as the webapp.")
    st.stop()

# --- 2. API Calling Function ---
INDICATOR_CODES = {
    'gdp_billion_usd': 'NY.GDP.MKTP.CD',
    'inflation_rate': 'FP.CPI.TOTL.ZG',
    'unemployment_rate': 'SL.UEM.TOTL.ZS',
    'economic_growth': 'NY.GDP.MKTP.KD.ZG'
}

def fetch_world_bank_data(country_code, year):
    data = {}
    for feature, code in INDICATOR_CODES.items():
        url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{code}?date={year}&format=json"
        try:
            response = requests.get(url, timeout=10)
            response_json = response.json()
            if len(response_json) > 1 and response_json[1] and response_json[1][0]['value'] is not None:
                value = response_json[1][0]['value']
                if feature == 'gdp_billion_usd':
                    value /= 1_000_000_000
                data[feature] = value
            else:
                data[feature] = None
        except (requests.exceptions.RequestException, IndexError, TypeError):
            data[feature] = None
    return data

# --- 3. App Layout with Tabs ---
st.set_page_config(layout="wide")
st.title("Hybrid Poverty Rate Prediction Dashboard")
st.markdown("""
Choose your method: Use the **Live API** to fetch real economic data or use the **Manual Scenario Builder** to test hypothetical situations.
""")

# Create the tabs
tab1, tab2 = st.tabs(["Live API Prediction", "Manual Scenario Builder"])

# --- TAB 1: LIVE API PREDICTION ---
with tab1:
    st.header("Predict from Live World Bank Data")
    
    # Input controls for the API
    known_countries = {
        'Australia': 'AUS', 'Bangladesh': 'BGD', 'Brazil': 'BRA', 'Canada': 'CAN', 
        'China': 'CHN', 'France': 'FRA', 'Germany': 'DEU', 'India': 'IND', 
        'Indonesia': 'IDN', 'Italy': 'ITA', 'Japan': 'JPN', 'Malaysia': 'MYS', 
        'Pakistan': 'PAK', 'Russia': 'RUS', 'South Korea': 'KOR', 'Turkey': 'TUR', 
        'United Kingdom': 'GBR', 'United States': 'USA'
    }
    col1, col2 = st.columns(2)
    with col1:
        selected_country_name = st.selectbox("Select a Country", options=list(known_countries.keys()), key="api_country")
    with col2:
        selected_year = st.selectbox("Select a Year", options=list(range(2022, 2010, -1)), key="api_year")
    
    selected_country_code = known_countries[selected_country_name]

    # Fetch button
    if st.button("Fetch Data & Predict", key="api_button"):
        with st.spinner(f"Fetching {selected_year} data for {selected_country_name}..."):
            live_data = fetch_world_bank_data(selected_country_code, selected_year)

        if None in live_data.values():
            st.error(f"Could not retrieve all required data for {selected_country_name} for {selected_year}.")
        else:
            st.success("Successfully fetched data!")
            st.dataframe(pd.DataFrame([live_data]))
            input_data = pd.DataFrame([[live_data[f] for f in features]], columns=features)
            
            lr_pred = lr_model.predict(input_data)[0]
            rf_pred = rf_model.predict(input_data)[0]

            pred_col1, pred_col2 = st.columns(2)
            with pred_col1:
                st.metric("Random Forest Prediction", f"{rf_pred:.2f}%")
            with pred_col2:
                st.metric("Linear Regression Prediction", f"{lr_pred:.2f}%")

# --- TAB 2: MANUAL SCENARIO BUILDER ---
with tab2:
    st.header("Build a Custom Economic Scenario")
    st.markdown("Use the sliders to create a hypothetical scenario and see the model's predictions instantly.")
    
    # Manual input sliders
    gdp = st.number_input('GDP (in billion USD)', min_value=1.0, max_value=25000.0, value=2000.0, step=100.0)
    inflation = st.slider('Inflation Rate (%)', min_value=-2.0, max_value=100.0, value=5.0, step=0.1)
    unemployment = st.slider('Unemployment Rate (%)', min_value=1.0, max_value=90.0, value=5.5, step=0.1)
    growth = st.slider('Economic Growth (%)', min_value=-15.0, max_value=15.0, value=3.0, step=0.1)

    # Create dataframe from manual inputs
    manual_input_data = pd.DataFrame([[gdp, inflation, unemployment, growth]], columns=features)
    
    # Get predictions
    manual_lr_pred = lr_model.predict(manual_input_data)[0]
    manual_rf_pred = rf_model.predict(manual_input_data)[0]
    
    st.subheader("Model Predictions for Your Scenario")
    pred_col1_manual, pred_col2_manual = st.columns(2)
    with pred_col1_manual:
        st.metric("Random Forest Prediction", f"{manual_rf_pred:.2f}%")
    with pred_col2_manual:
        st.metric("Linear Regression Prediction", f"{manual_lr_pred:.2f}%")

# --- ALWAYS VISIBLE: MODEL PERFORMANCE SECTION ---
st.divider() # Adds a visual line separator
st.header("Model Performance & Explanation")
st.markdown("This section explains the models used for the predictions above. The performance was measured on historical test data.")

expander = st.expander("Click to see model performance details")
with expander:
    st.subheader("Evaluation Metrics (R-squared & MAE)")
    metrics_df = pd.DataFrame(metrics).T
    st.dataframe(metrics_df.style.highlight_max(axis=0, subset=['R2'], color='lightgreen').highlight_min(axis=0, subset=['MAE', 'MSE'], color='lightgreen'))
    
    st.subheader("What drives the predictions? (Feature Importance)")
    fig, ax = plt.subplots()
    sns.barplot(data=feature_importance_df, x='Importance', y='Feature', ax=ax, palette='viridis')
    st.pyplot(fig)