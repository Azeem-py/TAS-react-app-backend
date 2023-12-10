import smtplib
from email.mime.text import MIMEText

from .email_data import password,email

def send_otp_email(to_email, otp):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = email
    SMTP_PASSWORD = password

    # Replace with your own email details
    FROM_EMAIL = 'bljazeem@gmail.com'
    TO_EMAIL = to_email
    SUBJECT = 'Your OTP'
    OTP_MESSAGE = 'Your OTP is: ' + str(otp)

    # Create a MIME message object
    message = MIMEText(OTP_MESSAGE)
    message['From'] = FROM_EMAIL
    message['To'] = TO_EMAIL
    message['Subject'] = SUBJECT

    # Send the email
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
    smtp.sendmail(FROM_EMAIL, [TO_EMAIL], message.as_string())
    smtp.quit()
    

# send_otp_email('bljazeem@gmail.com', '12345555')