from app import get_api_connection

class AIModel:
    def __init__(self):
        self.chat_history = []

    def create_conversation(self, preamble, prompt):
        conn = get_api_connection()
        response = conn.chat(
            model="command-r-plus-08-2024",
            preamble=preamble,
            message=prompt
        )

        self.chat_history = response.chat_history
        return response.text

    def continue_conversation(self, preamble, prompt):
        if not self.chat_history:
            raise ValueError("Conversation not initialized.")

        conn = get_api_connection()
        response = conn.chat(
            model="command-r-plus-08-2024",
            preamble=preamble,
            message=prompt,
            chat_history=self.chat_history
        )
        
        self.chat_history = response.chat_history
        return response.text

    def stop_conversation(self):
        self.chat_history = []

    def generate_response(self, preamble, prompt):
        conn = get_api_connection()
        response = conn.chat(
            model="command-r-plus-08-2024",
            preamble=preamble,
            message=prompt
        )

        return response.text
