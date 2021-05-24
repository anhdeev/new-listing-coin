from sys import platform
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

platform_map = {
    'bscscan.com': 'Binance smart chain',
    'etherscan.io': 'Ethereum',
    'explorer.solana.com': 'Solana',
    'tronscan.org': 'Tron',
    'polkascan.io': 'Polkadot'
}

class Crawler(object):
    def __init__(self, url):
        self.url = url
        self.html = None
        self.soup = None

    def download(self):
        # Prepare the soup
        print(f"Now Scraping - {self.url}")
        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, "html.parser")

class CgCrawler(Crawler):
    def __init__(self, tokenId):
        self.base_url = 'https://www.coingecko.com/en/coins/'
        super().__init__(self.base_url + tokenId)
        self.contract = None
        self.icon = None
        self.explorer = None
        self.platform = None
        self.contract_selector = 'i.text-lg:nth-child(2)'
        self.icon_selector = 'div.coin-tag > span:nth-child(1) > img:nth-child(1)'
        self.explorer_selector = 'div.coin-link-row:nth-child(3) > div:nth-child(2) > a:nth-child(1)'
        super().download()

    def getContract(self):
        if not self.soup or not self.html:
            print('Error: soup is emtpy')
            return
        try:
            tag = self.soup.select_one(self.contract_selector)
            if tag: 
                self.contract = tag['data-address']

            tag = self.soup.select_one(self.icon_selector)
            if tag:
                self.icon = tag['src']

            tag = self.soup.select_one(self.explorer_selector)
            if tag:
                self.explorer = tag['href']
                domain = urlparse(self.explorer).netloc
                print (domain)

            if(self.icon and self.contract):
                return {'platform_image': self.icon, 'contract': self.contract, 'explorer': self.explorer, 'platform': platform_map[domain]}
            else:
                return None
        except Exception as e:
            print(e)
            return e