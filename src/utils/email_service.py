"""
Automated Email Notification Service for Critical System Alerts.
Uses SMTP and background tasks to dispatch HTML formatted emails to multiple recipients.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any, List
from src.config.config import (
    SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, RECIPIENT_EMAILS
)
from src.utils.logger import logger

def build_alert_email_html(alert: Dict[str, Any], prediction_value: float = None) -> str:
    """
    Constructs an HTML template for critical energy alert emails.
    """
    pred_str = f"{prediction_value:.2f} kWh" if prediction_value is not None else "N/A"
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; background: #ffffff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            .header {{ background-color: #FF4B4B; color: #ffffff; padding: 15px; border-radius: 6px 6px 0 0; text-align: center; }}
            .content {{ padding: 20px 0; font-size: 15px; color: #333333; line-height: 1.6; }}
            .field {{ font-weight: bold; color: #111111; }}
            .action-box {{ background-color: #fff3f3; border-left: 4px solid #FF4B4B; padding: 12px; margin: 15px 0; border-radius: 4px; }}
            .footer {{ font-size: 12px; color: #888888; text-align: center; border-top: 1px solid #eeeeee; padding-top: 15px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🚨 CRITICAL ENERGY ALERT</h2>
            </div>
            <div class="content">
                <p><span class="field">Building:</span> {alert.get('building', 'Campus Wide')}</p>
                <p><span class="field">Severity:</span> <span style="color:#FF4B4B; font-weight:bold;">{alert.get('severity', 'CRITICAL')}</span></p>
                <p><span class="field">Category:</span> {alert.get('category', 'System Alert')}</p>
                <p><span class="field">Prediction Reading:</span> {pred_str}</p>
                <p><span class="field">Timestamp:</span> {alert.get('timestamp', 'N/A')}</p>
                <p><span class="field">Message:</span> {alert.get('message', '')}</p>
                
                <div class="action-box">
                    <span class="field" style="color:#FF4B4B;">Recommended Action:</span><br/>
                    {alert.get('recommended_action', 'Inspect system immediately.')}
                </div>
            </div>
            <div class="footer">
                Campus Energy Prediction & Optimization System • Automated Alert Service
            </div>
        </div>
    </body>
    </html>
    """

def send_critical_alert_email(alert: Dict[str, Any], prediction_value: float = None, recipients: List[str] = None):
    """
    Sends email notification for Critical alerts via SMTP.
    Safely logs and handles all SMTP exceptions.
    """
    if alert.get("severity") != "Critical":
        return

    recipients_to_send = recipients or RECIPIENT_EMAILS
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        logger.warning(
            f"SMTP credentials not configured in .env. Email dispatch simulated for alert in {alert.get('building')}."
        )
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚨 CRITICAL ALERT: {alert.get('category')} in {alert.get('building')}"
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(recipients_to_send)

        html_body = build_alert_email_html(alert, prediction_value)
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipients_to_send, msg.as_string())
        
        logger.info(f"Critical alert email successfully dispatched to {recipients_to_send}.")
    except Exception as e:
        logger.error(f"Failed to send critical alert email: {e}")
