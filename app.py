import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
import wget
import warnings

warnings.filterwarnings("ignore")

# --- Page config ---
st.set_page_config(page_title="Phone Addiction App", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
        html, body, [class*='css']  {
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #6a0dad;
        }
        .main-button button {
            background-color: #6a0dad !important;
            color: white !important;
            font-size: 18px !important;
            padding: 0.75rem 1rem !important;
            border-radius: 8px !important;
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Download CSV from Google Drive ---
file_id = '1plAz7EEeNs8j6WEYaBdLywyX9A9qMprS'
url = f'https://drive.google.com/uc?export=download&id={file_id}'
filename = 'phone_behavior_data.csv'

if not os.path.exists(filename):
    wget.download(url, filename)

# --- Load dataset ---
try:
    df = pd.read_csv(filename)
    df['Screen On Time (min/day)'] = df['Screen On Time (hours/day)'] * 60
    df['Engagement Ratio'] = df['App Usage Time (min/day)'] / df['Screen On Time (min/day)']
except Exception as e:
    st.error("Failed to load dataset. Please check the file or URL.")

# --- Navigation state ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- NAVIGATION BUTTONS ---
def main_nav():
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

if st.session_state.page == 'home':
    main_nav()

# --- SECTION 1: Our Data ---
elif st.session_state.page == 'section1':
    st.header("1. Our Data")
    try:
        st.image("images/opening_gif.gif")
    except:
        st.warning("Image 'opening_gif.gif' not found. Make sure it's uploaded to /images.")
    st.markdown("""
    This dataset captures a rich set of real-world behavioral signals from mobile phone users, including app usage time, screen-on time, data consumption, and the number of apps installed. These variables provide a practical foundation for exploring digital engagement patterns and identifying potential signs of overuse or phone addiction.
    """)
    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'

# --- SECTION 2: Demographics ---
elif st.session_state.page == 'section2':
    st.header("2. Demographics Don't Matter")
    try:
        st.image("images/bimodal_distribution.png")
        st.image("images/demographics_boxplots.png")
    except:
        st.warning("Some demographic images not found. Check /images folder.")
    st.markdown("Chi-square tests show no meaningful link between gender, OS, device model, or age band and high usage.")
    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'

# --- SECTION 3: Variables ---
elif st.session_state.page == 'section3':
    st.header("3. The Story Begins with Variables")
    try:
        st.image("images/final_summary_banner.png")
    except:
        st.warning("Image 'final_summary_banner.png' not found.")
    st.markdown("""
    App Usage Time shows a clear bimodal distribution, with peaks around 100 and 500 minutes per day.  
    Screen-On Time stretches up to 12 hours for some users.
    """)
    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'

# --- SECTION 4: Heavy Users ---
elif st.session_state.page == 'section4':
    st.header("4. The Heavy Users")
    try:
        st.image("images/final_summary_banner.png")
        st.image("images/class_behavior_chart.png")
        st.image("images/engagement_ratio.png")
    except:
        st.warning("Some images in this section are missing.")
    st.markdown("T-tests confirm that Class 5 tops every behavioural metric (app usage, screen time, data usage, apps installed) with p < 0.001.")
    st.markdown("Class 5 averages ~0.9, meaning most screen time is in apps, while lower classes are more scattered.")
    st.markdown("""
    **Findings from T-Test: Behavioral Differences in Class 5 Users**

    - App Usage Time: Class 5 users spend over twice as much time on apps compared to others.
    - Screen On Time: Their screens are active for more than 10 hours per day.
    - Battery Drain: Significantly higher battery usage.
    - Data Usage: Nearly triple the data consumption.
    - Number of Apps Installed: Over twice as many apps.
    """)
    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'

# --- SECTION 5: Apps Define You ---
elif st.session_state.page == 'section5':
    st.header("5. Your Number of Apps Define You")
    try:
        st.image("images/regression_apps_vs_screen.png")
        st.image("images/engagement_ratio.png")
    except:
        st.warning("One or more regression images are missing.")
    st.markdown("""
    The model revealed a strong and significant relationship:

    - Each additional app increases screen-on time by approximately 6.5 minutes/day.
    - The regression line fits the data closely with R² = 0.897.
    - The result is visually confirmed by the tight confidence interval.

    These findings suggest that the number of apps installed is not just a passive metric — it actively contributes to increased phone engagement.
    """)
    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'
