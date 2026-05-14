import streamlit as st
import os
import json
from datetime import datetime
import plotly.graph_objects as go
from cardiac_util import CardioCareAI

# ─────────────────────────────────────────────────────────────────────────────
# 🎨 Page Config & CSS
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CARDIO-CARE | AI Heart Assistant",
    page_icon="Cardio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Cardio Theme
st.markdown("""
<style>
    /* Theme Colors: Deep Red/Crimson (#8B0000, #DC143C, #FF6B6B) */
    :root {
        --primary: #DC143C;
        --secondary: #8B0000;
        --accent: #FF6B6B;
        --bg-dark: #1E1E1E;
        --card-bg: #2D2D2D;
        --text-light: #F0F2F6;
    }
    
    /* Global Styles */
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-light);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--accent) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Force All Text and Labels to be White */
    p, span, label, .stMarkdown, .stText {
        color: var(--text-light) !important;
    }
    
    /* Input Fields Styling (Text, Number, Dropdowns, Textareas) */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
        border: 1px solid #555555 !important;
        border-radius: 6px !important;
    }
    
    /* Selectboxes specifically */
    div[data-baseweb="select"] > div {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
        border: 1px solid #555555 !important;
    }
    
    /* Sidebar Text Force */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h4 {
        color: #FFFFFF !important;
    }
    
    /* Custom Cards */
    .card {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-left: 4px solid var(--primary);
    }
    
    /* Buttons */
    .stButton>button, .stFormSubmitButton>button, [data-testid="stFormSubmitButton"] button, [data-testid="baseButton-secondaryFormSubmit"] {
        background: linear-gradient(90deg, var(--secondary), var(--primary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover, [data-testid="stFormSubmitButton"] button:hover, [data-testid="baseButton-secondaryFormSubmit"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(220, 20, 60, 0.4) !important;
    }
    .stButton>button *, .stFormSubmitButton>button *, [data-testid="stFormSubmitButton"] button *, [data-testid="baseButton-secondaryFormSubmit"] * {
        color: white !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0A0A0F 0%, #1A0D16 100%) !important;
        border-right: 1px solid rgba(255, 42, 95, 0.2) !important;
        box-shadow: 4px 0 15px rgba(0,0,0,0.5) !important;
    }
    
    /* Sidebar Radio Button Cards */
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        background-color: rgba(30, 32, 44, 0.6) !important;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 42, 95, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin-bottom: 12px !important;
        width: 100% !important;
        box-sizing: border-box !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(255, 42, 95, 0.3) !important;
        border-color: #FF2A5F !important;
        background-color: rgba(255, 42, 95, 0.1) !important;
    }
    
    /* Header (Top Panel) */
    header[data-testid="stHeader"] {
        background: rgba(10, 10, 15, 0.8) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-bottom: 1px solid rgba(255, 42, 95, 0.2) !important;
    }
    header[data-testid="stHeader"] * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--accent);
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ⚙️ App State & Setup
# ─────────────────────────────────────────────────────────────────────────────
if 'patient_profile' not in st.session_state:
    st.session_state.patient_profile = {}
if 'risk_assessment' not in st.session_state:
    st.session_state.risk_assessment = None

# Initialize AI Engine securely
@st.cache_resource
def get_ai_engine(_cache_buster=4):
    try:
        return CardioCareAI()
    except Exception as e:
        import traceback
        st.error(f"Engine Init Error: {e}")
        st.error(traceback.format_exc())
        return None

# ─────────────────────────────────────────────────────────────────────────────
# 🚀 Navigation Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 0px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/2966/2966327.png' width='80'>
            <h2 style='color: var(--accent); font-family: Inter, sans-serif; margin-top: 10px; margin-bottom: 0px;'>CARDIO-CARE</h2>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h4 style='text-align: center; margin-top: -15px; margin-bottom: 10px;'>Navigation</h4>", unsafe_allow_html=True)
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
        
    page = st.radio("Go to", [
        "Dashboard",
        "Risk Assessment",
        "Diet Planner",
        "Exercise Planner",
        "Lifestyle Guide",
        "Medical Advice"
    ], key="current_page", label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("*AI-Powered Preventive Care*")

# ─────────────────────────────────────────────────────────────────────────────
# 📌 Page Renderers
# ─────────────────────────────────────────────────────────────────────────────
def navigate_to(page_name):
    st.session_state.current_page = page_name

def render_dashboard():
    # Inject scoped CSS only for Dashboard
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #091020 0%, #1A2942 100%) !important;
            color: #FFFFFF !important;
        }
        .card {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 20px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
            border-left: 5px solid #FFD700 !important;
        }
        .card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(255, 215, 0, 0.4) !important;
            border-color: rgba(255, 215, 0, 0.8) !important;
        }
        h1, h2, h3 {
            color: #FFFFFF !important;
            text-shadow: 0px 2px 4px rgba(0,0,0,0.3);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Cardio-Care Dashboard")
    st.markdown("Welcome to your personal AI-powered heart health assistant.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card" style="height: 180px;">
            <h3>Comprehensive Risk Assessment</h3>
            <p>Evaluate your heart health using advanced AI analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Start Assessment ➔", use_container_width=True, on_click=navigate_to, args=("Risk Assessment",))

    with col2:
        st.markdown("""
        <div class="card" style="height: 180px;">
            <h3>Personalized Plans</h3>
            <p>Get AI-tailored diet and exercise regimens designed specifically for your risk profile.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("View Diet Planner ➔", use_container_width=True, on_click=navigate_to, args=("Diet Planner",))

    with col3:
        st.markdown("""
        <div class="card" style="height: 180px;">
            <h3>Medical Guidance</h3>
            <p>Receive intelligent advice on when to seek professional medical attention.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Get Medical Advice ➔", use_container_width=True, on_click=navigate_to, args=("Medical Advice",))

    st.markdown("---")
    st.markdown("### Ask the AI Cardiologist")
    st.markdown("Have a general question about heart health? Ask our AI assistant below!")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a heart-related question..."):
        # Display user message in chat message container
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ai = get_ai_engine()
                if ai:
                    try:
                        response = ai.answer_general_query(prompt)
                        st.markdown(response)
                        # Add assistant response to chat history
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Failed to generate answer: {str(e)}")
                else:
                    st.error("AI Engine not initialized.")

def render_risk_assessment():
    st.title("Heart Health Risk Assessment")
    st.markdown("Provide your health parameters for an AI-driven cardiovascular risk evaluation.")
    
    with st.form("risk_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", 20, 100, 45)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)", "120/80")
            bmi = st.selectbox("BMI Category", ["Underweight", "Normal", "Overweight", "Obese"])
        with col2:
            cholesterol = st.text_input("Cholesterol Level (mg/dL) or Status", "Normal")
            heart_rate = st.number_input("Resting Heart Rate (bpm)", 40, 150, 72)
            diabetes = st.selectbox("Diabetes Status", ["No", "Prediabetes", "Type 1", "Type 2"])
            smoking = st.selectbox("Smoking Status", ["Never Smoked", "Former Smoker", "Current Smoker"])
        with col3:
            family_history = st.selectbox("Family History of Heart Disease", ["No", "Yes", "Unknown"])
            chest_pain = st.selectbox("Chest Pain Frequency", ["None", "Rare", "Occasional", "Frequent"])
            additional_symptoms = st.text_area("Any other symptoms? (e.g., shortness of breath)", "")
            
        submitted = st.form_submit_button("Analyze Risk Profile")
        
    if submitted:
        ai = get_ai_engine()
        if not ai:
            st.error("Failed to initialize AI Engine.")
            return
            
        with st.spinner("AI is analyzing your cardiovascular profile..."):
            try:
                # Save to session
                st.session_state.patient_profile = {
                    "age": age, "gender": gender, "blood_pressure": blood_pressure,
                    "cholesterol": cholesterol, "heart_rate": heart_rate,
                    "diabetes": diabetes, "smoking": smoking, "bmi": bmi,
                    "family_history": family_history, "chest_pain": chest_pain,
                    "additional_symptoms": additional_symptoms
                }
                
                result = ai.assess_heart_risk(**st.session_state.patient_profile)
                st.session_state.risk_assessment = result
                
                st.success("Analysis Complete!")
                
                # Display Results
                st.markdown("---")
                st.markdown(f"### Assessment Result: {result.risk_level} Risk")
                st.write(result.risk_summary)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### Key Risk Factors")
                    for factor in result.key_risk_factors:
                        st.markdown(f"- {factor}")
                        
                    st.markdown("#### Immediate Actions")
                    for action in result.immediate_actions:
                        st.markdown(f"- {action}")
                with c2:
                    st.markdown("#### Positive Health Factors")
                    for p_factor in result.positive_factors:
                        st.markdown(f"- {p_factor}")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

def render_diet_planner():
    st.title("Heart-Healthy Diet Planner")
    
    if not st.session_state.risk_assessment:
        st.warning("Please complete the Risk Assessment first to get a personalized diet plan.")
        return
    st.info("Your diet plan will be automatically synced with your cardiovascular risk profile (BP, Cholesterol, Diabetes)!")
    
    col1, col2 = st.columns(2)
    with col1:
        health_conditions = st.text_input("Other existing conditions (e.g., Hypertension, Celiac)", "None")
        dietary_preferences = st.selectbox("Dietary Preferences", ["None", "Vegetarian", "Vegan", "Keto", "Mediterranean", "Low-Carb"])
        allergies = st.text_input("Allergies or Intolerances", "None")
    with col2:
        meals_per_day = st.slider("Preferred Meals/Snacks per day", 2, 6, 4)
        cooking_time = st.selectbox("Available Cooking Time per meal", ["Under 15 mins", "15-30 mins", "30-60 mins", "No limit"])
    
    if st.button("Generate Diet Plan"):
        ai = get_ai_engine()
        with st.spinner("Creating your personalized nutrition plan..."):
            try:
                prof = st.session_state.patient_profile
                plan = ai.generate_diet_plan(
                    risk_level=st.session_state.risk_assessment.risk_level,
                    age=prof.get("age", 45),
                    gender=prof.get("gender", "Other"),
                    blood_pressure=prof.get("blood_pressure", "Unknown"),
                    cholesterol=prof.get("cholesterol", "Unknown"),
                    diabetes=prof.get("diabetes", "Unknown"),
                    health_conditions=health_conditions,
                    dietary_preferences=dietary_preferences,
                    allergies=allergies,
                    meals_per_day=meals_per_day,
                    cooking_time=cooking_time
                )
                
                st.markdown(f"### Recommended Diet: {plan.diet_type}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Foods to Include")
                    for f in plan.foods_to_eat:
                        st.write(f"- {f}")
                with col2:
                    st.markdown("#### Foods to Avoid")
                    for f in plan.foods_to_avoid:
                        st.write(f"- {f}")
                        
                st.markdown("#### Sample Meal Plan")
                for m in plan.meal_plan:
                    st.write(f"> {m}")
                    
                st.info("**Hydration Tips:** " + " | ".join(plan.hydration_tips))
                
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")

def render_exercise_planner():
    st.title("Cardiac Exercise Planner")
    
    if not st.session_state.risk_assessment:
        st.warning("Please complete the Risk Assessment first.")
        return
        
    current_fitness = st.selectbox("Current Fitness Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    health_conditions = st.text_area("Any physical limitations?", "None")
    
    if st.button("Generate Exercise Plan"):
        ai = get_ai_engine()
        with st.spinner("Designing safe workout routine..."):
            try:
                prof = st.session_state.patient_profile
                plan = ai.generate_exercise_plan(
                    risk_level=st.session_state.risk_assessment.risk_level,
                    age=prof.get("age", 45),
                    gender=prof.get("gender", "Other"),
                    current_fitness=current_fitness,
                    health_conditions=health_conditions
                )
                
                st.markdown(f"### Starting Level: {plan.fitness_level}")
                st.write(f"**Frequency & Duration:** {plan.duration_frequency}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### Recommended Exercises")
                    for e in plan.recommended_exercises:
                        st.write(f"- {e}")
                with c2:
                    st.markdown("#### Exercises to Avoid")
                    for e in plan.exercises_to_avoid:
                        st.write(f"- {e}")
                
                st.markdown("#### Warm-up & Cool-down")
                for w in plan.warm_up_cool_down:
                    st.write(f"- {w}")
                    
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")

def render_lifestyle_guide():
    st.title("Lifestyle Improvement Guide")
    
    if not st.session_state.risk_assessment:
        st.warning("Please complete the Risk Assessment first.")
        return
        
    stress_level = st.select_slider("Current Stress Level", options=["Low", "Moderate", "High", "Severe"])
    sleep_hours = st.number_input("Average Sleep (hours/night)", 2, 14, 7)
    occupation = st.text_input("Occupation / Activity type", "Desk job")
    
    if st.button("Analyze Lifestyle"):
        ai = get_ai_engine()
        with st.spinner("Formulating lifestyle recommendations..."):
            try:
                prof = st.session_state.patient_profile
                plan = ai.get_lifestyle_recommendations(
                    risk_level=st.session_state.risk_assessment.risk_level,
                    age=prof.get("age", 45),
                    smoking=prof.get("smoking", "Never"),
                    alcohol="Moderate", # Simplified
                    stress_level=stress_level,
                    sleep_hours=str(sleep_hours),
                    occupation=occupation
                )
                
                st.markdown(f"### Overall Lifestyle Score: {plan.overall_lifestyle_score}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### Habits to Build")
                    for h in plan.habits_to_build:
                        st.write(f"- {h}")
                    st.markdown("#### Stress Management")
                    for s in plan.stress_management:
                        st.write(f"- {s}")
                with c2:
                    st.markdown("#### Habits to Quit")
                    for h in plan.habits_to_quit:
                        st.write(f"- {h}")
                    st.markdown("#### Sleep Recommendations")
                    for s in plan.sleep_recommendations:
                        st.write(f"- {s}")
                        
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

def render_medical_advice():
    st.title("Medical Guidance")
    
    if not st.session_state.risk_assessment:
        st.warning("Please complete the Risk Assessment first.")
        return
        
    st.info("**Disclaimer:** This tool provides AI-generated guidance and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician.")
    
    current_medications = st.text_area("Current Medications", "None")
    
    if st.button("Get Medical Guidance"):
        ai = get_ai_engine()
        with st.spinner("Evaluating medical needs..."):
            try:
                prof = st.session_state.patient_profile
                plan = ai.get_medical_advice(
                    risk_level=st.session_state.risk_assessment.risk_level,
                    age=prof.get("age", 45),
                    symptoms=prof.get("additional_symptoms", "None"),
                    existing_conditions="None",
                    current_medications=current_medications
                )
                
                st.markdown(f"### Urgency Level: {plan.urgency_level}")
                st.markdown(f"**Recommended Specialist:** {plan.specialist_referral}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### Recommended Tests")
                    for t in plan.recommended_tests:
                        st.write(f"- {t}")
                    st.markdown("#### At-Home Monitoring")
                    for m in plan.monitoring_tips:
                        st.write(f"- {m}")
                with c2:
                    st.markdown("#### Warning Symptoms (Seek Immediate Care)")
                    for w in plan.warning_symptoms:
                        st.write(f"- {w}")
                        
            except Exception as e:
                st.error(f"Evaluation failed: {str(e)}")

# ─────────────────────────────────────────────────────────────────────────────
# 🔀 Router
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.current_page == "Dashboard":
    render_dashboard()
elif st.session_state.current_page == "Risk Assessment":
    render_risk_assessment()
elif st.session_state.current_page == "Diet Planner":
    render_diet_planner()
elif st.session_state.current_page == "Exercise Planner":
    render_exercise_planner()
elif st.session_state.current_page == "Lifestyle Guide":
    render_lifestyle_guide()
elif st.session_state.current_page == "Medical Advice":
    render_medical_advice()

