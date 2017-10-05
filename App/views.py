from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
import toolforge

def main2(request):
    if(request.method=='POST'):
        usr = request.POST['username']
        SqlQuery1 = "SELECT user_editcount FROM user WHERE user_name='" + usr + "';"
        SqlQuery2 = "SELECT ss_total_edits FROM site_stats"
        SqlQuery3 = "select rank from (select user_name, @curRank := @curRank + 1 as rank from user p, ( select @curRank := 0 ) q order by user_editcount DESC) q where user_name='"+usr+"';"
        SqlQuery4 = "select count(*) from user;"
        conn = toolforge.connect('kawiki_p')
        with conn.cursor() as curr:
            s1 = curr.execute(SqlQuery1)
            useredits_tup = curr.fetchall()
            s2 = curr.execute(SqlQuery2)
            totaledits_tup =curr.fetchall()
            s3 = curr.execute(SqlQuery3)
            userrank_tup = curr.fetchall()
            s4 = curr.execute(SqlQuery4)
            totalusers_tup = curr.fetchall()

        conn.close()
        useredits = useredits_tup[0][0]
        totaledits = totaledits_tup[0][0]
        userrank = userrank_tup[0][0]
        totalusers = totalusers_tup[0][0]

        percentile = 100-((userrank*100)/(totalusers+1))
        rating = (userrank/totalusers)*100
        if(rating<=1):
            userrating = "User lies in top 1%"
        elif(rating >1 and rating<=5):
            userrating = "User lies in top 5%" 
        elif(rating >5 and rating<=10):
            userrating = "User lies in top 10%"
        elif(rating >10 and rating<=20):
            userrating = "User lies in top 20%"
        elif(rating >20 and rating<=30):
            userrating = "User lies in top 30%"
        elif(rating >30 and rating<=40):
            userrating = "User lies in top 40%"
        elif(rating >40 and rating<=50):
            userrating = "User lies in top 50%"
        elif(rating >50 and rating<=60):
            userrating = "User lies below top 50%"
        elif(rating >60 and rating<=70):
            userrating = "User lies below top 60%"
        else:
             userrating =  "User lies below top 70%"
        return(render(request, 'Microtask1/task2.html',{'edits':useredits, 'name':usr, 'total_edits':totaledits, 'rank':userrank, 'total_users':totalusers, 'Percentile':percentile, 'user_rating':userrating}))
    else:
        return(render(request, 'Microtask1/task2.html',{}))
