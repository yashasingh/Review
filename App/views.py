from django.http import HttpResponse
from django.shortcuts import render
import json
import requests

def main(request):
    if(request.method=='POST'):
        usr = request.POST['username']  #Here, we get the username fetched from html page
        usr = usr.replace("&","")
        URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&ucuser="
        URL = URL + usr
        r = requests.get(URL)  #Recieved data in json-format
        if(r.status_code != 200):
            return(render(request,'App/index.html',{"error":'HTTP response ' + str(r.status_code)}))
        else:
            lst = json.loads(r.text)
            try:    
                if(lst['error']):
                    return(render(request,'App/index.html',{"error":lst['error']['info']}))
            except:   
                sub_lst = lst['query']['usercontribs'] #Contribution data extracted
                if(len(sub_lst)==0):
                    return(render(request,'App/index.html',{"error":"No Edits found"}))
            return(render(request,'App/index.html',{"contribution":sub_lst, "username":usr}))  #Here I send contribution for display on index.html page
    else:
        return(render(request,'App/index.html',{}))