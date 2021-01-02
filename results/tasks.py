from celery import shared_task
import time
from celery_progress.backend import ProgressRecorder


@shared_task(bind=True)
def do_work(self,list_of_work):
    progress_recorder = ProgressRecorder(self)
    for i in range(list_of_work):
        time.sleep(1)
        print(i)
        
        progress_recorder.set_progress(i+1,list_of_work)
    return 'work is complete'