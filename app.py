# Marketing Agent System with Streamlit Buttons per Agent

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
        with st.spinner("Fetching website content..."):
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                site_text = soup.get_text()
            except Exception as e:
                st.error(f"Failed to retrieve site content: {e}")
                site_text = ""

        def ask_gpt(prompt):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior digital marketing expert."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']

        st.subheader("🤖 Choose which agent to run:")

        if st.button("📢 Google Ads Agent"):
            prompt = f"""You are a Google Ads expert. Analyze the following website content and:
- Identify relevant keywords for ad campaigns
- Propose ad groups and audience segmentation
- Write 2 sample text ads
- Suggest budget allocation strategy

Website Content:
{site_text[:4000]}
"""
            result = ask_gpt(prompt)
            st.text_area("📢 Google Ads Plan", result, height=400)

        if st.button("📝 Creative Content Agent"):
            prompt = f"""You are a creative content strategist. Based on the website content below, generate:
- 3 original post ideas for Instagram or TikTok
- 1 video script idea (30 seconds)
- A catchy slogan related to the brand

Website Content:
{site_text[:4000]}
"""
            result = ask_gpt(prompt)
            st.text_area("📝 Creative Content Plan", result, height=400)

        if st.button("📚 Content Marketing Agent"):
            prompt = f"""You are a content marketing manager. Based on the website below, provide:
- Blog post topic ideas (5)
- 1 sample blog introduction (150 words)
- SEO keyword suggestions
- Suggestions for newsletter or thought leadership distribution

Website Content:
{site_text[:4000]}
"""
            result = ask_gpt(prompt)
            st.text_area("📚 Content Marketing Strategy", result, height=400)

        if st.button("🕵️‍♂️ Competitor Intelligence Agent"):
            prompt = f"""You are a competitor intelligence analyst. Given this website, assume it's a client's brand.
Your task is to:
- Suggest types of competitors they should monitor
- Recommend tools or sources to track competitors
- Propose what weekly insights they should collect
- Output it as a report template

Website Content:
{site_text[:4000]}
"""
            result = ask_gpt(prompt)
            st.text_area("🕵️ Competitor Monitoring Plan", result, height=400)
else:
    st.info("Please enter your OpenAI API key to begin.")
