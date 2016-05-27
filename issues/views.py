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
    #print geturl
    if len(geturl) > 0:
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

            get_url_api_data = requests.get(requested_api, params=parameters)
            last_24hr_url_api = get_url_api_data.url
            last_24hr_url_api_data = requests.get(last_24hr_url_api)
            #print last_24hr_url_api_data

            li_last_24hr_url_api = []
            for api_urls in last_24hr_url_api_data.json():
                li_last_24hr_url_api.append(api_urls["html_url"])

            #print li_last_24hr_url_api

            title_li = []
            for title in last_24hr_url_api_data.json():
                title_li.append(title['title'])

            dict_of_url_and_title = dict(zip(li_last_24hr_url_api, title_li))

            count = 0
            for updated_value in get_url_api_data.json():
                count += 1
            #print(count)

            last_7days = datetime.now() - timedelta(days=7)
            parameter2 = {'since': last_7days, 'per_page': 100}

            response_data = requests.get(requested_api, params=parameter2)
            less_than_7days_ago_api = response_data.url
            less_than_7days_ago_api_data = requests.get(less_than_7days_ago_api)

            li_less_than_7days_url_api = []
            for api_url in less_than_7days_ago_api_data.json():
                li_less_than_7days_url_api.append(api_url["html_url"])

            # find only urls which are in li_less_than_7days_url_api only but not in previous case

            li_less_than_7days_url_api = [urls for urls in li_less_than_7days_url_api if urls not in li_last_24hr_url_api]

            title_li2 = []
            for title in less_than_7days_ago_api_data.json():
                title_li2.append(title['title'])

            # find uniqe urls name
            title_li2 = [titles for titles in title_li2 if titles not in title_li]

            dict_of_url_and_title2 = dict(zip(li_less_than_7days_url_api, title_li2))

            count2 = 0
            for _value in response_data.json():
                count2 += 1

            count2 = count2 - count
            # for more than 7days ago
            more_than_7days = last_7days - timedelta(days=1000)
            parameter3 = {'since': more_than_7days, 'per_page': 100}

            response_data2 = requests.get(requested_api, params=parameter3)
            more_than_7days_ago_api = response_data2.url
            more_than_7days_ago_api_data = requests.get(more_than_7days_ago_api)
            #print more_than_7days_ago_api_data

            li_more_than_7days_url_api = []
            for api_url in more_than_7days_ago_api_data.json():
                li_more_than_7days_url_api.append(api_url["html_url"])

            li_more_than_7days_url_api = [url2 for url2 in li_more_than_7days_url_api if url2 not in li_less_than_7days_url_api if url2 not in li_last_24hr_url_api]


            title_li3 = []
            for title in more_than_7days_ago_api_data.json():
                title_li3.append(title['title'])

            title_li3 = [title2 for title2 in title_li3 if title2 not in title_li2 if title2 not in title_li]
            dict_of_url_and_title3 = dict(zip(li_more_than_7days_url_api, title_li3))



            # find total contributors in a public repository

            request_api = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4]) + "/stats/contributors"
            data = requests.get(request_api)
            #print data

            contributors_name_list = []
            contributors_login_url = []
            #total_contributors = 0

            for contributor in data.json():
                contributors_name_list.append(contributor['author']['login'])
                contributors_login_url.append(contributor['author']['html_url'])

            #print len(contributors_name_list)  # total contributors: this gives atmost 100
            #print(contributors_name_list)
            #print contributors_login_url

            dict_of_contributor_name_and_contributor_url = dict(zip(contributors_name_list, contributors_login_url))
            #print dict_of_contributor_name_and_contributor_url






            total_issues_greater_than_7days = total_issues_json["open_issues"] - count - count2
            params = {'total': total_issues, 'count': count, 'count2': count2, 'total_greater_than_7days': total_issues_greater_than_7days,\
                      'dict_of_url_and_title': dict_of_url_and_title, 'dict_of_url_and_title2': dict_of_url_and_title2, 'dict_of_url_and_title3': dict_of_url_and_title3, \
                      'dict_of_contributor_name_and_contributor_url': dict_of_contributor_name_and_contributor_url}

            return render(request, 'issues/getData.html', params)



        else:
            return render(request, 'issues/getData.html', {'error': "Invalid URL. url should be in format 'https://github.com/{org_name or user_name}/{repo_name}/{issues}'"})

    else:
        return render(request, 'issues/getData.html', {'error': "Please enter GitHub repo URL"})

def about(request):
    return render(request, 'issues/about.html', {})

