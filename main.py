# Import required packages
from CrawlerAndMail import WebCrawler, SendMail, ConfigReader, FirstCheck
from CrawlerAndMail.WriteLog import write_log
import time


class Application:
    def __init__(self):
        # Previous tables to remember the day before
        self.prevtable1 = ""
        self.prevtable2 = ""
        # Tables into which the crawler stores the data from the internet
        self.table1 = ""
        self.table2 = ""
        # When the program should be terminated
        self.terminate_app = False

    def fetch_tables(self):
        # fetches the website
        write_log("Checking for news...")

        fetch = WebCrawler.f.get_table_content()
        self.table1 = str(fetch[0])
        self.table2 = str(fetch[1])
        return self.table1, self.table2

    def check_the_information(self):
        # checks if the email should be send. returns true if the information should be send

        # if this is not here fetch_tables would never be ran
        table1, table2 = self.fetch_tables()

        if "Keine Vertretungen" not in table1 or "Keine Vertretungen" not in table2:
            if (self.prevtable2 == table1 and "Keine Vertretungen" in table2) or (
                    table1 == self.prevtable1 and table2 == self.prevtable2):
                return False
            return True

        return False

    def update_prevtables(self):
        # Remembers the previous tables on the website so that it doesn't send
        # the same information twice
        self.prevtable1 = self.table1
        self.prevtable2 = self.table2

    def sleep_between_check(self):
        time.sleep(ConfigReader.wait_between_check)

    def sleep_between_error(self):
        time.sleep(ConfigReader.wait_between_error_retry)

    def exception_keyboard_interrupt(self):
        # what to do when the app is stopped
        write_log("Application Terminated.")
        print("")
        print("{start}Application Terminated.{end}".format(start=FirstCheck.colors.WARNING, end=FirstCheck.colors.ENDC))
        self.terminate_app = True

    def exception_everything_else(self, exception):
        # if an error occures its being written down in the log
        write_log("An Error occurred:", exception,
                  "The program will precede in " + str(ConfigReader.wait_between_error_retry) + " seconds.")

        try:
            self.sleep_between_error()
        except KeyboardInterrupt:
            self.exception_keyboard_interrupt()

    def start_loop(self):
        while True:
            if self.check_the_information():
                write_log("Change Detected.", "Preceding to send emails.")
                SendMail.send_mail()
                self.update_prevtables()

            self.sleep_between_check()

    def run_application(self):
        try:
            self.start_loop()

        except KeyboardInterrupt:
            self.exception_keyboard_interrupt()
            # So that self.run_application() isn't run afterwards
            return None

        except Exception as e:
            self.exception_everything_else(e)
            if self.terminate_app is True:
                return None
            write_log("The program is preceding now.")

        self.run_application()

    def info_text(self):
        write_log("Application Started.")

        print("{start}Application Started.{end}".format(start=FirstCheck.colors.WARNING, end=FirstCheck.colors.ENDC))
        print("Remember to check the log! -> " + ConfigReader.log_path)
        print("To Exit Press: ⌃C")


if __name__ == "__main__":
    if FirstCheck.do_the_check():
        print("")
        app = Application()
        app.info_text()
        app.run_application()
