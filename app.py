import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. CONFIG & API ---
API_KEY = "AIzaSyBRJHW_2CMWzNJC0s6RO4OgacyfYPxnZ3I"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Mihir AI", layout="centered")

# --- 2. SAKT CSS (Patti aur Drag-Drop Hatane ke liye) ---
st.markdown("""
    <style>
    /* Sabse upar aur niche ki patti gayab */
    #MainMenu, footer, header {visibility: hidden !important; height: 0 !important;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration {display: none !important;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none !important;}
    
    /* Drag and Drop aur Browse files text hide karo */
    [data-testid="stFileUploader"] section { display: none !important; }
    [data-testid="stFileUploader"] label { display: none !important; }
    .st-emotion-cache-6v0v9m, .st-emotion-cache-1ae8k9e, .st-emotion-cache-9ycgxx { display: none !important; }

    /* Black Theme */
    body, .main { background-color: #000000; color: white; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}

    /* Plus (+) Button Positioning */
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 35px !important; left: 20px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploader"]::before { content: "＋"; font-size: 26px; color: #888; display: flex; align-items: center; justify-content: center; cursor: pointer; }

    /* Buttons Style */
    .stButton button { background-color: #1E1F20; color: white; border: 1px solid #333; border-radius: 15px; height: 80px; width: 100%; text-align: left; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAME ENTRY SYSTEM ---
if "user_name" not in st.session_state:
    st.markdown("<h1 style='color: white;'>Welcome!</h1>", unsafe_allow_html=True)
    name = st.text_input("Dost, apna naam likho:", key="name_input")
    if name:
        st.session_state.user_name = name
        st.rerun()
    st.stop() # Jab tak naam nahi likhega, aage nahi badhega

# --- 4. SESSION STATE & UI ---
if "messages" not in st.session_state: st.session_state.messages = []

if not st.session_state.messages:
    # Yahan user ka naam dynamic dikhega
    st.markdown(f"<h1 style='color: white;'>Hi {st.session_state.user_name}</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #888;'>Mihir AI se kya puchna hai?</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create art: "
        if st.button("🚀 Boost My Day"): st.session_state.temp = "Mihir dost, kuch mast sunao!"
    with col2:
        if st.button("🧠 Solve Anything"): st.session_state.temp = "Help me solve: "
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Kundali and Career."

# Display Chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])

# --- 5. INPUT ---
up_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
prompt = st.chat_input("Ask Mihir AI...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or up_file:
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyze image"})
    with st.chat_message("assistant"):
        try:
            # Action logic
            if any(x in (prompt or "").lower() for x in ["create", "photo", "art"]):
                url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "content": "Photo taiyar hai!", "img": url})
            else:
                if up_file: res = model.generate_content([f"User: {prompt}", PIL.Image.open(up_file)])
                else: res = model.generate_content(f"Be Mihir AI, a friend. Help {st.session_state.user_name}: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except: st.error("Ek baar refresh karein!")

st.markdown("<p style='text-align: center; color: #333;'>Powered by Mihir AI</p>", unsafe_allow_html=True)
