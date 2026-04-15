import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

sender   = os.getenv("EMAIL_SENDER")
password = os.getenv("EMAIL_PASSWORD")

print(f"Sender: {sender}")
print(f"Password set: {'Yes' if password else 'No'}")

msg = MIMEMultipart()
msg["From"]    = sender
msg["To"]      = sender
msg["Subject"] = "Test from Churn Agent"
msg.attach(MIMEText("This is a test email from your Churn Agent!", "plain"))

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, sender, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f" Error: {e}")