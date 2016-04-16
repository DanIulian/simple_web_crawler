#!/usr/bin/env python
import requests


def write_to_file(s):
	with open("failing_URLS.txt", 'a') as stream:
		stream.write(s + "\n")


def check_dataset(data_set):
	url = 'https://data.gov.ro/api/3/action/package_show?id=' + data_set
	response = requests.get(url)
	if response.status_code == 200:
		print("start checking url ")
		check_for_url(response, data_set)


def check_for_url(response, data_set):
	content = response.json()
	resources = content['result'].get('resources', [])
	for i, resource in enumerate(resources):
		print ("check resource for url", i)
		url = resource.get('url', '')
		if url:
			print ("found url")
			try:
				resp = requests.head(url, allow_redirects=True)
			except Exception:
				print('ERROR SSL', url)
				write_to_file('ERROR SSL ' + url)
				continue
			if resp.status_code != 200:
				write_to_file("{0} - {1} - {2}".format(data_set, content.get('name'), url))
				print(url, 'was bad')


def main():
	response = requests.get('https://data.gov.ro/api/3/action/package_list')
	if response.status_code == 200:
		content = response.json()['result']
		for i, data_set in enumerate(content):
			print("start checking data set ", i)
			check_dataset(data_set)


main()
