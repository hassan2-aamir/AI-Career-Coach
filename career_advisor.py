import os
from dotenv import load_dotenv
import requests
import gradio as gr
load_dotenv()

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


# Model and project settings
MODEL_ID = "ibm/granite-3-8b-instruct"
API_KEY = WATSONX_API_KEY
URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
PROJECT_ID = WATSONX_PROJECT_ID
AUTH_URL = "https://iam.cloud.ibm.com/identity/token"


def get_access_token(api_key):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(AUTH_URL, headers=headers, data=data, timeout=(10, 30))  # Increased timeout
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

ACCESS_TOKEN = get_access_token(API_KEY)

def generate_career_advice(position_applied, job_description, resume_content):
    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Construct the prompt
    prompt = f"""Analyze the following:
    Position: {position_applied}
    Job Description: {job_description}
    Resume: {resume_content}
    
    Please provide specific suggestions to improve the resume to better match the job requirements."""

    # Request payload
    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1024,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "project_id": PROJECT_ID

    }

    try:
        # Make API request
        response = requests.post(
            URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Handle response
        if response.status_code == 200:
            result = response.json()
            return result.get('results', [{}])[0].get('generated_text', 'No response generated')
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"

# Create Gradio interface
interface = gr.Interface(
    fn=generate_career_advice,
    inputs=[
        gr.Textbox(label="Position Applied For"),
        gr.Textbox(label="Job Description", lines=10),
        gr.Textbox(label="Resume Content", lines=10)
    ],
    outputs=gr.Textbox(label="Career Advice"),
    title="AI Career Advisor",
    description="Get personalized resume improvement suggestions based on job requirements."
)

# Launch the interface
if __name__ == "__main__":
    interface.launch()