import os
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv
from fastapi import HTTPException
from jinja2 import Template

'''Loading env''' # loading environmental variables
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Onboarding New Admin</title>
        </head>
        <body>
            <h1>Welcome {{ name }} to GIC where men are raised to sit on the throne of God</h1>
            <p>Email: {{ email }}</p>
        </body>
</html>
    """




async def send_email(subject, email_to):
    try:
        msg = MIMEText(html, "html")
        msg["Subject"] = subject
        msg["From"] = my_email
        msg["To"] = email_to

        port = 465  # for SSL

        # connect to the email server 
        server = SMTP_SSL("smtp.gmail.com", port)
        server.login(my_email, my_password)

        # send the email
        server.send_message(msg)
        server.quit()
        return {"message": "Check your email for verification"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    


async def send_password_reset_request_email(subject, email_to, template, context):
    try:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = my_email
        msg["To"] = email_to

        with open(template) as file_:
            template = Template(file_.read())
        body = template.render(context)
    
        msg.attach(MIMEText(body, "html"))

        port = 465  # for SSL

        # connect to the email server 
        server = SMTP_SSL("smtp.gmail.com", port)
        server.login(my_email, my_password)

        # send the email
        server.send_message(msg)
        server.quit()
        return {"message": "Check your email for verification"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)