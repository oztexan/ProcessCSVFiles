'''Process folders view, very simple'''
import os
import json
import threading
from django.http import JsonResponse
from django.shortcuts import render
import process_files
from .poll import NewFiles

WATCH_FOLDER = os.path.abspath(os.path.dirname(__name__)) + '/file_bucket'
POLL_FREQUENCY = 3

POLL = NewFiles()

def index(request):
    return render(request, 'index.html', locals())

def startThreadTask(request):
    t = threading.Thread(target=longTask)
    t.setDaemon(True)
    t.start()
    return JsonResponse({'status':'success'})

def checkThreadTask(request):
    # TODO Want to see full list of processed files
    # and in another pane, list of non-replaced trades
    return JsonResponse({
        'files' : json.dumps(POLL.get_processed_files()),
        'trades' : json.dumps(POLL.get_active_trades())
    })
    #return JsonResponse({'trades' : json.dumps(POLL.get_active_trades())})

def stopThreadTask(request):
    POLL.stop()
    return JsonResponse({'status':"stopped"})

def longTask():
    POLL.watch_folder(WATCH_FOLDER, POLL_FREQUENCY)
