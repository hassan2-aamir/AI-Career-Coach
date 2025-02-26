# AI Career Coach

An AI-powered career coaching application that helps job seekers optimize their job application materials using IBM watsonx AI.

## Overview

This project consists of three main components that assist users in their job search process:

1. **Resume Polisher**: Improves and tailors resumes for specific job positions
2. **Cover Letter Generator**: Creates customized cover letters based on job descriptions and resumes
3. **Career Advisor**: Provides personalized advice by analyzing job descriptions and resume content

## Technologies Used

- **Python**: Core programming language
- **IBM watsonx AI**: Uses the `granite-3-8b-instruct` model for natural language processing
- **Gradio**: Provides intuitive web interfaces for each application component
- **Requests**: Handles API communication with IBM watsonx
- **python-dotenv**: Manages environment variables for secure API key storage

## Getting Started

### Prerequisites

- Python 3.6+
- IBM Cloud account with watsonx API access

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/hassan2-aamir/ai-career-coach.git
    cd ai-career-coach
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Create a `.env` file with your IBM watsonx credentials:
    ```
    WATSONX_API_KEY=your_api_key
    WATSONX_PROJECT_ID=your_project_id
    ```

## Usage

### Resume Polisher
```
python resume_polisher.py
```
Input your position name, resume content, and optional polishing instructions to receive tailored improvements.

### Cover Letter Generator
```
python cover_letter.py
```
Enter company name, position name, job description, and resume content to generate a customized cover letter.

### Career Advisor
```
python career_advisor.py
```
Provide the position applied for, job description, and your resume for specific improvement suggestions.

## Privacy Note

This application processes personal resume information. All data is processed through IBM watsonx and is subject to their privacy policy.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
