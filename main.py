# Import required packages
from CrawlerAndMail import WebCrawler, SendMail, ConfigReader, FirstCheck
import time


# method to be executed
def final_one():
    print("{start}Application Started.{end}".format(start=FirstCheck.colors.WARNING, end=FirstCheck.colors.ENDC))
    print("Remember to check the log for Error Messages -> " + ConfigReader.log_path)
    print("To Exit Press: ⌃C")

    prevtable1 = ""
    prevtable2 = ""
    try:
        while True:
            # write checks in log
            with open(ConfigReader.log_path, "a") as log:
                log.write(ConfigReader.get_date() + ":\n")
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

                # Remembers the previous tables on the website so that it doesn't send
                # the same information twice
                prevtable1 = table1
                prevtable2 = table2

                # Sends the email
                SendMail.send_mail()
                time.sleep(ConfigReader.wait_between_check)

            else:
                time.sleep(ConfigReader.wait_between_check)
                continue

    # When terminating the app
    except KeyboardInterrupt:
        print("")
        print("{start}Application Terminated.{end}".format(start=FirstCheck.colors.WARNING, end=FirstCheck.colors.ENDC))

    # Everything else
    except Exception as e:
        with open(ConfigReader.log_path, "a") as log:
            log.write(ConfigReader.get_date() + ":\n")
            log.write("-- Non Email Error --\n")
            log.write(str(e) + "\n")
            log.write("\n")

        time.sleep(ConfigReader.wait_between_error_retry)
        final_one()


if __name__ == "__main__":
    if FirstCheck.do_the_check():
        print("")
        final_one()
