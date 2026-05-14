import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, field_validator

load_dotenv()


# ─────────────────────────────────────────────────────────────────────────────
# Pydantic Output Models
# ─────────────────────────────────────────────────────────────────────────────

class HeartRiskAssessment(BaseModel):
    risk_level: str = Field(description="Risk level: Low / Moderate / High / Critical")
    risk_summary: str = Field(description="Brief summary of the heart disease risk based on the provided parameters")
    key_risk_factors: List[str] = Field(description="Top risk factors identified from the provided data")
    immediate_actions: List[str] = Field(description="Immediate steps the user should take")
    positive_factors: List[str] = Field(description="Positive health factors identified")

    @field_validator("risk_level", mode="before")
    def clean_risk_level(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class DietPlan(BaseModel):
    diet_type: str = Field(description="Recommended diet type for heart health")
    foods_to_eat: List[str] = Field(description="Heart-healthy foods to include daily")
    foods_to_avoid: List[str] = Field(description="Foods to avoid for heart health")
    meal_plan: List[str] = Field(description="Sample meal plan (breakfast, lunch, dinner, snacks)")
    hydration_tips: List[str] = Field(description="Hydration and fluid intake recommendations")

    @field_validator("diet_type", mode="before")
    def clean_diet_type(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class ExercisePlan(BaseModel):
    fitness_level: str = Field(description="Recommended starting fitness level based on the user profile")
    recommended_exercises: List[str] = Field(description="Specific exercises recommended for heart health")
    duration_frequency: str = Field(description="How long and how often to exercise")
    exercises_to_avoid: List[str] = Field(description="Exercises to avoid given the health profile")
    warm_up_cool_down: List[str] = Field(description="Warm-up and cool-down routines")

    @field_validator("fitness_level", mode="before")
    def clean_fitness_level(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class LifestyleRecommendation(BaseModel):
    overall_lifestyle_score: str = Field(description="Overall lifestyle assessment: Poor / Fair / Good / Excellent")
    sleep_recommendations: List[str] = Field(description="Sleep hygiene and duration recommendations")
    stress_management: List[str] = Field(description="Stress management and mental wellness techniques")
    habits_to_build: List[str] = Field(description="Positive habits to develop for heart health")
    habits_to_quit: List[str] = Field(description="Harmful habits to eliminate for heart health")

    @field_validator("overall_lifestyle_score", mode="before")
    def clean_lifestyle_score(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


class MedicalAdvice(BaseModel):
    urgency_level: str = Field(description="Urgency to see a doctor: Routine / Soon / Urgent / Emergency")
    recommended_tests: List[str] = Field(description="Medical tests and screenings recommended")
    warning_symptoms: List[str] = Field(description="Symptoms that require immediate medical attention")
    specialist_referral: str = Field(description="Type of specialist to consult if needed")
    monitoring_tips: List[str] = Field(description="Parameters to self-monitor at home")

    @field_validator("urgency_level", mode="before")
    def clean_urgency(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)


# ─────────────────────────────────────────────────────────────────────────────
# CardioCareAI Main Class
# ─────────────────────────────────────────────────────────────────────────────

class CardioCareAI:
    def __init__(self):
        """
        Initialize with Groq API key from Streamlit secrets or environment variables.
        """
        import streamlit as st
        try:
            # Check Streamlit secrets first (used in Streamlit Cloud)
            api_key_value = st.secrets["GROQ_API_KEY"]
        except Exception:
            # Fallback to local environment variable
            api_key_value = os.environ.get("GROQ_API_KEY")

        if not api_key_value:
            raise ValueError(
                "API Key is missing! You need to add it to your Streamlit Cloud Secrets. "
                "Go to your Streamlit Dashboard -> App Settings -> Secrets, and add:\n"
                'GROQ_API_KEY = "your_actual_api_key_here"'
            )

        self.llm = ChatGroq(
            api_key=api_key_value,
            model="llama-3.1-8b-instant",
            temperature=0.7,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Heart Risk Assessment
    # ─────────────────────────────────────────────────────────────────────────
    def assess_heart_risk(
        self,
        age: int,
        gender: str,
        blood_pressure: str,
        cholesterol: str,
        heart_rate: str,
        diabetes: str,
        smoking: str,
        bmi: str,
        family_history: str,
        chest_pain: str,
        additional_symptoms: str,
    ) -> HeartRiskAssessment:
        """Generate a comprehensive heart disease risk assessment."""
        parser = PydanticOutputParser(pydantic_object=HeartRiskAssessment)

        prompt = PromptTemplate(
            template=(
                "As a cardiologist and heart health expert, assess the heart disease risk for this patient:\n\n"
                "Age: {age}\n"
                "Gender: {gender}\n"
                "Blood Pressure: {blood_pressure}\n"
                "Cholesterol Level: {cholesterol}\n"
                "Resting Heart Rate: {heart_rate}\n"
                "Diabetes: {diabetes}\n"
                "Smoking Status: {smoking}\n"
                "BMI Category: {bmi}\n"
                "Family History of Heart Disease: {family_history}\n"
                "Chest Pain/Discomfort: {chest_pain}\n"
                "Additional Symptoms: {additional_symptoms}\n\n"
                "Provide a thorough heart disease risk assessment in this EXACT JSON format:\n\n"
                "{{\n"
                '  "risk_level": "Low / Moderate / High / Critical",\n'
                '  "risk_summary": "2-3 sentence summary of the overall heart disease risk",\n'
                '  "key_risk_factors": ["Risk factor 1", "Risk factor 2", "Risk factor 3"],\n'
                '  "immediate_actions": ["Action 1", "Action 2", "Action 3"],\n'
                '  "positive_factors": ["Positive factor 1", "Positive factor 2"]\n'
                "}}\n\n"
                "Be compassionate, clear, and evidence-based. Always recommend consulting a doctor.\n"
                "{format_instructions}"
            ),
            input_variables=[
                "age", "gender", "blood_pressure", "cholesterol", "heart_rate",
                "diabetes", "smoking", "bmi", "family_history", "chest_pain",
                "additional_symptoms",
            ],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.llm.invoke(
                    prompt.format(
                        age=age, gender=gender, blood_pressure=blood_pressure,
                        cholesterol=cholesterol, heart_rate=heart_rate,
                        diabetes=diabetes, smoking=smoking, bmi=bmi,
                        family_history=family_history, chest_pain=chest_pain,
                        additional_symptoms=additional_symptoms,
                    )
                )
                parsed = parser.parse(response.content)
                if not parsed.risk_level or not parsed.key_risk_factors:
                    raise ValueError("Incomplete risk assessment")
                return parsed
            except Exception as e:
                if attempt == max_attempts - 1:
                    return HeartRiskAssessment(
                        risk_level="Moderate",
                        risk_summary="Unable to generate a full assessment at this time. Please consult a cardiologist for a proper evaluation based on your provided health parameters.",
                        key_risk_factors=["Unable to determine — please retry", "Consult a doctor for accurate assessment"],
                        immediate_actions=["Schedule an appointment with a cardiologist", "Monitor blood pressure daily", "Avoid strenuous activity until evaluated"],
                        positive_factors=["Seeking health information proactively"],
                    )
                continue

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Diet Plan
    # ─────────────────────────────────────────────────────────────────────────
    def generate_diet_plan(
        self,
        risk_level: str,
        age: int,
        gender: str,
        blood_pressure: str,
        cholesterol: str,
        diabetes: str,
        health_conditions: str,
        dietary_preferences: str,
        allergies: str,
        meals_per_day: int,
        cooking_time: str,
    ) -> DietPlan:
        """Generate a personalized heart-healthy diet plan."""
        parser = PydanticOutputParser(pydantic_object=DietPlan)

        prompt = PromptTemplate(
            template=(
                "As a clinical dietitian specializing in cardiovascular nutrition, create a personalized heart-healthy diet plan:\n\n"
                "Heart Disease Risk Level: {risk_level}\n"
                "Age & Gender: {age}, {gender}\n"
                "Clinical Profile -> BP: {blood_pressure}, Cholesterol: {cholesterol}, Diabetes: {diabetes}\n"
                "Existing Health Conditions: {health_conditions}\n"
                "Dietary Preferences: {dietary_preferences}\n"
                "Allergies/Intolerances: {allergies}\n"
                "Meals per Day: {meals_per_day}\n"
                "Cooking Time/Effort: {cooking_time}\n\n"
                "CRITICAL REQUIREMENT: You MUST strictly adhere to the Dietary Preferences ({dietary_preferences}). If the preference is Vegetarian or Vegan, you must NOT include ANY meat, fish, poultry, or eggs in the foods to eat or meal plan. Failure to respect dietary preferences is dangerous.\n\n"
                "Provide a detailed, practical diet plan in this EXACT JSON format:\n\n"
                "{{\n"
                '  "diet_type": "Name of the recommended diet approach",\n'
                '  "foods_to_eat": ["Food 1 with reason", "Food 2 with reason", "Food 3", "Food 4", "Food 5"],\n'
                '  "foods_to_avoid": ["Food 1 with reason", "Food 2 with reason", "Food 3", "Food 4"],\n'
                '  "meal_plan": ["Breakfast: ...", "Mid-morning snack: ...", "Lunch: ...", "Evening snack: ...", "Dinner: ..."],\n'
                '  "hydration_tips": ["Tip 1", "Tip 2", "Tip 3"]\n'
                "}}\n\n"
                "Make recommendations practical, affordable, and culturally appropriate for Indian context.\n"
                "{format_instructions}"
            ),
            input_variables=["risk_level", "age", "gender", "blood_pressure", "cholesterol", "diabetes", "health_conditions", "dietary_preferences", "allergies", "meals_per_day", "cooking_time"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.llm.invoke(
                    prompt.format(
                        risk_level=risk_level, age=age, gender=gender,
                        blood_pressure=blood_pressure, cholesterol=cholesterol,
                        diabetes=diabetes, health_conditions=health_conditions,
                        dietary_preferences=dietary_preferences, allergies=allergies,
                        meals_per_day=meals_per_day, cooking_time=cooking_time
                    )
                )
                parsed = parser.parse(response.content)
                if not parsed.diet_type or not parsed.foods_to_eat:
                    raise ValueError("Incomplete diet plan")
                return parsed
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise RuntimeError(f"Failed to generate diet plan after {max_attempts} attempts: {str(e)}")
                continue

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Exercise Plan
    # ─────────────────────────────────────────────────────────────────────────
    def generate_exercise_plan(
        self,
        risk_level: str,
        age: int,
        gender: str,
        current_fitness: str,
        health_conditions: str,
    ) -> ExercisePlan:
        """Generate a tailored cardiac exercise plan."""
        parser = PydanticOutputParser(pydantic_object=ExercisePlan)

        prompt = PromptTemplate(
            template=(
                "As a cardiac rehabilitation exercise physiologist, create a safe and effective exercise plan:\n\n"
                "Heart Disease Risk Level: {risk_level}\n"
                "Age: {age}\n"
                "Gender: {gender}\n"
                "Current Fitness Level: {current_fitness}\n"
                "Health Conditions/Limitations: {health_conditions}\n\n"
                "Provide a safe, evidence-based exercise plan in this EXACT JSON format:\n\n"
                "{{\n"
                '  "fitness_level": "Beginner / Intermediate / Active",\n'
                '  "recommended_exercises": ["Exercise 1 with description", "Exercise 2", "Exercise 3", "Exercise 4", "Exercise 5"],\n'
                '  "duration_frequency": "Specific guidance on duration and how many days per week",\n'
                '  "exercises_to_avoid": ["Exercise to avoid 1 with reason", "Exercise 2 with reason"],\n'
                '  "warm_up_cool_down": ["Warm-up step 1", "Warm-up step 2", "Cool-down step 1", "Cool-down step 2"]\n'
                "}}\n\n"
                "Prioritize safety above all. For high/critical risk users, recommend only very gentle activity.\n"
                "{format_instructions}"
            ),
            input_variables=["risk_level", "age", "gender", "current_fitness", "health_conditions"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.llm.invoke(
                    prompt.format(
                        risk_level=risk_level, age=age, gender=gender,
                        current_fitness=current_fitness, health_conditions=health_conditions,
                    )
                )
                parsed = parser.parse(response.content)
                if not parsed.fitness_level or not parsed.recommended_exercises:
                    raise ValueError("Incomplete exercise plan")
                return parsed
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise RuntimeError(f"Failed to generate exercise plan after {max_attempts} attempts: {str(e)}")
                continue

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Lifestyle Recommendations
    # ─────────────────────────────────────────────────────────────────────────
    def get_lifestyle_recommendations(
        self,
        risk_level: str,
        age: int,
        smoking: str,
        alcohol: str,
        stress_level: str,
        sleep_hours: str,
        occupation: str,
    ) -> LifestyleRecommendation:
        """Generate comprehensive lifestyle improvement recommendations."""
        parser = PydanticOutputParser(pydantic_object=LifestyleRecommendation)

        prompt = PromptTemplate(
            template=(
                "As a preventive cardiologist and lifestyle medicine expert, provide comprehensive lifestyle recommendations:\n\n"
                "Heart Disease Risk Level: {risk_level}\n"
                "Age: {age}\n"
                "Smoking Status: {smoking}\n"
                "Alcohol Consumption: {alcohol}\n"
                "Stress Level: {stress_level}\n"
                "Average Sleep Hours: {sleep_hours}\n"
                "Occupation/Activity Level: {occupation}\n\n"
                "CRITICAL SCORING RULE: Be highly strict with the 'overall_lifestyle_score'. If the user's stress level is 'High' or 'Severe', OR if they sleep less than 6 hours a night, their lifestyle score MUST be rated as 'Poor' or 'Critical'. Do not artificially inflate the score to 'Fair' or 'Good' if their basic sleep and stress metrics are failing.\n\n"
                "Provide detailed, actionable lifestyle recommendations in this EXACT JSON format:\n\n"
                "{{\n"
                '  "overall_lifestyle_score": "Poor / Fair / Good / Excellent",\n'
                '  "sleep_recommendations": ["Sleep tip 1", "Sleep tip 2", "Sleep tip 3"],\n'
                '  "stress_management": ["Stress technique 1", "Stress technique 2", "Stress technique 3"],\n'
                '  "habits_to_build": ["Positive habit 1", "Positive habit 2", "Positive habit 3", "Positive habit 4"],\n'
                '  "habits_to_quit": ["Harmful habit 1 with impact", "Harmful habit 2 with impact", "Harmful habit 3"]\n'
                "}}\n\n"
                "Be encouraging but realistic. Provide specific, step-by-step behavioral changes.\n"
                "{format_instructions}"
            ),
            input_variables=["risk_level", "age", "smoking", "alcohol", "stress_level", "sleep_hours", "occupation"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.llm.invoke(
                    prompt.format(
                        risk_level=risk_level, age=age, smoking=smoking,
                        alcohol=alcohol, stress_level=stress_level,
                        sleep_hours=sleep_hours, occupation=occupation,
                    )
                )
                parsed = parser.parse(response.content)
                if not parsed.overall_lifestyle_score or not parsed.habits_to_build:
                    raise ValueError("Incomplete lifestyle recommendations")
                return parsed
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise RuntimeError(f"Failed to generate lifestyle recommendations after {max_attempts} attempts: {str(e)}")
                continue

    # ─────────────────────────────────────────────────────────────────────────
    # 5. Medical Advice
    # ─────────────────────────────────────────────────────────────────────────
    def get_medical_advice(
        self,
        risk_level: str,
        age: int,
        symptoms: str,
        existing_conditions: str,
        current_medications: str,
    ) -> MedicalAdvice:
        """Generate medical guidance on when and how to seek care."""
        parser = PydanticOutputParser(pydantic_object=MedicalAdvice)

        prompt = PromptTemplate(
            template=(
                "As a cardiologist providing guidance (not a diagnosis), advise this patient on their medical care needs:\n\n"
                "Heart Disease Risk Level: {risk_level}\n"
                "Age: {age}\n"
                "Current Symptoms: {symptoms}\n"
                "Existing Medical Conditions: {existing_conditions}\n"
                "Current Medications: {current_medications}\n\n"
                "Provide medical guidance in this EXACT JSON format:\n\n"
                "{{\n"
                '  "urgency_level": "Routine / Soon / Urgent / Emergency",\n'
                '  "recommended_tests": ["Test 1 with reason", "Test 2 with reason", "Test 3"],\n'
                '  "warning_symptoms": ["Symptom requiring immediate ER visit 1", "Symptom 2", "Symptom 3"],\n'
                '  "specialist_referral": "Type of specialist and reason",\n'
                '  "monitoring_tips": ["What to monitor at home 1", "What to monitor 2", "What to monitor 3"]\n'
                "}}\n\n"
                "IMPORTANT: Always clarify this is guidance only and NOT a medical diagnosis.\n"
                "Recommend professional medical consultation for any health concerns.\n"
                "{format_instructions}"
            ),
            input_variables=["risk_level", "age", "symptoms", "existing_conditions", "current_medications"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.llm.invoke(
                    prompt.format(
                        risk_level=risk_level, age=age, symptoms=symptoms,
                        existing_conditions=existing_conditions, current_medications=current_medications,
                    )
                )
                parsed = parser.parse(response.content)
                if not parsed.urgency_level or not parsed.recommended_tests:
                    raise ValueError("Incomplete medical advice")
                return parsed
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise RuntimeError(f"Failed to generate medical advice after {max_attempts} attempts: {str(e)}")
                continue

    # ─────────────────────────────────────────────────────────────────────────
    # 6. General AI Assistant Query
    # ─────────────────────────────────────────────────────────────────────────
    def answer_general_query(self, query: str) -> str:
        """Answer general heart-related queries directly on the dashboard."""
        prompt = PromptTemplate(
            template=(
                "As an AI cardiologist and heart health assistant, answer the following query from a user.\n"
                "Provide accurate, helpful, and concise information.\n"
                "Important: If the user asks for personal medical advice or mentions severe symptoms (like chest pain), "
                "always remind them to consult a doctor or seek emergency medical help immediately.\n\n"
                "User Query: {query}\n\n"
                "Answer:"
            ),
            input_variables=["query"]
        )

        try:
            response = self.llm.invoke(prompt.format(query=query))
            return response.content
        except Exception as e:
            raise RuntimeError(f"Failed to generate answer: {str(e)}")
