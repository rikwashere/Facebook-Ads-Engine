# Facebook Ads Engine
This script tracks a list of Facebook Page and tweets when they launch a new political advertisment, using Facebook's Ads Library API. The ads are then stored in a MongoDB database, facilitating subsequent analysis.

This script was used by the author to write an article in NRC Handelsblad about the usage of political ads in a 2019 election in the Netherlands. <a href='https://www.nrc.nl/nieuws/2019/05/20/sp-adverteert-het-meest-op-facebook-a3960892'>Read it here (Dutch)</a>.

You can find my Twitter bot in action <a href='https://twitter.com/fbadtrackernl'>@fbadtrackernl</a>. 


# Usage
- Clone repository
- run: <pip install -r requirements.txt> from shell
- Add API keys to helpers.py
   - Add Twitter keys to helpers/connectTwitter(), <a href='https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html'>see Twitter docs<a/>.
  - For Facebook acces token, follow these steps:
    - Get user access token from <a href='https://developers.facebook.com/tools/explorer/?classic=0'>Graph API Explorer</a>.
    - Extend access token using <a href='https://developers.facebook.com/tools/debug/accesstoken/'>access token debugger</a>. 
    - Add token to getAccessToken()
- Add your target Pages to helpers/returnPages() and add page_url, page_id, page_title and a twitter_handle 
- Run adScraper.py locally or on a server using a task manage, I use PM2 on a Digital Ocean droplet.

# Extras
Helpers.py contains a function returnActiveAds() that returns all ads currently active. 

# To do
Do something about Facebook token expiring.
