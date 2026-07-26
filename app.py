import os
import joblib
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Spam Detection System", page_icon="🛡️", layout="centered"
)

st.markdown(
    """
    <style>
    @import url('https://api.fontshare.com/v2/css?f[]=clash-display@600,700,800&f[]=satoshi@400,500,700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@200;300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown, p, span, div, li {
        font-family: 'Satoshi', sans-serif !important;
        color: #2D3748 !important; /* Dark slate text for off-white background */
    }
    
    /* Elegant Off-White Background */
    .stApp {
        background-color: #FAFAFC !important;
    }

    h1, h2, h3, .gradient-text, .section-header {
        font-family: 'Clash Display', sans-serif !important;
    }

    button, .stButton > button,
    label, .stLabel,
    input, select, textarea,
    div[data-baseweb="slider"] *,
    div[data-baseweb="select"] * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: 0.03em !important;
    }

    /* Input Wrappers */
    div[data-testid="stSlider"], div[data-testid="stSelectbox"], div[data-testid="stNumberInput"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 8px 0px !important;
        margin-bottom: 24px !important;
        animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Labels */
    div[data-testid="stSlider"] label, div[data-testid="stSelectbox"] label, div[data-testid="stNumberInput"] label {
        color: #718096 !important; /* Soft gray */
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase;
        margin-bottom: 12px !important;
        transition: color 0.4s ease !important;
    }
    div[data-testid="stSlider"]:hover label, div[data-testid="stSelectbox"]:hover label, div[data-testid="stNumberInput"]:hover label {
        color: #4C1D95 !important; /* Deep Purple on hover */
    }

    /* Number Input Styling */
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background: #FFFFFF !important;
        border-radius: 6px !important;
        border: 1px solid rgba(107, 33, 168, 0.15) !important;
        transition: border-color 0.35s cubic-bezier(0.16, 1, 0.3, 1), background 0.35s ease !important;
    }
    div[data-testid="stNumberInput"] div[data-baseweb="input"]:hover, div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {
        background: #F4F0FA !important;
        border-color: rgba(107, 33, 168, 0.4) !important;
    }
    div[data-testid="stNumberInput"] input {
        color: #6B21A8 !important; /* Deep Purple */
        -webkit-text-fill-color: #6B21A8 !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
    }

    /* Slider Track */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child > div,
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child > div > div {
        height: 4px !important;
        border-radius: 2px !important;
        transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1), left 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child > div {
        background-color: rgba(107, 33, 168, 0.1) !important;
        box-shadow: none !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child > div:nth-child(2),
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child > div > div:first-child {
        background: #6B21A8 !important;
        box-shadow: none !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child > div:nth-child(3),
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child > div > div:first-child {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Slider Thumb */
    div[data-baseweb="slider"] div[role="slider"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: left 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-baseweb="slider"] div[role="slider"]::before { display: none !important; }
    div[data-baseweb="slider"] div[role="slider"]::after {
        content: "";
        position: absolute;
        width: 10px !important;
        height: 10px !important;
        background: #6B21A8 !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 4px rgba(107, 33, 168, 0.3) !important;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease !important;
        border: none !important;
    }
    div[data-testid="stSlider"]:hover div[data-baseweb="slider"] div[role="slider"]::after {
        transform: scale(1.5) !important;
        box-shadow: 0 0 10px rgba(107, 33, 168, 0.4) !important;
    }
    div[data-baseweb="slider"] div[role="slider"]:active::after,
    div[data-baseweb="slider"] div[role="slider"]:focus::after {
        transform: scale(1.3) !important;
        box-shadow: 0 0 12px rgba(107, 33, 168, 0.5) !important;
    }

    /* Thumb Values */
    div[data-testid="stThumbValue"],
    div[data-baseweb="slider"] div[role="slider"] div {
        color: #6B21A8 !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        transform-origin: bottom center !important;
        -webkit-text-fill-color: #6B21A8 !important;
    }
    div[data-testid="stThumbValue"] *,
    div[data-baseweb="slider"] div[role="slider"] div * {
        color: #6B21A8 !important;
        font-weight: 700 !important;
        -webkit-text-fill-color: #6B21A8 !important;
    }
    div[data-testid="stSlider"]:hover div[data-testid="stThumbValue"],
    div[data-testid="stSlider"]:hover div[data-baseweb="slider"] div[role="slider"] div {
        transform: scale(1.05) translateY(-1px) !important;
    }

    /* Tick Bar Hide/Show */
    div[data-testid="stSliderTickBar"] {
        display: flex !important;
        justify-content: space-between !important;
        padding-top: 10px !important;
        opacity: 0 !important;
        transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stSlider"]:hover div[data-testid="stSliderTickBar"] {
        opacity: 1 !important;
    }
    div[data-testid="stSliderTickBar"] svg, div[data-testid="stSliderTickBar"] path, div[data-testid="stSliderTickBar"] div:empty {
        display: none !important;
    }
    div[data-testid="stSliderTickBar"]::before, div[data-testid="stSliderTickBar"]::after,
    div[data-testid="stSliderTickBar"] div::before, div[data-testid="stSliderTickBar"] div::after {
        display: none !important;
    }
    div[data-testid="stSliderTickBar"] * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        color: #A0AEC0 !important;
        background: transparent !important;
    }

    /* Section Headers */
    .section-header {
        color: #718096;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 42px;
        margin-bottom: 25px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(107, 33, 168, 0.15);
        background: none;
        display: block;
    }

    /* Buttons */
    .element-container:has(.stButton) {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        margin-top: 18px !important;
    }
    div.stButton {
        width: auto !important;
        display: flex !important;
        justify-content: center !important;
    }
    div.stButton > button {
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: auto !important;
        min-width: 0 !important;
        padding: 13px 30px !important;
        border-radius: 8px !important;
        background: #6B21A8 !important;
        border: none !important;
        color: #FFFFFF !important;
        overflow: hidden !important;
        transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), background 0.45s ease, box-shadow 0.45s ease !important;
        box-shadow: 0 4px 14px rgba(107, 33, 168, 0.25);
    }
    div.stButton > button p, div.stButton > button span {
        margin: 0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 11px !important;
        font-weight: 800 !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        color: #FFFFFF !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.015);
        background: #581C87 !important;
        box-shadow: 0 8px 25px rgba(107, 33, 168, 0.35);
    }
    div.stButton > button:active {
        transform: translateY(0px) scale(0.985);
    }

    /* Animations & Background */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes textShine {
        0% { background-position: 0% center; }
        100% { background-position: 100% center; }
    }
    .gradient-text {
        background: linear-gradient(120deg, #6B21A8 30%, #9F7AEA 50%, #6B21A8 70%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textShine 4s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
    }
    .gradient-text-red {
        background: linear-gradient(120deg, #E53E3E 30%, #FC8181 50%, #E53E3E 70%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textShine 4s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
    }

    .block-container {
        margin-top: -64px !important;
    }

    body::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.05;
        z-index: 0;
        background-image: radial-gradient(#6B21A8 1.5px, transparent 1.5px);
        background-size: 12px 12px;
    }

    .main .block-container {
        animation: pageReveal 900ms cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes pageReveal {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .result-reveal {
        animation: resultReveal 650ms cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes resultReveal {
        from { opacity: 0; transform: translateY(14px); filter: blur(6px); }
        to { opacity: 1; transform: translateY(0); filter: blur(0px); }
    }
    
    .result-box {
        background: #FFFFFF; 
        border: 1px solid rgba(107,33,168,0.1); 
        border-left: 4px solid #6B21A8; 
        border-radius: 8px; 
        padding: 1.5rem; 
        margin-top: 40px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "xgboost_champion_pipeline.pkl")
    # Using joblib instead of pickle to prevent STACK_GLOBAL error
    return joblib.load(model_path)


model_loaded = False
try:
    model = load_model()
    model_loaded = True
except FileNotFoundError:
    load_error = "xgboost_champion_pipeline.pkl not found. Make sure it is in the same folder as app.py."
except Exception as e:
    load_error = str(e)

st.markdown(
    """
    <h1 style='font-size: 60px; margin-bottom: 0; line-height: 1.1; text-align: center;'>
        Fiverr Spammer
        <span class='gradient-text' style='display: block; font-size: 68px; font-weight: 800;'>Detection</span>
    </h1>
    <p style='color: #718096; font-size: 15px; margin-top: 20px; text-align: center; font-weight: 500;'>
        Advanced behavioral analysis powered by optimized XGBoost, utilizing the top 15 features that drive 85.31% of the model's predictive power.
    </p>
    <div style='height: 24px;'></div>
    """,
    unsafe_allow_html=True,
)

if not model_loaded:
    st.error(f"⚠️ Could not load model — {load_error}")
    st.stop()

st.markdown(
    "<div class='section-header'>👤 User Activity Metrics</div>",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    x20 = st.slider("Feature X20", min_value=0, max_value=1, value=0)
    x19 = st.number_input("Feature X19", min_value=0, max_value=250, value=2)
    x25 = st.number_input("Feature X25", min_value=0, max_value=700, value=0)
    x6 = st.slider("Feature X6", min_value=1, max_value=5, value=4)
    x49 = st.slider("Feature X49", min_value=0, max_value=1, value=0)
with col2:
    x7 = st.slider("Feature X7", min_value=1, max_value=15, value=1)
    x4 = st.slider("Feature X4", min_value=1, max_value=5, value=1)
    x11 = st.slider("Feature X11", min_value=0, max_value=1, value=0)
    x36 = st.slider("Feature X36", min_value=0, max_value=10, value=0)
    x5 = st.slider("Feature X5", min_value=1, max_value=20, value=2)
with col3:
    x22 = st.slider("Feature X22", min_value=1, max_value=60, value=17)
    x8 = st.slider("Feature X8", min_value=1, max_value=35, value=21)
    x2 = st.slider("Feature X2", min_value=1, max_value=250, value=147)
    x9 = st.slider("Feature X9", min_value=1, max_value=50, value=14)
    x13 = st.slider("Feature X13", min_value=0, max_value=15, value=0)

st.markdown("<div style='height: 34px;'></div>", unsafe_allow_html=True)

if st.button("Analyze User Behavior"):

    # 1. Initialize all 51 features to 0 (baseline)
    input_dict = {f"X{i}": 0 for i in range(1, 52)}

    # 2. Overwrite the top 15 features with the user inputs from the UI
    input_dict.update(
        {
            "X20": x20,
            "X19": x19,
            "X25": x25,
            "X6": x6,
            "X49": x49,
            "X7": x7,
            "X4": x4,
            "X11": x11,
            "X36": x36,
            "X5": x5,
            "X22": x22,
            "X8": x8,
            "X2": x2,
            "X9": x9,
            "X13": x13,
        }
    )

    # 3. Convert to DataFrame maintaining correct column order expected by the pipeline
    input_df = pd.DataFrame([input_dict])
    input_df = input_df[[f"X{i}" for i in range(1, 52)]]

    try:
        # Predict Class and Probability
        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0][1]

        st.markdown(
            """
            <div class="result-reveal" style="text-align:center; margin-top:38px; padding:42px 20px 12px;">
                <p style="color:#718096; font-size:11px; font-weight:700; letter-spacing:0.22em; text-transform:uppercase; margin:0 0 18px;">
                    Account Analysis Result
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if pred == 1:
            st.markdown(
                f"<h1 style='text-align:center; font-size:52px; margin:0; font-family:Clash Display, sans-serif; line-height:1;' class='gradient-text-red'>POTENTIAL SPAMMER</h1>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<h1 style='text-align:center; font-size:52px; margin:0; font-family:Clash Display, sans-serif; line-height:1;' class='gradient-text'>LEGITIMATE USER</h1>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='width:46px; height:2px; background:rgba(107, 33, 168, 0.22); margin:28px auto 0; border-radius: 2px;'></div>",
            unsafe_allow_html=True,
        )

        # Build insight text based on prediction probability
        if prob > 0.8:
            insight_text = "Highly suspicious behavioral patterns detected. Immediate manual review recommended."
        elif prob > 0.5:
            insight_text = "Questionable behavior identified. Account flagged by automated systems."
        elif prob > 0.2:
            insight_text = "Some unusual metrics present, but mostly aligns with legitimate activity."
        else:
            insight_text = "Behavioral footprint is consistent with standard, legitimate platform usage."

        st.markdown(
            f"""
            <div class="result-reveal result-box">
                <p style="color: #4A5568; font-size: 0.9rem; margin: 0; line-height: 1.5; font-family: 'Plus Jakarta Sans', sans-serif;">
                    <span style="color: #6B21A8; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.75rem;">Confidence Score: {prob*100:.1f}%</span><br><br>
                    {insight_text}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Smooth scroll to results
        st.components.v1.html(
            """
            <script>
                const result = window.parent.document.querySelector('.result-reveal');
                if (result) {
                    result.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            </script>
            """,
            height=0,
        )

    except Exception as e:
        st.error(f"Computation Error: {e}")

st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

st.components.v1.html(
    """
    <script>
    const doc = window.parent.document;

    function centerButton() {
        doc.querySelectorAll('.stButton').forEach(el => {
            el.style.setProperty('display', 'flex', 'important');
            el.style.setProperty('justify-content', 'center', 'important');
            let parent = el.parentElement;
            while (parent) {
                parent.style.setProperty('display', 'flex', 'important');
                parent.style.setProperty('justify-content', 'center', 'important');
                if (parent.classList.contains('block-container')) break;
                parent = parent.parentElement;
            }
        });
    }

    centerButton();
    new MutationObserver(centerButton).observe(doc.body, { childList: true, subtree: true });

    const buttons = doc.querySelectorAll('.stButton > button');

    buttons.forEach(btn => {
        btn.addEventListener('mousemove', e => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const moveX = (x - rect.width / 2) * 0.04;
            const moveY = (y - rect.height / 2) * 0.10;

            btn.style.transform = `
                translate(${moveX}px, ${moveY - 2}px)
                scale(1.02)
            `;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });
    </script>
    """,
    height=0,
    width=0,
)
