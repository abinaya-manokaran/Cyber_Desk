import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from gtts import gTTS
import os

# Streamlit Page Config
st.set_page_config(page_title="Rural Cyber-Help Desk", page_icon="🛡️", layout="wide")

# App Header
st.title("🛡️ Rural Community Cyber-Help Desk: Real-Time Scam & Risk Analytics")

# 1. Multi-Language Selection
language = st.sidebar.selectbox(
    "🌐 Choose Assistant Language / மொழியைத் தேர்ந்தெடுக்கவும்:", 
    ["Tamil (தமிழ்)", "Tanglish", "English"]
)

# Language Dictionary for UI & Speech Configuration
if language == "Tamil (தமிழ்)":
    tts_lang = "ta"
    sim_title = "📲 புதிய SMS அறிவிப்பு பகுப்பாய்வு (SMS Notification Analysis)"
    analyze_btn = "🔔 அறிவிப்பை பகுப்பாய்வு செய் (Read & Analyze SMS)"
    scam_msg = "🚨 எச்சரிக்கை: இது ஒரு மோசடி குறுஞ்செய்தி! எந்த இணைப்பையும் கிளிக் செய்ய வேண்டாம்!"
    safe_msg = "✅ பாதுகாப்பு: இது ஒரு சாதாரண குறுஞ்செய்திதான்."
    input_label = "✍️ சொந்தமாக SMS டைப் செய்யவும் அல்லது தேர்வு செய்யவும் (Enter or Paste Custom SMS):"
    
    # Tamil Voice Text
    voice_scam = "எச்சரிக்கை! இது ஒரு போலியான மோசடி குறுஞ்செய்தி. யாரும் எந்த இணைப்பையும் கிளிக் செய்ய வேண்டாம்."
    voice_safe = "பாதுகாப்பான செய்தி. இது ஒரு சாதாரண குறுஞ்செய்திதான்."

elif language == "Tanglish":
    tts_lang = "en"
    sim_title = "📲 Puthu SMS Notification Analysis"
    analyze_btn = "🔔 Notification Read & Analyze Pannu"
    scam_msg = "🚨 ALERT: Idhu oru Fake Fraud Message! Link-ai click seyyavendam!"
    safe_msg = "✅ SAFE: Idhu normal message thaan."
    input_label = "✍️ Custom SMS Type/Paste Pannunga:"
    
    # Tanglish Voice Text
    voice_scam = "Warning! Idhu oru fake fraud message. Yaarum link-ai click seyyavendam!"
    voice_safe = "Safe message. Idhu oru normal message thaan."

else: # English
    tts_lang = "en"
    sim_title = "📲 Live Incoming SMS Notification Analysis"
    analyze_btn = "🔔 Read & Analyze Notification"
    scam_msg = "🚨 ALERT: Scam Detected! Do not click any links!"
    safe_msg = "✅ SAFE: Legitimate Message."
    input_label = "✍️ Enter or Paste Custom SMS Received:"
    
    # English Voice Text
    voice_scam = "Warning! Scam message detected. Do not click any links."
    voice_safe = "Safe message. This is a legitimate message."

# --- MODEL TRAINING SECTION ---
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

# Behavioral K-Means Model
behavior_data = pd.DataFrame({
    'User_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Monthly_Transactions': [2, 25, 22, 3, 20, 1, 18, 24, 4, 15],
    'Digital_Awareness_Score': [20, 90, 88, 25, 82, 15, 85, 92, 30, 78]
})
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
behavior_data['Risk_Cluster'] = kmeans.fit_predict(behavior_data[['Monthly_Transactions', 'Digital_Awareness_Score']])

# --- UI DASHBOARD LAYOUT ---
st.subheader(sim_title)

# Option to toggle between Preset Samples and Custom Manual Input
input_mode = st.radio("Choose Input Mode:", ["✍️ Type Custom SMS", "📋 Select Sample SMS"])

if input_mode == "📋 Select Sample SMS":
    sample_sms_list = [
        "Urgent: Your SBI Bank Account has been locked! Verify KYC now: http://sbi-fake.com",
        "Hi Abinaya, please bring the computer science notes tomorrow.",
        "Congratulations! You won Rs. 50,000 cash reward. Click to claim immediately.",
        "Your electricity connection will be disconnected by 9 PM tonight due to unpaid bill."
    ]
    selected_sms = st.selectbox("📩 Select Sample Notification:", sample_sms_list)
else:
    selected_sms = st.text_area(input_label, value="Urgent: Your bank account has been suspended! Update details now.")

# Permission Toggle Simulation
allow_notification = st.checkbox("🔔 Allow SMS Read & Voice Alert Permission (இணைப்பு அனுமதி)", value=True)

if allow_notification:
    if st.button(analyze_btn):
        if selected_sms.strip() != "":
            # NLP Cognitive Analysis
            X_test = vectorizer.transform([selected_sms])
            prediction = nlp_model.predict(X_test)[0]
            prob = nlp_model.predict_proba(X_test)[0]
            scam_score = prob[0] * 100 if nlp_model.classes_[0] == 'Scam' else prob[1] * 100

            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### 🧠 Cognitive Analytics (NLP Analysis)")
                st.info(f"**Incoming Message Text:**\n_{selected_sms}_")
                
                if prediction == 'Scam':
                    st.error(scam_msg)
                    voice_text = voice_scam
                else:
                    st.success(safe_msg)
                    voice_text = voice_safe

                # Reliable Audio Generation using gTTS for Tamil and other languages
                try:
                    tts = gTTS(text=voice_text, lang=tts_lang, slow=False)
                    audio_file = "voice_alert.mp3"
                    tts.save(audio_file)
                    st.audio(audio_file, format='audio/mp3', autoplay=True)
                except Exception as e:
                    st.warning("Audio generation note: Text alert active.")

                # Live Bar Chart for Cognitive NLP Scam Confidence
                st.markdown("#### 📊 Live Scam Risk Score")
                fig_cog, ax_cog = plt.subplots(figsize=(5, 3))
                ax_cog.bar(['Safe Score', 'Scam Risk Score'], [100 - scam_score, scam_score], color=['green', 'red'])
                ax_cog.set_ylabel("Percentage (%)")
                st.pyplot(fig_cog)

            with col2:
                st.markdown("### 📊 Behavioral Analytics (K-Means Clustering)")
                st.write("User Risk Segmentation for Rural Community")
                
                # Live Plotting K-Means
                fig_beh, ax_beh = plt.subplots(figsize=(5, 3.8))
                
                cluster_0_data = behavior_data[behavior_data['Risk_Cluster'] == 0]
                cluster_1_data = behavior_data[behavior_data['Risk_Cluster'] == 1]

                ax_beh.scatter(cluster_0_data['Monthly_Transactions'], 
                               cluster_0_data['Digital_Awareness_Score'], 
                               color='red', label='High Risk (Low Literacy)', s=80)
                
                ax_beh.scatter(cluster_1_data['Monthly_Transactions'], 
                               cluster_1_data['Digital_Awareness_Score'], 
                               color='green', label='Safe Users', s=80)
                
                # Highlighting current simulated target user
                ax_beh.scatter([2], [20], color='yellow', edgecolor='black', s=200, marker='*', label='Current SMS Recipient')
                ax_beh.set_xlabel('Monthly Digital Transactions')
                ax_beh.set_ylabel('Digital Awareness Score')
                ax_beh.legend(loc='lower right', fontsize='small')
                ax_beh.grid(True)
                st.pyplot(fig_beh)
        else:
            st.warning("Please type or select a message to analyze.")
