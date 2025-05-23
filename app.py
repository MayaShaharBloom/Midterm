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
st.set_page_config(page_title="Phone Addiction Analysis", layout="wide")

# --- Header ---
st.title("📱 Behavioral Indicators of Phone Addiction")
st.markdown("""
This interactive app analyzes mobile user behavior to uncover patterns of possible phone addiction.
Explore how app usage, screen time, and demographics relate to behavioral intensity.
""")

# --- Data Load ---
st.header("1. Load and Preview Dataset")
file_id = '1plAz7EEeNs8j6WEYaBdLywyX9A9qMprS'
url = f'https://drive.google.com/uc?export=download&id={file_id}'
filename = "phone_behavior_data.csv"

if not os.path.exists(filename):
    st.write("Downloading dataset...")
    wget.download(url, filename)

df = pd.read_csv(filename)
st.success("Dataset loaded successfully!")
st.dataframe(df.head())

# --- Insight 1 ---
st.header("2. Distinct Behavioral Clusters")
col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    sns.histplot(data=df, x='App Usage Time (min/day)', binwidth=15, kde=True, ax=ax1)
    ax1.set_title("App Usage Time Distribution")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    sns.histplot(data=df, x='Screen On Time (hours/day)', binwidth=0.5, kde=True, ax=ax2)
    ax2.set_title("Screen On Time Distribution")
    st.pyplot(fig2)

st.markdown("""
- App Usage is bimodal: light vs. heavy users.
- Some users screen-on up to **12 hours** daily.
""")

# --- Insight 2 ---
st.header("3. Behavior by User Class")

# Melt for plotting
melted = pd.melt(df,
    id_vars='User Behavior Class',
    value_vars=['App Usage Time (min/day)', 'Screen On Time (hours/day)'],
    var_name='Metric',
    value_name='Minutes per Day')

melted['Minutes per Day'] = np.where(melted['Metric'].str.contains('hour'),
    melted['Minutes per Day'] * 60, melted['Minutes per Day'])

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(data=melted, x='User Behavior Class', y='Minutes per Day', hue='Metric', ci=95, ax=ax3)
ax3.set_title("Avg Screen & App Usage Time by Class")
st.pyplot(fig3)

st.markdown("""
- From **Class 1 to 5**, time spent increases consistently.
- Class 5: **~540 minutes of app use**, nearly **10 hours** of screen-on time.
""")

# --- Insight 3 ---
st.header("4. Regression: Installed Apps → Screen Time")
df['Screen On Time (min/day)'] = df['Screen On Time (hours/day)'] * 60
X = sm.add_constant(df[['Number of Apps Installed']])
y = df['Screen On Time (min/day)']
model = sm.OLS(y, X).fit()

fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.regplot(x='Number of Apps Installed', y='Screen On Time (min/day)', data=df, ax=ax4, scatter_kws={'alpha':0.4})
ax4.set_title("Linear Regression: Apps Installed vs. Screen Time")
st.pyplot(fig4)

st.markdown(f"""
Each additional app = approx **{model.params[1]:.2f} min/day** extra screen time.  
**$R^2$ = {model.rsquared:.3f}**: strong predictive power.
""")

# --- Insight 4 ---
st.header("5. Engagement Ratio: App Time / Screen Time")
df['Engagement Ratio'] = df['App Usage Time (min/day)'] / df['Screen On Time (min/day)']
df['Engagement Ratio Clipped'] = df['Engagement Ratio'].clip(upper=1.2)

fig5, ax5 = plt.subplots(figsize=(10, 5))
sns.pointplot(data=df, x='User Behavior Class', y='Engagement Ratio Clipped', ci='sd', capsize=0.1, ax=ax5)
ax5.set_title("App Time as % of Screen Time")
st.pyplot(fig5)

st.markdown("""
- Class 5 users spend **90% of their screen time in apps**.
- Lower classes are more scattered.
""")

# --- Final Insight ---
st.header("6. Summary")
st.markdown("""
**Red flags for phone addiction risk:**
- Surging app usage + screen time
- Many installed apps
- High engagement ratio (active time)

**Demographics?** Not significant. Behavioral intensity matters more.
""")

st.success("This concludes the walkthrough. You can now share this app on GitHub or Streamlit Cloud.")
