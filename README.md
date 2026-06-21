# AI Threat Map

A tool that helps you find security threats in applications that use LLMs.

## What's the problem?

When you build an app with an LLM like Claude, there are security risks specific to LLMs — like prompt injection, data leaks, hallucinations. Existing threat modeling tools don't focus on these. So I built this.

## How does it work?

You tell it about your app — what it does, what LLM it uses, what features it has, what data it processes. It generates a threat model showing what could go wrong and how to fix it.

## What it does

- Creates threat models using STRIDE framework
- Identifies LLM-specific risks: prompt injection, data leakage, hallucinations, training data poisoning
- Uses Claude API to generate the threats
- Simple web form to fill out
- Open source

## Tech

- Backend: Python, FastAPI, Claude API
- Frontend: React, JavaScript

## Setup

1. Clone:
```bash
git clone https://github.com/TheAlchemistSec/ai-threat-map.git
cd ai-threat-map
```

2. Backend:
```bash
cd backend
pip3 install -r requirements.txt
echo "ANTHROPIC_API_KEY=your-api-key" > .env
python3 -m uvicorn main:app --reload
```

3. Frontend (new terminal):
```bash
cd frontend
npm install
npm start
```

4. Open `http://localhost:3000` and fill out the form

## Example

Input your app details:
- App Name: Customer Support Chatbot
- LLM: Claude
- Features: File uploads, web search
- Data: Customer emails, company docs

Get back a threat report showing risks and how to fix them.

## Next steps

- Add real vulnerability scanning
- Support more LLMs
- Better visualizations

## License

MIT
