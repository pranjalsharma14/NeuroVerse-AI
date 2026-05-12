import streamlit as st
from openai import OpenAI
import datetime
 
# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroVerse AI Content Studio",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ─────────────────────────────────────────────
# GLOBAL CSS  — forces light theme on every element
# so dark-mode OS/browser setting never bleeds through
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
 
/* == FORCE LIGHT BASE ON EVERYTHING == */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="block-container"],
.main, .block-container,
[class*="css"] {
    background-color: #FFF7FB !important;
    color: #1F2937 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
 
/* == HIDE STREAMLIT CHROME == */
#MainMenu, footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
 
/* == SIDEBAR == */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] section {
    background: linear-gradient(160deg, #fff0f8 0%, #f5f0ff 100%) !important;
    border-right: 1px solid #f0e6f8 !important;
}
[data-testid="stSidebar"] * { color: #1F2937 !important; }
 
/* == ALL BUTTONS == */
.stButton > button {
    background: linear-gradient(135deg, #FF6FAE, #A78BFA) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.55rem 1.4rem !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    box-shadow: 0 4px 16px rgba(255,111,174,0.28) !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(255,111,174,0.38) !important;
}
.stButton > button p { color: #ffffff !important; }
 
/* == DOWNLOAD BUTTON == */
.stDownloadButton > button {
    background: #ffffff !important;
    color: #A78BFA !important;
    border: 1.5px solid #A78BFA !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
}
.stDownloadButton > button p { color: #A78BFA !important; }
 
/* == TEXT INPUTS == */
.stTextArea textarea,
.stTextInput input {
    background-color: #fdfaff !important;
    color: #1F2937 !important;
    border: 1.5px solid #e9d8f9 !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: #A78BFA !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.14) !important;
}
 
/* == SELECTBOX == */
.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"] > div {
    background-color: #fdfaff !important;
    border: 1.5px solid #e9d8f9 !important;
    border-radius: 12px !important;
    color: #1F2937 !important;
}
[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: #ffffff !important;
    color: #1F2937 !important;
}
[data-baseweb="option"] {
    background-color: #ffffff !important;
    color: #1F2937 !important;
}
[data-baseweb="option"]:hover { background-color: #f5f0ff !important; }
 
/* == SLIDER == */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, #FF6FAE, #A78BFA) !important;
}
 
/* == LABELS == */
label {
    color: #374151 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}
 
/* == EXPANDER == */
[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border: 1.5px solid #f0e6fb !important;
    border-radius: 14px !important;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    background-color: #ffffff !important;
}
[data-testid="stExpander"] > div > div {
    background-color: #ffffff !important;
}
[data-testid="stExpander"] svg { color: #A78BFA !important; }
 
/* == MARKDOWN == */
.stMarkdown p, .stMarkdown li,
.stMarkdown h1, .stMarkdown h2,
.stMarkdown h3, .stMarkdown h4 {
    color: #1F2937 !important;
}
 
/* == CODE BLOCK (copy area) == */
[data-testid="stCode"] pre,
.stCode pre {
    background-color: #f8f4ff !important;
    color: #374151 !important;
    border: 1.5px solid #e9d8f9 !important;
    border-radius: 12px !important;
}
[data-testid="stCode"] code { color: #374151 !important; }
[data-testid="stCode"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
 
/* == ALERTS == */
.stAlert { border-radius: 12px !important; }
 
/* == DIVIDER == */
hr { border-color: #f0e6f8 !important; margin: 0.8rem 0 !important; }
 
/* == SPINNER == */
.stSpinner > div { border-top-color: #FF6FAE !important; }
 
/* == SCROLLBAR == */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #e0c9f5; border-radius: 999px; }
 
/* == CONTAINERS == */
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="column"] {
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
TOOLS = [
    {"id": "blog",       "label": "Blog Writer",           "icon": "✍️"},
    {"id": "instagram",  "label": "Instagram Caption",     "icon": "📸"},
    {"id": "linkedin",   "label": "LinkedIn Post",         "icon": "💼"},
    {"id": "youtube",    "label": "YouTube Script",        "icon": "🎬"},
    {"id": "adcopy",     "label": "Ad Copy",               "icon": "📣"},
    {"id": "email",      "label": "Email Writer",          "icon": "📧"},
    {"id": "pitch",      "label": "Startup Pitch",         "icon": "🚀"},
    {"id": "product",    "label": "Product Description",   "icon": "🛍️"},
    {"id": "tweet",      "label": "Tweet Generator",       "icon": "🐦"},
    {"id": "seo",        "label": "SEO Content",           "icon": "🔍"},
    {"id": "hashtag",    "label": "Hashtag Generator",     "icon": "#️⃣"},
    {"id": "rewrite",    "label": "AI Rewrite Tool",       "icon": "🔄"},
    {"id": "tone",       "label": "Tone Changer",          "icon": "🎨"},
    {"id": "summarize",  "label": "AI Summarizer",         "icon": "📝"},
    {"id": "hook",       "label": "Hook Generator",        "icon": "🎣"},
    {"id": "title",      "label": "Viral Title Generator", "icon": "🔥"},
]
 
TONES = [
    "Professional", "Casual", "Friendly", "Witty",
    "Bold", "Inspirational", "Empathetic", "Persuasive", "Humorous", "Minimalist",
]
LANGUAGES = ["English", "Hindi", "Hinglish"]
MODELS = [
    "google/gemini-2.0-flash-001",
    "openai/gpt-4o-mini",
    "openai/gpt-3.5-turbo",
    "anthropic/claude-3-haiku",
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
]
 
TOOL_PROMPTS = {
    "blog":      "Write a detailed, SEO-optimized blog post about: {prompt}. Use proper headings, subheadings, and a compelling introduction.",
    "instagram": "Write engaging Instagram captions for: {prompt}. Include emojis and a CTA. Provide 3 variations.",
    "linkedin":  "Write a professional, engaging LinkedIn post about: {prompt}. Make it thought-provoking with a personal angle.",
    "youtube":   "Write a complete YouTube video script for: {prompt}. Include hook, intro, main content sections, and outro with CTA.",
    "adcopy":    "Write high-converting ad copy for: {prompt}. Include headline, body, and CTA. Provide 3 variations (Facebook, Google, Instagram).",
    "email":     "Write a professional email about: {prompt}. Include subject line, greeting, body, and signature.",
    "pitch":     "Write a compelling startup pitch for: {prompt}. Include problem, solution, market size, business model, and ask.",
    "product":   "Write a compelling product description for: {prompt}. Highlight features, benefits, and include a CTA.",
    "tweet":     "Write 5 engaging tweets about: {prompt}. Each under 280 characters. Make them viral-worthy.",
    "seo":       "Write SEO-optimized content about: {prompt}. Include target keywords naturally, meta description, and proper structure.",
    "hashtag":   "Generate 30 relevant hashtags for content about: {prompt}. Organize by popularity (high, medium, niche).",
    "rewrite":   "Rewrite and significantly improve this content: {prompt}. Make it more engaging, clear, and impactful.",
    "tone":      "Rewrite this content in a {tone} tone: {prompt}. Maintain the core message but transform the voice completely.",
    "summarize": "Summarize this content concisely: {prompt}. Include key points and main takeaways.",
    "hook":      "Write 10 powerful scroll-stopping hooks for content about: {prompt}. Create curiosity with each one.",
    "title":     "Generate 15 viral click-worthy titles for: {prompt}. Include numbers, power words, and emotional triggers.",
}
 
MODEL_INFO = {
    "google/gemini-2.0-flash-001":           ("⚡ Very fast, great quality", "Free"),
    "openai/gpt-4o-mini":                    ("💡 Smart & affordable",       "Paid"),
    "openai/gpt-3.5-turbo":                  ("📦 Classic reliable model",   "Paid"),
    "anthropic/claude-3-haiku":              ("🌸 Great writing quality",    "Paid"),
    "meta-llama/llama-3.1-8b-instruct:free": ("🦙 Free open-source option", "Free"),
    "mistralai/mistral-7b-instruct:free":    ("🌪️ Free fast EU model",      "Free"),
}
 
# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "workspace",
        "selected_tool": "blog",
        "history": [],
        "output": "",
        "api_status": None,
        "selected_model": MODELS[0],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
 
init_state()
 
# ─────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────
def get_client():
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        return OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    except Exception:
        return None
 
def check_api_status():
    client = get_client()
    if not client:
        return False
    try:
        client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5,
        )
        return True
    except Exception:
        return False
 
def generate_content(tool_id, prompt, tone, language, creativity):
    client = get_client()
    if not client:
        return None, "❌ API key not found. Add your OpenRouter key to `.streamlit/secrets.toml`."
 
    template = TOOL_PROMPTS.get(tool_id, "{prompt}")
    full_prompt = template.format(prompt=prompt, tone=tone)
 
    lang_note = {
        "Hindi":    "Respond entirely in Hindi (Devanagari script).",
        "Hinglish": "Respond in Hinglish (mix of Hindi and English in Roman script).",
    }.get(language, "")
 
    system_msg = (
        f"You are NeuroVerse AI, a world-class content creator and copywriter.\n"
        f"Tone: {tone}\n{lang_note}\n"
        "Format your response using Markdown. Be creative and deliver high-quality output."
    )
 
    try:
        response = client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": full_prompt},
            ],
            max_tokens=2000,
            temperature=creativity,
        )
        return response.choices[0].message.content, None
    except Exception as e:
        err = str(e)
        if "401" in err or "auth" in err.lower():
            return None, "❌ Invalid API key. Please check your OpenRouter key."
        elif "429" in err:
            return None, "⏳ Rate limit reached. Please wait a moment and try again."
        elif "model" in err.lower():
            return None, f"⚠️ Model not available: {st.session_state.selected_model}. Try another."
        else:
            return None, f"❌ Error: {err}"
 
# ─────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────
def page_hero(title: str, subtitle: str):
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#fff0f7 0%,#f3f0ff 55%,#eff6ff 100%);
        border-radius:20px;padding:1.5rem 1.8rem;
        margin-bottom:1.3rem;border:1px solid #f0e6fb;
    ">
        <div style="
            font-family:'Nunito',sans-serif;font-size:1.5rem;font-weight:800;
            background:linear-gradient(135deg,#FF6FAE,#A78BFA);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;margin-bottom:0.2rem;line-height:1.25;
        ">{title}</div>
        <div style="font-size:0.82rem;color:#9CA3AF;font-weight:500;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
 
 
def section_header(text: str):
    st.markdown(f"""
    <div style="
        font-family:'Nunito',sans-serif;font-size:0.95rem;font-weight:700;
        color:#374151;margin:0.4rem 0 0.7rem 0;
        padding-bottom:0.35rem;border-bottom:2px solid #f0e6fb;
    ">{text}</div>
    """, unsafe_allow_html=True)
 
 
def sidebar_label(text: str):
    st.markdown(
        f'<div style="font-size:0.62rem;font-weight:700;letter-spacing:0.1em;'
        f'text-transform:uppercase;color:#C4B5D5;margin-bottom:0.35rem;">{text}</div>',
        unsafe_allow_html=True,
    )
 
# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="
            font-family:'Nunito',sans-serif;font-size:1.3rem;font-weight:800;
            background:linear-gradient(135deg,#FF6FAE,#A78BFA);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;line-height:1.2;margin-bottom:0.15rem;
        ">🌸 NeuroVerse AI</div>
        <div style="font-size:0.7rem;color:#9CA3AF;font-weight:500;
                    letter-spacing:0.03em;margin-bottom:1.3rem;">
            Content Studio · All-in-One AI Writer
        </div>
        """, unsafe_allow_html=True)
 
        # Navigation
        sidebar_label("Navigation")
        for page_id, icon, label in [
            ("workspace", "🖊️", "Workspace"),
            ("history",   "📚", "History"),
            ("settings",  "⚙️", "Settings"),
        ]:
            is_active = st.session_state.page == page_id
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{page_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.page = page_id
                st.rerun()
 
        st.markdown("<hr>", unsafe_allow_html=True)
 
        # Model selector
        sidebar_label("AI Model")
        idx = MODELS.index(st.session_state.selected_model) if st.session_state.selected_model in MODELS else 0
        model = st.selectbox("Model", MODELS, index=idx, label_visibility="collapsed")
        if model != st.session_state.selected_model:
            st.session_state.selected_model = model
            st.session_state.api_status = None
 
        st.markdown("<hr>", unsafe_allow_html=True)
 
        # API status
sidebar_label("API Status")

if st.session_state.api_status is None:
    badge_style = "background:#f3f4f6;color:#6B7280;"
    badge_text  = "⚪ Not checked"
elif st.session_state.api_status:
    badge_style = "background:#dcfce7;color:#15803d;"
    badge_text  = "● Connected"
else:
    badge_style = "background:#fee2e2;color:#dc2626;"
    badge_text  = "● Error"
 
col1, col2 = st.columns([3, 1], vertical_alignment="center")

badge_style_local = locals().get("badge_style", "background:#f3f4f6;color:#6B7280;")
badge_text_local = locals().get("badge_text", "⚪ Not checked")

with col1:
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:8px;'>"
        f"<span style='{badge_style_local}padding:0.2rem 0.7rem;border-radius:999px;"
        f"font-size:0.72rem;font-weight:600;white-space:nowrap;'>"
        f"{badge_text_local}</span></div>",
        unsafe_allow_html=True
    )

with col2:
    if st.button("Test", key="sidebar_test", use_container_width=True):
        with st.spinner("..."):
            st.session_state.api_status = check_api_status()
        st.rerun()
        # History count
        count = len(st.session_state.history)
        if count:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(
                f'<div style="text-align:center;font-size:0.73rem;color:#9CA3AF;">'
                f'💾 {count} saved generation{"s" if count != 1 else ""}</div>',
                unsafe_allow_html=True,
            )
 
# ─────────────────────────────────────────────
# WORKSPACE PAGE
# ─────────────────────────────────────────────
def render_workspace():
    tool = next((t for t in TOOLS if t["id"] == st.session_state.selected_tool), TOOLS[0])
 
    # App title + active tool hero
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#fff0f7 0%,#f3f0ff 55%,#eff6ff 100%);
        border-radius:20px;padding:1.5rem 1.8rem;
        margin-bottom:1.3rem;border:1px solid #f0e6fb;
    ">
        <div style="
            font-family:'Nunito',sans-serif;font-size:1.5rem;font-weight:800;
            background:linear-gradient(135deg,#FF6FAE,#A78BFA);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;margin-bottom:0.15rem;line-height:1.25;
        ">🌸 NeuroVerse AI Content Studio</div>
        <div style="font-size:0.8rem;color:#9CA3AF;font-weight:500;margin-bottom:0.9rem;">
            Your all-in-one AI writing assistant
        </div>
        <div style="
            display:inline-flex;align-items:center;gap:0.5rem;
            background:#ffffff;border-radius:12px;padding:0.4rem 1rem;
            box-shadow:0 2px 10px rgba(167,139,250,0.12);border:1.5px solid #ede4fc;
        ">
            <span style="font-size:1.2rem;">{tool['icon']}</span>
            <span style="font-family:'Nunito',sans-serif;font-size:0.98rem;
                         font-weight:800;color:#374151;">{tool['label']}</span>
            <span style="font-size:0.68rem;color:#A78BFA;font-weight:700;
                         background:#f3f0ff;padding:0.1rem 0.5rem;border-radius:999px;">Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    # ── Tool Switcher expander ──
    # NOTE: no st.markdown HTML wrapper around/below this expander,
    # which was the cause of the phantom extra box.
    with st.expander("🔧  Switch Tool", expanded=False):
        cols = st.columns(4)
        for i, t in enumerate(TOOLS):
            with cols[i % 4]:
                marker = "✅ " if t["id"] == st.session_state.selected_tool else ""
                if st.button(
                    f"{marker}{t['icon']} {t['label']}",
                    key=f"tool_{t['id']}",
                    use_container_width=True,
                ):
                    st.session_state.selected_tool = t["id"]
                    st.session_state.output = ""
                    st.rerun()
 
    # ── Input controls (pure Streamlit, no HTML div wrappers) ──
    section_header("✏️  Your Prompt")
 
    placeholders = {
        "blog":      "E.g. 10 benefits of morning meditation for busy professionals...",
        "instagram": "E.g. A cozy autumn café vibe with pumpkin latte...",
        "linkedin":  "E.g. My journey from engineer to entrepreneur — lessons learned...",
        "youtube":   "E.g. How to build a passive income stream with digital products...",
        "adcopy":    "E.g. A productivity app for remote teams called 'FocusFlow'...",
        "email":     "E.g. Follow-up email after a sales demo to a startup founder...",
        "pitch":     "E.g. An AI-powered personal finance app for Gen Z...",
        "product":   "E.g. Premium wireless noise-cancelling headphones for creators...",
        "tweet":     "E.g. Why most people fail at building habits...",
        "seo":       "E.g. How to lose weight without going to the gym...",
        "hashtag":   "E.g. A travel photography Instagram account...",
        "rewrite":   "Paste your content here to rewrite and improve it...",
        "tone":      "Paste the content you want to change the tone of...",
        "summarize": "Paste the long article or content to summarize...",
        "hook":      "E.g. A course about mastering public speaking...",
        "title":     "E.g. A guide to starting a successful podcast...",
    }
 
    user_prompt = st.text_area(
        "Prompt",
        placeholder=placeholders.get(st.session_state.selected_tool, "Describe what you need..."),
        height=130,
        label_visibility="collapsed",
    )
 
    col1, col2, col3 = st.columns(3)
    with col1:
        tone = st.selectbox("🎨 Tone", TONES)
    with col2:
        language = st.selectbox("🌐 Language", LANGUAGES)
    with col3:
        creativity = st.slider(
            "✨ Creativity", 0.1, 1.5, 0.8, 0.1,
            help="Low = focused  |  High = more creative",
        )
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # Action buttons
    gc, cc = st.columns([4, 1])
    with gc:
        generate_clicked = st.button("✨  Generate with AI →", key="gen_btn", use_container_width=True)
    with cc:
        if st.button("🗑️ Clear", key="clear_btn", use_container_width=True):
            st.session_state.output = ""
            st.rerun()
 
    # Generate logic
    if generate_clicked:
        if not user_prompt.strip():
            st.warning("Please enter a prompt first! 🌸")
        else:
            with st.spinner(f"✨ Crafting your {tool['label']}..."):
                result, error = generate_content(
                    st.session_state.selected_tool, user_prompt, tone, language, creativity,
                )
            if error:
                st.error(error)
            else:
                st.session_state.output = result
                st.session_state.history.insert(0, {
                    "tool":      tool["label"],
                    "tool_icon": tool["icon"],
                    "prompt":    user_prompt[:120] + ("..." if len(user_prompt) > 120 else ""),
                    "output":    result,
                    "tone":      tone,
                    "language":  language,
                    "model":     st.session_state.selected_model,
                    "timestamp": datetime.datetime.now().strftime("%b %d, %Y · %I:%M %p"),
                })
                st.rerun()
 
    # Output area
    if st.session_state.output:
        output_text = st.session_state.output
        words = len(output_text.split())
        chars = len(output_text)
 
        st.markdown("<hr>", unsafe_allow_html=True)
 
        # Header + word count
        hc1, hc2 = st.columns([3, 1])
        with hc1:
            section_header("✨  Generated Content")
        with hc2:
            st.markdown(
                f'<div style="text-align:right;padding-top:0.35rem;">'
                f'<span style="font-size:0.72rem;background:#f3f0ff;color:#7C3AED;'
                f'padding:0.2rem 0.7rem;border-radius:999px;font-weight:600;">'
                f'{words} words · {chars} chars</span></div>',
                unsafe_allow_html=True,
            )
 
        # Rendered markdown
        st.markdown(output_text)
 
        st.markdown("<hr>", unsafe_allow_html=True)
 
        # Copy hint + native code block (has built-in copy icon)
        st.markdown(
            '<div style="font-size:0.75rem;color:#9CA3AF;font-weight:600;margin-bottom:0.3rem;">'
            '📋 Click the copy icon in the top-right corner of the box below:</div>',
            unsafe_allow_html=True,
        )
        st.code(output_text, language=None)
 
        # Download + Regenerate
        dc, rc = st.columns(2)
        with dc:
            st.download_button(
                "⬇️  Download TXT",
                data=output_text.encode("utf-8"),
                file_name=f"neuroverse_{tool['id']}_{datetime.date.today()}.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_btn",
            )
        with rc:
            if st.button("🔄  Regenerate", use_container_width=True, key="regen_btn"):
                if user_prompt.strip():
                    with st.spinner("🔄 Regenerating..."):
                        result, error = generate_content(
                            st.session_state.selected_tool, user_prompt, tone, language, creativity,
                        )
                    if error:
                        st.error(error)
                    else:
                        st.session_state.output = result
                        st.rerun()
                else:
                    st.warning("Please enter a prompt first!")
 
# ─────────────────────────────────────────────
# HISTORY PAGE
# ─────────────────────────────────────────────
def render_history():
    page_hero("📚  Generation History",
              "Browse, reuse, and download your past AI-generated content.")
 
    if not st.session_state.history:
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;
                    background:#ffffff;border-radius:18px;border:1.5px solid #f0e6fb;">
            <div style="font-size:2.8rem;margin-bottom:0.8rem;">🌸</div>
            <div style="font-size:1.05rem;font-weight:700;color:#374151;margin-bottom:0.3rem;">
                No history yet
            </div>
            <div style="font-size:0.83rem;color:#9CA3AF;">
                Start generating content and it'll appear here!
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
 
    h1, h2 = st.columns([3, 1])
    with h1:
        st.markdown(
            f'<div style="font-size:0.84rem;color:#6B7280;font-weight:600;padding-top:0.3rem;">'
            f'{len(st.session_state.history)} generation(s) saved this session</div>',
            unsafe_allow_html=True,
        )
    with h2:
        if st.button("🗑️  Clear All", key="clear_hist", use_container_width=True):
            st.session_state.history = []
            st.rerun()
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"{item['tool_icon']}  {item['tool']}  ·  {item['timestamp']}", expanded=False):
            st.markdown(
                f'<div style="font-size:0.82rem;font-weight:600;color:#374151;margin-bottom:0.2rem;">'
                f'Prompt: {item["prompt"]}</div>'
                f'<div style="font-size:0.7rem;color:#9CA3AF;">'
                f'Model: {item["model"]} · Tone: {item["tone"]} · Language: {item["language"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown("---")
            st.markdown(item["output"])
            d1, d2, d3 = st.columns(3)
            with d1:
                st.download_button(
                    "⬇️ Download",
                    data=item["output"].encode("utf-8"),
                    file_name=f"neuroverse_history_{i+1}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key=f"dl_hist_{i}",
                )
            with d2:
                if st.button("🖊️ Load to Workspace", key=f"load_{i}", use_container_width=True):
                    st.session_state.output = item["output"]
                    match = next((t for t in TOOLS if t["label"] == item["tool"]), None)
                    if match:
                        st.session_state.selected_tool = match["id"]
                    st.session_state.page = "workspace"
                    st.rerun()
            with d3:
                if st.button("🗑️ Delete", key=f"del_{i}", use_container_width=True):
                    st.session_state.history.pop(i)
                    st.rerun()
 
# ─────────────────────────────────────────────
# SETTINGS PAGE  — Model + About + Tips only
# (API configuration section removed)
# ─────────────────────────────────────────────
def render_settings():
    page_hero("⚙️  Settings", "Manage your AI model and explore app features.")
 
    # ── Model Selection ──
    section_header("🤖  Model Selection")
 
    for m_id, (m_desc, m_tier) in MODEL_INFO.items():
        is_sel     = m_id == st.session_state.selected_model
        tier_bg    = "#dcfce7" if m_tier == "Free" else "#fef9c3"
        tier_fg    = "#15803d" if m_tier == "Free" else "#854d0e"
        card_bg    = "#f5f0ff" if is_sel else "#fdfaff"
        card_bdr   = "#A78BFA" if is_sel else "#ede9fe"
        check      = " ✅" if is_sel else ""
        st.markdown(f"""
        <div style="
            display:flex;align-items:center;justify-content:space-between;
            padding:0.65rem 0.95rem;border-radius:12px;margin-bottom:0.5rem;
            background:{card_bg};border:1.5px solid {card_bdr};
        ">
            <div>
                <div style="font-size:0.8rem;font-weight:700;color:#1F2937;">{m_id}{check}</div>
                <div style="font-size:0.7rem;color:#6B7280;">{m_desc}</div>
            </div>
            <span style="font-size:0.65rem;font-weight:700;
                         background:{tier_bg};color:{tier_fg};
                         padding:0.15rem 0.55rem;border-radius:999px;">{m_tier}</span>
        </div>
        """, unsafe_allow_html=True)
 
    new_model = st.selectbox(
        "Select active model",
        MODELS,
        index=MODELS.index(st.session_state.selected_model),
        key="settings_model_sel",
    )
    if new_model != st.session_state.selected_model:
        st.session_state.selected_model = new_model
        st.session_state.api_status = None
        st.success(f"✅ Model changed to: {new_model}")
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # ── About ──
    section_header("🌸  About NeuroVerse AI")
    st.markdown("""
    **NeuroVerse AI Content Studio** is your all-in-one AI writing assistant.
 
    | Feature | Detail |
    |---|---|
    | 🖊️ Tools | 16 content generators |
    | 🌐 Languages | English, Hindi, Hinglish |
    | 🎨 Tones | 10 writing tones |
    | 💾 History | Auto-saved per session |
    | ⚡ Engine | OpenRouter (100+ models) |
    | 🐍 Stack | Python + Streamlit |
                
    Built with ❤️ using Python & Streamlit | NeuroVerse AI by Pranjal Sharma
    """)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # ── Tips ──
    section_header("💡  Quick Tips")
    st.markdown("""
    - **Creativity 0.7–0.9** gives the best balance of quality and originality
    - **Free models** — Gemini Flash and Llama are free via OpenRouter
    - **Hinglish** works great for Indian social media audiences
    - **Regenerate** multiple times to get fresh variations
    - **History** saves all generations until you refresh or close the tab
    """)
 
# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────
render_sidebar()
 
if st.session_state.page == "workspace":
    render_workspace()
elif st.session_state.page == "history":
    render_history()
elif st.session_state.page == "settings":
    render_settings()
st.markdown("""
<hr style="margin-top:2rem;margin-bottom:0.8rem;border-color:#f0e6f8;">

<div style="
    text-align:center;
    font-size:0.75rem;
    color:#9CA3AF;
    padding-bottom:1.2rem;
    font-weight:500;
">
    © 2026 NeuroVerse AI · All Rights Reserved<br>
    Built with ❤️ by <b>Pranjal Sharma</b>
</div>
""", unsafe_allow_html=True)
