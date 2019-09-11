from prettytable import PrettyTable
from datetime import datetime
from twython import Twython
from pymongo import MongoClient
import json
import sys

def getAccessToken():
  """ Add your own Facebook access token here, see Readme for details """
	return ""

def connectTwitter():
  """ Add your own Twitter API keys here, see Readme for details """
	auth = {
		'APP_KEY' : '',
		'APP_SECRET' : '',
		'ACCESS_TOKEN' : '',
		'ACCESS_TOKEN_SECRET':''
		}

	twitter = Twython(auth['APP_KEY'], auth['APP_SECRET'], auth['ACCESS_TOKEN'], auth['ACCESS_TOKEN_SECRET'])
	
	if twitter:
		print 'Authenticated.'
	else:
		sys.exit('Error with Twitter API')
			
	return twitter

def returnActiveAds(ads):
	active_ads = []
	table = PrettyTable()
	table.field_names = ['by', 'start', 'now', 'stop', 'active']
	now = datetime.now()

	for ad in ads:
		ad_start = datetime.strptime(ad['ad_delivery_start_time'], '%Y-%m-%dT%H:%M:%S+0000')
		if not ad.has_key('ad_delivery_stop_time'):
			active = True
		else:
			ad_stop = datetime.strptime(ad['ad_delivery_stop_time'], '%Y-%m-%dT%H:%M:%S+0000')
			active = False

		if active == False:
			if now > ad_start and now < ad_stop:
				active = True
				active_ads.append(ad)
			else:
				active = False

		table.add_row([ad['page_name'], ad_start.isoformat(), now, ad_stop.isoformat(), active])

	print '%i ads are active.' % len(active_ads)
	print table

	return active_ads

