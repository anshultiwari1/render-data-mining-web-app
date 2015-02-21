# -*- coding: utf-8 -*-
"""
StereoD.
Author  : Anshul Tiwari
Date    : Jan 21, 2015

Description : This holds all the rpc.
"""
import datetime
from datetime import datetime, timedelta, date
import xmlrpclib
from models import *
import urllib2

from SimpleXMLRPCServer             import SimpleXMLRPCDispatcher

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCDispatcher

from django.contrib.auth.models     import User
from django.contrib.auth.models     import Group
from django.core.mail               import send_mail
from django.db.models               import Q
from django.http                    import HttpResponse
from django.views.decorators.csrf 	import csrf_exempt
from django.core.files.base import ContentFile
import jsonrpclib
import json
import sys
import os
from ast import literal_eval

sys.path.append("/home/anshul/dev/python/Tractor-2.0/lib/python2.7/site-packages/")
import tractor.api.query as tq

dispatcherJson = SimpleJSONRPCDispatcher(encoding=None)

# enable intospection, then map it to a different method, the system.listMethods call gets overwritten later
dispatcherJson.register_introspection_functions()

# Set true to log every rpc call to sentry
LOG_RPC = False

@csrf_exempt
def jsonrpc_handler(request):
  if len(request.POST):
    response = HttpResponse(mimetype="application/json")
    response.write(dispatcherJson._marshaled_dispatch(request.raw_post_data))
  else:
    return HttpResponse("No POST data, this url is for rpc calls only.")
  response['Content-length'] = str(len(response.content))
  return response


def setClientServer(server):
  print server
  tq.closeEngineClient()
  #tq.setEngineClientParam(hostname="{0}".format(server), user="anshul", port=1503, debug=True)
  tq.setEngineClientParam(hostname="{0}".format(server), port=1503, debug=True)
  return "success"


def getShotList(info):
  #jobslist = {'title': 'seq_scn_sho_ver', 'owner': 'me', 'range': '1001-1201', 'time': '00:00:00'}
  #jobslist = tq.jobs("done and stoptime >-1d", columns=["title","owner","jid","numdone","stoptime"], sortby=["title"])
  print info
  if info["user"] == "":
    if info["seq"] == "": # default case
      jobslist = tq.jobs("done and stoptime >-1d", columns=["title","owner","jid","numdone","stoptime"], sortby=["title"])
      print "default"
    else:
      if info["scn"] == "":
	jobslist = tq.jobs("title like seq{0}_ and done and stoptime >-1d".format(info["seq"]), columns=["title","owner","jid","numdone","stoptime"], sortby=["title"])
	print "only seq"
      else:
	if info["shot"] == "":
	  jobslist = tq.jobs("title like seq{0}_scn{1}_ and done and stoptime >-1d".format(info["seq"], info["scn"]), columns=["title","owner","jid","numdone","stoptime"], sortby=["title"])
	  print "seq and scn"
	else:
	  jobslist = tq.jobs("title like seq{1}_scn{2}_sh{3} and done and stoptime >-1d".format(info["seq"], info["scn"], info["shot"]), columns=["title","owner","jid","numdone","stoptime"], sortby=["title"])
	  print "seq, scn and shot"
  else:
    if info["seq"] == "":
      jobslist = tq.jobs("owner={0} and done and stoptime >-1d".format(info["user"]), columns=["title","owner","jid","numdone","stoptime"], sortby=["title"])
      print "only user"
    else:
      if info["scn"] == "":
	jobslist = tq.jobs("owner={0} and title like seq{1}_ and done and stoptime >-1d".format(info["user"], info["seq"]), columns=["title","owner","jid","numdone","stoptime"], sortby=["title"])
	print "only user and seq"
      else:
	if info["shot"] == "":
	  jobslist = tq.jobs("owner={0} and title like seq{1}_scn{2}_ and done and stoptime >-1d".format(info["user"], info["seq"], info["scn"]), columns=["title","owner","jid","numdone","stoptime"], sortby=["title"])
	  print "user, seq and scn"
	else:
	  jobslist = tq.jobs("owner={0} and title like seq{1}_scn{2}_sh{3} and done and stoptime >-1d".format(info["user"], info["seq"], info["scn"], info["shot"]), columns=["title","owner","jid","numdone","stoptime"], sortby=["title"])
	  print "user, seq, scn and shot"

  return jobslist


