import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import ttest_ind, chi2_contingency
import os
import wget
import warnings

warnings.filterwarnings("ignore")
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

# --- File IDs from Google Drive ---
image_ids = {
    "opening_gif.gif": "15PlzbNjnNZtpfqEfApjHVboUIPIwJLPn",
    "bimodal_distribution.png": "1VRspHsklHglAxgrCwqAimY6tOqKQgKRA",
    "class_behavior_chart.png": "1QttIuEGH2g8fcMIf9Lq_qcfDC6B8_pye",
    "regression_apps_vs_screen.png": "13HJDBgsyh4IcY7E8MdC7AukjW533ikR_",
    "engagement_ratio.png": "1TiIc_7z6u0MFNCX22sZqkHgtNjUVbm6C",
    "final_summary_banner.png": "1Wq3mTgpUpK0EOPsLDb-LP2CTzAfSkNcN",
    "demographics_boxplots.png": "1wZXnTRQtkv67nH5HEdLb9CXVRGwtM7Ia"
}

# --- Download images from Drive ---
for filename, file_id in image_ids.items():
    if not os.path.exists(filename):
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        wget.download(url, filename)

# --- Download and load CSV from Drive ---
csv_id = '1plAz7EEeNs8j6WEYaBdLywyX9A9qMprS'
csv_url = f'https://drive.google.com/uc?export=download&id={csv_id}'
csv_filename = 'phone_behavior_data.csv'
if not os.path.exists(csv_filename):
    wget.download(csv_url, csv_filename)

try:
    df = pd.read_csv(csv_filename)
    df['Screen On Time (min/day)'] = df['Screen On Time (hours/day)'] * 60
    df['Engagement Ratio'] = df['App Usage Time (min/day)'] / df['Screen On Time (min/day)']
except Exception as e:
    st.error("Failed to load dataset.")

# --- Navigation logic ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def home():
    st.title("📱 Behavioral Indicators of Phone Addiction")
    st.subheader("Explore the sections below:")
    st.markdown("<div class='main-button'>", unsafe_allow_html=True)
    for i, name in enumerate([
        "1. Our Data",
        "2. Demographics Don't Matter",
        "3. The Story Begins with Variables",
        "4. The Heavy Users",
        "5. Your Number of Apps Define You"
    ]):
        if st.button(name):
            st.session_state.page = f'section{i+1}'
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.page == 'home':
    home()

elif st.session_state.page == 'section1':
    st.header("1. Our Data")
    st.image("opening_gif.gif")
    st.markdown("""
    This dataset captures a rich set of real-world behavioral signals from mobile phone users, including app usage time, screen-on time, data consumption, and the number of apps installed. These variables provide a practical foundation for exploring digital engagement patterns and identifying potential signs of overuse or phone addiction.
    """)
    if st.button("⬅ Back to Home"): st.session_state.page = 'home'

elif st.session_state.page == 'section2':
    st.header("2. Demographics Don't Matter")
    st.image("bimodal_distribution.png")
    st.image("demographics_boxplots.png")
    st.markdown("Chi-square tests show no meaningful link between gender, OS, device model, or age band and high usage.")
    if st.button("⬅ Back to Home"): st.session_state.page = 'home'

elif st.session_state.page == 'section3':
    st.header("3. The Story Begins with Variables")
    fig, axs = plt.subplots(1, 2, figsize=(16, 5))
    sns.histplot(df['App Usage Time (min/day)'], binwidth=15, kde=True, ax=axs[0])
    axs[0].set_title("App Usage Time Distribution")
    sns.histplot(df['Screen On Time (hours/day)'], binwidth=0.5, kde=True, ax=axs[1])
    axs[1].set_title("Screen On Time Distribution")
    st.pyplot(fig)
    st.image("final_summary_banner.png")
    st.markdown("App Usage Time shows a clear bimodal distribution, with peaks around 100 and 500 minutes/day. Screen-On Time stretches up to 12 hours.")
    if st.button("⬅ Back to Home"): st.session_state.page = 'home'

elif st.session_state.page == 'section4':
    st.header("4. The Heavy Users")
    fig, ax = plt.subplots(figsize=(10, 6))
    melted = pd.melt(df,
        id_vars='User Behavior Class',
        value_vars=['App Usage Time (min/day)', 'Screen On Time (hours/day)'],
        var_name='Metric',
        value_name='Minutes per Day')
    melted['Minutes per Day'] = np.where(melted['Metric'].str.contains('hour'), melted['Minutes per Day']*60, melted['Minutes per Day'])
    sns.barplot(data=melted, x='User Behavior Class', y='Minutes per Day', hue='Metric', ci=95, ax=ax)
    ax.set_title("Avg Screen & App Usage Time by Class")
    st.pyplot(fig)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    df['Engagement Ratio Clipped'] = df['Engagement Ratio'].clip(upper=1.2)
    sns.pointplot(data=df, x='User Behavior Class', y='Engagement Ratio Clipped', ci='sd', capsize=0.1, ax=ax2)
    ax2.set_title("App Time as % of Screen Time")
    st.pyplot(fig2)
    st.image("final_summary_banner.png")
    st.markdown("T-tests confirm that Class 5 tops every behavioural metric (p < 0.001). Class 5 averages ~0.9 engagement.")
    if st.button("⬅ Back to Home"): st.session_state.page = 'home'

elif st.session_state.page == 'section5':
    st.header("5. Your Number of Apps Define You")
    df['Number of Apps Installed'] = df['Number of Apps Installed'].astype(float)
    X = sm.add_constant(df[['Number of Apps Installed']])
    y = df['Screen On Time (min/day)']
    model = sm.OLS(y, X).fit()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='Number of Apps Installed', y='Screen On Time (min/day)', data=df, ax=ax, scatter_kws={'alpha':0.4})
    ax.set_title("Regression: Apps Installed vs. Screen Time")
    st.pyplot(fig)
    st.image("engagement_ratio.png")
    st.markdown("""
    The model revealed a strong and significant relationship:

    - Each additional app increases screen-on time by approx. 6.5 min/day.
    - R² = 0.897 confirms the tight linear relationship.
    - Visual confirmation from the regression and engagement images.
    """)
    if st.button("⬅ Back to Home"): st.session_state.page = 'home'
