import math
import toolforge

from django.http import HttpResponse
from django.shortcuts import render


def get_the_user_percentile(request):
    """
    Function to display the user percentile of Georgian wiki
    """
    if request.method=='POST':
        username = request.POST['username']
        
        conn = toolforge.connect('kawiki_p')
        with conn.cursor() as cursor:
            # Get the edit count for the user
            s1 = cursor.execute("SELECT user_editcount FROM user WHERE user_name = %s",[username])
            useredits_tup = cursor.fetchall()
            # Get total edit counts of all users
            s2 = cursor.execute("SELECT ss_total_edits FROM site_stats")
            totaledits_tup =cursor.fetchall()
            # Get the rank of the user 
            s3 = cursor.execute("SELECT 1+ (SELECT count(*) from user a WHERE a.user_editcount > b.user_editcount) as RNK FROM user b WHERE user_name = %s",[username])
            userrank_tup = cursor.fetchall()
            # Get total count of the users
            s4 = cursor.execute("select count(*) from user")
            totalusers_tup = cursor.fetchall()
        conn.close()

        try:    
            useredits = useredits_tup[0][0]
            totaledits = totaledits_tup[0][0]
            userrank = userrank_tup[0][0]
            totalusers = totalusers_tup[0][0]
            # Calculates user percentile
            percentile = 100-(math.ceil((userrank / totalusers)*100))
            return render(request,
                         'App/task2.html',
                         {'edits':useredits,
                          'name':username,
                          'total_edits':totaledits,
                          'rank':userrank,
                          'total_users':totalusers,
                          'percentile':percentile}
                          )
        except:
            return render(request, 'App/task2.html',{"false_query": 1})
 
    if request.method == 'GET':
        return render(request, 'App/task2.html')
