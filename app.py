import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans

# Streamlit Page Config
st.set_page_config(page_title="Cyber-Help Desk", page_icon="🛡️", layout="wide")

st.title("🛡️ Rural Community Cyber-Help Desk: AI Scam & Risk Analyzer")

# 1. Language Selector
language = st.sidebar.selectbox(
    "🌐 Choose Language / மொழியைத் தேர்ந்தெடுக்கவும்:", 
    ["Tanglish", "Tamil (தமிழ்)", "English"]
)

# Text Translations
if language == "Tamil (தமிழ்)":
    subtitle = "கிராமப்புற மக்களுக்கான குரல் வழி மற்றும் நேரலை சைபர் மோசடி பகுப்பாய்வு உதவி மையம்."
    voice_label = "🎙️ குரல் மூலம் பேசவும் / Voice Assistant (SMS-ஐப் படிக்கவும்):"
    sample_label = "📲 போனுக்கு வந்த குறுஞ்செய்தியைத் தேர்ந்தெடுக்கவும் (Quick Select SMS):"
    nlp_title = "🧠 Cognitive Analytics (NLP Scam Detection)"
    kmeans_title = "📊 Behavioral Analytics (K-Means User Risk Segmentation)"
    scam_msg = "🚨 எச்சரிக்கை: இது ஆபத்தான மோசடி குறுஞ்செய்தி! எந்த இணைப்பையும் கிளிக் செய்ய வேண்டாம்."
    safe_msg = "✅ பாதுகாப்பு: இது சாதாரண நம்பகமான குறுஞ்செய்தி."
elif language == "English":
    subtitle = "Voice-assisted and Live AI-driven Cyber Fraud Analysis for Rural Communities."
    voice_label = "🎙️ Speak / Voice Assistant (Read SMS aloud):"
    sample_label = "📲 Quick Select Recent Incoming SMS Notification:"
    nlp_title = "🧠 Cognitive Analytics (NLP Scam Detection)"
    kmeans_title = "📊 Behavioral Analytics (K-Means User Risk Segmentation)"
    scam_msg = "🚨 ALERT: SCAM DETECTED! Do not click any links or share OTP!"
    safe_msg = "✅ SAFE: This is a legitimate and safe message."
else:  # Tanglish
    subtitle = "Gramathu makkalukana Voice-assisted Live Cyber Scam & Risk Analyzer."
    voice_label = "🎙️ Voice Assistant (Message-ah pesi analyze pannunga):"
    sample_label = "📲 Phone-ku vantha SMS Notification-ah choose pannunga:"
    nlp_title = "🧠 Cognitive Analytics (NLP Scam Detection)"
    kmeans_title = "📊 Behavioral Analytics (K-Means User Risk Segmentation)"
    scam_msg = "🚨 ALERT: SCAM DETECTED! Idhu fake message, link-ah click panna vendam!"
    safe_msg = "✅ SAFE: Idhu normal-ana safe message thaan."

st.write(f"*{subtitle}*")
st.markdown("---")

# ---------------------------------------------------------
# 2. ML Models Setup (NLP & K-Means)
# ---------------------------------------------------------
# NLP Training Data
training_messages = [
    "Your bank account is blocked. Click the link to update KYC immediately.",
    "Congratulations! You won a lottery of 10 lakhs. Call this number to claim.",
    "Hi, are we meeting for project discussion tomorrow at 10 AM?",
    "Urgent: Your electricity bill will be disconnected tonight. Pay via this link.",
    "Your OTP for banking transaction is 4892. Do not share with anyone.",
    "Mom, please pick up some groceries on your way back home.",
    "Your credit card reward points are expiring today. Redeem now.",
    "Hey, let's catch up for coffee this weekend."
]
labels = ['Scam', 'Scam', 'Non-Scam', 'Scam', 'Non-Scam', 'Non-Scam', 'Scam', 'Non-Scam']

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_messages)
nlp_model = MultinomialNB()
nlp_model.fit(X_train, labels)

# K-Means Behavioral Clustering Setup
behavior_data = pd.DataFrame({
    'User_ID': range(1, 11),
    'Monthly_Transactions': [2, 25, 22, 3, 20, 1, 18, 24, 4, 15],
    'Digital_Awareness_Score': [20, 90, 88, 25, 82, 15, 85, 92, 30, 78]
})
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
behavior_data['Risk_Cluster'] = kmeans.fit_predict(behavior_data[['Monthly_Transactions', 'Digital_Awareness_Score']])

# ---------------------------------------------------------
# 3. Live Interface (Voice Assistant & Real-Time Select)
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📩 Live SMS Input / Notification Simulator")
    
    # Quick Incoming SMS Simulation Dropdown
    sample_sms = st.selectbox(
        sample_label,
        [
            "-- Select / Choose SMS --",
            "Urgent: Your bank account is blocked. Click link to update KYC immediately.",
            "Congratulations! You won a cash reward of 5 Lakhs. Click to claim.",
            "Your electricity bill disconnection notice. Pay immediately via link.",
            "Hi Abinaya, can you share the project update notes by evening?",
            "Your OTP for payment is 9042. Do not disclose to anyone."
        ]
    )
    
    # Manual / Audio Input Box
    user_message = st.text_area(voice_label, value="" if sample_sms.startswith("--") else sample_sms, height=100)

# ---------------------------------------------------------
# 4. Live Analytics Execution
# ---------------------------------------------------------
with col2:
    st.subheader(nlp_title)
    
    if user_message.strip() != "":
        # NLP Cognitive Analysis
        X_test = vectorizer.transform([user_message])
        prediction = nlp_model.predict(X_test)[0]
        
        if prediction == 'Scam':
            st.error(scam_msg)
            # Browser Voice Alert Speech Synthesis HTML
            st.components.v1.html(
                f"<script>var msg = new SpeechSynthesisUtterance('Alert! Scam Message Detected.'); window.speechSynthesis.speak(msg);</script>",
                height=0
            )
        else:
            st.success(safe_msg)
            st.components.v1.html(
                f"<script>var msg = new SpeechSynthesisUtterance('Safe Message.'); window.speechSynthesis.speak(msg);</script>",
                height=0
            )
            
        st.markdown("---")
        st.subheader(kmeans_title)
        
        # Dynamic Behavioral Cluster Chart
        fig, ax = plt.subplots(figsize=(6, 3.5))
        
        # User Risk Assignment Based on Message Threat Level
        current_user_awareness = 20 if prediction == 'Scam' else 85
        current_user_tx = 3 if prediction == 'Scam' else 20
        
        ax.scatter(behavior_data[behavior_data['Risk_Cluster'] == 0]['Monthly_Transactions'], 
                   behavior_data[behavior_data['Risk_Cluster'] == 0]['Digital_Awareness_Score'], 
                   color='red', s=80, label='High Risk (Low Literacy)')
        
        ax.scatter(behavior_data[behavior_data['Risk_Cluster'] == 1]['Monthly_Transactions'], 
                   behavior_data[behavior_data['Risk_Cluster'] == 1]['Digital_Awareness_Score'], 
                   color='green', s=80, label='Low Risk (Digitally Aware)')
        
        # Highlight Current Analyzing User
        ax.scatter([current_user_tx], [current_user_awareness], color='yellow', edgecolor='black', s=200, marker='*', label='Current Live User')
        
        ax.set_xlabel("Monthly Transactions")
        ax.set_ylabel("Digital Awareness Score")
        ax.legend(fontsize=8)
        ax.grid(True)
        st.pyplot(fig)
        
    else:
        st.info("👈 Choose or speak an SMS message on the left to view Live Cognitive & Behavioral Analytics!")
