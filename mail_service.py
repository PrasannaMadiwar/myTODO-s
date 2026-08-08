import resend
from configuration import Settings

resend.api_key = Settings.RESEND_API_KEY

 

def send_email(to_email:str, subject:str, description:str):
    try:
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": subject,
            "html": description
            })
    except Exception as e:
        print(f"Error sending email: {e}")    
        