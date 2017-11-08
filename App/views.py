import json
import math
import requests
import toolforge
import urllib.parse

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.http import urlquote


def index(request):
    return render(request, 'App/home.html')     


def get_recent_english_edits(request):
    """
    Display the recent english edits of the user.
    """

    if request.method == 'POST':

        # Here, we get the username
        username = request.POST['username']
        # if username is submitted blank 
        if not username:
            return render(request, "App/index.html", {"error": "Please enter a username"})

        # if username is not blank
        params = {'ucuser': username}

        encoded = urllib.parse.urlencode(params)

        URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&"

        URL = "{}{}".format(URL, encoded)

        # Recieved data in json-format
        response = requests.get(URL)
 
        if response.status_code == 200:
            lst = json.loads(response.text)
            try:
                # if username contains invalid value
                if lst['error']:
                    return render(request,
                                  'App/index.html',
                                  {"error":lst['error']['info']}
                                 )
            except:
                # Contribution data extracted
                sub_lst = lst['query']['usercontribs']

                # if user has no edits 
                if len(sub_lst) == 0:
                    return render(request,
                                  'App/index.html',
                                  {"error": "0 edits found for username {}".format(username)})

                # Send contribution data for display
                return render(request,
                              'App/index.html',
                              {"contribution": sub_lst, "username": username})
        else:
            return render(request,
                          'App/index.html',
                          {"error": 'Exit code {}'.format(str(response.status_code)),
                           }
                          )

    if request.method == 'GET':
        return render(request, 'App/index.html')


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
            percentile = math.ceil((userrank / totalusers)*100)
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

def get_article_view_count(request):
    """
    Display analysis of last 5 edits made by user.
    """
    if request.method=='POST':
        # Here, we get the username
        username = request.POST['username']
        # if username is submitted blank 
        if not username:
            return render(request, "App/task4.html", {"error": "Please enter a username"})
        # if username is not blank
        details = list()
        parameters = {'action':'query',
                      'format':'json',
                      'list':'usercontribs',
                      'uclimit':'5',
                      'ucuser':username}
        url_base = 'https://en.wikipedia.org/w/api.php?'
        # Recieved data in json-format
        response = requests.get(url_base, params = parameters)
        if response.status_code == 200:
            try:
                # Edit data extracted
                edits_data = json.loads(response.text)
                if 'error' in edits_data:
                    raise Error(edits_data['error']['info'])
                contributions = [i for i in edits_data['query']['usercontribs']]
                # if user has no edits 
                if len(contributions) == 0:
                    raise Error("0 edits found for username {}".format(username))
                for articles in contributions:
                    url_ores = "https://ores.wikimedia.org/v3/scores/enwiki/{}".format(str(articles['revid']))
                    # recieve ORES response
                    response2 = requests.get(url_ores)
                    if response2.status_code != 200:
                        raise Error("ORES failed to return response")
                    # if successfull response from ORES
                    data = json.loads(response2.text)
                    analysis = data['enwiki']['scores'][str(articles['revid'])]
                    predictions = {'goodfaith': analysis['goodfaith']['score']['prediction'],
                                   #'reverted': analysis['reverted']['score']['prediction'],
                                   'damaging': analysis['damaging']['score']['prediction'],
                                   'draftquality': analysis['draftquality']['score']['prediction'],
                                   'quality': analysis['wp10']['score']['prediction'],
                                   'title': articles['title'],
                                   'comment': articles['comment'],
                                   'timestamp': articles['timestamp'],
                                   'revid': articles['revid'],
                                   'user': articles['user']}
                    details.append(predictions)
            except Exception as err:
                return(render(request,
                              'App/task4.html',
                              {'error': err}))
            context = {'articles': details}
            return render(request, 'App/task4.html', context)
        else:
            return render(request,
                          'App/index.html',
                          {"error": 'Exit code {}'.format(str(response.status_code))})
    else:
        return render(request,'App/task4.html',{})

def task5(request):
    if request.method=='POST':
        username = request.POST['username']
        try:
            if not username:
                raise Error("Please enter a username")
            params = {'action':'query',
                      'format':'json',
                      'list':'usercontribs',
                      'uclimit':'5',
                      'ucuser':username }
            url_base = 'https://en.wikipedia.org/w/api.php?'
            # Recieved data in json-format
            response = requests.get(url_base, params = params)
            if response.status_code == 200:
                edits_data = json.loads(response.text)
                if 'error' in edits_data:
                    raise Error(edits_data['error']['info'])
                title_list = [i['title'] for i in edits_data['query']['usercontribs']]
                if len(title_list) == 0:
                    raise Error("No edits found for user")
                details = list()
                for title in title_list:
                    if title: 
                        project = 'en.wikipedia.org'
                        access = 'all-access'
                        agent = 'all-agents'
                        article = urlquote(title)
                        granularity = 'monthly'
                        start = '20170101'
                        end = '20171106'
                        url_viewcount = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{}/{}/{}/{}/{}/{}/{}".format(
                            project,
                            access,
                            agent,
                            article,
                            granularity,
                            start,
                            end)
                        view_response = requests.get(url_viewcount)
                        if view_response.status_code != 200:
                            raise Error('Exit code {}'.format(str(response.status_code)))
                        view_data = json.loads(view_response.text)
                        total_view_count = 0
                        for i in view_data['items']:
                            total_view_count += i['views'] 
                        display_dict = {'Title': title,
                                         'Views': total_view_count}
                        details.append(display_dict)
                context = {'articles': details}
                return render(request, 'App/task5.html', context)

        except Exception as err: 
            return render(request, 'App/task5.html', {'error': err})

    else:
        return(render(request,'App/task5.html',{}))
