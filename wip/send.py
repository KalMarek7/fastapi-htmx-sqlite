from sqlite3 import Connection, Row
from email.mime.text import MIMEText
import smtplib
from database import date_filtered_items
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.job import Job


def email_notification(days: int, email: dict) -> str:
    return build_message(days, email)
    # send_email(email)


def build_message(days: int, email: dict) -> str:
    connection = Connection("./database/food.db")
    connection.row_factory = Row

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


def start_scheduler(scheduler: BackgroundScheduler, days: int, time: str, email: dict) -> Job:
    # Specify the start hour (24-hour format)
    start_hour = int(time.split(":")[0])
    start_minute = int(time.split(":")[1])
    print(start_hour, start_minute)

    # Add a job that runs daily at the specified hour and minute
    job = scheduler.add_job(
        email_notification,
        CronTrigger(hour=start_hour, minute=start_minute),
        kwargs={"days": days, "email": email}
    )
    scheduler.print_jobs()
    scheduler.start()
    scheduler.print_jobs()
    return job


def format_job(job: Job) -> dict:
    return {
        "id": job.id,
        "next_run_time": str(job.next_run_time),
        "trigger": str(job.trigger)
    }
