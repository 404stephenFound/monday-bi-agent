import google.generativeai as genai
from datetime import datetime

class BIAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        
        # Robust model discovery logic to avoid 404 errors
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if 'models/gemini-1.5-flash' in available_models:
                self.model_name = 'gemini-1.5-flash'
            elif 'models/gemini-pro' in available_models:
                self.model_name = 'gemini-pro'
            else:
                self.model_name = available_models[0].replace('models/', '')
                
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            self.model_name = 'gemini-pro'
            self.model = genai.GenerativeModel(self.model_name)

    def answer_query(self, user_query, deals, work_orders):
        # Setting the context date for relative queries (e.g., "this quarter")
        today = datetime.now().strftime("%Y-%m-%d")

        system_prompt = f"""
        You are the Skylark Business Intelligence Agent. Your goal is to provide high-level 
        strategic synthesis of Sales Pipeline (Deals) and Flight Operations (Work Orders).

        TODAY'S DATE: {today}

        GOALS:
        1. ANSWER BUSINESS QUESTIONS: Focus on revenue, pipeline health, and operational bottlenecks.
        2. DATA RESILIENCE: Handle messy data (e.g., '2024-Q1', 'Jan-24', null values). Use logic to normalize them.
        3. LEADERSHIP INSIGHTS: Provide "Why it matters" instead of just raw lists.
        4. CROSS-BOARD ANALYSIS: Correlate deals won with work orders assigned.

        FORMATTING RULES:
        - Use Markdown headers (###) for clarity.
        - Use 🟢 for "Completed/Won/Healthy".
        - Use 🟡 for "In Progress/Messy Data/Incomplete".
        - Use 🔴 for "Stalled/Delayed/High Risk".
        - ALWAYS conclude with a specific section: "### 💡 Founder's Action Item".

        CONTEXT DATA:
        Deals Board: {deals}
        Work Orders Board: {work_orders}
        """

        try:
            # Generate the response using the refined system prompt
            full_user_input = f"{system_prompt}\n\nUser Question: {user_query}"
            response = self.model.generate_content(full_user_input)
            
            if response and response.text:
                return response.text
            else:
                return "The agent could not generate a summary. Please ensure your Monday.com boards have data."
        except Exception as e:
            return f"Agent Logic Error: {str(e)}. (Using model: {self.model_name})"