def getShotTime(jid):
  #cmd = "$(pwd)/rpc/getJobTime.sh"
  #tlist = os.system(cmd)
  s = timedelta(seconds=0)
  for l in tlist:
    l = l["elapsedreal"]
    s+=timedelta(seconds=int(l))
    '''
    c = l.split(':')
    if len(c) < 2:
      c.insert(0,0)
    s+=int(c[0])*3600+int(c[1])*60+int(c[2])
  mi,se=divmod(s,60)
  hr,mi=divmod(mi,60)
  totTime, avgtime = (hr,mi,se)'''
  totTime, avgtime = (str(s),str(s/tlen))
  return (totTime, avgtime)


def getFrameList(jid):
  job = tq.jobs("jid={0}".format(jid), columns=["title","owner","jid","numdone"])[0]
  title, owner, numdone = job["title"].lower(), job["owner"], job["numdone"]

  #taskslist = {'tid': 'tid', 'time': '00:00:00'}
  taskslist = tq.tasks("jid={0}".format(jid), columns=["tid","title"], sortby=["tid"])
  invocslist = tq.invocations("jid={0} and current=True".format(jid), columns=["tid","elapsedreal"], sortby=["tid"])
  if len(invocslist) > 1:	tlen = job["numdone"]-1
  else:		tlen = job["numdone"]
  if len(taskslist) > 1 and "sim" not in title: 	taskslist = taskslist[1:]


  time_spent = timedelta(seconds=0)
  for frame,task in zip(invocslist,taskslist):
    time_task = timedelta(seconds=int(frame["elapsedreal"]))
    frame["elapsedreal"] = str(time_task)
    time_spent+= time_task
    if "Processing" in task["title"]:
	frame["frame"] = task["title"].split(' ')[1].split('-')[0]
    else:	frame["frame"] = task["title"]
  totTime = str(time_spent)
  avgTime = str(time_spent/tlen - timedelta(microseconds=(time_spent/tlen).microseconds))

  #cmd = "$(pwd)/rpc/getAllTasks.sh"
  #tlist = os.system(cmd)
  return invocslist, totTime, avgTime, title, owner, numdone


def getAllJobsTime(info):
  #print info
  jobs = tq.jobs("done and and owner={0} and title like seq{1}_scn{2}_sh{3}".format(info["user"], info["seq"], info["scn"], info["shot"]), columns=["title","owner","jid","numdone"], archive=True)

  if len(jobs):
    time_spent = timedelta(seconds=0)
    totalFrames = 0
    for j in jobs:
      tasks = tq.invocations("jid={0} and current=True".format(j["jid"]), columns=["tid","elapsedreal"], sortby=["tid"], archive=True)
      totalFrames += j["numdone"]-1
      for t in tasks:
	time_task = timedelta(seconds=int(t["elapsedreal"]))
	time_spent+= time_task
    totTime = str(time_spent)
    avgTime = str(time_spent/totalFrames - timedelta(microseconds=(time_spent/totalFrames).microseconds))

  else:
    totTime = avgTime = "NA" #str(timedelta(seconds=0))
    totalFrames = len(jobs)
  return totTime, avgTime, totalFrames, len(jobs)


def frameDetails():
  task = {'jobId': '999', 'tId': '1001', 'rTime' : '00:00:00'}
  return task


def printCSV():
  user = os.getenv('USERNAME')
  csvFile = '/'+user+'/Downloads/render_report.csv'
  f = open(csvFile, 'w+')
  f.write("")
  f.close()
  return "success"


dispatcherJson.register_function(setClientServer,				"setClientServer")
dispatcherJson.register_function(getShotList,					"getShotList")
dispatcherJson.register_function(getShotTime,					"getShotTime")
dispatcherJson.register_function(getFrameList,					"getFrameList")
dispatcherJson.register_function(getAllJobsTime,				"getAllJobsTime")
dispatcherJson.register_function(frameDetails,					"frameDetails")
dispatcherJson.register_function(printCSV,					"printCSV")

