# Import required packages
from CrawlerAndMail import WebCrawler, SendMail, ConfigReader, FirstCheck
from CrawlerAndMail.WriteLog import write_log
import time


# if the program re runs it self after an error it doesn't forget the prevtables
# they wont be set back to prevtable1 = "" in th method final_one()
# so the program still knows what happend earlier to the tables
prevtable1 = ""
prevtable2 = ""


# method to be executed
def final_one():
    global prevtable1
    global prevtable2

    try:
        while True:
            # write checks in log
            write_log("Checking for news...")

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

                # logging the change
                write_log("Change Detected.", "Preceding to send emails.")

                # Sends the email
                SendMail.send_mail()
                time.sleep(ConfigReader.wait_between_check)

                # Remembers the previous tables on the website so that it doesn't send
                # the same information twice
                prevtable1 = table1
                prevtable2 = table2

            # if there is nothing new it just checks later
            else:
                time.sleep(ConfigReader.wait_between_check)
                continue

    # When terminating the app
    except KeyboardInterrupt:
        write_log("Application Terminated.")

        print("")
        print("{start}Application Terminated.{end}".format(start=FirstCheck.colors.WARNING, end=FirstCheck.colors.ENDC))

    # Everything else
    except Exception as e:
        write_log("An Error occurred:", e,
                  "The program will precede in " + str(ConfigReader.wait_between_error_retry) + " seconds.")

        # if the program is terminated during the error retry timer
        try:
            time.sleep(ConfigReader.wait_between_error_retry)

        except KeyboardInterrupt:
            write_log("Application Terminated.")

            print("")
            print("{start}Application Terminated.{end}".format(start=FirstCheck.colors.WARNING,
                                                               end=FirstCheck.colors.ENDC))

            # So that the final_one() Method isn't run afterwards
            return None

        # if the program isn't terminated the script logs and repeats itself
        write_log("The program is preceding now.")
        final_one()


# The text the user gets when running the app. And also the start will be logged
def info_text():
    write_log("Application Started.")

    print("{start}Application Started.{end}".format(start=FirstCheck.colors.WARNING, end=FirstCheck.colors.ENDC))
    print("Remember to check the log! -> " + ConfigReader.log_path)
    print("To Exit Press: ⌃C")


# The script being run if the check (FirstCheck.do_the_check()) comes out right
if __name__ == "__main__":
    if FirstCheck.do_the_check():
        print("")
        info_text()
        final_one()
