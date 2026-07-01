from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, Field
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class FeedbackPayload(BaseModel):
    name: str = Field(default="", max_length=100)
    email: str = Field(default="", max_length=255)
    rating: int = Field(ge=1, le=5)
    category: str = Field(max_length=50)
    subject: str = Field(max_length=200)
    message: str = Field(max_length=5000)
    browser: str = Field(default="Unknown")
    app_version: str = Field(default="Unknown")

def send_feedback_email(data: FeedbackPayload, client_ip: str):
    # Attempt to use SMTP if configured, else just log it (useful for local dev)
    smtp_server = os.environ.get("SMTP_SERVER", "")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")
    support_email = "support@ilmora.com"

    body = f"""
-----------------------------------------
ILMORA USER FEEDBACK
-----------------------------------------
Name: {data.name or 'Anonymous'}
Email: {data.email or 'Not provided'}
Rating: {data.rating}/5
Category: {data.category}
Subject: {data.subject}

Message:
{data.message}

-----------------------------------------
Metadata:
Timestamp: {datetime.utcnow().isoformat()}Z
Browser: {data.browser}
App Version: {data.app_version}
IP Address: {client_ip}
-----------------------------------------
"""

    if not smtp_server:
        logger.info(f"Feedback received (SMTP not configured). Logging to console:\n{body}")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user or "no-reply@ilmora.com"
        msg['To'] = support_email
        msg['Subject'] = f"[{data.category}] ILMORA Feedback: {data.subject}"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        if smtp_user and smtp_password:
            server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        logger.info("Feedback email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send feedback email: {e}")

# Simple in-memory rate limiting dict (IP -> Timestamp)
# In production, Redis would be better, but this suffices for the requirement
rate_limits = {}
RATE_LIMIT_SECONDS = 60

@router.post("/")
async def submit_feedback(payload: FeedbackPayload, request: Request, background_tasks: BackgroundTasks):
    client_ip = request.client.host if request.client else "unknown"
    
    # Rate Limiting
    now = datetime.utcnow().timestamp()
    if client_ip in rate_limits:
        last_request = rate_limits[client_ip]
        if now - last_request < RATE_LIMIT_SECONDS:
            raise HTTPException(status_code=429, detail="Too many feedback requests. Please wait a moment.")
    rate_limits[client_ip] = now

    # Offload email sending to background task to ensure fast API response
    background_tasks.add_task(send_feedback_email, payload, client_ip)
    
    return {"status": "success", "message": "Feedback submitted successfully."}
