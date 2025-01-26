# utils/email.py
import requests
import os

def send_email(subject, recipients, body, sender=None):
    try:
        api_key = os.getenv("MAILJET_API_KEY")
        api_secret = os.getenv("MAILJET_API_SECRET")
        sender_email = sender or os.getenv("MAILJET_SENDER_EMAIL")

        url = "https://api.mailjet.com/v3.1/send"
        headers = {"Content-Type": "application/json"}
        payload = {
            "Messages": [
                {
                    "From": {"Email": sender_email, "Name": "personalLifeorganizer"},
                    "To": [{"Email": email} for email in recipients],
                    "Subject": subject,
                    "TextPart": body,
                }
            ]
        }

        response = requests.post(url, auth=(api_key, api_secret), json=payload, headers=headers)
        if response.status_code == 200:
            return {"success": True, "message": "Email sent successfully."}
        else:
            return {"success": False, "message": response.text}
    except Exception as e:
        return {"success": False, "message": str(e)}
