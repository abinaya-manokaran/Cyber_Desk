import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cyber-Help Desk", page_icon="🛡️", layout="wide")

# App Header
st.title("🛡️ Rural Community Cyber-Help Desk: Real-Time AI Scam Detector")

# Language Selector
language = st.selectbox("Choose Language / மொழியைத் தேர்ந்தெடுக்கவும்:", ["Tanglish", "Tamil (தமிழ்)", "English"])

if language == "Tamil (தமிழ்)":
    sub_title = "கிராமப்புற மக்களுக்கான நேரலை சைபர் மோசடி கண்டறிதல் மற்றும் உளவியல் பகுப்பாய்வு மையம்."
    notif_header = "🔔 புதிய குறுஞ்செய்தி அறிவிப்பு (Incoming SMS Notification Banner)"
    sample_header = "📩 மாதிரிச் செய்திகளைச் சோதிக்க கிளிக் செய்யவும் (Quick Sample SMS):"
    custom_header = "✍️ அல்லது புதிய குறுஞ்செய்தியை உள்ளிடவும் (Custom SMS Input):"
    btn_text = "பகுப்பாய்வு செய் (Analyze)"
elif language == "English":
    sub_title = "Real-time automated scam detection & behavioral analytics for rural communities."
    notif_header = "🔔 Incoming SMS Notification Banner"
    sample_header = "📩 Click to test Quick Sample SMS:"
    custom_header = "✍️ Or Enter / Paste Any Custom SMS:"
    btn_text = "Analyze Message"
else: # Tanglish
    sub_title = "Gramathu makkalukana real-time scam detection & behavioral analytics help desk."
    notif_header = "🔔 New Incoming SMS Notification Banner"
    sample_header = "📩 Sample SMS-ah click panni test pannunga:"
    custom_header = "✍️ Alladhu pudhu SMS-ah inge type pannunga:"
    btn_text = "Message-ah Analyze Pannunga"

st.caption(sub_title)

# --- 1. NLP MODEL TRAINING (COGNITIVE ANALYTICS) ---
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

# Session state to track user history for live analytics
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. SAMPLE MESSAGES FOR EASY TESTING ---
samples = [
    "Urgent: Your electricity bill unpaid. Disconnection tonight! Link: http://bit.ly/pay",
    "Congratulations! You won 1 ShareAuto Lucky Draw. Call 9876543210",
    "Hi Abinaya, can you send the class notes for today's lecture?",
    "Your SBI account blocked due to pending KYC. Click link to verify."
]

st.subheader(sample_header)
cols = st.columns(len(samples))
selected_sample = ""

for i, sample in enumerate(samples):
    if cols[i].button(f"SMS {i+1}", key=f"btn_{i}"):
        selected_sample = sample

st.markdown("---")

# --- 3. INPUT AREA (TYPED OR CLICKED) ---
st.subheader(custom_header)
user_msg = st.text_input("Incoming SMS Text:", value=selected_sample)

if st.button(btn_text) or user_msg:
    if user_msg.strip() != "":
        X_test = vectorizer.transform([user_msg])
        pred = nlp_model.predict(X_test)[0]
        
        # Save to history for real-time dynamic analytics
        st.session_state.history.append({'message': user_msg, 'prediction': pred})
        
        # --- NOTIFICATION POP-UP BANNER SIMULATION ---
        st.markdown("### " + notif_header)
        if pred == 'Scam':
            st.error(f"🚨 **POP-UP ALERT: SCAM SMS DETECTED!**\n\n**Received Text:** \"{user_msg}\"\n\n🛑 *Warning: Do NOT click any links or make payments!*")
        else:
            st.success(f"✅ **POP-UP NOTIFICATION: SAFE MESSAGE**\n\n**Received Text:** \"{user_msg}\"\n\n🟢 *This message appears legitimate.*")

# --- 4. REAL-TIME DYNAMIC ANALYTICS DASHBOARD ---
st.markdown("---")
st.header("📊 Real-Time Analytics Dashboard")

col_left, col_right = st.columns(2)

# Module A: Cognitive Analytics (NLP Analysis)
with col_left:
    st.subheader("🧠 Cognitive Analytics (NLP Scam Ratio)")
    if len(st.session_state.history) > 0:
        df_hist = pd.DataFrame(st.session_state.history)
        scam_counts = df_hist['prediction'].value_counts()
        
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.pie(scam_counts, labels=scam_counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
        ax1.set_title("Live Analyzed Messages Distribution")
        st.pyplot(fig1)
        st.write(f"Total Messages Analyzed Live: **{len(df_hist)}**")
    else:
        st.info("No messages analyzed yet in this session. Test a message above to see live NLP analytics!")

# Module B: Behavioral Analytics (K-Means Clustering)
with col_right:
    st.subheader("👥 Behavioral Analytics (K-Means User Risk)")
    
    # Simulating village user risk segmentation
    np.random.seed(42)
    behavior_data = pd.DataFrame({
        '
