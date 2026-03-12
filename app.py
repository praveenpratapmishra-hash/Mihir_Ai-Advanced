import streamlit as st
import google.generativeai as genai
import PIL.Image
import time

# --- 1. CONFIG & API (Aapki Nayi Key) ---
API_KEY = "AIzaSyBRJHW_2CMWzNJC0s6RO4OgacyfYPxnZ3I"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. PREMIUM GEMINI LOOK (CSS) ---
st.set_page_config(page_title="Mihir AI", layout="centered")

st.markdown("""
    <style>
    /* Sab branding hide karo */
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration, div[data-testid="stStatusWidget"] {display: none !important;}
    body, .main { background-color: #000000; color: white; }
    
    /* No Avatar Faces */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; padding: 10px 0px !important; }

    /* Gemini Style Input Bar */
    .stChatInputContainer { 
        position: fixed !important; bottom: 30px !important; 
        background: #1E1F20 !important; border-radius: 30px !important;
        border: 1px solid #333 !important; padding: 5px 15px !important;
    }
    
    /* Plus (+) Button Logic */
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 35px !important; left: 20px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploaderSection"] { border: none !important; padding: 0 !important; }
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 26px; color: #888; background: transparent;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
    }}
    [data-testid="stFileUploader"] section > label { display: none !important; }

    /* 4 Grid Buttons Styling */
    .stButton button {
        background-color: #1E1F20; color: #E3E3E3; border: 1px solid #333;
        border-radius: 15px; padding: 15px; height: 100px; width: 100%; text-align: left; font-size: 14px;
    }
    .stButton button:hover { border-color: #4A90E2; background-color: #2D2E30; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE (Memory & Ads) ---
if "messages" not in st.session_state: st.session_state.messages = []
if "photo_count" not in st.session_state: st.session_state.photo_count = 0
if "show_ui" not in st.session_state: st.session_state.show_ui = True

# --- 4. TOP UI (4 Buttons) ---
if st.session_state.show_ui and not st.session_state.messages:
    st.markdown("<h1 style='color: white;'>Hi Praveen Pratap</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #888; margin-top: -15px;'>Mihir AI se kya puchna hai?</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎨 Create Photo\n(Ghibli, Mandala, AI Art)"): st.session_state.temp = "Create art: "
        if st.button("🚀 Boost My Day\n(Sayari, Chutkule, Story)"): st.session_state.temp = "Mihir dost, kuch mast sunao!"
    with c2:
        if st.button("🧠 Solve Anything\n(Math, Science, All Subjects)"): st.session_state.temp = "Help me solve: "
        if st.button("☸️ Kundali Reading\n(Full Chart & PDF Advice)"): st.session_state.temp = "Kundali and Career analysis."

# Display Chat History
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])
        if "is_kundali" in m:
            if st.button("📥 Watch Ad & Download Full PDF"):
                st.components.v1.html("<script>if(window.AppCreator24){window.AppCreator24.showRewardVideo();}</script>", height=0)
                st.success("Ad ke baad download shuru...")

# --- 5. INPUT HANDLING ---
up_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
prompt = st.chat_input("Ask Gemini...")

if "temp" in st.session_state: 
    prompt = st.session_state.pop("temp")
    st.session_state.show_ui = False

if prompt or up_file:
    st.session_state.show_ui = False
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyze image"})
    
    with st.chat_message("assistant"):
        try:
            # Reward Logic for Photos
            is_photo = any(x in (prompt or "").lower() for x in ["create", "photo", "art", "banao"])
            if is_photo and st.session_state.photo_count >= 5:
                st.warning("🔒 5 photos poori ho gayi! Reward Ad dekhein.")
                st.components.v1.html("<script>if(window.AppCreator24){window.AppCreator24.showRewardVideo();}</script>", height=0)
                st.session_state.photo_count = 0 # Reset after ad
            
            # Generating Content
            if is_photo:
                url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
                st.image(url)
                st.session_state.photo_count += 1
                st.session_state.messages.append({"role": "assistant", "content": "Photo taiyar hai!", "img": url})
            elif "kundali" in (prompt or "").lower():
                res = "Aapki Kundali analysis taiyar hai. Full PDF ke liye niche click karein."
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res, "is_kundali": True})
            else:
                if up_file:
                    res = model.generate_content([f"User: {prompt}", PIL.Image.open(up_file)])
                else:
                    res = model.generate_content(f"You are Mihir AI, a friendly boy. Expert in all subjects. Reply in Hinglish: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except:
            st.error("Dost, ek baar refresh karo!")

st.markdown("<p style='text-align: center; color: #333; margin-top: 50px;'>Powered by Mihir AI</p>", unsafe_allow_html=True)
