from datetime import datetime
import time
import threading

global f


def print_something():
    print('cron ***************is**************** run')
    f = 0
    while True:
        time.sleep(5)
        f = f+1
        print("2313131232131")
        print(datetime.now())
        if f > 2:
            print_something()


def run_cron_job():
    print('cron ***************is**************** runing')
    job_thread = threading.Thread(target=print_something)
    job_thread.daemon = True
    job_thread.start()
