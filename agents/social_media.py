import os
import json
import requests
import schedule
import time
from datetime import datetime, timedelta
from config import (
    OPENAI_API_KEY,
    FACEBOOK_PAGE_ID,
    FACEBOOK_ACCESS_TOKEN,
    INSTAGRAM_BUSINESS_ID,
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET,
    LINKEDIN_CLIENT_ID,
    LINKEDIN_CLIENT_SECRET,
    TIKTOK_ACCESS_TOKEN,
    GOOGLE_ANALYTICS_ID
)
from agents.content_creator import ContentCreator

class SocialMediaAgent:
    def __init__(self):
        self.content_creator = ContentCreator()
        self.platforms = {
            'facebook': self.post_to_facebook,
            'instagram': self.post_to_instagram,
            'twitter': self.post_to_twitter,
            'linkedin': self.post_to_linkedin,
            'tiktok': self.post_to_tiktok
        }
        self.analytics_data = {}
        self.load_schedule()

    def create_campaign(self, campaign_name, platforms, content_type, target_audience, schedule_frequency):
        """Create and schedule a social media campaign"""
        campaign = {
            'name': campaign_name,
            'platforms': platforms,
            'content_type': content_type,
            'target_audience': target_audience,
            'schedule': schedule_frequency,
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        # Save campaign to database
        self.save_campaign(campaign)
        
        # Schedule posts
        self.schedule_posts(campaign)
        
        return campaign

    def generate_content(self, content_type, target_audience):
        """Generate platform-optimized content using AI"""
        prompt = f"Create engaging {content_type} content for {target_audience} that will perform well on social media. Include relevant hashtags and emojis."
        return self.content_creator.generate_content(prompt)

    def schedule_posts(self, campaign):
        """Schedule posts based on campaign frequency"""
        frequency = campaign['schedule']
        
        if frequency == 'daily':
            schedule.every().day.at("09:00").do(
                self.execute_campaign_post, campaign
            )
        elif frequency == 'weekly':
            schedule.every().monday.at("10:00").do(
                self.execute_campaign_post, campaign
            )
        elif frequency == 'hourly':
            schedule.every().hour.do(
                self.execute_campaign_post, campaign
            )
        
        # Start scheduler in background thread
        self.start_scheduler()

    def execute_campaign_post(self, campaign):
        """Create and post content for a campaign"""
        content = self.generate_content(
            campaign['content_type'],
            campaign['target_audience']
        )
        
        for platform in campaign['platforms']:
            if platform in self.platforms:
                self.platforms[platform](content)
                
                # Track analytics
                self.track_analytics(campaign['name'], platform)

    def post_to_facebook(self, content):
        """Post content to Facebook"""
        url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/feed"
        params = {
            'message': content,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        response = requests.post(url, params=params)
        return response.json()

    def post_to_instagram(self, content):
        """Post content to Instagram"""
        # First upload the media container
        container_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_BUSINESS_ID}/media"
        params = {
            'image_url': self.generate_ai_image(content),
            'caption': content,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        container_response = requests.post(container_url, params=params)
        container_id = container_response.json().get('id')
        
        # Now publish the container
        publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_BUSINESS_ID}/media_publish"
        params = {
            'creation_id': container_id,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        return requests.post(publish_url, params=params).json()

    def post_to_twitter(self, content):
        """Post content to Twitter"""
        import tweepy
        
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        
        # Split content if too long
        if len(content) > 280:
            content = content[:277] + "..."
        
        return api.update_status(content)

    def post_to_linkedin(self, content):
        """Post content to LinkedIn"""
        # LinkedIn API requires multiple steps for authentication
        # This is a simplified version
        auth_url = "https://www.linkedin.com/oauth/v2/accessToken"
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': LINKEDIN_CLIENT_ID,
            'client_secret': LINKEDIN_CLIENT_SECRET
        }
        auth_response = requests.post(auth_url, data=auth_data)
        access_token = auth_response.json().get('access_token')
        
        # Now post content
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "author": "urn:li:person:YOUR_PROFILE_ID",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        return requests.post(post_url, headers=headers, json=payload).json()

    def post_to_tiktok(self, content):
        """Post content to TikTok"""
        # TikTok API requires a multi-step process
        # This is a simplified version
        upload_url = "https://open-api.tiktok.com/video/upload/"
        params = {
            'access_token': TIKTOK_ACCESS_TOKEN,
            'video': self.generate_ai_video(content)
        }
        response = requests.post(upload_url, files=params)
        video_id = response.json().get('video_id')
        
        # Now create the post
        post_url = "https://open-api.tiktok.com/video/create/"
        params = {
            'access_token': TIKTOK_ACCESS_TOKEN,
            'video_id': video_id,
            'title': content[:150],
            'privacy_level': 'PUBLIC'
        }
        return requests.post(post_url, params=params).json()

    def generate_ai_image(self, prompt):
        """Generate AI image using DALL-E"""
        import openai
        openai.api_key = OPENAI_API_KEY
        
        response = openai.Image.create(
            prompt=f"Social media image for post: {prompt}",
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']

    def generate_ai_video(self, prompt):
        """Generate AI video (simplified - would use video generation API)"""
        # In a real implementation, this would use a video generation API
        # For demo purposes, return a placeholder
        return "https://example.com/generated-video.mp4"

    def track_analytics(self, campaign_name, platform):
        """Track campaign performance in analytics"""
        if campaign_name not in self.analytics_data:
            self.analytics_data[campaign_name] = {}
        
        if platform not in self.analytics_data[campaign_name]:
            self.analytics_data[campaign_name][platform] = {
                'impressions': 0,
                'engagement': 0,
                'clicks': 0
            }
        
        # Simulate analytics data - in real implementation would use APIs
        self.analytics_data[campaign_name][platform]['impressions'] += 1000
        self.analytics_data[campaign_name][platform]['engagement'] += 50
        self.analytics_data[campaign_name][platform]['clicks'] += 10
        
        # Send to Google Analytics
        self.send_to_google_analytics(campaign_name, platform)

    def send_to_google_analytics(self, campaign_name, platform):
        """Send analytics data to Google Analytics"""
        params = {
            'v': '1',  # API Version
            'tid': GOOGLE_ANALYTICS_ID,  # Tracking ID
            'cid': '555',  # Client ID
            't': 'event',  # Hit type
            'ec': 'social_media',  # Event category
            'ea': 'post',  # Event action
            'el': campaign_name,  # Event label
            'ev': self.analytics_data[campaign_name][platform]['engagement'],
            'cd1': platform  # Custom dimension
        }
        requests.post('https://www.google-analytics.com/collect', params=params)

    def optimize_content(self, content, platform):
        """Optimize content for specific platform"""
        prompt = f"Optimize this content for {platform}: {content}"
        return self.content_creator.generate_content(prompt)

    def load_schedule(self):
        """Load existing campaigns from database and schedule them"""
        # In real implementation, this would load from database
        campaigns = self.get_active_campaigns()
        
        for campaign in campaigns:
            self.schedule_posts(campaign)

    def get_active_campaigns(self):
        """Retrieve active campaigns from database"""
        # Placeholder - would query database in real implementation
        return [
            {
                'name': 'Main Awareness Campaign',
                'platforms': ['facebook', 'instagram'],
                'content_type': 'brand awareness',
                'target_audience': 'South African entrepreneurs',
                'schedule': 'daily'
            }
        ]

    def save_campaign(self, campaign):
        """Save campaign to database"""
        # Placeholder - would save to database in real implementation
        print(f"Saving campaign: {campaign['name']}")

    def start_scheduler(self):
        """Run the scheduler in a background thread"""
        import threading
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)
        
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()

    def create_helper_agent(self, specialization):
        """Create a specialized helper agent"""
        helper_creator = HelperCreator()
        return helper_creator.create_agent(specialization)
