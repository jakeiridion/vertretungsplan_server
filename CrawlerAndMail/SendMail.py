# Import required packages
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from CrawlerAndMail import WebCrawler, ConfigReader

# Use stop variable to break the programm ones an error occurs in main file
stop = 0


# Sends mail to everyone in the email_list
def send_mail():
    # make stop global so that it can be changed and set stop to 0
    global stop

    stop = 0
    html = WebCrawler.f.get_entire_table()
    msg = MIMEMultipart('alternative')

    with open(ConfigReader.email_list_path) as elist:
        for email in elist:
            succes = 0
            # Continue if its a comment
            if email[0] == "#" or email == "\n":
                continue

            msg["From"] = ConfigReader.bot_email
            msg["To"] = email
            msg["Subject"] = "Vertretungsplan Info. " + WebCrawler.stand

            part = MIMEText(html, 'html')
            msg.attach(part)

            # Special Error handling so that the server can be quit
            try:
                server = smtplib.SMTP(ConfigReader.smtp_server, ConfigReader.smtp_server_port)
                server.starttls()
                server.login(ConfigReader.bot_email, ConfigReader.bot_password)
                server.sendmail(ConfigReader.bot_email, email, msg.as_string())

            except Exception as e:
                # Write Error in log files
                with open(ConfigReader.log_path, "a") as log:
                    log.write(ConfigReader.get_date() + ":\n")
                    log.write("-- Email Error --\n")
                    log.write(str(e) + "\n")
                    log.write("\n")

                # Error occurred:
                succes = 1

            if succes == 0:
                with open(ConfigReader.log_path, "a") as log:
                    log.write(ConfigReader.get_date() + ":\n")
                    log.write("Email successfully send to: " + email + "\n")
                    log.write("\n")
