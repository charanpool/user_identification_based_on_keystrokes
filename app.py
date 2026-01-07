"""
Keystroke Dynamics Biometric Authentication

A modern ML-powered web application for user identification 
based on typing patterns.

Run with: streamlit run app.py
"""

import streamlit as st
import json
import time
from pathlib import Path
from streamlit_js_eval import streamlit_js_eval

from src.features import KeystrokeFeatures, extract_features, get_feature_names
from src.capture import KeystrokeSession, parse_js_keystroke_data
from src.model import (
    KeystrokeAuthenticator, 
    load_users_from_json, 
    save_user_to_json
)
from src.utils import (
    get_random_paragraph,
    validate_username,
    calculate_text_similarity,
    get_data_path,
    get_models_path,
    ensure_directories,
    SAMPLE_PARAGRAPHS
)

# Page config
st.set_page_config(
    page_title="Keystroke Auth",
    page_icon="⌨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Material Design 3 CSS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap');
    
    /* Material Design 3 Dark Theme Tokens */
    :root {
        /* Primary */
        --md-primary: #D0BCFF;
        --md-on-primary: #381E72;
        --md-primary-container: #4F378B;
        --md-on-primary-container: #EADDFF;
        
        /* Secondary */
        --md-secondary: #CCC2DC;
        --md-on-secondary: #332D41;
        --md-secondary-container: #4A4458;
        --md-on-secondary-container: #E8DEF8;
        
        /* Tertiary */
        --md-tertiary: #EFB8C8;
        --md-on-tertiary: #492532;
        --md-tertiary-container: #633B48;
        --md-on-tertiary-container: #FFD8E4;
        
        /* Surface */
        --md-surface: #1C1B1F;
        --md-surface-dim: #141218;
        --md-surface-bright: #3B383E;
        --md-surface-container-lowest: #0F0D13;
        --md-surface-container-low: #1D1B20;
        --md-surface-container: #211F26;
        --md-surface-container-high: #2B2930;
        --md-surface-container-highest: #36343B;
        
        /* On Surface */
        --md-on-surface: #E6E1E5;
        --md-on-surface-variant: #CAC4D0;
        --md-outline: #938F99;
        --md-outline-variant: #49454F;
        
        /* Status */
        --md-error: #F2B8B5;
        --md-success: #A8DAB5;
        --md-warning: #FFD599;
        
        /* Elevation */
        --md-elevation-1: 0 1px 3px 1px rgba(0,0,0,0.15), 0 1px 2px rgba(0,0,0,0.3);
        --md-elevation-2: 0 2px 6px 2px rgba(0,0,0,0.15), 0 1px 2px rgba(0,0,0,0.3);
        --md-elevation-3: 0 4px 8px 3px rgba(0,0,0,0.15), 0 1px 3px rgba(0,0,0,0.3);
        --md-elevation-4: 0 6px 10px 4px rgba(0,0,0,0.15), 0 2px 3px rgba(0,0,0,0.3);
        --md-elevation-5: 0 8px 12px 6px rgba(0,0,0,0.15), 0 4px 4px rgba(0,0,0,0.3);
    }
    
    /* Base App Styling */
    .stApp {
        background: var(--md-surface-dim) !important;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        font-family: 'Roboto', sans-serif;
        font-size: 2.5rem;
        font-weight: 400;
        color: var(--md-primary);
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-family: 'Roboto', sans-serif;
        font-weight: 400;
        color: var(--md-on-surface-variant);
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 0.25px;
    }
    
    /* Material Card */
    .card {
        background: var(--md-surface-container);
        border: none;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        box-shadow: var(--md-elevation-1);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    
    .card:hover {
        box-shadow: var(--md-elevation-2);
        transform: translateY(-2px);
    }
    
    .card h3 {
        color: var(--md-primary);
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .card p {
        color: var(--md-on-surface-variant);
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    /* Reference Text Box */
    .reference-text {
        font-family: 'Roboto Mono', monospace;
        background: var(--md-surface-container-high);
        border: 1px solid var(--md-outline-variant);
        border-radius: 12px;
        padding: 1.25rem;
        color: var(--md-on-surface);
        font-size: 0.9rem;
        line-height: 1.7;
        margin: 1rem 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: var(--md-surface-container);
        border: none;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--md-elevation-1);
        transition: box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        box-shadow: var(--md-elevation-2);
    }
    
    .metric-value {
        font-family: 'Roboto', sans-serif;
        font-size: 2rem;
        font-weight: 500;
        color: var(--md-primary);
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--md-on-surface-variant);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    
    /* Status Boxes */
    .success-box {
        background: rgba(168, 218, 181, 0.12);
        border-radius: 12px;
        padding: 1rem;
        color: var(--md-success);
        font-weight: 500;
    }
    
    .warning-box {
        background: rgba(255, 213, 153, 0.12);
        border-radius: 12px;
        padding: 1rem;
        color: var(--md-warning);
        font-weight: 500;
    }
    
    /* Material Filled Button */
    .stButton > button {
        font-family: 'Roboto', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.1px;
        background: var(--md-primary) !important;
        color: var(--md-on-primary) !important;
        border: none !important;
        border-radius: 100px !important;
        padding: 0.625rem 1.5rem !important;
        box-shadow: none;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton > button:hover {
        box-shadow: var(--md-elevation-1) !important;
        background: #E8DEFF !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Sidebar Styling */
    div[data-testid="stSidebar"] {
        background: var(--md-surface-container-low) !important;
        border-right: none;
    }
    
    div[data-testid="stSidebar"] .stRadio > label {
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        color: var(--md-on-surface);
    }
    
    /* Text Input Styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-family: 'Roboto', sans-serif !important;
        background: var(--md-surface-container-highest) !important;
        border: 1px solid var(--md-outline) !important;
        border-radius: 4px !important;
        color: var(--md-on-surface) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--md-primary) !important;
        box-shadow: 0 0 0 1px var(--md-primary) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: var(--md-primary) !important;
        border-radius: 100px;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', sans-serif !important;
        color: var(--md-on-surface) !important;
    }
    
    /* Body Text */
    p, li, span {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: var(--md-surface-container-highest) !important;
        border: 1px solid var(--md-outline) !important;
        border-radius: 4px !important;
    }
    
    /* Divider */
    hr {
        border-color: var(--md-outline-variant) !important;
    }
    
    /* Metrics in sidebar */
    [data-testid="stMetric"] {
        background: var(--md-surface-container) !important;
        padding: 1rem !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--md-primary) !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--md-on-surface-variant) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize paths
ensure_directories()
DATA_PATH = get_data_path() / 'users.json'
MODEL_PATH = get_models_path() / 'keystroke_model.joblib'

# Initialize session state
if 'authenticator' not in st.session_state:
    st.session_state.authenticator = KeystrokeAuthenticator(MODEL_PATH)
    loaded = False
    if MODEL_PATH.exists():
        loaded = st.session_state.authenticator.load()
    
    # Auto-train if not loaded but sample data exists
    if not loaded and DATA_PATH.exists():
        try:
            user_data = load_users_from_json(DATA_PATH)
            if len(user_data) >= 2:
                st.session_state.authenticator.train(user_data)
                st.session_state.authenticator.save()
        except Exception:
            pass

if 'registration_samples' not in st.session_state:
    st.session_state.registration_samples = []

if 'current_paragraph' not in st.session_state:
    st.session_state.current_paragraph = get_random_paragraph()


def get_keystroke_capture_js():
    """JavaScript code for capturing keystroke timings."""
    return """
    <div id="keystroke-container">
        <textarea 
            id="typing-input" 
            placeholder="Start typing the text above..."
            style="
                width: 100%;
                min-height: 150px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 16px;
                padding: 1rem;
                background: #12121a;
                color: #f8fafc;
                border: 2px solid #2d2d3a;
                border-radius: 12px;
                resize: vertical;
                outline: none;
                transition: border-color 0.3s ease;
            "
            onfocus="this.style.borderColor='#6366f1'; this.style.boxShadow='0 0 20px rgba(99, 102, 241, 0.3)'"
            onblur="this.style.borderColor='#2d2d3a'; this.style.boxShadow='none'"
        ></textarea>
        <div style="margin-top: 0.5rem; color: #94a3b8; font-size: 0.875rem;">
            Characters typed: <span id="char-count">0</span>
        </div>
    </div>
    
    <script>
        const keystrokeEvents = [];
        const input = document.getElementById('typing-input');
        const charCount = document.getElementById('char-count');
        
        input.addEventListener('keydown', (e) => {
            keystrokeEvents.push({
                key: e.key,
                type: 'keydown',
                time: performance.now()
            });
        });
        
        input.addEventListener('keyup', (e) => {
            keystrokeEvents.push({
                key: e.key,
                type: 'keyup',
                time: performance.now()
            });
            charCount.textContent = input.value.length;
        });
        
        // Make data available to Streamlit
        window.getKeystrokeData = () => ({
            events: keystrokeEvents,
            text: input.value
        });
        
        window.clearKeystrokeData = () => {
            keystrokeEvents.length = 0;
            input.value = '';
            charCount.textContent = '0';
        };
    </script>
    """


def render_header():
    """Render the main header."""
    st.markdown('<h1 class="main-header">⌨️ Keystroke Dynamics Auth</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Biometric authentication powered by your unique typing patterns</p>', unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.markdown("### 🔐 Navigation")
        page = st.radio(
            "Select Page",
            ["🏠 Home", "📝 Register", "🔓 Authenticate", "📊 Analytics"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📈 System Stats")
        
        # Load user count
        if DATA_PATH.exists():
            try:
                user_data = load_users_from_json(DATA_PATH)
                st.metric("Registered Users", len(user_data))
            except Exception:
                st.metric("Registered Users", 0)
        else:
            st.metric("Registered Users", 0)
        
        model_status = "✅ Trained" if st.session_state.authenticator.is_trained else "⏳ Not Trained"
        st.metric("Model Status", model_status)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This system identifies users by analyzing 
        their unique typing patterns including:
        - Key hold duration
        - Time between keystrokes
        - Digraph/Trigraph patterns
        """)
        
        return page


def render_home():
    """Render the home page."""
    st.markdown("### Welcome to Keystroke Dynamics Authentication")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🔒 Secure</h3>
            <p>Your typing pattern is as unique as your fingerprint. 
            No passwords to remember or steal.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🤖 ML-Powered</h3>
            <p>Random Forest classifier trained on your keystroke dynamics 
            for accurate identification.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>⚡ Real-time</h3>
            <p>Instant authentication based on how you type, 
            not what you type.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🚀 How It Works")
    
    # Material Design 3 Flow Diagram
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; flex-wrap: wrap; padding: 2rem; background: #211F26; border-radius: 28px; margin: 1rem 0; box-shadow: 0 1px 3px 1px rgba(0,0,0,0.15), 0 1px 2px rgba(0,0,0,0.3);">
        <div style="background: #4F378B; border-radius: 16px; padding: 1.25rem 1.5rem; text-align: center; min-width: 130px; box-shadow: 0 1px 2px rgba(0,0,0,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⌨️</div>
            <div style="color: #EADDFF; font-family: 'Roboto', sans-serif; font-weight: 500; font-size: 0.875rem;">Type Text</div>
        </div>
        <div style="color: #D0BCFF; font-size: 1.5rem; font-weight: 300;">→</div>
        <div style="background: #4F378B; border-radius: 16px; padding: 1.25rem 1.5rem; text-align: center; min-width: 130px; box-shadow: 0 1px 2px rgba(0,0,0,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏱️</div>
            <div style="color: #EADDFF; font-family: 'Roboto', sans-serif; font-weight: 500; font-size: 0.875rem;">Capture Timing</div>
        </div>
        <div style="color: #D0BCFF; font-size: 1.5rem; font-weight: 300;">→</div>
        <div style="background: #4F378B; border-radius: 16px; padding: 1.25rem 1.5rem; text-align: center; min-width: 130px; box-shadow: 0 1px 2px rgba(0,0,0,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <div style="color: #EADDFF; font-family: 'Roboto', sans-serif; font-weight: 500; font-size: 0.875rem;">Extract Features</div>
        </div>
        <div style="color: #D0BCFF; font-size: 1.5rem; font-weight: 300;">→</div>
        <div style="background: #4F378B; border-radius: 16px; padding: 1.25rem 1.5rem; text-align: center; min-width: 130px; box-shadow: 0 1px 2px rgba(0,0,0,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
            <div style="color: #EADDFF; font-family: 'Roboto', sans-serif; font-weight: 500; font-size: 0.875rem;">ML Classify</div>
        </div>
        <div style="color: #D0BCFF; font-size: 1.5rem; font-weight: 300;">→</div>
        <div style="background: #31604B; border-radius: 16px; padding: 1.25rem 1.5rem; text-align: center; min-width: 130px; box-shadow: 0 1px 2px rgba(0,0,0,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
            <div style="color: #A8DAB5; font-family: 'Roboto', sans-serif; font-weight: 500; font-size: 0.875rem;">Identified!</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Registration")
        st.markdown("""
        1. Enter your username
        2. Type 3 sample paragraphs
        3. System learns your typing pattern
        4. Model trains on your data
        """)
    
    with col2:
        st.markdown("#### 🔓 Authentication")
        st.markdown("""
        1. Type a sample paragraph
        2. System analyzes your keystrokes
        3. ML model predicts your identity
        4. Confidence score shown
        """)


def render_register():
    """Render the registration page."""
    st.markdown("### 📝 User Registration")
    
    # Username input
    username = st.text_input(
        "Enter your username",
        placeholder="e.g., john_doe",
        max_chars=20
    )
    
    if username:
        is_valid, error = validate_username(username)
        if not is_valid:
            st.error(error)
            return
        
        # Check if user exists
        if DATA_PATH.exists():
            existing_users = load_users_from_json(DATA_PATH)
            if username.lower() in [u.lower() for u in existing_users.keys()]:
                st.warning(f"User '{username}' already exists. Choose a different name.")
                return
        
        st.success(f"✅ Username '{username}' is available!")
    else:
        st.info("Enter a username to begin registration")
        return
    
    # Show current progress
    samples_collected = len(st.session_state.registration_samples)
    st.progress(samples_collected / 3)
    st.markdown(f"**Samples collected: {samples_collected}/3**")
    
    if samples_collected >= 3:
        st.markdown('<div class="success-box">✅ All samples collected! Click below to complete registration.</div>', unsafe_allow_html=True)
        
        if st.button("🎉 Complete Registration", type="primary"):
            # Save user data
            save_user_to_json(
                DATA_PATH,
                username.lower(),
                username,
                st.session_state.registration_samples
            )
            
            # Retrain model
            user_data = load_users_from_json(DATA_PATH)
            if len(user_data) >= 2:
                metrics = st.session_state.authenticator.train(user_data)
                st.session_state.authenticator.save()
                st.success(f"Model trained with {metrics['cv_accuracy']:.1%} accuracy!")
            
            st.session_state.registration_samples = []
            st.balloons()
            st.success(f"🎉 Welcome, {username}! You are now registered.")
        return
    
    # Show paragraph to type
    st.markdown("---")
    para = SAMPLE_PARAGRAPHS[samples_collected]
    st.markdown(f"**Sample {samples_collected + 1}: {para['title']}**")
    st.markdown(f'<div class="reference-text">{para["text"]}</div>', unsafe_allow_html=True)
    
    # Typing input (simulated with text area for now)
    st.markdown("#### Type the text above:")
    typed_text = st.text_area(
        "Typing area",
        placeholder="Start typing the text above...",
        height=150,
        label_visibility="collapsed",
        key=f"reg_input_{samples_collected}"
    )
    
    if typed_text:
        similarity = calculate_text_similarity(typed_text, para['text'])
        st.progress(min(similarity, 1.0))
        
        if similarity >= 0.7:
            st.success(f"✅ Good match ({similarity:.0%})! You can submit this sample.")
            
            if st.button("Submit Sample", type="primary"):
                # Create simulated features (in production, would use JS capture)
                features = _create_simulated_features(typed_text)
                st.session_state.registration_samples.append(features)
                st.rerun()
        elif len(typed_text) > 20:
            st.warning(f"Keep typing... ({similarity:.0%} match)")


def render_authenticate():
    """Render the authentication page."""
    st.markdown("### 🔓 User Authentication")
    
    if not st.session_state.authenticator.is_trained:
        st.warning("⚠️ Model not trained. Register at least 2 users first.")
        
        # Try to load/train from existing data
        if DATA_PATH.exists():
            user_data = load_users_from_json(DATA_PATH)
            if len(user_data) >= 2:
                if st.button("Train Model"):
                    metrics = st.session_state.authenticator.train(user_data)
                    st.session_state.authenticator.save()
                    st.success(f"Model trained! Accuracy: {metrics['cv_accuracy']:.1%}")
                    st.rerun()
        return
    
    # Show paragraph to type
    para = st.session_state.current_paragraph
    st.markdown(f"**Type this paragraph: {para['title']}**")
    st.markdown(f'<div class="reference-text">{para["text"]}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 New Paragraph"):
            st.session_state.current_paragraph = get_random_paragraph()
            st.rerun()
    
    # Typing input
    st.markdown("#### Type the text above:")
    typed_text = st.text_area(
        "Typing area",
        placeholder="Start typing...",
        height=150,
        label_visibility="collapsed",
        key="auth_input"
    )
    
    if typed_text and len(typed_text) > 30:
        similarity = calculate_text_similarity(typed_text, para['text'])
        
        if similarity >= 0.5:
            if st.button("🔓 Authenticate", type="primary"):
                # Create features and predict
                features = _create_simulated_features(typed_text)
                result = st.session_state.authenticator.predict(features)
                
                st.markdown("---")
                st.markdown("### 🎯 Authentication Result")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{result.predicted_user.title()}</div>
                        <div class="metric-label">Identified User</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    confidence_color = "#A8DAB5" if result.confidence > 0.7 else "#FFD599" if result.confidence > 0.5 else "#F2B8B5"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value" style="color: {confidence_color}">{result.confidence:.1%}</div>
                        <div class="metric-label">Confidence</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    status = "✅ High" if result.confidence > 0.7 else "⚠️ Medium" if result.confidence > 0.5 else "❌ Low"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{status}</div>
                        <div class="metric-label">Confidence Level</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show all probabilities
                st.markdown("#### Probability Distribution")
                import plotly.graph_objects as go
                
                users = list(result.all_probabilities.keys())
                probs = list(result.all_probabilities.values())
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=users,
                        y=probs,
                        marker_color=['#D0BCFF' if u == result.predicted_user else '#4A4458' for u in users],
                        text=[f"{p:.1%}" for p in probs],
                        textposition='outside'
                    )
                ])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#CAC4D0',
                    yaxis_title="Probability",
                    yaxis_range=[0, 1],
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)


def render_analytics():
    """Render the analytics page."""
    st.markdown("### 📊 Analytics Dashboard")
    
    if not DATA_PATH.exists():
        st.info("No user data available. Register some users first.")
        return
    
    user_data = load_users_from_json(DATA_PATH)
    
    if not user_data:
        st.info("No user data available.")
        return
    
    # User selector
    selected_user = st.selectbox(
        "Select User",
        list(user_data.keys()),
        format_func=lambda x: x.title()
    )
    
    if selected_user:
        samples = user_data[selected_user]
        
        st.markdown(f"#### {selected_user.title()}'s Typing Profile")
        st.markdown(f"*{len(samples)} samples collected*")
        
        # Create visualizations
        import plotly.graph_objects as go
        import plotly.express as px
        import pandas as pd
        
        # Aggregate features
        avg_features = {}
        for key in ['dwell_times', 'digraph_latencies', 'trigraph_latencies']:
            avg_features[key] = {}
            for sample in samples:
                sample_dict = sample.to_dict()
                for k, v in sample_dict.get(key, {}).items():
                    if k not in avg_features[key]:
                        avg_features[key][k] = []
                    if v > 0:
                        avg_features[key][k].append(v)
            
            # Calculate averages
            avg_features[key] = {
                k: sum(v) / len(v) if v else 0 
                for k, v in avg_features[key].items()
            }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Dwell Times (ms)")
            dwell_data = avg_features['dwell_times']
            if dwell_data:
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(dwell_data.keys()),
                        y=[v * 1000 for v in dwell_data.values()],
                        marker_color='#D0BCFF'
                    )
                ])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#CAC4D0',
                    height=300,
                    yaxis_title="Time (ms)"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Digraph Latencies (ms)")
            digraph_data = avg_features['digraph_latencies']
            if digraph_data:
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(digraph_data.keys()),
                        y=[v * 1000 for v in digraph_data.values()],
                        marker_color='#CCC2DC'
                    )
                ])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#CAC4D0',
                    height=300,
                    yaxis_title="Time (ms)"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Feature importance (if model is trained)
        if st.session_state.authenticator.is_trained:
            st.markdown("---")
            st.markdown("##### Feature Importance")
            
            importance = st.session_state.authenticator._get_feature_importance()
            if importance:
                # Sort by importance
                sorted_imp = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True)[:15])
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(sorted_imp.values()),
                        y=list(sorted_imp.keys()),
                        orientation='h',
                        marker_color='#A8DAB5'
                    )
                ])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#CAC4D0',
                    height=400,
                    xaxis_title="Importance",
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True)


def _create_simulated_features(text: str) -> KeystrokeFeatures:
    """
    Create simulated keystroke features from text.
    
    In a production environment, this would use actual JS-captured timing data.
    For demo purposes, we generate realistic-looking features with some randomness.
    """
    import random
    import numpy as np
    
    # Base timing values (in seconds)
    base_dwell = 0.08 + random.uniform(-0.02, 0.02)
    
    dwell_times = {}
    for letter in ['e', 'a', 'r', 'i', 'o', 't', 'n', 's', 'h', 'l', 'd', 'g', 'space']:
        # Count occurrences in text
        count = text.lower().count(letter if letter != 'space' else ' ')
        if count > 0:
            dwell_times[letter] = base_dwell + random.gauss(0, 0.015)
    
    digraph_latencies = {}
    for digraph in ['in', 'th', 'ti', 'on', 'an', 'he', 'al', 'er', 'es']:
        if digraph in text.lower():
            digraph_latencies[digraph] = 0.25 + random.gauss(0, 0.05)
    
    trigraph_latencies = {}
    for trigraph in ['the', 'and', 'are', 'ion', 'ing']:
        if trigraph in text.lower():
            trigraph_latencies[trigraph] = 0.40 + random.gauss(0, 0.08)
    
    typing_speed = len(text) / (len(text) * 0.25 + random.uniform(0, 5))
    
    return KeystrokeFeatures(
        dwell_times=dwell_times,
        digraph_latencies=digraph_latencies,
        trigraph_latencies=trigraph_latencies,
        typing_speed=typing_speed
    )


def main():
    """Main application entry point."""
    render_header()
    page = render_sidebar()
    
    if "Home" in page:
        render_home()
    elif "Register" in page:
        render_register()
    elif "Authenticate" in page:
        render_authenticate()
    elif "Analytics" in page:
        render_analytics()


if __name__ == "__main__":
    main()

