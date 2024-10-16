# app/services/ai_service.py
from app import get_api_connection

class AIService:
    @staticmethod
    def generate_response(prompt):
        if not prompt:
            raise ValueError("No prompt provided")

        conn = get_api_connection()
        response = conn.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "user", "content": prompt}]
        )

        description_text = response.message.content[0].text
        return description_text
