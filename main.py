
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

GPT_MODEL = "gpt-4-1106-preview"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JobProposalData(BaseModel):
    job_title: str
    company_name: str
    job_description: str
    your_name: str
    your_contact: str


gpt_msg = """
[Job Title]
- {job_title}

[Company Name]
- {company_name}

[Job Description]
- {job_description}

[Your Name]
- {your_name}

[Your Contact]
- {your_contact}

[Personalized Message]
- [Craft a personalized message expressing your interest in the position and why you believe you are a strong fit. Highlight relevant skills and experiences.]

[Closing]
- [Conclude the proposal with a polite closing statement expressing your eagerness to discuss your application further.]
"""


def chat_completion_request(messages, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY
    }
    json_data = {"model": model, "messages": messages}
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=json_data,
    )
    return response.json()


def generate_openai_messages(proposal_data: JobProposalData):
    system_str = """
    You are an AI-powered job application assistant, crafting personalized job proposals for various positions. Your goal is to create compelling and unique proposals tailored to the specific job details provided.
    """

    messages = [
        {"role": "system", "content": system_str},
        {"role": "system", "content": gpt_msg.format(
            job_title=proposal_data.job_title,
            company_name=proposal_data.company_name,
            job_description=proposal_data.job_description,
            your_name=proposal_data.your_name,
            your_contact=proposal_data.your_contact,
        )},
    ]

    return messages


@app.post("/generate_proposal")
async def generate_proposal(proposal_data: JobProposalData):
    messages = generate_openai_messages(proposal_data)
    response = chat_completion_request(messages)

    summary = None
    try:
        summary = response["choices"][0]["message"]["content"]
    except:
        summary = response["message"]["content"]

    return {"response": summary}


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)