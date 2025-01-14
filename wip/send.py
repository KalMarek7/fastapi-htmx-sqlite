from sqlite3 import Connection
from email.mime.text import MIMEText
import smtplib
from database import date_filtered_items


def email_notification(connection: Connection, days: int, email: dict) -> str:
    return build_message(connection, days, email)
    # send_email(email)


def build_message(connection: Connection, days: int, email: dict) -> str:
    items = date_filtered_items(connection, days)
    items_dict = items.model_dump()
    if len(items_dict["items"]) == 0:
        print("No items with specified filter")
        return "No items with specified filter"
    else:
        message = ""
        for item in items_dict["items"]:
            message += f"""
            Name: {item['name']}<br>
            Expiry date: {item['expiry_date']}<br>
            Category: {item['category']}<br>
            Notes: {item['notes']}<br>
            <br><br>
            """

        message = f"Hello. Below you'll find food items about to expire in the next {
            days} days.<br><br>" + message

        return send_email({**email, "message": message})


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
