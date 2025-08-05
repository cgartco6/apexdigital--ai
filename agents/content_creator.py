import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class ContentCreator:
    def generate_content(self, topic, keywords, tone="professional"):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a content creator AI. Generate engaging content about {topic} using keywords: {keywords}. Tone: {tone}"},
            ],
            max_tokens=1000
        )
        return response.choices[0].message['content']
    
    def optimize_seo(self, content, keywords):
        # SEO optimization logic
        return f"SEO optimized content: {content}"
    
    def initialize_content_plan(self, project_name):
        # Create content calendar
        content_calendar = ContentCalendar()
        content_calendar.generate_plan(project_name)
