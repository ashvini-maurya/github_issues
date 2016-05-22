from django.shortcuts import render, HttpResponse, render_to_response
import requests
import json
from datetime import datetime, timedelta
from django.template.context import RequestContext


def index(request):
    context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
    return render_to_response('issues/index.html', context_instance=context)

def getUrl(request):
    geturl = request.GET['URL']
    splitted_url = (geturl).split('/')
    r = requests.get(geturl)

    if r.status_code == 200:
        total_issues_api = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4])
        total_issues_response = requests.get(total_issues_api)
        total_issues_json = total_issues_response.json()
        total_issues = total_issues_json["open_issues"]

        last_24hr = datetime.now() - timedelta(hours=24)
        parameters = {'since': last_24hr, 'per_page': 100}

        requested_api = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4]) + "/issues?"
        #print requested_api

        get_url_api_data = requests.get(requested_api, params=parameters)
        last_24hr_url_api = get_url_api_data.url
        last_24hr_url_api_data = requests.get(last_24hr_url_api)

        li_last_24hr_url_api = []
        for api_urls in last_24hr_url_api_data.json():
            li_last_24hr_url_api.append(api_urls["html_url"])

        title_li = []
        for title in last_24hr_url_api_data.json():
            title_li.append(title['title'])

        dict_of_url_and_title = dict(zip(li_last_24hr_url_api, title_li))

        count = 0
        for updated_value in get_url_api_data.json():
            count += 1

        last_7days = last_24hr - timedelta(days=7)
        parameter2 = {'since': last_7days, 'per_page': 100}

        response_data = requests.get(requested_api, params=parameter2)
        less_than_7days_ago_api = response_data.url
        less_than_7days_ago_api_data = requests.get(less_than_7days_ago_api)

        li_less_than_7days_url_api = []
        for api_url in less_than_7days_ago_api_data.json():
            li_less_than_7days_url_api.append(api_url["html_url"])

        title_li2 = []
        for title in less_than_7days_ago_api_data.json():
            title_li2.append(title['title'])

        dict_of_url_and_title2 = dict(zip(li_less_than_7days_url_api, title_li2))

        count2 = 0
        for _value in response_data.json():
            count2 += 1

# for more than 7days ago
        more_than_7days = last_7days - timedelta(days=1000)
        parameter3 = {'since': more_than_7days, 'per_page': 500}

        response_data2 = requests.get(requested_api, params=parameter3)
        more_than_7days_ago_api = response_data2.url
        more_than_7days_ago_api_data = requests.get(more_than_7days_ago_api)

        li_more_than_7days_url_api = []
        for api_url in more_than_7days_ago_api_data.json():
            li_more_than_7days_url_api.append(api_url["html_url"])

        title_li3 = []
        for title in more_than_7days_ago_api_data.json():
            title_li3.append(title['title'])

        dict_of_url_and_title3 = dict(zip(li_more_than_7days_url_api, title_li3))




        total_issues_greater_than_7days = total_issues_json["open_issues"] - count - count2
        params = {'total': total_issues, 'count': count, 'count2': count2, 'total_greater_than_7days': total_issues_greater_than_7days, 'dict_of_url_and_title': dict_of_url_and_title, 'dict_of_url_and_title2': dict_of_url_and_title2, 'dict_of_url_and_title3': dict_of_url_and_title3}
        return render(request, 'issues/getData.html', params)


    else:
        return HttpResponse("Invalid URL. url should be in format 'https://github.com/{org_name or user_name}/{repo_name}/{issues}'")

def about(request):
    return render(request, 'issues/about.html', {})

