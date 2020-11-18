from datetime import datetime


class Logger:
    LOG_NAME = 'controller.log'

    @staticmethod
    def add_log(message):
        output = "\n{}\t{}".format(str(datetime.now()), message)
        with open(Logger.LOG_NAME, 'a') as log_file:
            log_file.writelines(output)
