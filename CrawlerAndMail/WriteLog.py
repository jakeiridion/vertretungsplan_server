from CrawlerAndMail.ConfigReader import log_path, get_date


def write_log(*texts):
    with open(log_path, "a") as log:
        log.write(get_date() + ":\n")

        # For every paragraph a new line is written in the log
        for text in texts:
            log.write(str(text) + "\n")

        log.write("\n")
