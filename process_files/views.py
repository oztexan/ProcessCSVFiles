from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import threading
from .models import *
import time
from .poll import *
import process_files
import json

WATCH_FOLDER = os.path.dirname(process_files.__file__) + '/fixtures'
POLL = NewFiles()

def index(request):
    return render(request, 'index.html', locals())

def startThreadTask(request):
    try:
        t = threading.Thread(target=longTask)
        t.setDaemon(True)
        t.start()
        return JsonResponse({'status':'success'})
    except Exception as inst:
        print(inst)
        return JsonResponse({'status':'error' & inst})

def checkThreadTask(request):
    return JsonResponse({'files' : json.dumps(POLL.get_new())})

def stopThreadTask(request):
    POLL.stop()
    return JsonResponse({'status':"stopped"})


def longTask():
    # previously processed is list of files already processed & stored in database
    # with the status = "processed"
    # print('previously processed', ProcessedFiles.objects.all())
    #previously_processed = [pf['filename'] for pf in ProcessedFiles.objects().all()]
    POLL.watch_folder(WATCH_FOLDER, 5)
    # print("Received task",id)
    # time.sleep(3)
    # task = ThreadTask.objects.get(pk=id)
    # task.is_done = True
    # task.save()
    # print("Finishing task",id)
