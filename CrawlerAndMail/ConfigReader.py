# Import required packages
import configparser
from urllib.parse import urljoin
import os


# import Variables from the settings file
cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.ini")
cfg = configparser.ConfigParser()
cfg.read(cfg_path)

url = cfg.get("Settings", "url")
# Create post and other url:
post_url = urljoin(url, "/includes/project/auth/login.php")
end_url = urljoin(url, "/service/vertretungsplan")

elternportal_email = cfg.get("Settings", "elternportal_email")
elternportal_password = cfg.get("Settings", "elternportal_password")

bot_email = cfg.get("Settings", "bot_email")
bot_password = cfg.get("Settings", "bot_password")
smtp_server = cfg.get("Settings", "smtp_server")
smtp_server_port = int(cfg.get("Settings", "smtp_server_port"))

wait_between_check = int(cfg.get("Settings", "wait_between_check"))
wait_between_error_retry = int(cfg.get("Settings", "wait_between_error_retry"))