from django.http import HttpResponse
from django.shortcuts import render
import math
import json
import requests
import toolforge

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