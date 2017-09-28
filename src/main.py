import os
from datetime import datetime

if __name__ == "__main__":
    try:
        log = open("log.txt", "a")
        log.write("Started bot at " + str(datetime.now()) + "\n")
        log.close()
        os.system("python bot_impl.py >> log.txt 2>&1")
    except IOError as e:
        print("Failed to start logging: " + e.strerror)
        os.system("python bot_impl.py")
