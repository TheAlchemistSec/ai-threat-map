import os
from dotenv import load_dotenv
from fastapi import FastAPI
from anthropic import Anthropic
from fastapi.middleware.cors import CORSMiddleware
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from fastapi.responses import StreamingResponse

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
    
    threat_text = message.content[0].text

    # Calculate risk score
    high_count = threat_text.count('High')
    medium_count = threat_text.count('Medium')
    low_count = threat_text.count('Low')

    total_threats = high_count + medium_count + low_count

    # Risk calculation: High=3 points, Medium=2, Low=1
    risk_score = (high_count * 3) + (medium_count * 2) + (low_count * 1)
    max_possible_score = total_threats * 3 if total_threats > 0 else 1
    risk_percentage = int((risk_score / max_possible_score) * 100)

    # Determine risk level
    if risk_percentage >= 70:
        risk_level = "Critical"
    elif risk_percentage >= 50:
        risk_level = "High"
    elif risk_percentage >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "threat_model": threat_text,
        "risk_score": risk_percentage,
        "risk_level": risk_level,
        "threat_breakdown": {
            "high": high_count,
            "medium": medium_count,
            "low": low_count
        }
    }
@app.get("/export-pdf")
def export_pdf(app_name: str, risk_level: str, risk_score: int, threat_model: str):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#000000'),
        spaceAfter=30,
    )
    story.append(Paragraph("AI Threat Map Report", title_style))
    story.append(Spacer(1, 0.2*inch))

    # App Info
    story.append(Paragraph(f"<b>Application:</b> {app_name}", styles['Normal']))
    story.append(Paragraph(f"<b>Risk Level:</b> {risk_level}", styles['Normal']))
    story.append(Paragraph(f"<b>Risk Score:</b> {risk_score}%", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Threats
    story.append(Paragraph("Identified Threats", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    for line in threat_model.split('\n'):
        if line.strip() and '|' in line:
            story.append(Paragraph(line, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))

    doc.build(story)
    buffer.seek(0)
    
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={app_name}_threat_model.pdf"}
    )

@app.get("/")
def root():
    return {"message": "AI Threat Map API is running"}