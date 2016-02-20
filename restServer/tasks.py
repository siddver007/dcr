from __future__ import absolute_import
from celery import shared_task
import sched, time, math
from celery import task



@task
def test(end_time):
    while True:
    	print 'Request is running...'
    return 'OK'