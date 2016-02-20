from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from celery.exceptions import TaskRevokedError
from celery import current_task
from celery.result import ResultBase, AsyncResult, TimeoutError
from celery.task.control import revoke, inspect
from tasks import test
import urllib2 , datetime



def startRequest(req):
	if 'connId' in req.GET.keys() and 'timeOut' in req.GET.keys() and len(req.GET) == 2:
		
		flag = True
		i = inspect()
		hostname = str(i.active().keys()[0])	
		for conn in i.active()[hostname]:
			if req.GET['connId'] == str(conn['id']):
				flag = False
				break

		if flag == True:		
			try:
				currentTimeStamp = datetime.datetime.now()
				endingTimeStamp = currentTimeStamp + datetime.timedelta(seconds = int(req.GET['timeOut']))
				res = test.apply_async(args = [str(endingTimeStamp)] , task_id = req.GET['connId'])
				try:
					res.get(timeout = int(req.GET['timeOut']))
					return JsonResponse({'status' : 'OK'})
				except TimeoutError:
					revoke(res.id, terminate=True)
					return JsonResponse({'status' : 'OK'})	
			except Exception:
					return JsonResponse({'Exception' : 'The request was either hard killed or was already processed'})	
		
		else:
			return JsonResponse({'Exception' : 'Request is already running'})

	else:
		return JsonResponse({'Exception' : 'Invalid API call'})


def killRequest(req):
	if req.method == 'GET':
		pid = req.GET['connId']
	elif req.method == 'PUT':
		data = json.loads(req.body)
		pid = str(data['connId'])
	
	flag = True
	i = inspect()
	hostname = str(i.active().keys()[0])	
	for conn in i.active()[hostname]:
		if pid == str(conn['id']):
			flag = False
			break

			
	reqResult = AsyncResult(pid)
	if reqResult.result != 'OK' and str(reqResult.result) != 'revoked' and str(reqResult.result) != 'terminated':
		if flag == False:
			revoke(pid, terminate=True)
			return JsonResponse({'status' : 'Killed'})
		else:	
			return JsonResponse({'Exception' : 'Invalid connectionID : ' + pid})
	else:
		if reqResult.result == 'OK':
			return JsonResponse({'Exception' : 'Task was already completed'})
		else:
			return JsonResponse({'Exception' : 'Task was already revoked'})		
				
		

def timeRemaining(req):
	i = inspect()
	hostname = str(i.active().keys()[0])
	reqDelta = {}
	for conn in i.active()[hostname]:
		endingTimeStampString = str(conn['args']).replace('[','').replace(']','').replace('u','').replace('\'','')
		print str(conn['args'][0])
		print endingTimeStampString
		endingTimeStamp = datetime.datetime.strptime(endingTimeStampString, '%Y-%m-%d %H:%M:%S.%f')
		print endingTimeStamp
		reqDelta[str(conn['id'])] = str(int((endingTimeStamp - datetime.datetime.now()).total_seconds()))
	return JsonResponse(reqDelta)


def activeRequests(req):
	i = inspect()
	return JsonResponse(i.active())


