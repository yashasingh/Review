from django.http import HttpResponse
from django.shortcuts import render
import json
import requests

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")    

def main(request):
    if(request.method=='POST'):
        usr = request.POST['username']  #Here, we get the username fetched from html page
        usr = usr.replace("&","%26")
        URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&ucuser="
        URL = URL + usr
        r = requests.get(URL)  #Recieved data in json-format
        if(r.status_code != 200):
            return(render(request,'App/index.html',{"error":'HTTP response ' + str(r.status_code)}))
        else:
            lst = json.loads(r.text)
            try:    
                if(lst['error']):
                    return(render(request,'App/index.html',{"error":'INVALID INPUT'}))
            except:   
                sub_lst = lst['query']['usercontribs'] #Contribution data extracted
                if(len(sub_lst)==0):
                    return(render(request,'App/index.html',{"error":"No Edits found"}))
            return(render(request,'App/index.html',{"contribution":sub_lst, "username":usr}))  #Here I send contribution for display on index.html page
    else:
        return(render(request,'App/index.html',{}))

def main(request):
    if(request.method=='POST'):
        usr = request.POST['username']  #Here, we get the username fetched from html page
        URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&ucuser="
        URL = URL + usr
        r = requests.get(URL)  #Recieved data in json-format
        if(r.status_code != 200):
            return(render(request,'App/index.html',{"error":'HTTP response ' + str(r.status_code)}))
        else:
            lst = json.loads(r.text)
            if(lst['error']):
                return(render(request,'App/index.html',{"error":'INVALID INPUT'}))
            else:   
                sub_lst = lst['query']['usercontribs'] #Contribution data extracted
                if(not sub_list):
                    return(request,'App/index.html',{'error':"No Edits found"})
            return(render(request,'App/index.html',{'contribution':sub_lst, 'username':usr}))  #Here I send contribution for display on index.html page
    else:
        return(render(request,'App/index.html',{}))