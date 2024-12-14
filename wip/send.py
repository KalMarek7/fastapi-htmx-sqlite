from email.mime.text import MIMEText
import smtplib


def send_email(email: dict) -> str:
    msg = MIMEText(email["message"], "html")
    msg["Subject"] = email["subject"]
    msg["From"] = email["from_addr"]
    msg["To"] = email["to_addr"]

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email["from_addr"], email["password"])
    try:
        server.sendmail(email["from_addr"], email["to_addr"], msg.as_string())
        print("Email sent successfully")
        return "Email sent successfully"
    except smtplib.SMTPException as e:
        print("Unable to send email")
        print("Error:", e)
        return "Unable to send email. Error: " + str(e)
    finally:
        server.quit()
