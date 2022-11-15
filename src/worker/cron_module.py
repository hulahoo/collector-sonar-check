from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class CronModule:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def add_job(self, time, func,*args):
        """%H:%M"""
        self.scheduler.add_job(func, 'interval',minutes=time,replace_existing=True,args=args)

    def start(self):
        self.scheduler.print_jobs()
        print('scheduler start')
        self.scheduler.start()