def returnPages():
  """ You can add your own Facebook Pages here, these are the pages for the political parties in the Dutch Tweede Kamer, including party leaders """"
	return {	'PVDA' : {
				'page_url' : 'https://www.facebook.com/PartijvandeArbeid/', 
				'page_id' : '113895885305052',
				'page_title' : 'Partij van de Arbeid (PvdA)',
				'twitter_handle' : 'pvda',
			},
			'Lodewijk Asscher' : {
				'page_url' : 'https://www.facebook.com/LodewijkAsscher/', 
				'page_id' : '254918764596191',
				'page_title' : 'Lodewijk Asscher',
				'twitter_handle' : 'LodewijkA',
			},
			'FVD' : {
				'page_url' : 'https://www.facebook.com/forumvoordemocratie/', 
				'page_id' : '609816282477420',
				'page_title' : 'Forum voor Democratie -FVD',
				'twitter_handle' : 'fvdemocratie',
			},
			'Thierry Baudet' : { 
				'page_url' : 'https://www.facebook.com/forumvoordemocratie/', 
				'page_id' : '379837259062033',
				'page_title' : 'Thierry Baudet',
				'twitter_handle' : 'thierrybaudet',
			},
			'VVD' : {
				'page_url' : 'https://www.facebook.com/VVD/', 
				'page_id' : '121264564551002',
				'page_title' : 'VVD',
				'twitter_handle' : 'VVD'
			},
			'Klaas Dijkhoff' : {
				'page_url' : 'https://www.facebook.com/klaasdijkhoff/', 
				'page_id' : '124282324250399',
				'page_title' : 'Klaas Dijkhoff',
				'twitter_handle' : 'Dijkhoff'
			},
			'CDA' : {
				'page_url' : 'https://www.facebook.com/kiesCDA/', 
				'page_id' : '320374518118',
				'page_title' : 'CDA',
				'twitter_handle' : 'cdavandaag'
			},
			'Sybrand Buma' : {
				'page_url' : 'https://www.facebook.com/sybrandbumacda/', 
				'page_id' : '1111353662231954',
				'page_title' : 'Sybrand Buma',
				'twitter_handle' : 'sybrandbuma'
			},
			'D66' : {
				'page_url' : 'https://www.facebook.com/D66/', 
				'page_id' : '52985377549',
				'page_title' : 'D66',
				'twitter_handle' : 'D66'
			},
			'Rob Jetten' : {
				'page_url' : 'https://www.facebook.com/RobJetten/', 
				'page_id' : '684205995075734',
				'page_title' : 'Rob Jetten',
				'twitter_handle' : 'RobJetten'
			},
			'50+' : {
				'page_url' : 'https://www.facebook.com/50PLUSpartij-347623668624706/', 
				'page_id' : '347623668624706',
				'page_title' : '50PLUSpartij',
				'twitter_handle' : '50pluspartij'
			},		
			'GL' : {
				'page_url' : 'https://www.facebook.com/groenlinks/', 
				'page_id' : '175740570505',
				'page_title' : 'GroenLinks',
				'twitter_handle' : 'groenlinks'
			},
			'Jesse Klaver' : {
				'page_url' : 'https://www.facebook.com/jesseklaver/', 
				'page_id' : '687496011309020',
				'page_title' : 'Jesse Klaver',
				'twitter_handle' : 'jesseklaver'
			},
			'DENK' : {
				'page_url' : 'https://www.facebook.com/DenkNL/', 
				'page_id' : '596153377149961',
				'page_title' : 'DENK',
				'twitter_handle' : 'DenkNL'
			},
			'Tunahan Kuzu' : {
				'page_url' : 'https://www.facebook.com/KiesKuzu/', 
				'page_id' : '1550088745275913',
				'page_title' : 'Tunahan Kuzu',
				'twitter_handle' : 'tunahankuzu'
			},
			'SP' : {
				'page_url' : 'https://www.facebook.com/SocialistischePartij/', 
				'page_id' : '128393027527',
				'page_title' : 'SP',
				'twitter_handle' : 'SPNL'
			},
			'Lilian Marijnisssen' : {
				'page_url' : 'https://www.facebook.com/LilianMarijnissenSP/', 
				'page_id' : '844559615710915',
				'page_title' : 'Lilian Marijnissen',
				'twitter_handle' : 'MarijnissenL'
			},
			'CU' : {
				'page_url' : 'https://www.facebook.com/ChristenUnie/', 
				'page_id' : '211661062254003',
				'page_title' : 'ChristenUnie',
				'twitter_handle' : 'christenunie'
			},
			'Gert-Jan Segers' : {
				'page_url' : 'https://www.facebook.com/gertjansegersCU/', 
				'page_id' : '147772805659767',
				'page_title' : 'Gert Jan Segers',
				'twitter_handle' : 'gertjansegers'
			},
			'SGP' : {
				'page_url' : 'https://www.facebook.com/SGPnieuws/', 
				'page_id' : '433611050005553',
				'page_title' : 'SGP',
				'twitter_handle' : 'SGPNieuws'
			},
			'Kees van der Staaij' : {
				'page_url' : 'https://www.facebook.com/keesvanderstaaij/', 
				'page_id' : '135227606660572',
				'page_title' : 'Kees van der Staaij',
				'twitter_handle' : 'keesvdstaaij'
			},
			'PVDD' : {
				'page_url' : 'https://www.facebook.com/PartijvoordeDieren/', 
				'page_id' : '102287806490622',
				'page_title' : 'Partij voor de Dieren',
				'twitter_handle' : 'PartijvdDieren'
			},
			'Marianne Thieme' : {
				'page_url' : 'https://www.facebook.com/mariannethieme/', 
				'page_id' : '126389617450422',
				'page_title' : 'Marianne Thieme',
				'twitter_handle' : 'mariannethieme'
			},
			'Geert Wilders' : {
				'page_url' : 'https://www.facebook.com/geertwilders/', 
				'page_id' : '202064936858448',
				'page_title' : 'Geert Wilders',
				'twitter_handle' : 'geertwilderspvv'
			},
			'PVV' : {
				'page_url' : 'https://www.facebook.com/PVV.PartijvoordeVrijheid/', 
				'page_id' : '141639003175865',
				'page_title' : 'PVV',
				'twitter_handle' : 'PVV'
			},
					
	}

if __name__ == "__main__":
	client = MongoClient()
	db = client.adlibrary
	print '%i ads in libary. %i are active.' % (db.ads.count(), len(returnActiveAds(db.ads.find())))
  sys.exit()
