# Class that handles creating a log file for each game
class Log:
    def __init__(self):
        self._log = ""

    def write_line(self, line):
        self._log += line + "\n"

    def create_log(self):
        f = open("Logs/log.txt", "a")
        f.write(self._log)
        f.write("----------------------------------------\n")
        f.close()