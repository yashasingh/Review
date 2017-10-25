import json
import requests
import urllib.parse

from django.http import HttpResponse
from django.shortcuts import render


def user_revisions_analysis(request):
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
        url_parameters = urllib.parse.urlencode(parameters)
        url1 = 'https://en.wikipedia.org/w/api.php?{}'.format(url_parameters)
        
        # Recieved data in json-format
        response = requests.get(url1)
 
        if response.status_code == 200:
            lst = json.loads(response.text)
            try:
                # if username contains invalid value
                if lst['error']:
                    return render(request,
                                  'App/task4.html',
                                  {"error":lst['error']['info']}
                                 )
            except:
                # Edit data extracted
                edits_data = json.loads(response.text)
                contributions = [i for i in edits_data['query']['usercontribs']]
                # if user has no edits 
                if len(contributions) == 0:
                    return render(request,
                                  'App/task4.html',
                                  {"error": "0 edits found for username {}".format(username)})

                for articles in contributions:
                    url2 = "https://ores.wikimedia.org/v3/scores/enwiki/" + str(articles['revid'])
                    # recieve ORES response
                    response2 = requests.get(url2)
                    if response2.status_code != 200:
                        return render(request,
                                      'App/tesk4.html',
                                      {"error": "ORES failed to return response"})

                    # if successfull response from ORES
                    data = json.loads(response2.text)
                    analysis = data['enwiki']['scores'][str(articles['revid'])]
                    predictions = {'goodfaith': analysis['goodfaith']['score']['prediction'],
                                   'reverted': analysis['reverted']['score']['prediction'],
                                   'damaging': analysis['damaging']['score']['prediction'],
                                   'draftquality': analysis['draftquality']['score']['prediction'],
                                   'quality': analysis['wp10']['score']['prediction'],
                                   'title': articles['title'],
                                   'comment': articles['comment'],
                                   'timestamp': articles['timestamp'],
                                   'revid': articles['revid'],
                                   'user': articles['user']}
                    details.append(predictions)
        context = {'articles': details}
        return render(request,'App/task4.html',context)

    else:
        return render(request,'App/task4.html',{})
