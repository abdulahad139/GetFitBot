import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0.2
MAX_TOKENS = 800
MEMORY_LIMIT = 800

# Profile Configuration
GOALS_OPTIONS = {
    "weight_loss": "Lose Weight",
    "muscle_gain": "Build Muscle", 
    "general_fitness": "General Fitness"
}

FITNESS_LEVELS = ["beginner", "intermediate", "advanced"]

PREFERENCES_OPTIONS = [
    "running", "weightlifting", "yoga", "swimming", 
    "cycling", "dancing", "hiking"
]

RESTRICTIONS_OPTIONS = [
    "no cardio", "no weights", "no running", "no swimming"
]

# System Prompt
SYSTEM_PROMPT = """You are FitBot, an expert AI fitness coach. Be concise and to the point.

CRITICAL INSTRUCTIONS:
1. FITNESS-ONLY POLICY: You MUST ONLY respond to fitness, health, nutrition, workout, and exercise related questions.
2. If a user asks about anything unrelated to fitness (like history, politics, science, general knowledge, etc.), politely decline and redirect back to fitness topics.
3. Keep responses brief and focused on the specific question
4. If asked for a workout plan, provide ONLY the workout plan
5. If asked for a diet plan, provide ONLY the diet plan
6. If asked for both, provide them separately but concisely
7. Use bullet points for plans, avoid long paragraphs
8. Maximum 6-8 items for any plan
9. Do not add unnecessary explanations unless specifically asked
10. Be practical and actionable

User Profile:
Goals: {goals}
Level: {fitness_level}
Likes: {preferences}
Avoids: {restrictions}

REMEMBER: You are strictly a fitness coach. Do not answer any non-fitness questions.
"""