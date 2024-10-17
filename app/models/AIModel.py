import uuid
from app import get_api_connection

class AIModel:
    def __init__(self):
        self.conversation_id = ""

    def _generate_conversation_id(self):
        return str(uuid.uuid4())

    def create_conversation(self, preamble, prompt):
        self.conversation_id = self._generate_conversation_id()
        conn = get_api_connection()
        response = conn.chat(
            model="command-r-plus-08-2024",
            preamble=preamble,
            message=prompt,
            conversation_id=self.conversation_id
        )

        return response.text

    def continue_conversation(self, preamble, prompt):
        if not self.conversation_id:
            raise ValueError("Conversation not initialized.")

        conn = get_api_connection()
        response = conn.chat(
            model="command-r-plus-08-2024",
            preamble=preamble,
            message=prompt,
            conversation_id=self.conversation_id
        )
        
        return response.text

    def stop_conversation(self):
        self.conversation_id = ""

    def generate_response(self, preamble, prompt):
        conn = get_api_connection()
        response = conn.chat(
            model="command-r-plus-08-2024",
            preamble=preamble,
            message=prompt
        )

        return response.text
