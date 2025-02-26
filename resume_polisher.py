# Import necessary packages
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
    response = requests.post(AUTH_URL, headers=headers, data=data, timeout=(10, 30))
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

ACCESS_TOKEN = get_access_token(API_KEY)

# Function to polish the resume using the model
def polish_resume(position_name, resume_content, polish_prompt=""):
    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Check if polish_prompt is provided and adjust the combined_prompt accordingly
    if polish_prompt and polish_prompt.strip():
        prompt = f"Given the resume content: '{resume_content}', polish it based on the following instructions: {polish_prompt} for the {position_name} position."
    else:
        prompt = f"Suggest improvements for the following resume content: '{resume_content}' to better align with the requirements and expectations of a {position_name} position. Return the polished version, highlighting necessary adjustments for clarity, relevance, and impact in relation to the targeted role."
    
    # Request payload
    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1024,
            "min_new_tokens": 0,
            "temperature": 0.7,
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

# Create Gradio interface for the resume polish application
resume_polish_application = gr.Interface(
    fn=polish_resume,
    inputs=[
        gr.Textbox(label="Position Name", placeholder="Enter the name of the position..."),
        gr.Textbox(label="Resume Content", placeholder="Paste your resume content here...", lines=20),
        gr.Textbox(label="Polish Instruction (Optional)", placeholder="Enter specific instructions or areas for improvement (optional)...", lines=2),
    ],
    outputs=gr.Textbox(label="Polished Content"),
    title="Resume Polish Application",
    description="This application helps you polish your resume. Enter the position you want to apply, your resume content, and specific instructions or areas for improvement (optional), then get a polished version of your content."
)

# Launch the application
if __name__ == "__main__":
    resume_polish_application.launch()