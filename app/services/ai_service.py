# app/services/ai_service.py
from app import get_api_connection
from app.models.AIModel import AIModel

class AIService:
    @staticmethod
    def generate_response(prompt):
        model = AIModel()
        preamble = "Answer in one sentence"

        model.create_conversation(preamble, prompt) # prompt = "I love ..."
        response_text = model.continue_conversation(preamble, "What do I love ?")
        model.stop_conversation()

        return response_text