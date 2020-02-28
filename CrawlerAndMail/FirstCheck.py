import signal
import smtplib
from CrawlerAndMail import ConfigReader
from CrawlerAndMail.Colors import colors
import requests


# checks if you can connect to the internet
def check_internet_connection():
    try:
        requests.get("https://www.google.de")

    except requests.exceptions.ConnectionError:
        return False

    return True


# checks if we get the 200 respond code
def check_response_code():
    code = requests.get(ConfigReader.url)
    if "200" in str(code):
        return True

    else:
        return False


def check_logindata():
    with requests.session() as s:
        login_data = {"username": ConfigReader.elternportal_email,
                      "password": ConfigReader.elternportal_password}

        r = s.get(ConfigReader.url)
        r = s.post(ConfigReader.post_url, data=login_data)
        if "Benutzername/Passwort inkorrekt." in r.text:
            return False

        else:
            return True


def check_email():
    def port_error(signum, frame):
        raise Exception("Wrong Port")

    signal.signal(signal.SIGALRM, port_error)
    signal.alarm(5)

    try:
        server = smtplib.SMTP(ConfigReader.smtp_server, ConfigReader.smtp_server_port)
        server.starttls()
        server.login(ConfigReader.bot_email, ConfigReader.bot_password)

    except Exception as e:
        return False

    finally:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)

    return True


def do_the_check():
    # dictionary to store the booleans
    checks = {}

    print("Checking for {start}Connection Errors{end} and for possible {start}wrong login data{end}...".format(start=colors.OKGREEN, end=colors.ENDC))
    print("")

    checks["Internet Connection:\t\t\t\t"] = check_internet_connection()

    # If there is no connection every test will fail so it just returns False and informs the user
    if check_internet_connection() is False:
        print(list(checks.keys())[0] + colors.FAIL + "Error" + colors.ENDC)
        print("")
        print("{font}{underline}{color}Due to no internet connection all the other tests will come out wrong.{end}".format(font=colors.BOLD, underline=colors.UNDERLINE, color=colors.FAIL, end=colors.ENDC))
        print("{font}{color}{underline}So fix your Internet Connection!{end}".format(font=colors.BOLD, underline=colors.UNDERLINE, color=colors.FAIL, end=colors.ENDC))
        return False

    checks["Connection to Elternportal Website:\t"] = check_response_code()
    checks["Login Data for Elternportal:\t\t"] = check_logindata()
    checks["Login Data for Bot email service:\t"] = check_email()

    for check in checks:
        print(check + str(checks[check]).replace("True", colors.OKBLUE + "Working" + colors.ENDC).replace("False", colors.FAIL + "Error" + colors.ENDC))

    if False in checks.values():
        return False

    else:
        return True
