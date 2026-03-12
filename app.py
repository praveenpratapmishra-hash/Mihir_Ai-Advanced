import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. API CONNECTION (Safe Mode) ---
API_KEY = "AIzaSyBRJHW_2CMWzNJC0s6RO4OgacyfYPxnZ3I"
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("Connection Error! Please check your internet.")

# --- 2. 100% CLEAN UI CSS (No Patti, No Streamlit Branding) ---
st.set_page_config(page_title="Mihir AI", layout="centered")

st.markdown("""
    <style>
    /* Sabhi patti aur menus ko jad se khatam karo */
    header, footer, .stDeployButton, #MainMenu, #stDecoration {display: none !important; visibility: hidden !important;}
    [data-testid="stStatusWidget"], [data-testid="stToolbar"] {display: none !important;}
    
    /* Manage App patti ko force hide karo */
    div[class^="st-emotion-cache-1wb59as"], .st-emotion-cache-80989f, .st-emotion-cache-1vt458s {display: none !important;}
    
    /* Drag & Drop aur Browse files text poora saaf */
    [data-testid="stFileUploader"] section { display: none !important; }
    [data-testid="stFileUploader"] label { display: none !important; }
    .st-emotion-cache-6v0v9m, .st-emotion-cache-1ae8k9e { display: none !important; }

    /* Pure Black Professional Theme */
    body, .main { background-color: #000000 !important; color: white !important; }
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}

    /* Gemini Plus (+) Button & Input Box */
    .stChatInputContainer { border-radius: 30px !important; background: #1E1F20 !important; border: 1px solid #333 !important; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 35px !important; left: 20px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploader"]::before { content: "＋"; font-size: 26px; color: #888; display: flex; align-items: center; justify-content: center; cursor: pointer; }
    
    /* Grid Buttons */
    .stButton button { background-color: #1E1F20; color: white; border: 1px solid #333; border-radius: 15px; height: 80px; width: 100%; text-align: left; padding-left: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DYNAMIC USER SYSTEM ---
if "user_name" not in st.session_state:
    st.markdown("<h1 style='color: white;'>Mihir AI</h1>", unsafe_allow_html=True)
    name = st.text_input("Dost, apna naam bataiye:", key="name_input")
    if name:
        st.session_state.user_name = name
        st.rerun()
    st.stop()

# --- 4. CHAT SYSTEM ---
if "messages" not in st.session_state: st.session_state.messages = []

# Home Screen (Buttons)
if not st.session_state.messages:
    st.markdown(f"<h1 style='color: white;'>Hi {st.session_state.user_name}</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #888;'>Main aapki kaise madad kar sakta hoon?</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create art: "
        if st.button("🚀 Boost My Day"): st.session_state.temp = "Mihir dost, kuch mast sunao!"
    with c2:
        if st.button("🧠 Solve Anything"): st.session_state.temp = "Help me solve: "
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Kundali and Career analysis."

# Messages Display
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])

# --- 5. INPUT HANDLING ---
up_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
prompt = st.chat_input("Ask Mihir AI...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or up_file:
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyzing image..."})
    with st.chat_message("assistant"):
        try:
            # Action logic
            if any(x in (prompt or "").lower() for x in ["create", "photo", "art"]):
                url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "content": "Photo taiyar hai!", "img": url})
            else:
                if up_file: 
                    img = PIL.Image.open(up_file)
                    res = model.generate_content([f"User: {prompt}", img])
                else: 
                    res = model.generate_content(f"You are Mihir AI, a friendly boy. Reply in Hinglish. Help {st.session_state.user_name}: {prompt}")
                
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.markdown("Dost, ek choti si dikkat aayi hai, par main abhi theek hoon! Kya main fir se koshish karun?")

st.markdown("<p style='text-align: center; color: #111; font-size: 10px;'>Powered by Mihir AI</p>", unsafe_allow_html=True)
