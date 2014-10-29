__author__ = 'eyob'
from django_cron import CronJobBase, Schedule
from Yaas.models import Auction
from datetime import datetime

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'Yaas.my_cron_job'

    def do(self):
        auctions = Auction.objects.order_by('end_date').filter(state_id=1)
        for auction in auctions:
            if auction.end_date < datetime.today():
                auction.state_id = 4