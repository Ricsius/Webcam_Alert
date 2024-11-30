import os
import smtplib
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS = os.getenv("MY_MAIL")
PASSWORD = os.getenv("PEMAIL_PASSWORD")

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    with open(image_path, "rb") as file:
        content = file.read()
    
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL_ADDRESS, PASSWORD)
    gmail.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email_message.as_string())
    gmail.quit()