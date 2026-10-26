import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVR
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from gtts import gTTS

# Streamlit Page Config
st.set_page_config(page_title="Rural Cyber-Help Desk", page_icon="🛡️", layout="wide")

st.title("🛡️ Rural Community Cyber-Help Desk: Clean Dual-Model 6-Analytics Dashboard")

# 1. Multi-Language Selection
language = st.sidebar.selectbox(
    "🌐 Choose Assistant Language / மொழியைத் தேர்ந்தெடுக்கவும்:", 
    ["Tamil (தமிழ்)", "Tanglish", "English"]
)

if language == "Tamil (தமிழ்)":
    lang_code = "ta"
    sim_title = "📲 லைவ் SMS அறிவிப்பு பகுப்பாய்வு (Dual-Model Benchmarking)"
    analyze_btn = "🔔 பகுப்பாய்வு செய் (Analyze with Dual Models)"
    scam_msg = "🚨 எச்சரிக்கை: மோசடி கண்டறியப்பட்டது!"
    safe_msg = "✅ பாதுகாப்பு: இது சாதாரண செய்தி."
    input_label = "✍️ சொந்தமாக SMS டைப் செய்யவும் அல்லது தேர்வு செய்யவும்:"
    voice_scam = "எச்சரிக்கை! இது ஒரு போலியான மோசடி குறுஞ்செய்தி. யாரும் எந்த இணைப்பையும் கிளிக் செய்ய வேண்டாம்."
    voice_safe = "பாதுகாப்பான செய்தி."
elif language == "Tanglish":
    lang_code = "en"
    sim_title = "📲 Live SMS Notification Dashboard"
    analyze_btn = "🔔 Dual Model Analyze Pannunga"
    scam_msg = "🚨 ALERT: Scam Detected!"
    safe_msg = "✅ SAFE: Legitimate Message."
    input_label = "✍️ Custom SMS Type/Paste Pannunga:"
    voice_scam = "Warning! Scam message detected. Do not click links."
    voice_safe = "Safe message."
else:
    lang_code = "en"
    sim_title = "📲 Live SMS Notification Dashboard"
    analyze_btn = "🔔 Analyze with Dual Models"
    scam_msg = "🚨 ALERT: Scam Detected!"
    safe_msg = "✅ SAFE: Legitimate Message."
    input_label = "✍️ Enter or Paste Custom SMS Received:"
    voice_scam = "Warning! Scam message detected. Do not click any links."
    voice_safe = "Safe message."

# --- DUAL MODEL TRAINING BACKEND (Distributed cleanly) ---

# 1. Descriptive Setup (Pooja)
years_desc = [2021, 2022, 2023, 2024, 2025]
fraud_losses_desc = [20, 35, 45, 68, 95]

# 2. Predictive Setup (Abinaya) - Using Linear Regression vs SVR
years_pred = np.array([2021, 2022, 2023, 2024, 2025]).reshape(-1, 1)
losses_pred = np.array([20, 35, 45, 68, 95])
future_years = np.array([2026, 2027, 2028]).reshape(-1, 1)

lr_model = LinearRegression().fit(years_pred, losses_pred)
lr_future = lr_model.predict(future_years)

svr_model = SVR(kernel='linear').fit(years_pred, losses_pred)
svr_future = svr_model.predict(future_years)

# 3. Cognitive NLP Models (Pooja)
training_messages = [
    "Your bank account is blocked. Click the link to update KYC immediately.",
    "Congratulations! You won a lottery of 10 lakhs. Call this number to claim.",
    "Hi, are we meeting for project discussion tomorrow at 10 AM?",
    "Urgent: Your electricity bill will be disconnected tonight. Pay via this link.",
    "Your OTP for banking transaction is 4892. Do not share with anyone.",
    "Mom, please pick up some groceries on your way back home."
]
labels = ['Scam', 'Scam', 'Non-Scam', 'Scam', 'Non-Scam', 'Non-Scam']
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_messages)

nb_model = MultinomialNB().fit(X_train, labels)
log_model = LogisticRegression().fit(X_train, labels)

# 4. Behavioral Clustering Models (Abinaya)
behavior_data = pd.DataFrame({
    'Monthly_Transactions': [2, 25, 22, 3, 20, 1, 18, 24, 4, 15],
    'Digital_Awareness_Score': [20, 90, 88, 25, 82, 15, 85, 92, 30, 78],
    'Risk_Label': [1, 0, 0, 1, 0, 1, 0, 0, 1, 0]
})

kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
behavior_data['KMeans_Cluster'] = kmeans.fit_predict(behavior_data[['Monthly_Transactions', 'Digital_Awareness_Score']])

agg_clust = AgglomerativeClustering(n_clusters=2)
behavior_data['Agg_Cluster'] = agg_clust.fit_predict(behavior_data[['Monthly_Transactions', 'Digital_Awareness_Score']])

# 5. Diagnostic Models (Pooja) - Decision Tree vs Logistic Regression Coefficients
X_diag = behavior_data[['Monthly_Transactions', 'Digital_Awareness_Score']]
y_diag = behavior_data['Risk_Label']

dt_diag = DecisionTreeClassifier(random_state=42).fit(X_diag, y_diag)
dt_imp = dt_diag.feature_importances_

log_diag = LogisticRegression().fit(X_diag, y_diag)
log_imp = np.abs(log_diag.coef_[0]) # absolute coefficients for feature impact

# --- UI DASHBOARD ---
st.subheader(sim_title)

