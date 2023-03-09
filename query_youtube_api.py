#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import urlexpander_custom
import regex
import json
from googleapiclient.discovery import build

DEVELOPER_KEY = "[YOUR_API_KEY_HERE]"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def expand_telegram(url):
	headers = {
    	'referer': 'https://www.google.com/',
    	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
		}

	response = requests.get(url, headers=headers)
	ignore_pattern = 'win-rar\.com'
	found_links = []

	if response.status_code == 200:
		soup = BeautifulSoup(response.content, 'html.parser')
		for link in soup.find_all('a'):
			href = link.get('href')
			if href:
				if not regex.search(ignore_pattern, str(href)):
					found_links.append(href)
	return found_links

def url_expander(url, newfile):
	telegraph_pattern = 'https:\/\/telegra\.ph\/'
	isshort = urlexpander_custom.is_short(url)

	if isshort:
		try:
			expanded_url = urlexpander_custom.expand(url).replace('https://href.li/?','')
		except:
			return
		newfile.write("Expanded: " + expanded_url + '\n')
		if (urlexpander_custom.is_short(expanded_url) and expanded_url != url) or regex.search(telegraph_pattern, expanded_url):
			url_expander(expanded_url, newfile)
			return

	if regex.search(telegraph_pattern, url):
		url_to_write = expand_telegram(url)
		for extracted_url in url_to_write:
			newfile.write("Telegra.ph Expanded: " + extracted_url.replace('https://href.li/?','') + '\n')
			if urlexpander_custom.is_short(extracted_url) or regex.search(telegraph_pattern, extracted_url):
				url_expander(extracted_url, newfile)
				return
		
def parse_response(json_content, verbose_output):
	ids = []
	for item in json_content['items']:
		ids.append(str(item['id']['videoId']))

	headers = {
    'Accept': 'application/json',
	}

	for element in ids:
		urls = []
		indv_response = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&id='+element+'&key=' + DEVELOPER_KEY, headers=headers)
		if indv_response.status_code == 200:
			json_content = indv_response.json()
			for item in json_content['items']:
				verbose_output.write("Video URL: https://www.youtube.com/watch?v=" + element + "\nChannel ID: " + (item['snippet']['channelId']) + \
					"\nChannel Title: " + (item['snippet']['channelTitle']) + "\nDescription: \n" + (item['snippet']['description']) + "\n")
				urls = regex.findall(url_pattern, str(item['snippet']['description']))
				verbose_output.write("URLs: \n")
				for url in urls:
					if not regex.findall(ignore_pattern, str(url)):
						verbose_output.write(url + '\n')
						total_urls.append(url)
			verbose_output.write('\n\n------------------------------------------------------------------------------------------------\nSection End\n------------------------------------------------------------------------------------------------\n')
		else:
			continue

total_urls = []

##Add to ignore_pattern as needed
url_pattern = r'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)'
ignore_pattern = "(youtube|ytimg|googlevideo|ggpht|virustotal|googleusercontent|google|gstatic|adobe|twitter|soundcloud|facebook|instagram|tiktok|linkedin)\\.com|(schema|js|ietf)\\.org|youtu\\.be|amzn\\.to|wsop\\.so|\\.\\.$"

##Customize fields as needed
request = youtube.search().list(
    q = 'cracked software',
    part = 'snippet',
    type = 'video',
    maxResults = 10,
    order = 'relevance',
    videoDuration = 'short',
    safeSearch = 'none',
    publishedAfter = '2023-03-06T00:00:00Z',
    relevanceLanguage = 'en',
    key = DEVELOPER_KEY
)

verbose_output = open('yt_api_verbose.txt', 'a')
while request:
    response = request.execute()
    parse_response(response, verbose_output)
    request = youtube.search().list_next(request, response)

verbose_output.close()

total_urls.sort()
urls_deduped = list(set(total_urls))

newfile = open("expanded_links.txt", "a")
for url in urls_deduped:
	##write url
	newfile.write('\n'+ url + '\n')
	url_expander(url, newfile)

newfile.close()
