import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
import warnings

warnings.filterwarnings("ignore")

# --- Page config ---
st.set_page_config(page_title="Phone Addiction App", layout="wide")

# --- Styling ---
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #6a0dad;
    }
    .main-button {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        max-width: 400px;
    }
    .main-button button {
        background-color: #6a0dad !important;
        color: white !important;
        font-size: 18px !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Load dataset ---
try:
    df = pd.read_csv("phone_behavior_data.csv")
    df['Screen On Time (min/day)'] = df['Screen On Time (hours/day)'] * 60
    df['Engagement Ratio'] = df['App Usage Time (min/day)'] / df['Screen On Time (min/day)']
except Exception as e:
    st.error("Dataset not found. Please make sure 'phone_behavior_data.csv' is in the repo.")

# --- Main navigation logic ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- Homepage with buttons ---
if st.session_state.page == 'home':
    st.title("📱 Behavioral Indicators of Phone Addiction")
    st.subheader("Explore the sections below:")
    st.markdown("<div class='main-button'>", unsafe_allow_html=True)
    if st.button("1. Our Data"):
        st.session_state.page = 'section1'
    if st.button("2. Demographics Don't Matter"):
        st.session_state.page = 'section2'
    if st.button("3. The Story Begins with Variables"):
        st.session_state.page = 'section3'
    if st.button("4. The Heavy Users"):
        st.session_state.page = 'section4'
    if st.button("5. Your Number of Apps Define You"):
        st.session_state.page = 'section5'
    st.markdown("</div>", unsafe_allow_html=True)

# --- Section 1 ---
elif st.session_state.page == 'section1':
    st.header("1. Our Data")
    st.image("images/opening_gif.gif")
    st.markdown("""
    This dataset captures a rich set of real-world behavioral signals from mobile phone users, including app usage time, screen-on time, data consumption, and the number of apps installed. These variables provide a practical foundation for exploring digital engagement patterns and identifying potential signs of overuse or phone addiction.
    """)
    st.button("Back", on_click=lambda: st.session_state.update(page='home'))

# --- Section 2 ---
elif st.session_state.page == 'section2':
    st.header("2. Demographics Don't Matter")
    st.image("images/bimodal_distribution.png")
    st.markdown("Chi-square tests show no meaningful link between gender, OS, device model, or age band and high usage.")
    st.image("images/demographics_boxplots.png")
    st.button("Back", on_click=lambda: st.session_state.update(page='home'))

# --- Section 3 ---
elif st.session_state.page == 'section3':
    st.header("3. The Story Begins with Variables")
    st.image("images/final_summary_banner.png")
    st.markdown("""
    App Usage Time shows a clear bimodal distribution, with peaks around 100 and 500 minutes per day.  
    Screen-On Time stretches up to 12 hours for some users.
    """)
    st.button("Back", on_click=lambda: st.session_state.update(page='home'))

# --- Section 4 ---
elif st.session_state.page == 'section4':
    st.header("4. The Heavy Users")
    st.image("images/final_summary_banner.png")
    st.markdown("T-tests confirm that Class 5 tops every behavioural metric (app usage, screen time, data usage, apps installed) with p < 0.001.")
    st.markdown("Class 5 averages ~0.9, meaning most screen time is in apps, while lower classes are more scattered. Class 4 also shows a high use of apps in screen on time.")
    st.markdown("""
    **Findings from T-Test: Behavioral Differences in Class 5 Users**

    - App Usage Time: Class 5 users spend over twice as much time on apps compared to others.
    - Screen On Time: Their screens are active for more than 10 hours per day.
    - Battery Drain: Significantly higher battery usage.
    - Data Usage: Nearly triple the data consumption.
    - Number of Apps Installed: Over twice as many apps.
    """)
    st.image("images/class_behavior_chart.png")
    st.image("images/engagement_ratio.png")
    st.button("Back", on_click=lambda: st.session_state.update(page='home'))

# --- Section 5 ---
elif st.session_state.page == 'section5':
    st.header("5. Your Number of Apps Define You")
    st.markdown("""
    The model revealed a strong and significant relationship:

    - Each additional app increases screen-on time by approximately 6.5 minutes/day.
    - The regression line fits the data closely with R² = 0.897.
    - The result is visually confirmed by the tight confidence interval.

    These findings suggest that the number of apps installed is not just a passive metric — it actively contributes to increased phone engagement.
    """)
    st.image("images/regression_apps_vs_screen.png")
    st.image("images/engagement_ratio.png")
    st.button("Back", on_click=lambda: st.session_state.update(page='home'))
