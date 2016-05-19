from django.shortcuts import render, HttpResponse, render_to_response
import requests
import json
from datetime import datetime, timedelta
from django.template.context import RequestContext



def index(request):
    context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
    return render_to_response('base.html', context_instance=context)

def getUrl(request):
    geturl = request.GET['URL']
    splitted_url = (geturl).split('/')
    r = requests.get(geturl)

    if r.status_code == 200:
        total_issues_api = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4])
        #print total_issues_api
        total_issues_response = requests.get(total_issues_api)
        print total_issues_response
        total_issues_json = total_issues_response.json()
        total_issues = total_issues_json["open_issues"]
        print total_issues

        last_24hr = datetime.now() - timedelta(hours=24)
        parameters = {'since': last_24hr}

        issue_api_in_last_24hr = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4]) + "/issues?"
        get_url_api_data = requests.get(issue_api_in_last_24hr, params=parameters)
        last_24hr_url_api = get_url_api_data.url
        last_24hr_url_api_data = requests.get(last_24hr_url_api)

        li_last_24hr_url_api = []
        for api_urls in last_24hr_url_api_data.json():
            li_last_24hr_url_api.append(api_urls["url"])


        title_li = []
        for title in last_24hr_url_api_data.json():
            title_li.append(title['title'])
        print(title_li)

        count = 0
        for updated_value in get_url_api_data.json():
            count += 1

        print "last 24hr: ", count

        last_7days = last_24hr - timedelta(days=7)
        parameter2 = {'since': last_7days}
        issue_api_in_less_than_7days_but_greater_than_24hr = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4]) + "/issues?"
        response_data = requests.get(issue_api_in_less_than_7days_but_greater_than_24hr, params=parameter2)
        count2 = 0
        for _value in response_data.json():
            count2 += 1

        total_issues_greater_than_7days = total_issues_json["open_issues"] - count - count2
        params = {'total': total_issues, 'count': count, 'count2': count2, 'total_greater_than_7days': total_issues_greater_than_7days, 'li_last_24hr_url_api': li_last_24hr_url_api, 'title': title_li}
        return render(request, 'issues/getData.html', params)


    else:
        return HttpResponse("Invalid URL. url should be in format 'https://github.com/{org_name or user_name}/{repo_name}/{issues}'")

def about(request):
    return render(request, 'issues/about.html', {})

