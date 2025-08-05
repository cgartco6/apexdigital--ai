import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class SalesAgent:
    def generate_quote(self, requirements):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a sales agent for NexusAI. Generate fair quotes based on these requirements. Structure as: Base price, Add-ons, Total, Payment options."},
                {"role": "user", "content": requirements}
            ],
            max_tokens=250
        )
        
        quote = response.choices[0].message['content']
        
        # Save to CRM
        self._save_to_crm(requirements, quote)
        return quote
    
    def _save_to_crm(self, requirements, quote):
        # Integration with CRM system
        pass
    
    def upgrade_account(self, user_id, new_plan):
        # Handle plan upgrades
        payment_agent = PaymentAgent()
        return payment_agent.process_upgrade(user_id, new_plan)
