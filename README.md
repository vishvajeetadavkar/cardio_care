# CARDIO-CARE: AI-Powered Heart Health Assistant

CARDIO-CARE is an AI-powered preventive heart healthcare decision-support system designed to assess cardiovascular risk and provide personalized health recommendations. It uses advanced natural language processing to deliver tailored guidance on diet, exercise, lifestyle, and medical follow-ups.

**Note:** This is a pure LLM-driven application powered by Groq and LangChain. It uses AI reasoning based on provided clinical parameters. It is **not** a substitute for professional medical advice.

## 🌟 Features

- **❤️ Risk Assessment:** AI-driven cardiovascular risk evaluation based on clinical parameters (age, blood pressure, cholesterol, etc.).
- **🥗 Diet Planner:** Personalized heart-healthy nutrition plans based on risk level and dietary preferences.
- **🏃 Exercise Planner:** Safe and effective cardiac exercise routines tailored to current fitness levels.
- **💡 Lifestyle Guide:** Comprehensive lifestyle improvement recommendations, covering stress, sleep, and habits.
- **🩺 Medical Guidance:** Intelligent advice on when to seek professional medical attention and what symptoms to monitor.

## 🏗️ Architecture

- **Frontend:** Streamlit dashboard with a premium dark-mode cardio theme.
- **AI Orchestration:** LangChain for prompt management and structured Pydantic outputs.
- **Model:** Llama 3.1 8B Instant via Groq Cloud API for fast, reliable inference.
- **Data Flow:** User inputs -> Streamlit Session State -> LangChain Prompts -> Groq API -> Pydantic parsing -> Streamlit UI.

## 🚀 Setup & Installation

1. **Clone or Navigate to the Directory:**
   Make sure you are in the project folder.

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **API Key Setup:**
   - Get a free API key from [Groq Console](https://console.groq.com/).
   - Copy `.env.example` to `.env` and add your key, OR enter it directly in the Streamlit sidebar when running the app.

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## 👥 Target Users
- **Preventive Care Advocates:** Individuals wanting to assess their heart health and adopt better lifestyles.
- **Health Coaches & Dietitians:** Professionals looking for AI-assisted starting points for client plans.
- **General Public:** For awareness and educational purposes regarding cardiovascular health.

## ⚖️ Disclaimer
This application provides AI-generated information for educational purposes only. It is not intended to diagnose, treat, cure, or prevent any disease. Always consult a qualified healthcare provider for medical diagnosis and treatment.
