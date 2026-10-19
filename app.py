import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Rural Cyber-Help Desk", page_icon="🛡️", layout="wide")

st.title("🛡️ Community Cyber-Help Desk: Real-Time Scam & Behavioral Analytics")

# ---------------------------------------------------------
# LANGUAGE SELECTOR
# ---------------------------------------------------------
language = st.sidebar.selectbox(
    "Choose Language / மொழியைத் தேர்ந்தெடுக்கவும்:", 
    ["Tamil (தமிழ்)", "Tanglish", "English"]
)

if language == "Tamil (தமிழ்)":
    sub_title = "கிராமப்புற மக்களுக்கான நேரலை சைபர் மோசடி மற்றும் பயனர் ஆபத்து பகுப்பாய்வு மையம்."
    notif_title = "📲 புதிய SMS அறிவிப்பு (Real-Time Incoming SMS Notification):"
    nlp_header = "🧠 காக்னிடிவ் பகுப்பாய்வு (Cognitive NLP Scam Detector)"
    kmeans_header = "📊 பிஹேவியரல் பகுப்பாய்வு (Behavioral K-Means Clustering)"
    scam_alert = "🚨 எச்சரிக்கை: இது ஒரு போலி மோசடி குறுஞ்செய்தி (Scam)! எந்த இணைப்பையும் கிளிக் செய்ய வேண்டாம்."
    safe_alert = "✅ பாதுகாப்பு: இது ஒரு சாதாரண பாதுகாப்பான குறுஞ்செய்தி (Safe)."
    btn_text = "குறுஞ்செய்தியைப் பகுப்பாய்வு செய் (Analyze SMS)"
elif language == "English":
    sub_title = "Real-time AI-driven cyber scam detection and user risk analytics for rural communities."
    notif_title = "📲 Incoming SMS Notification Banner:"
    nlp_header = "🧠 Cognitive Analytics (NLP Scam Detection)"
    kmeans_header = "📊 Behavioral Analytics (K-Means Risk Clustering)"
    scam_alert = "🚨 ALERT: SCAM DETECTED! Do not click any links or share OTPs."
    safe_alert = "✅ SAFE: This is a legitimate message."
    btn_text = "Analyze SMS"
else: # Tanglish
    sub_title = "Gramathu makkalukana real-time scam detection matrum user risk analytics desk."
    notif_title = "📲 Puthu SMS Notification (Incoming Alert):"
    nlp_header = "🧠 Cognitive Analytics (NLP Scam Detection)"
    kmeans_header = "📊 Behavioral Analytics (K-Means Clustering)"
    scam_alert = "🚨 ALERT: SCAM DETECTED! Idhu fake message, link-ah click pannatheenga!"
    safe_alert = "✅ SAFE: Idhu normal safe message thaan."
    btn_text = "Message-ah Analyze Pannunga"

st.caption(sub_title)

# ---------------------------------------------------------
# 1. COGNITIVE MODULE (NLP NAIVE BAYES MODEL TRAINING)
# ---------------------------------------------------------
train_msgs = [
    "Your bank account is blocked. Click the link to update KYC immediately.",
    "Congratulations! You won a lottery of 10 lakhs. Call this number to claim.",
    "Hi, are we meeting for project discussion tomorrow at 10 AM?",
    "Urgent: Your electricity bill will be disconnected tonight. Pay via this link.",
    "Your OTP for banking transaction is 4892. Do not share with anyone.",
    "Mom, please pick up some groceries on your way back home.",
    "Your credit card reward points are expiring today. Redeem now.",
    "Hey, let's catch up for coffee this weekend."
]
train_labels = ['Scam', 'Scam', 'Non-Scam', 'Scam', 'Non-Scam', 'Non-Scam', 'Scam', 'Non-Scam']

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_msgs)
nlp_model = MultinomialNB()
nlp_model.fit(X_train, train_labels)

# Initialize Session State for Analytics History
if 'analyzed_count' not in st.session_state:
    st.session_state['analyzed_count'] = 0
if 'scam_count' not in st.session_state:
    st.session_state['scam_count'] = 0

# ---------------------------------------------------------
# MOCK NOTIFICATION / SAMPLE MESSAGES SECTION
# ---------------------------------------------------------
st.markdown("---")
st.subheader(notif_title)

# Sample buttons simulating live incoming SMS notifications
col_s1, col_s2, col_s3 = st.columns(3)
selected_sample = ""

if col_s1.button("📩 Sample 1: Bank Blocked Alert"):
    selected_sample = "Urgent: Your SBI account is blocked today. Click http://bit.ly/fake-bank to unblock immediately."
if col_s2.button("📩 Sample 2: Lottery Winner"):
    selected_sample = "Congratulations! You won Rs 500,000 cash prize. Call 9876543210 to claim reward."
if col_s3.button("📩 Sample 3: Friend Message"):
    selected_sample = "Hi Abinaya, please send the computer science assignment notes before evening."

# Main Input / Speech Box
user_msg = st.text_area("SMS Input / Voice Input Text:", value=selected_sample, height=80)

# Voice Assistant Speech Output Simulation (Web Speech Synthesizer Script)
def speak_message(text):
    js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{text}");
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(js_code, height=0)

# ---------------------------------------------------------
# 2. REAL-TIME ANALYSIS EXECUTION
# ---------------------------------------------------------
if st.button(btn_text, type="primary"):
    if user_msg.strip() != "":
        st.session_state['analyzed_count'] += 1
        X_test = vectorizer.transform([user_msg])
        pred = nlp_model.predict(X_test)[0]

        st.subheader(nlp_header)
        if pred == 'Scam':
            st.error(scam_alert)
            st.session_state['scam_count'] += 1
            speak_message("Warning! Scam Detected. Do not click links.")
        else:
            st.success(safe_alert)
            speak_message("Safe Message. No fraud detected.")
    else:
        st.warning("Please select or enter an SMS message.")

# ---------------------------------------------------------
# 3. BEHAVIORAL MODULE (LIVE DYNAMIC K-MEANS CLUSTERING)
# ---------------------------------------------------------
st.markdown("---")
st.subheader(kmeans_header)

# Dynamic Behavioral Data based on desk activity
user_data = {
    'User_Group': ['Village A', 'Village B', 'Village C', 'Village D', 'Village E', 'Current Desk Analytics'],
    'Transactions_Freq': [3, 25, 2, 22, 1, st.session_state['analyzed_count'] * 3],
    'Digital_Awareness_Score': [20, 85, 15, 90, 25, max(10, 100 - (st.session_state['scam_count'] * 20))]
}

df_behavior = pd.DataFrame(user_data)

# K-Means Clustering
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
df_behavior['Cluster'] = kmeans.fit_predict(df_behavior[['Transactions_Freq', 'Digital_Awareness_Score']])

# Layout: Table & Graph side by side
col_tab, col_graph = st.columns([1, 1])

with col_tab:
    st.write("📋 **Live Community Risk Profile:**")
    st.dataframe(df_behavior[['User_Group', 'Transactions_Freq', 'Digital_Awareness_Score']])

with col_graph:
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ['red' if c == 0 else 'green' for c in df_behavior['Cluster']]
    ax.scatter(df_behavior['Transactions_Freq'], df_behavior['Digital_Awareness_Score'], c=colors, s=120)
    
    ax.set_title("Behavioral Clustering (Red = High Risk, Green = Digitally Aware)")
    ax.set_xlabel("Transaction / Activity Frequency")
    ax.set_ylabel("Digital Awareness Score")
    ax.grid(True)
    st.pyplot(fig)
