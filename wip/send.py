from email.mime.text import MIMEText
import smtplib


def send_email(email: dict) -> None:
    """Send an email using the provided arguments."""
    msg = MIMEText(email["message"])
    msg["Subject"] = email["subject"]
    msg["From"] = email["from_addr"]
    msg["To"] = email["to_addr"]

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email["from_addr"], email["password"])
    try:
        server.sendmail(email["from_addr"], email["to_addr"], msg.as_string())
        print("Email sent successfully")
    except smtplib.SMTPException as e:
        print("Error: unable to send email")
        print(e)
    server.quit()


if __name__ == "__main__":
    email = {
        "subject": "Test Email",
        "message": "Hello, this is a test email.",
        "from_addr": "appsandscripts7@gmail.com",
        "to_addr": "marekkal7@gmail.com",
        "password": "nimp qzkw hkjh epta"
    }
    send_email(email)
