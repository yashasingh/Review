import json
import requests
import urllib.parse

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.http import urlquote


def get_article_view_count(request):
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
