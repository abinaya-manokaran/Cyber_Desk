import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from gtts import gTTS

# Streamlit Page Config
st.set_page_config(page_title="Rural Cyber-Help Desk", page_icon="🛡️", layout="wide")

st.title("🛡️ Rural Community Cyber-Help Desk: Complete 6-Module Analytics Dashboard")

# 1. Multi-Language Selection
language = st.sidebar.selectbox(
    "🌐 Choose Assistant Language / மொழியைத் தேர்ந்தெடுக்கவும்:", 
    ["Tamil (தமிழ்)", "Tanglish", "English"]
)

if language == "Tamil (தமிழ்)":
    lang_code = "ta"
    sim_title = "📲 லைவ் SMS அறிவிப்பு & 6-Analytics பகுப்பாய்வு"
    analyze_btn = "🔔 பகுப்பாய்வு செய்து தீர்வு காண்க (Analyze & Prescribe)"
    scam_msg = "🚨 எச்சரிக்கை: மோசடி கண்டறியப்பட்டது!"
    safe_msg = "✅ பாதுகாப்பு: இது சாதாரண செய்தி."
    input_label = "✍️ சொந்தமாக SMS டைப் செய்யவும் அல்லது தேர்வு செய்யவும்:"
    voice_scam = "எச்சரிக்கை! இது ஒரு போலியான மோசடி குறுஞ்செய்தி. யாரும் எந்த இணைப்பையும் கிளிக் செய்ய வேண்டாம்."
    voice_safe = "பாதுகாப்பான செய்தி."
elif language == "Tanglish":
    lang_code = "en"
    sim_title = "📲 Live SMS Notification & 6-Analytics Dashboard"
    analyze_btn = "🔔 Analyze & Prescription Eduthukonga"
    scam_msg = "🚨 ALERT: Scam Detected!"
    safe_msg = "✅ SAFE: Legitimate Message."
    input_label = "✍️ Custom SMS Type/Paste Pannunga:"
    voice_scam = "Warning! Scam message detected. Do not click links."
    voice_safe = "Safe message."
else:
    lang_code = "en"
    sim_title = "📲 Live SMS Notification & 6-Analytics Dashboard"
    analyze_btn = "🔔 Analyze & Generate Prescription"
    scam_msg = "🚨 ALERT: Scam Detected!"
    safe_msg = "✅ SAFE: Legitimate Message."
    input_label = "✍️ Enter or Paste Custom SMS Received:"
    voice_scam = "Warning! Scam message detected. Do not click any links."
    voice_safe = "Safe message."

# --- MODELS TRAINING (Modules 1 to 6 Backend Setup) ---
# 1 & 2. Descriptive & Predictive (Simulated Trend & Loss Prediction)
years = ['2024', '2025', '2026 (Est)', '2027 (Proj)', '2028 (Proj)']
fraud_losses = [45, 68, 95, 130, 175] # in Crores

# 3. Cognitive NLP Model (Pooja's Part)
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
nlp_model = MultinomialNB()
nlp_model.fit(X_train, labels)

# 4. Behavioral K-Means Model (Abinaya's Part)
behavior_data = pd.DataFrame({
    'Monthly_Transactions': [2, 25, 22, 3, 20, 1, 18, 24, 4, 15],
    'Digital_Awareness_Score': [20, 90, 88, 25, 82, 15, 85, 92, 30, 78],
    'Risk_Label': [1, 0, 0, 1, 0, 1, 0, 0, 1, 0] # 1: High Risk, 0: Safe
})
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
behavior_data['Risk_Cluster'] = kmeans.fit_predict(behavior_data[['Monthly_Transactions', 'Digital_Awareness_Score']])

