# app/services/ai_service.py
from app.models.AIModel import AIModel
import sys, io

class AIService:
    @staticmethod
    def generate_response(prompt):
        model = AIModel()
        preamble = "Answer in one sentence"

        model.create_conversation(preamble, prompt) # prompt = "I love ..."
        response_text = model.continue_conversation(preamble, "What do I love ?")
        model.stop_conversation()

        return response_text
    
    @staticmethod
    def generate_and_execute_python(prompt):
        model = AIModel()
        preamble = """
            Generate only the code, with no descriptions or commentaries. 
            Generate it in brute text format, with no triples backticks.
        """

        response_text = model.generate_response(preamble, prompt) # prompt = "Generate and execute a Python function to ..."
        
        generated_code = response_text.replace('```python', '').replace('```', '').strip()

        old_stdout = sys.stdout
        buffer = io.StringIO()

        try:
            sys.stdout = buffer
            exec(generated_code)
        except Exception as e:
            sys.stdout = old_stdout
            return f"Erreur lors de l'exécution : {str(e)}"

        sys.stdout = old_stdout
        script_output = buffer.getvalue()

        return script_output