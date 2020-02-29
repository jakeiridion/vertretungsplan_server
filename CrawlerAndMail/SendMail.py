# Import required packages
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from CrawlerAndMail import WebCrawler, ConfigReader
from CrawlerAndMail.WriteLog import write_log


# Sends mail to everyone in the email_list
def send_mail():
    html = WebCrawler.f.get_entire_table()
    msg = MIMEMultipart('alternative')

    with open(ConfigReader.email_list_path) as elist:
        for email in elist:
            # Continue if it is a comment or no @ is in the 'email' (line)
            if email[0] == "#" or email == "\n" or "@" not in email:
                continue

            msg["From"] = ConfigReader.bot_email
            msg["To"] = email
            msg["Subject"] = "Vertretungsplan Info. " + WebCrawler.date

            part = MIMEText(html, 'html')
            msg.attach(part)

            server = smtplib.SMTP(ConfigReader.smtp_server, ConfigReader.smtp_server_port)
            server.starttls()
            server.login(ConfigReader.bot_email, ConfigReader.bot_password)
            server.sendmail(ConfigReader.bot_email, email, msg.as_string())

            # strip because there is a \n at the end
            write_log("Email successfully send to: " + email.rstrip())
