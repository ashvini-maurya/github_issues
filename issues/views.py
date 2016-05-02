from django.shortcuts import render
import requests
import json
from datetime import datetime, timedelta


def index(request):
    return render(request, 'issues/index.html', {})

def getUrl(request):
    geturl= request.GET['URL']
    splitted_url = (geturl).split('/')
    total_issues_api = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4])
    total_issues_response = requests.get(total_issues_api)
    total_issues_json = total_issues_response.json()
    total_issues = total_issues_json["open_issues"]
    #print "Total number of open issues: " + str(total_issues_json["open_issues"])


    last_24hr = datetime.now() - timedelta(hours=24)
    parameters = {'since': last_24hr}
    issue_api_in_last_24hr = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4]) + "/issues?"
    get_url_api_data = requests.get(issue_api_in_last_24hr, params=parameters)

    count = 0
    for updated_value in get_url_api_data.json():
        count += 1
    #print "Total number of opened issues in last 24 Hours: " + str(count)

    last_7days = last_24hr - timedelta(days=7)
    parameter2 = {'since': last_7days}
    issue_api_in_less_than_7days_but_greater_than_24hr = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4]) + "/issues?"
    response_data = requests.get(issue_api_in_less_than_7days_but_greater_than_24hr, params=parameter2)
    count2 = 0
    for _value in response_data.json():
        count2 += 1
    #print "Total number of open issues that were opened more than 24 Hours but less than 7 days ago: " + str(count2)

    #print "Total Number of open issues that were opened more than 7 days ago: " + str((total_issues_json["open_issues"] - count - count2))

    total_issues_greater_than_7days = total_issues_json["open_issues"] - count - count2
    return render(request, 'issues/getData.html', {'total': total_issues, 'count': count, 'count2': count2, 'total_greater_than_7days': total_issues_greater_than_7days})



def about(request):
    return render(request, 'issues/about.html', {})

