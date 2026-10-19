import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
import plotly.express as px

st.set_page_config(page_title="Rural Cyber-Help Desk", layout="wide")

# 1. Voice Assistant Function (Browser Text-to-Speech via JavaScript)
def speak_text(text, lang='ta-IN'):
    js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{text}');
            msg.lang = '{lang}';
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(js_code, height=0)

# Title & Language Selector
st.title("🛡️ Rural Community Cyber-Help Desk (Live Analytics & Voice Assistant)")

language = st.sidebar.selectbox(
    "🌐 Choose Language / மொழி:", 
    ["Tamil (தமிழ்)", "Tanglish", "English"]
)

# Train NLP Scam Model
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

# Train Behavioral K-Means Model
behavior_data = pd.DataFrame({
    'User_ID': range(1, 11),
    'Monthly_Transactions': [2, 25, 22, 3, 20, 1, 18, 24, 4, 15],
    'Digital_Awareness_Score': [20, 90, 88, 25, 82, 15, 85, 92, 30, 78]
})
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
behavior_data['Risk_Cluster'] = kmeans.fit_predict(behavior_data[['Monthly_Transactions', 'Digital_Awareness_Score']])

# 2. Live Notification Simulation Section (No Manual Typing Needed!)
st.subheader("📲 Incoming SMS Live Detector & Voice Alert")

preset_sms = st.radio(
    "Select Simulated Incoming SMS (Notification Simulation):",
    [
        "🚨 [SCAM] Your bank account is blocked. Click link to verify KYC.",
        "🚨 [SCAM] Urgent: Electricity bill unpaid. Disconnecting tonight!",
        "✅ [SAFE] Hi Abinaya, please send the python project notes."
    ]
)

if st.button("🔔 Simulate Incoming SMS Notification"):
    # Extract clean text
    incoming_text = preset_sms.split("] ")[1]
    
    # NLP Prediction
    X_test = vectorizer.transform([incoming_text])
    prediction = nlp_model.predict(X_test)[0]
    probs = nlp_model.predict_proba(X_test)[0]
    scam_prob = round(max(probs) * 100, 2)

    # UI Alert & Voice Assistant Logic
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info(f"**Incoming Message:** {incoming_text}")
        if prediction == 'Scam':
            st.error("🚨 ALERT: SCAM DETECTED!")
            
            if language == "Tamil (தமிழ்)":
                voice_msg = "எச்சரிக்கை! இது ஒரு போலியான மோசடி செய்தி! யாரும் லிங்கை கிளிக் செய்ய வேண்டாம்!"
            elif language == "Tanglish":
                voice_msg = "Alert! Idhu oru fake scam message! Yaarum link click panna vendam!"
            else:
                voice_msg = "Warning! This is a scam message. Do not click any link!"
                
            speak_text(voice_msg)
        else:
            st.success("✅ SAFE / NON-SCAM MESSAGE")
            
            if language == "Tamil (தமிழ்)":
                voice_msg = "இது ஒரு பாதுகாப்பான செய்தி."
            elif language == "Tanglish":
                voice_msg = "Idhu oru safe-ana normal message."
            else:
                voice_msg = "This is a safe message."
                
            speak_text(voice_msg)

    # 3. Live Analytics Dashboard
    st.markdown("---")
    st.subheader("📊 Live Analytics Dashboard")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("### 🧠 Cognitive Analytics (NLP Confidence)")
        fig_nlp = px.bar(
            x=['Scam Probability', 'Safe Probability'], 
            y=[probs[1]*100 if nlp_model.classes_[1]=='Scam' else probs[0]*100, 
               probs[0]*100 if nlp_model.classes_[0]=='Non-Scam' else probs[1]*100],
            color=['Scam', 'Safe'],
            color_discrete_map={'Scam': 'red', 'Safe': 'green'},
            labels={'x': 'Analysis', 'y': 'Percentage (%)'},
            title="Cognitive Model Confidence Level"
        )
        st.plotly_chart(fig_nlp, use_container_width=True)

    with chart_col2:
        st.markdown("### 👥 Behavioral Analytics (K-Means User Segmentation)")
        fig_kmeans = px.scatter(
            behavior_data, 
            x='Monthly_Transactions', 
            y='Digital_Awareness_Score',
            color='Risk_Cluster',
            title="Rural User Cyber Risk Clustering",
            labels={'Risk_Cluster': 'Cluster Group'}
        )
        st.plotly_chart(fig_kmeans, use_container_width=True)
