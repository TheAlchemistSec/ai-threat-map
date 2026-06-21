import os
from dotenv import load_dotenv
from fastapi import FastAPI
from anthropic import Anthropic
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

client = Anthropic(api_key=api_key)

@app.post("/threat-model")
def generate_threat_model(app_name: str, llm_type: str, features: str, data_types: str):
    prompt = f"""You are an LLM security expert. Generate a STRIDE-based threat model for this AI application.

App Name: {app_name}
LLM Type: {llm_type}
Features: {features}
Data Types: {data_types}

For each STRIDE category (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), identify LLM-specific threats.

Format output as:
THREAT_NAME | SEVERITY (High/Medium/Low) | DESCRIPTION | MITIGATION

Keep it concise and actionable."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return {"threat_model": message.content[0].text}

@app.get("/")
def root():
    return {"message": "AI ThreadMap API is running"}