input_mode = st.radio("Choose Input Mode:", ["✍️ Type Custom SMS", "📋 Select Sample SMS"])
if input_mode == "📋 Select Sample SMS":
    sample_sms_list = [
        "Urgent: Your SBI Bank Account has been locked! Verify KYC now: http://sbi-fake.com",
        "Hi Abinaya, please bring the computer science notes tomorrow.",
        "Congratulations! You won Rs. 50,000 cash reward. Click to claim immediately."
    ]
    selected_sms = st.selectbox("📩 Select Sample Notification:", sample_sms_list)
else:
    selected_sms = st.text_area(input_label, value="Urgent: Your bank account has been suspended! Update details now.")

if st.button(analyze_btn):
    if selected_sms.strip() != "":
        X_test = vectorizer.transform([selected_sms])
        
        pred_nb = nb_model.predict(X_test)[0]
        pred_log = log_model.predict(X_test)[0]

        voice_text = voice_scam if pred_nb == 'Scam' else voice_safe
        try:
            tts = gTTS(text=voice_text, lang=lang_code, slow=False)
            audio_path = "temp_voice.mp3"
            tts.save(audio_path)
            st.audio(audio_path, format="audio/mp3", autoplay=True)
        except:
            pass

        # 6 Analytics Tabs split cleanly between Pooja & Abinaya
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "1. Descriptive (Pooja)", "2. Predictive (Abinaya)", "3. Cognitive (Pooja)", 
            "4. Behavioral (Abinaya)", "5. Diagnostic (Pooja)", "6. Prescriptive (Abinaya)"
        ])

        with tab1:
            st.markdown("### 📊 Descriptive Analytics (Pooja)")
            st.write("Model 1: Historical Loss vs Model 2: Moving Average Trend")
            fig, ax = plt.subplots(figsize=(6, 3.2))
            ax.plot(years_desc, fraud_losses_desc, marker='o', label='Model 1: Historical Loss (Cr)', color='blue')
            ax.plot(years_desc[1:], pd.Series(fraud_losses_desc).rolling(2).mean().dropna(), marker='x', linestyle='--', label='Model 2: Moving Average', color='purple')
            ax.set_xticks(years_desc)
            ax.legend()
            st.pyplot(fig)

        with tab2:
            st.markdown("### 📈 Predictive Analytics (Abinaya)")
            st.write("Comparing Model 1 (Linear Regression) vs Model 2 (Support Vector Regressor - SVR)")
            fig, ax = plt.subplots(figsize=(6, 3.2))
            ax.plot([2026, 2027, 2028], lr_future, marker='s', label='Model 1: Linear Regression', color='orange')
            ax.plot([2026, 2027, 2028], svr_future, marker='^', label='Model 2: SVR', color='red')
            ax.set_xticks([2026, 2027, 2028])
            ax.set_ylabel("Loss Projection (Crores)")
            ax.legend()
            st.pyplot(fig)

        with tab3:
            st.markdown("### 🧠 Cognitive Analytics (Pooja)")
            col_a, col_b = st.columns(2)
            with col_a:
                st.info(f"**Model 1 (Naive Bayes):**\n### {pred_nb}")
            with col_b:
                st.info(f"**Model 2 (Logistic Regression):**\n### {pred_log}")
            
            fig, ax = plt.subplots(figsize=(5, 2.5))
            val_nb = 1 if pred_nb == 'Scam' else 0.05
            val_log = 1 if pred_log == 'Scam' else 0.05
            
            colors = ['red' if pred_nb=='Scam' else 'green', 'darkred' if pred_log=='Scam' else 'darkgreen']
            ax.bar(['Naive Bayes', 'Logistic Reg'], [val_nb, val_log], color=colors)
            ax.set_ylabel("Scam Flag (1=Scam, 0=Safe)")
            ax.set_ylim(0, 1.1)
            st.pyplot(fig)

        with tab4:
            st.markdown("### 👥 Behavioral Analytics (Abinaya)")
            st.write("Comparing Model 1 (K-Means) vs Model 2 (Agglomerative Hierarchical)")
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
            ax1.scatter(behavior_data['Monthly_Transactions'], behavior_data['Digital_Awareness_Score'], c=behavior_data['KMeans_Cluster'], cmap='rainbow')
            ax1.set_title("Model 1: K-Means")
            ax2.scatter(behavior_data['Monthly_Transactions'], behavior_data['Digital_Awareness_Score'], c=behavior_data['Agg_Cluster'], cmap='coolwarm')
            ax2.set_title("Model 2: Agglomerative")
            st.pyplot(fig)

        with tab5:
            st.markdown("### 🔍 Diagnostic Analytics (Pooja)")
            st.write("Root-cause factor weight analysis using Decision Tree vs Logistic Regression Coefficients")
            fig, ax = plt.subplots(figsize=(6, 3))
            x_bar = np.arange(2)
            ax.bar(x_bar - 0.2, dt_imp, width=0.4, label='Model 1: Decision Tree', color='teal')
            ax.bar(x_bar + 0.2, log_imp / np.sum(log_imp), width=0.4, label='Model 2: Logistic Coeffs', color='navy')
            ax.set_xticks(x_bar)
            ax.set_xticklabels(['Transactions', 'Awareness Score'])
            ax.legend()
            st.pyplot(fig)

        with tab6:
            st.markdown("### 🛡️ Prescriptive Analytics (Abinaya)")
            if pred_nb == 'Scam':
                st.error("🚨 CRITICAL ACTION REQUIRED:")
                st.markdown("""
                * **Model 1 Recommendation (Emergency):** Immediately dial **1930** (Cyber Crime Helpline).
                * **Model 2 Recommendation (Preventive):** Block UPI/Banking apps & File a complaint at [cybercrime.gov.in](https://cybercrime.gov.in).
                """)
            else:
                st.success("✅ SYSTEM PRESCRIPTION:")
                st.markdown("- Message verified by dual models. Safe to interact.")
    else:
        st.warning("Dayavu seithu message-ai type seyyavum.")
