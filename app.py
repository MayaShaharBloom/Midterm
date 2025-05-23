import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Phone Addiction Dashboard", layout="wide")

# Set custom font and color
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
        }
        .main {background-color: #ffffff;}
        h1, h2, h3 {color: #6a0dad;}
        .stButton>button {
            color: white;
            background-color: #6a0dad;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Load dataset
file_path = "phone_behavior_data.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df['Screen On Time (min/day)'] = df['Screen On Time (hours/day)'] * 60
    df['Engagement Ratio'] = df['App Usage Time (min/day)'] / df['Screen On Time (min/day)']
else:
    st.error("Dataset not found. Please ensure the CSV is present.")

# Sidebar navigation
st.sidebar.title("Explore the Story")
page = st.sidebar.radio("Go to:", (
    "Main Page", 
    "1. Our Data", 
    "2. Demographics Don't Matter", 
    "3. The Story Begins with Variables", 
    "4. The Heavy Users", 
    "5. Your Number of Apps Define You"
))

# --- Main Page ---
if page == "Main Page":
    st.title("📱 Behavioral Indicators of Phone Addiction")
    st.markdown("Navigate the sections using the menu on the left to explore the behavioral markers of excessive phone usage.")

# --- Section 1 ---
elif page == "1. Our Data":
    st.header("1. Our Data")
    st.image("images/opening_gif.gif")
    st.markdown("""
    This  dataset captures a rich set of real-world behavioral signals from mobile phone users, including app usage time, screen-on time, data consumption, and the number of apps installed. These variables provide a practical foundation for exploring digital engagement patterns and identifying potential signs of overuse or phone addiction.
    """)

# --- Section 2 ---
elif page == "2. Demographics Don't Matter":
    st.header("2. Demographics Don't Matter")
    st.image("images/bimodal_distribution.png")
    st.markdown("Chi-square tests show no meaningful link between gender, OS, device model, or age band and high usage.")
    st.image("images/demographics_boxplots.png")

# --- Section 3 ---
elif page == "3. The Story Begins with Variables":
    st.header("3. The Story Begins with Variables")
    st.image("images/final_summary_banner.png")
    st.markdown("""
    App Usage Time shows a clear bimodal distribution, with peaks around 100 and 500 minutes per day. 
    Screen-On Time stretches up to 12 hours for some users.
    """)

# --- Section 4 ---
elif page == "4. The Heavy Users":
    st.header("4. The Heavy Users")
    st.image("images/final_summary_banner.png")
    st.markdown("T-tests confirm that Class 5 tops every behavioural metric (app usage, screen time, data usage, apps installed) with p < 0.001")
    st.markdown("Class 5 averages ~0.9, meaning most screen time is in apps, while lower classes are more scattered. Class 4 also shows a high use of apps in screen on time")
    st.markdown("""
    Findings from T-Test: Behavioral Differences in Class 5 Users.  
    
    To understand what distinguishes heavy users (Class 5) from the rest of the population, I conducted independent t-tests on key behavioral metrics. The results show statistically significant differences across all variables except age.

    - App Usage Time: Class 5 users spend over twice as much time on apps compared to others.
    - Screen On Time: Their screens are active for more than 10 hours per day, suggesting high engagement or phone dependence.
    - Battery Drain: Significantly higher battery usage reflects constant device activity across functions.
    - Data Usage: Nearly triple the data consumption indicates more online activity (streaming, browsing, social media).
    - Number of Apps Installed: Class 5 users have over twice the number of apps, pointing to broader and more frequent app exploration.
    """)
    st.image("images/class_behavior_chart.png")
    st.image("images/engagement_ratio.png")

# --- Section 5 ---
elif page == "5. Your Number of Apps Define You":
    st.header("5. Your Number of Apps Define You")
    st.markdown("""
    The model revealed a strong and significant relationship: 

    - Each additional app increases screen-on time by approximately 6.5 minutes/day
    - The regression line fits the data closely with R² = 0.897
    - The result is also visually confirmed by the strong linear trend and tight confidence interval around the red regression line

    These findings suggest that the number of apps installed is not just a passive metric — it actively contributes to increased phone engagement. This supports our hypothesis that app diversity drives screen dependence, a key indicator of potential overuse.
    """)
    st.image("images/regression_apps_vs_screen.png")
    st.image("images/engagement_ratio.png")
