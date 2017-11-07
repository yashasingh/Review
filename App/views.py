import json
import requests
import urllib.parse

from django.http import HttpResponse
from django.shortcuts import render


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
        params = {'action':'query',
                  'format':'json',
                  'list':'usercontribs',
                  'ucuser': username}


        URL = "https://en.wikipedia.org/w/api.php?"

        # Recieved data in json-format
        response = requests.get(URL, params = params)
 
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
        