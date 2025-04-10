# Marketing Agent System with Streamlit Interface and secure API key entry

import requests
from bs4 import BeautifulSoup
import openai
import streamlit as st

# Streamlit App
st.set_page_config(page_title="Marketing Agent System", layout="wide")
st.title("🚀 Marketing Agent System")

# Secure API Key Entry
openai_api_key = st.text_input("🔑 Enter your OpenAI API key (kept private)", type="password")

url = st.text_input("🌐 Enter Website URL to Analyze")

if openai_api_key:
    openai.api_key = openai_api_key

    if url:
        with st.spinner("Analyzing website and generating plan..."):

            class MarketingAgentSystem:
                def __init__(self, website_url):
                    self.website_url = website_url
                    self.brand_data = {}
                    self.google_ads_agent = GoogleAdsAgent()
                    self.social_media_agent = SocialMediaAgent()
                    self.media_content_agent = MediaContentAgent()
                    self.campaign_ideas_agent = CampaignIdeasAgent()
                    self.competitor_analysis_agent = CompetitorAnalysisAgent()

                def analyze_website(self):
                    self.brand_data = self.extract_brand_info(self.website_url)

                def extract_brand_info(self, url):
                    try:
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        text = soup.get_text()
                        gpt_summary = self.summarize_with_gpt(text)
                        return gpt_summary
                    except Exception as e:
                        return {"error": str(e)}

                def summarize_with_gpt(self, text):
                    prompt = f"""
                    Analyze the following website content and extract the following:
                    - Brand name
                    - Industry type
                    - List of products or services
                    - Brand tone and style
                    - Relevant SEO keywords

                    Website Content:
                    {text[:4000]}
                    """
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a digital marketing analyst."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    return response["choices"][0]["message"]["content"]

                def run_agents_analysis(self):
                    self.google_ads_agent.analyze(self.brand_data)
                    self.social_media_agent.analyze(self.brand_data)
                    self.media_content_agent.analyze(self.brand_data)
                    self.campaign_ideas_agent.analyze(self.brand_data)
                    self.competitor_analysis_agent.analyze(self.brand_data)

                def should_work_with_brand(self):
                    scores = [
                        self.google_ads_agent.score,
                        self.social_media_agent.score,
                        self.media_content_agent.score,
                        self.campaign_ideas_agent.score,
                        self.competitor_analysis_agent.score
                    ]
                    return sum(scores) / len(scores) > 7

                def generate_work_plan(self):
                    return {
                        "google_ads": self.google_ads_agent.generate_plan(),
                        "social_media": self.social_media_agent.generate_plan(),
                        "media_content": self.media_content_agent.generate_plan(),
                        "campaigns": self.campaign_ideas_agent.generate_plan(),
                        "competitors": self.competitor_analysis_agent.generate_plan(),
                    }

            class GoogleAdsAgent:
                def analyze(self, brand_data):
                    self.score = 8
                def generate_plan(self):
                    return ["Create Google Ads campaign with branded and generic keywords"]

            class SocialMediaAgent:
                def analyze(self, brand_data):
                    self.score = 7
                def generate_plan(self):
                    return ["Analyze current social profiles", "Open missing channels"]

            class MediaContentAgent:
                def analyze(self, brand_data):
                    self.score = 6
                def generate_plan(self):
                    return ["Create brand story video", "Reels and product photos"]

            class CampaignIdeasAgent:
                def analyze(self, brand_data):
                    self.score = 9
                def generate_plan(self):
                    return ["Back-to-school campaign", "Limited time promotions"]

            class CompetitorAnalysisAgent:
                def analyze(self, brand_data):
                    self.score = 7.5
                def generate_plan(self):
                    return ["Track competitors", "Identify brand differentiators"]

            system = MarketingAgentSystem(url)
            summary = system.analyze_website()

            if isinstance(summary, dict) and "error" in summary:
                st.error(f"Error: {summary['error']}")
            else:
                st.subheader("🔍 Brand Summary")
                st.text(summary)

                system.run_agents_analysis()
                if system.should_work_with_brand():
                    st.success("✅ This brand is suitable to work with.")
                    st.subheader("📋 Work Plan")
                    work_plan = system.generate_work_plan()
                    for section, tasks in work_plan.items():
                        st.markdown(f"### {section.replace('_', ' ').title()}")
                        for task in tasks:
                            st.markdown(f"- {task}")
                else:
                    st.warning("🚫 This brand is not suitable at this time.")
else:
    st.info("Please enter your OpenAI API key to begin.")
