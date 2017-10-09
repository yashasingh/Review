from django.http import HttpResponse
from django.shortcuts import render
import math
import json
import requests
import toolforge

<<<<<<< HEAD
def main2(request):
    if(request.method=='POST'):
        username = request.POST['username']
        conn = toolforge.connect('kawiki_p')
        with conn.cursor() as cursor:
            s1 = cursor.execute("SELECT user_editcount FROM user WHERE user_name = %s",[username])
            useredits_tup = cursor.fetchall()
            s2 = cursor.execute("SELECT ss_total_edits FROM site_stats")
            totaledits_tup =cursor.fetchall()
            s3 = cursor.execute("SELECT 1+ (SELECT count(*) from user a WHERE a.user_editcount > b.user_editcount) as RNK FROM user b WHERE user_name = %s",[username])
            userrank_tup = cursor.fetchall()
            s4 = cursor.execute("select count(*) from user")
            totalusers_tup = cursor.fetchall()
        conn.close()

        try:    
            useredits = useredits_tup[0][0]
            totaledits = totaledits_tup[0][0]
            userrank = userrank_tup[0][0]
            totalusers = totalusers_tup[0][0]
            percentile = 100-((userrank*100)/(totalusers+1))
            rating = math.ceil((userrank/totalusers)*100)
            userrating = "User lies in top "+str(rating) + "%"
            return(render(request, 'App/task2.html',{'edits':useredits, 'name':username, 'total_edits':totaledits, 'rank':userrank, 'total_users':totalusers, 'Percentile':percentile, 'user_rating':userrating}))
        except:
            return(render(request, 'App/task2.html',{"false_query":1}))
 
    else:
        return(render(request, 'App/task2.html',{}))
=======
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
>>>>>>> a613a3594c61bb8763f52a83420d06ff03422567
