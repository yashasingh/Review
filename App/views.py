import json
import requests
import urllib.parse

from django.http import HttpResponse
from django.shortcuts import render


def main(request):
    """
    Display the recent english edits of the user.
    """

    if request.method == 'POST':

        # Here, we get the username fetched from html page
        username = request.POST['username']
        params={'ucuser':username}
        encoded = urllib.parse.urlencode(params)

        URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&"

        URL = "{}{}".format(URL, encoded)

        # Recieved data in json-format
        response = requests.get(URL)

        if(response.status_code != 200):
            return render(request,
                          'App/index.html',
                          {"error":'HTTP response {}'.format(str(response.status_code),)
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
