import requests
import json
from datetime import datetime, timedelta
import re

issues = raw_input("Enter a valid github repo issues URL:")
r = requests.get(issues)
splitted_url = (r.url).split('/')

#issue_url_regex = re.compile('^https://github.com/[a-zA-Z0-9]*/[a-zA-Z0-9]*/issues$')
#if issue_url_regex:
if r.status_code == 200:#and splitted_url[0] == "https" and splitted_url[1] == "" and splitted_url[2] == "github.com" and splitted_url[5] == "issues":
	
	total_issues_api = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4])
	#print total_issues_api
	total_issues_response = requests.get(total_issues_api)
	total_issues_json = total_issues_response.json()
	print "Total number of open issues: " + str(total_issues_json["open_issues"])
	


	
	last_24hr = datetime.now() - timedelta(hours=24)
	parameters = {'since': last_24hr}
	issue_api_in_last_24hr = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4]) + "/issues?"
	get_url_api_data = requests.get(issue_api_in_last_24hr, params=parameters)

	count = 0
	for updated_value in get_url_api_data.json():
		count += 1
		#print updated_value["updated_at"]
	print "Total number of opened issues in last 24 Hours: " + str(count)


	
	last_7days = last_24hr - timedelta(days=7)
	parameter2 = {'since': last_7days}	
	issue_api_in_less_than_7days_but_greater_than_24hr = "https://api.github.com/repos/" + str(splitted_url[3]) + "/" + str(splitted_url[4]) + "/issues?"
	response_data = requests.get(issue_api_in_less_than_7days_but_greater_than_24hr, params=parameter2)
	count2 = 0
	for _value in response_data.json():
                count2 += 1
        print "Total number of open issues that were opened more than 24 Hours but less than 7 days ago: " + str(count2)


	print "Total Number of open issues that were opened more than 7 days ago: " + str((total_issues_json["open_issues"] - count - count2))

else:
	print "Invalid URL. url should in format 'https://github.com/{org_name or user_name}/{repo_name}/{issues}'"


