from django.http import HttpResponse
from django.shortcuts import render
import math
import json
import requests
import toolforge

def main2(request):
    if(request.method=='POST'):
        flag = 1
        usr = request.POST['username']
        a = 1 if re.match("^[a-zA-Z0-9_ ]*$", s) else 0
        if(!a):
            flag=0
            return(render(request, 'Microtask1/task2.html',{"false_query":1}))
        SqlQuery1 = "SELECT user_editcount FROM user WHERE user_name='" + usr + "';"
        SqlQuery2 = "SELECT ss_total_edits FROM site_stats"
        #SqlQuery3 = "select rank from (select user_name, @curRank := @curRank + 1 as rank from user p, ( select @curRank := 0 ) q order by user_editcount DESC) q where user_name='"+usr+"';"
        SqlQuery3 = "SELECT 1+(SELECT count(*) from user a WHERE a.user_editcount > b.user_editcount) as RNK FROM user b WHERE user_name='"+usr+"';"
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
        try:    
            useredits = useredits_tup[0][0]
            totaledits = totaledits_tup[0][0]
            userrank = userrank_tup[0][0]
            totalusers = totalusers_tup[0][0]
        except:
            flag = 0 

        if(flag):    
            percentile = 100-((userrank*100)/(totalusers+1))
            rating = math.ceil((userrank/totalusers)*100)
            userrating = "User lies in top "+str(rating) + "%"
            return(render(request, 'Microtask1/task2.html',{'edits':useredits, 'name':usr, 'total_edits':totaledits, 'rank':userrank, 'total_users':totalusers, 'Percentile':percentile, 'user_rating':userrating}))
        return(render(request, 'Microtask1/task2.html',{"false_query":1}))
    else:
        return(render(request, 'Microtask1/task2.html',{}))
