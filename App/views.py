import json
import requests
#import toolforge
import urllib.parse

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return(render(request, 'App/home.html',{}))     

def main(request):
    """
    Display the recent english edits of the user.
    """

    if request.method == 'POST':

        # Here, we get the username fetched from html page
        username = request.POST['username']
        print (username)
        params={'ucuser':username}
        encoded = urllib.parse.urlencode(params)

        URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&"

        URL = "{}{}".format(URL, encoded)
        print (URL)

        # Recieved data in json-format
        response = requests.get(URL)

        print(response.status_code)

        if(response.status_code != 200):
            return render(request,
                          'App/index.html',
                          {"error":'HTTP response {}'.format(str(response.status_code)),
                           "response": "Invalid username",
                           "code": 1}
                          )
        else:
            lst = json.loads(response.text)
            try:
                if lst['error']:
                    return render(request,
                                 'App/index.html',
                                 {"error":lst['error']['info']})
            except:
                # Contribution data extracted
                sub_lst = lst['query']['usercontribs']
                if len(sub_lst) == 0:
                    return render(request,
                                 'App/index.html',
                                 {"error":"No Edits found for username {}".format(username)})

            # Send contribution data for display
            return render(request,
                         'App/index.html',
                         {"contribution":sub_lst, "username":username})
    else:
        return render(request, 'App/index.html')


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
            percentile = 100-(math.ceil((userrank/totalusers)*100))
            return(render(request, 'App/task2.html',{'edits':useredits, 'name':username, 'total_edits':totaledits, 'rank':userrank, 'total_users':totalusers, 'percentile':percentile}))
        except:
            return(render(request, 'App/task2.html',{"false_query":1}))
 
    else:
        return(render(request, 'App/task2.html',{}))
