import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import random

# Page Configuration
st.set_page_config(page_title="Rural Cyber-Help Desk", page_icon="🛡️", layout="wide")

st.title("🛡️ Community Cyber-Help Desk: Real-Time Scam & Behavioral Analytics")

# 1. Sidebar - Language & Voice Assistant Settings
st.sidebar.header("🌐 Help Desk Settings")
language = st.sidebar.selectbox("Select Language / மொழி:", ["Tamil (தமிழ்)", "Tanglish", "English"])
voice_enabled = st.sidebar.checkbox("🔊 Enable Voice Assistant (குரல் உதவி)", value=True)

# Language Mapping
if language == "Tamil (தமிழ்)":
    sub_title = "கிராமப்புற மக்களுக்கான நேரலை சைபர் மோசடி கண்டறிதல் மற்றும் பகுப்பாய்வு மையம்."
    btn_text = "📲 நேரலை SMS நோட்டிபிகேஷனைப் பெறுக (Simulate SMS)"
    anal_title = "📊 நேரலை பகுப்பாய்வு (Live Analytics Dashboard)"
elif language == "English":
    sub_title = "Real-time AI-Driven Scam Detection & Risk Analytics for Rural Communities."
    btn_text = "📲 Receive Live Incoming SMS"
    anal_title = "📊 Live Analytics Dashboard"
else:  # Tanglish
    sub_title = "Gramathu makkalukaana real-time AI scam detection app."
    btn_text = "📲 Live Incoming SMS Simulate Pannunga"
    anal_title = "📊 Live Analytics Dashboard"

st.markdown(f"*{sub_title}*")

# 2. NLP Model Training Setup (Cognitive Analytics)
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

# Session State Initialization for Live Analytics tracking
if 'processed_count' not in st.session_state:
    st.session_state['processed_count'] = 0
    st.session_state['scam_count'] = 0
    st.session_state['safe_count'] = 0
    st.session_state['current_msg'] = ""

# Sample incoming SMS pool for quick testing without typing
sample_sms_pool = [
    "ALERT: Your SBI Debit Card is suspended. Click http://sbi-verify.com to unblock.",
    "Can you please send the notes for data analytics class?",
    "WINNER! You have won Rs 50,000 cash prize. Call 9876543210 now.",
    "Dear Customer, your electricity connection will be cut at 9 PM. Pay bill now.",
    "Hi, I reached home safely. Will call you later."
]

# Layout Split: Left (Notification & Input) | Right (Analytics)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📲 Live SMS Notification Listener")
    
    # Simulate Incoming SMS Button (For Rural People Simulation)
    if st.button(btn_text):
        st.session_state['current_msg'] = random.choice(sample_sms_pool)
    
    # Manual Input option (If needed)
    user_input = st.text_area("Or incoming SMS content:", value=st.session_state['current_msg'], height=100)
    
    analyzed_status = None
    voice_msg = ""
    
    if user_input.strip() != "":
        X_test = vectorizer.transform([user_input])
        pred = nlp_model.predict(X_test)[0]
        probs = nlp_model.predict_proba(X_test)[0]
        scam_prob = probs[list(nlp_model.classes_).index('Scam')] * 100
        
        st.session_state['processed_count'] += 1
        
        if pred == 'Scam':
            st.session_state['scam_count'] += 1
            st.error(f"🚨 **SCAM DETECTED!** (Risk Level: {scam_prob:.1f}%)")
            if language == "Tamil (தமிழ்)":
                voice_msg = "எச்சரிக்கை! இது ஒரு போலி செய்தி. யாருக்கும் பணம் அனுப்ப வேண்டாம்!"
            elif language == "English":
                voice_msg = "Warning! This is a scam message. Do not click any link!"
            else:
                voice_msg = "Alert! Idhu oru fake message. Link-ai click செய்ய வேண்டாம்!"
        else:
            st.session_state['safe_count'] += 1
            st.success(f"✅ **SAFE MESSAGE** (Safety Score: {100-scam_prob:.1f}%)")
            if language == "Tamil (தமிழ்)":
                voice_msg = "இது ஒரு பாதுகாப்பான சாதாரண செய்தி."
            elif language == "English":
                voice_msg = "This is a safe and normal message."
            else:
                voice_msg = "Idhu oru normal-aana safe message."

        # JavaScript Web Speech API Integration for Native Voice Output
        if voice_enabled and voice_msg:
            tts_script = f"""
                <script>
                    var msg = new SpeechSynthesisUtterance("{voice_msg}");
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                </script>
            """
            components.html(tts_script, height=0)

with col2:
    st.subheader(anal_title)
    
    # Live Counters
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Analyzed", st.session_state['processed_count'])
    m2.metric("Scams Blocked 🚨", st.session_state['scam_count'])
    m3.metric("Safe Messages ✅", st.session_state['safe_count'])
    
    st.write("---")
    
    # Behavioral Analytics - K-Means Clustering Visual
    st.subheader("🧠 Behavioral Risk Segmentation (K-Means)")
    
    # Synthetic live behavioral data based on help desk activity
    np.random.seed(42)
    awareness = np.random.randint(10, 95, 12)
    tx_freq = np.random.randint(1, 30, 12)
    
    df_kmeans = pd.DataFrame({'Transactions': tx_freq, 'Awareness': awareness})
    km = KMeans(n_clusters=2, random_state=42, n_init=10)
    df_kmeans['Cluster'] = km.fit_predict(df_kmeans[['Transactions', 'Awareness']])
    
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.scatter(df_kmeans[df_kmeans['Cluster']==0]['Transactions'], 
               df_kmeans[df_kmeans['Cluster']==0]['Awareness'], color='red', label='High Risk Group')
    ax.scatter(df_kmeans[df_kmeans['Cluster']==1]['Transactions'], 
               df_kmeans[df_kmeans['Cluster']==1]['Awareness'], color='green', label='Safe Group')
    ax.set_xlabel("Monthly Digital Usage")
    ax.set_ylabel("Digital Awareness Score")
    ax.legend(loc='lower right', fontsize='small')
    ax.grid(True)
    st.pyplot(fig)
