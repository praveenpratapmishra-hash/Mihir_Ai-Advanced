import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. CONFIG ---
st.set_page_config(page_title="Mihir AI", layout="centered")

# --- 2. SAKT PROFESSIONAL CSS (No Patti, No Streamlit Branding) ---
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu, #stDecoration {display: none !important; visibility: hidden !important;}
    [data-testid="stStatusWidget"], [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none !important;}
    div[class^="st-emotion-cache-1wb59as"], .st-emotion-cache-80989f, .st-emotion-cache-1vt458s {display: none !important;}
    [data-testid="stFileUploader"] section, [data-testid="stFileUploader"] label { display: none !important; }
    body, .main { background-color: #000000 !important; color: white !important; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    .stChatInputContainer { border-radius: 30px !important; background: #1E1F20 !important; border: 1px solid #333 !important; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 35px !important; left: 20px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploader"]::before { content: "＋"; font-size: 26px; color: #888; display: flex; align-items: center; justify-content: center; }
    .stButton button { background-color: #1E1F20; color: white; border: 1px solid #333; border-radius: 15px; height: 60px; width: 100%; text-align: left; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API INITIALIZATION ---
API_KEY = "AIzaSyBRJHW_2CMWzNJC0s6RO4OgacyfYPxnZ3I"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 4. USER SESSION ---
if "user_name" not in st.session_state:
    st.markdown("<h1 style='color: white;'>Mihir AI</h1>", unsafe_allow_html=True)
    name = st.text_input("Apna naam likhein:", key="name_input")
    if name:
        st.session_state.user_name = name
        st.rerun()
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []

# --- 5. UI DISPLAY ---
if not st.session_state.messages:
    st.markdown(f"<h1>Hi {st.session_state.user_name}</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#888;'>Main Mihir AI hoon. Kya madad karun?</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create art: "
    with c2:
        if st.button("🧠 Solve Anything"): st.session_state.temp = "Solve this problem: "

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])

# --- 6. INPUT ---
up_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
prompt = st.chat_input("Ask Mihir AI...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or up_file:
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyze image"})
    with st.chat_message("assistant"):
        try:
            if any(x in (prompt or "").lower() for x in ["create", "photo", "art"]):
                url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "content": "Taiyar hai!", "img": url})
            else:
                content = [prompt] if prompt else ["Analyze this image"]
                if up_file: content.append(PIL.Image.open(up_file))
                response = model.generate_content(content)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.markdown("Dost, server busy hai. Ek baar fir se likhein!")

st.markdown("<p style='text-align: center; color: #111;'>Powered by Mihir AI</p>", unsafe_allow_html=True)

