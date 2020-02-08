# Import required packages
from CrawlerAndMail import WebCrawler, SendMail, ConfigReader
import time
from datetime import datetime
import os

log_path = os.path.join(os.path.dirname(__file__), "log")
today = str(datetime.now().strftime("%d.%m.%Y - %H:%M:%S"))


# method to be executed at the end
def final_one():
    global today
    print("Application Started.")
    print("Remember to check the log for Error Messages -> " + log_path)
    print("To Exit Press: ⌃C")

    prevtable1 = ""
    prevtable2 = ""
    try:
        while True:
            # get the date
            today = str(datetime.now().strftime("%d.%m.%Y - %H:%M:%S"))

            # write checks in log
            with open(log_path, "a") as log:
                log.write(today + ":\n")
                log.write("Checking for news...\n")
                log.write("\n")

            # Fetches the website
            fetch = WebCrawler.f.get_table_content()
            table1 = str(fetch[0])
            table2 = str(fetch[1])

            # Continues when there is nothing new or if something new just moved up a day
            if "Keine Vertretungen" not in table1 or "Keine Vertretungen" not in table2:
                if (prevtable2 == table1 and "Keine Vertretungen" in table2) or (
                        table1 == prevtable1 and table2 == prevtable2):
                    time.sleep(ConfigReader.wait_between_check)
                    continue

                prevtable1 = table1
                prevtable2 = table2

                # Send the email
                SendMail.send_mail()

                # Break when Error occurred
                if SendMail.stop == 1:
                    break

                time.sleep(ConfigReader.wait_between_check)

            else:
                time.sleep(ConfigReader.wait_between_check)
                continue

    # When terminating the app
    except KeyboardInterrupt:
        print("")
        print("Application terminated")

    # When the login data is wrong
    except IndexError:
        with open(log_path, "a") as log:
            log.write(today + ":\n")
            log.write("-- Connection Error --\n")
            log.write("Couldn't crawl Elternportal" + "\n")
            log.write("\n")
            print("")
            print("Error: Check your Elternportal login data")

    # Everything else
    except Exception as e:
        with open(log_path, "a") as log:
            log.write(today + ":\n")
            log.write("-- Non Email Error --\n")
            log.write(str(e) + "\n")
            log.write("\n")

        time.sleep(ConfigReader.wait_between_error_retry)
        final_one()


if __name__ == "__main__":
    final_one()
