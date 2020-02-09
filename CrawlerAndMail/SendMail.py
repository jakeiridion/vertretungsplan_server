# Import required packages
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from CrawlerAndMail import WebCrawler, ConfigReader
import time
import main

# Use stop variable to break the programm ones an error occurs in main file
stop = 0


# Sends mail to everyone in the email_list
def send_mail():
    # make stop global so that it can be changed and set stop to 0
    global stop

    stop = 0
    html = WebCrawler.f.get_entire_table()
    msg = MIMEMultipart('alternative')

    with open("email_list") as elist:
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
                with open(main.log_path, "a") as log:
                    log.write(main.get_date() + ":\n")
                    log.write("-- Email Error --\n")
                    log.write(str(e) + "\n")
                    log.write("\n")

                # Error occurred:
                succes = 1

            finally:

                # If the server variable couldnt be created it means that the connection to the email server couldn't be
                # established due to Wrong login data
                try:
                    server.quit()
                except UnboundLocalError:

                    # Write Error in log files
                    with open(main.log_path, "a") as log:
                        log.write(main.get_date() + ":\n")
                        log.write("-- Email Error --\n")
                        log.write("Couldnt Reach Email-Server, Check your Bot Configurations" + "\n")
                        log.write("\n")

                    print("")
                    print("Error: Check your Bot Configurations")
                    stop = 1

                # Wait a half second before sending the next email
                time.sleep(0.5)

            # Writes a successful entry in log files when no  error occurred
            if succes == 0:
                with open(main.log_path, "a") as log:
                    log.write(main.get_date() + ":\n")
                    log.write("Email successfully send to: " + email + "\n")
                    log.write("\n")