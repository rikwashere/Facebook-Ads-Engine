from pymongo import MongoClient, errors
from urlparse import urlparse
import requests
import helpers
import json	
import time
import sys

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def crawlAdLibrary(targets):
	out = []

	for chunk in chunker(targets.keys(), 10):
		ads_archive = 'https://graph.facebook.com/v3.1/ads_archive'
		fields = ['ad_creative_body', 'demographic_distribution', 'ad_snapshot_url', 'impressions', 'page_name', 'region_distribution', 'spend', 'ad_creative_link_title', 'ad_creative_link_description', 'ad_creative_link_caption', 'ad_creation_time', 'ad_delivery_start_time', 'ad_delivery_stop_time' ]

		page_ids = [targets[party]['page_id'] for party in chunk]
		params = {	'access_token' : helpers.getAccessToken(), 
					'ad_reached_countries' : 'NL',
					'ad_type' : 'POLITICAL_AND_ISSUE_ADS',
					'ad_active_status': 'ALL',
					'search_page_ids' : ','.join(page_ids),
					'fields' : ','.join(fields)
		}

		print 'Requesting %i parties.' % len(page_ids)
		r = requests.get(ads_archive, params=params)

		response = json.loads(r.text)

		if r.status_code == 200:
			out += response['data']
		else:
			print response['error']['error_user_msg']
			sys.exit(response['error']['message'])

	print 'OK. Found %i ads' % len(out)
	return out
	
def returnParams():
	fields = ['ad_creative_body', 'demographic_distribution', 'ad_snapshot_url', 'impressions', 'page_name', 'region_distribution', 'spend', 'ad_creative_link_title', 'ad_creative_link_description', 'ad_creative_link_caption', 'ad_creation_time', 'ad_delivery_start_time', 'ad_delivery_stop_time' ]

	params = {	'access_token' : helpers.getAccessToken(), 
				'ad_reached_countries' : 'NL',
				'ad_type' : 'POLITICAL_AND_ISSUE_ADS',
				'ad_active_status': 'ACTIVE',
				'fields' : ','.join(fields)
		}

	return 'https://graph.facebook.com/v3.1/ads_archive', params



def crawlActiveAds(targets):
	out = [] 

	for chunk in chunker(targets.keys(), 10):
		ads_archive = 'https://graph.facebook.com/v3.1/ads_archive'
		fields = ['ad_creative_body', 'demographic_distribution', 'ad_snapshot_url', 'impressions', 'page_name', 'region_distribution', 'spend', 'ad_creative_link_title', 'ad_creative_link_description', 'ad_creative_link_caption', 'ad_creation_time', 'ad_delivery_start_time', 'ad_delivery_stop_time' ]

		page_ids = [targets[party]['page_id'] for party in chunk]
		params = {	'access_token' : helpers.getAccessToken(), 
					'ad_reached_countries' : 'NL',
					'ad_type' : 'POLITICAL_AND_ISSUE_ADS',
					'ad_active_status': 'ACTIVE',
					'search_page_ids' : ','.join(page_ids),
					'fields' : ','.join(fields)
		}

		print 'Requesting %i parties.' % len(page_ids)
		r = requests.get(ads_archive, params=params)

		response = json.loads(r.text)

		if r.status_code == 200:
			out += response['data']
		else:
			print response['error']['error_user_msg']
			sys.exit(response['error']['message'])

	print 'OK. Found %i active ads' % len(out)
	return out

def sendTweet(ad):
	client = MongoClient()
	db = client.adlibrary
		
	twitter = helpers.connectTwitter()
	parties = helpers.returnPages()

	page = ad['page_name']
	for party in parties:
		if page == parties[party]['page_title']:
			twitter_handle = parties[party]['twitter_handle']

	msg = '@FbAdTrackerNL Nieuwe advertentie door {}. \n- Geschat bereik: {} - {}\n- Geschatte kosten: {} - {}\nTekst: "'.format( twitter_handle, int(ad['impressions']['lower_bound']), int(ad['impressions']['upper_bound']),	int(ad['spend']['lower_bound']), int(ad['spend']['upper_bound']) )

	msg += ad['ad_creative_body'][:276 - len(msg)] + '..."'
	
	try:
		tweet = twitter.update_status(status=msg, in_reply_to_status_id=1115982344941391874)
	except:
		print msg

	time.sleep(10)

if __name__ == '__main__':
	while True:
		client = MongoClient()
		db = client.adlibrary
		pages = helpers.returnPages()
		new_ads = []
		data_out = crawlAdLibrary(pages)

		for ad in data_out:
			parsed_url = urlparse(ad['ad_snapshot_url'])
			ad_id = parsed_url.query.split('&')[0].split('id=')[1]
			ad['_id'] = ad_id

			try:
				db.ads.insert_one(ad)
				sendTweet(ad)
			except errors.DuplicateKeyError:
				print 'Already crawled %s' % ad['_id']

		time.sleep(5 * 60)
