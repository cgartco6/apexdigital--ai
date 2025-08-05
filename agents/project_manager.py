import requests
from config import GITHUB_API_TOKEN

class ProjectManager:
    def create_project(self, project_name, description):
        headers = {
            "Authorization": f"token {GITHUB_API_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "name": project_name,
            "description": description,
            "private": True
        }
        
        response = requests.post("https://api.github.com/user/repos", json=payload, headers=headers)
        
        if response.status_code == 201:
            repo = response.json()
            self._assign_agents(project_name)
            return repo['html_url']
        else:
            return None
    
    def _assign_agents(self, project_name):
        # Assign appropriate AI agents to the project
        content_creator = ContentCreator()
        content_creator.initialize_content_plan(project_name)
        
        social_media = SocialMediaAgent()
        social_media.setup_channels(project_name)
    
    def create_helper_agent(self, project_id, specialization):
        helper_creator = HelperCreator()
        return helper_creator.create_agent(project_id, specialization)
