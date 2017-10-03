from django.http import HttpResponse
from django.shortcuts import render
import json
import requests

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")    

def main(request):
	if(request.method=='POST'):
		usr = request.POST['username']  #Here, we get the useranme fetched from html page
		URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&ucuser="
		URL = URL + usr
		r = requests.get(URL)  #Recieved data in json-format
		lst = json.loads(r.text)
		sub_lst = lst['query']['usercontribs'] #Contribution data extracted
		try:
			fetched_user = sub_lst[0]['user']
			fetched_user_id = sub_lst[0]['userid']
		except:
			fetched_user = fetched_user_id = 'No user found'
		return(render(request,'App/index.html',{'contribution':sub_lst, 'username':fetched_user, 'userid':fetched_user_id}))  #Here I send contribution for display on index.html page
	else:
		return(render(request,'App/index.html',{}))
