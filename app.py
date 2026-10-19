import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
import time

# Streamlit Page Config
st.set_page_config(page_title="Cyber-Help Desk", page_icon="🛡️", layout="wide")

st.title("🛡️ Community Cyber-Help Desk (Real-Time AI Alert)")

# 1. Language Selection & Voice Settings
st.sidebar.header("⚙️ Settings / அமைப்புகள்")
language = st.sidebar.selectbox(
    "Choose Language / மொழி:", 
    ["Tamil (தமிழ்)", "Tanglish", "English"]
)

enable_voice = st.sidebar.checkbox("🔊 Enable AI Voice Alert", value=True)

# Language Dictionary
text_dict = {
    "Tamil (தமிழ்)": {
        "title": "கிராமப்புற மக்களுக்கான நேரடி சைபர் பாதுகாப்பு மையம்",
        "incoming": "📲 போனில் புதிதாக வந்த குறுஞ்செய்தி (Incoming SMS Alert):",
        "scam": "🚨 எச்சரிக்கை: இது மோசடி செய்தி! (SCAM DETECTED)",
        "safe": "✅ இது பாதுகாப்பான செய்தி (SAFE MESSAGE)",
        "risk_high": "🔴 உயர் அபாய நிலை (High Risk User): உடனடி விழிப்புணர்வு தேவை!",
        "risk_safe": "🟢 பாதுகாப்பான நிலை (Low Risk User)",
        "voice_lang": "ta-IN"
    },
    "Tanglish": {
        "title": "Rural Community Cyber-Help Desk",
        "incoming": "📲 Phone-ku vantha pudhiya message (Incoming SMS Alert):",
        "scam": "🚨 ALERT: Idhu Fraud / Scam Message!",
        "safe": "✅ Idhu Safe-ana Normal Message.",
        "risk_high": "🔴 High Cyber Risk! Carefulla irunga.",
        "risk_safe": "🟢 Low Risk User - Safe Level.",
        "voice_lang": "en-IN"
    },
    "English": {
        "title": "Rural Cyber Awareness & Real-Time Help Desk",
        "incoming": "📲 Live Incoming SMS Notification:",
        "scam": "🚨 ALERT: SCAM DETECTED!",
        "safe": "✅ SAFE / Legitimate Message.",
        "risk_high": "🔴 High Risk Category User Detected!",
        "risk_safe": "🟢 Low Risk Category User.",
        "voice_lang": "en-US"
    }
}

txt = text_dict[language]
st.write(f"### {txt['title']}")

# 2. NLP Model Training (Cognitive Analytics)
training_messages = [
    "Your bank account is blocked. Click link to update KYC.",
    "Congratulations! You won a lottery of 10 lakhs. Call now.",
    "Urgent: Electricity bill unpaid. Disconnection tonight.",
    "Your credit card reward points expiring today. Redeem fast.",
    "Hi Abinaya, project notes sent to your email.",
    "Your OTP for bank transaction is 4892. Do not share.",
    "Mom, please buy groceries on your way home.",
    "Meeting rescheduled to 4 PM tomorrow."
]
labels = ['Scam', 'Scam', 'Scam', 'Scam', 'Non-Scam', 'Non-Scam', 'Non-Scam', 'Non-Scam']

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_messages)
nlp_model = MultinomialNB()
nlp_model.fit(X_train, labels)

# Session State for Live Analytics Tracking
if 'scam_count' not in st.session_state:
    st.session_state.scam_count = 0
if 'safe_count' not in st.session_state:
    st.session_state.safe_count = 0
if 'last_msg' not in st.session_state:
    st.session_state.last_msg = ""

# Function for Browser Speech Synthesis (Voice Assistant)
def speak_text(text, lang_code):
    js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{text}');
            msg.lang = '{lang_code}';
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(js_code, height=0)

# 3. Interactive Notification Simulation (No Typing Needed for Rural Users!)
st.subheader("📩 Quick Test Notifications (கிளிக் செய்து சோதிக்கவும்):")

col1, col2, col3, col4 = st.columns(4)

selected_msg = None
if col1.button("🚨 Bank Block Scam"):
    selected_msg = "Your SBI bank account is blocked. Click here to verify KYC immediately!"
if col2.button("🚨 Electricity Disconnect"):
    selected_msg = "Urgent: Power supply will be disconnected tonight. Pay bill via link."
if col3.button("✅ Normal OTP Msg"):
    selected_msg = "Your OTP for transaction is 9821. Do not share with anyone."
if col4.button("✅ Friend Message"):
    selected_msg = "Hi, let us meet tomorrow morning for coffee."

# Manual custom input option if needed
custom_msg = st.text_input("Or enter any other message to test:")
if custom_msg:
    selected_msg = custom_msg

# 4. Live Analysis Engine
if selected_msg:
    st.session_state.last_msg = selected_msg
    X_test = vectorizer.transform([selected_msg])
    pred = nlp_model.predict(X_test)[0]

    # Display Notification Popup Box
    st.info(f"{txt['incoming']}\n\n**\"{selected_msg}\"**")

    # Cognitive Analytics Output
    st.subheader("🧠 Cognitive Analytics (NLP Scam Analysis)")
    if pred == 'Scam':
        st.error(txt['scam'])
        st.session_state.scam_count += 1
        if enable_voice:
            speak_text("Warning! This is a scam message. Do not click any links.", txt['voice_lang'])
    else:
        st.success(txt['safe'])
        st.session_state.safe_count += 1
        if enable_voice:
            speak_text("This message is safe.", txt['voice_lang'])

# 5. Live Behavioral Analytics (K-Means Clustering)
st.markdown("---")
st.subheader("📊 Behavioral Analytics (Live K-Means User Risk Segmentation)")

total_received = st.session_state.scam_count + st.session_state.safe_count

if total_received > 0:
    # Behavioral Metrics
    scam_ratio = (st.session_state.scam_count / total_received) * 100
    
    # K-Means Clustering Logic
    # Features: [Total Messages Received, Percentage of Scam Exposure]
    user_data = pd.DataFrame({
        'Total_Messages': [total_received, 10, 2],
        'Scam_Exposure_%': [scam_ratio, 90.0, 10.0]
    })
    
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(user_data)
    current_user_cluster = clusters[0]

    # Metrics Display
    m1, m2, m3 = st.columns(3)
    m1.metric("Total SMS Analyzed", total_received)
    m2.metric("Scam Alerts Triggered", st.session_state.scam_count)
    m3.metric("Scam Exposure Rate", f"{scam_ratio:.1f}%")

    if current_user_cluster == 1 or scam_ratio > 40:
        st.warning(f"User Risk Status: {txt['risk_high']}")
    else:
        st.info(f"User Risk Status: {txt['risk_safe']}")
else:
    st.write("வார்த்தைகளையோ அல்லது பட்டனையோ கிளிக் செய்து லைவ் அனலிட்டிக்ஸைத் தொடங்குங்கள்.")