# 5. Diagnostic Model (Root Cause Analysis using Decision Tree Feature Importance)
X_diag = behavior_data[['Monthly_Transactions', 'Digital_Awareness_Score']]
y_diag = behavior_data['Risk_Label']
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_diag, y_diag)
importance = dt_model.feature_importances_

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
        # Prediction
        X_test = vectorizer.transform([selected_sms])
        prediction = nlp_model.predict(X_test)[0]
        prob = nlp_model.predict_proba(X_test)[0]
        scam_score = prob[0] * 100 if nlp_model.classes_[0] == 'Scam' else prob[1] * 100

        # Voice output via gTTS
        voice_text = voice_scam if prediction == 'Scam' else voice_safe
        try:
            tts = gTTS(text=voice_text, lang=lang_code, slow=False)
            audio_path = "temp_voice.mp3"
            tts.save(audio_path)
            st.audio(audio_path, format="audio/mp3", autoplay=True)
        except:
            pass

        # Displaying 6 Analytics Modules in Tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "1. Descriptive", "2. Predictive", "3. Cognitive (NLP)", 
            "4. Behavioral (K-Means)", "5. Diagnostic (Root-Cause)", "6. Prescriptive (Action)"
        ])

        with tab1:
            st.markdown("### 📊 Descriptive Analytics (Historical Trend)")
            st.write("Past records show cyber fraud attempts increasing rapidly across rural sectors.")
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(years[:2], fraud_losses[:2], marker='o', color='blue', linewidth=2)
            ax.set_ylabel("Fraud Cases (Thousands)")
            st.pyplot(fig)

        with tab2:
            st.markdown("### 📈 Predictive Analytics (Future Fraud Growth)")
            st.write("Linear Regression projection of cyber financial loss for upcoming years.")
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(years, fraud_losses, marker='s', color='orange', linestyle='--', linewidth=2)
            ax.set_ylabel("Projected Losses (Crores)")
            st.pyplot(fig)

        with tab3:
            st.markdown("### 🧠 Cognitive Analytics (Pooja's NLP Module)")
            st.info(f"Analyzed Text: _{selected_sms}_")
            if prediction == 'Scam':
                st.error(scam_msg)
            else:
                st.success(safe_msg)
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(['Safe Score', 'Scam Risk Score'], [100 - scam_score, scam_score], color=['green', 'red'])
            st.pyplot(fig)

        with tab4:
            st.markdown("### 👥 Behavioral Analytics (Abinaya's K-Means Module)")
            st.write("User Risk Segmentation based on digital habits & literacy.")
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.scatter(behavior_data[behavior_data['Risk_Cluster'] == 0]['Monthly_Transactions'], 
                       behavior_data[behavior_data['Risk_Cluster'] == 0]['Digital_Awareness_Score'], color='green', label='Safe')
            ax.scatter(behavior_data[behavior_data['Risk_Cluster'] == 1]['Monthly_Transactions'], 
                       behavior_data[behavior_data['Risk_Cluster'] == 1]['Digital_Awareness_Score'], color='red', label='High Risk')
            ax.legend(loc='lower right')
            st.pyplot(fig)

        with tab5:
            st.markdown("### 🔍 Diagnostic Analytics (Root-Cause Feature Importance)")
            st.write("Why do rural users fall prey? Decision Tree identifies core vulnerability drivers:")
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(['Monthly Transactions', 'Digital Awareness Score'], importance, color=['purple', 'teal'])
            ax.set_ylabel("Impact Weight")
            st.pyplot(fig)

        with tab6:
            st.markdown("### 🛡️ Prescriptive Analytics (Actionable Solution Engine)")
            if prediction == 'Scam':
                st.error("🚨 CRITICAL ACTION REQUIRED FOR RURAL CITIZEN:")
                st.markdown("""
                1. **Immediate Action:** Do not click links or share UPI PIN / OTP.
                2. **Emergency Helpline:** Call **1930** (National Cyber Crime Helpline) immediately.
                3. **Official Reporting:** File a complaint at [cybercrime.gov.in](https://cybercrime.gov.in).
                4. **Community Alert:** Notify local village cyber volunteer help desk.
                """)
            else:
                st.success("✅ SYSTEM PRESCRIPTION:")
                st.markdown("""
                - Message appears safe. Standard digital hygiene maintained. No action needed.
                """)
    else:
        st.warning("Dayavu seithu message-ai type seyyavum.")
