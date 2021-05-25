import json
from pycoingecko import CoinGeckoAPI
from crawler import CgCrawler
from simple_telegram_bot import TeleBot
from formatter import formatString
import time

class CoinGeckoClient:
    def __init__(self):
        self.api = CoinGeckoAPI()
        self.tele = TeleBot()
        self.coinList = []
        self.coinListUpdate= []
        self.coinNumber = 0
        self._refreshCoinList();
        self.waiting = []
        time.sleep(30)

    def _refreshCoinList(self):
        try:
            self.coinListUpdate = self.api.get_coins_list()
            self.coinNumber = len(self.coinListUpdate)
        except Exception as e:
            print(e)


    # Get platform, id, symbol,name
    def _getDetail(self, item):
        rst = None
        tokenId = item['id']
        print ('Get coin data: ' + tokenId)
        # Get data via API
        rst = self.api.get_coin_by_id(tokenId, localization="false", tickers="false", market_data="false", community_data="false", developer_data="false")
        if rst.get('error'):
            print('Error: ' + rst.get('error') + ' , appending to waiting list')
            self.waiting.append(tokenId)
            return None
        # Get data via crawler
        # cg = CgCrawler(tokenId)
        # data2 = cg.getContract()

        # if(not data2):
        #     rst = tokenId + ' is not a token!'
        # else:
        #     rst = {**data1[0], **data2}

        data2 = self.api.get_coins_markets('usd', ids=tokenId)
        if len(data2) >= 1:
            rst['image'] = data2[0].get('image')
            rst['current_price'] = data2[0].get('current_price')
            rst['market_cap'] = data2[0].get('market_cap')
            rst['high_24h'] = data2[0].get('high_24h')
            rst['low_24h'] = data2[0].get('low_24h')
            rst['ath'] = data2[0].get('ath')
            rst['total_supply'] = data2[0].get('total_supply')
            rst['circulating_supply'] = data2[0].get('circulating_supply')

        return rst

    def _getPrice(self, coinId):
        pass

    def _extractNewCoin(self, length):
        index = 0
        while index < length:
            if index >= self.coinNumber:
                return self.coinListUpdate[index]
            if self.coinList[index]['id'] != self.coinListUpdate[index]['id']:
                return self.coinListUpdate[index]
            index += 1

        return None

    def update(self):
        try:
            #print("Updating....")
            rst = None
            self._refreshCoinList()
            newCoinNumber = len(self.coinListUpdate)

            if self.coinNumber != newCoinNumber:
                coin = self._extractNewCoin(newCoinNumber)
                if coin:
                    rst = self._getDetail(coin)
                # update new coin list
                self.coinList = self.coinListUpdate
                self.coinNumber = newCoinNumber
                print("Updated list:" + str(newCoinNumber))
            else:
                if len(self.waiting) > 0:
                    print('Retry for ', self.waiting[0])
                    rst = self._getDetail({'id':self.waiting[0]})
                    if rst:
                        self.waiting.pop(0)
            if rst:
                print("Result: " + str(rst))
            return rst
        except Exception as e:
            print(e)
            return None

########## MAIN #############
import threading

def _timer(client):
    try:
        if client:
            rst = client.update()
            if rst and type(rst) is dict:
                formatted_msg = formatString({
                    'platform': rst.get('asset_platform_id'),
                    'explorer': rst['links']['blockchain_site'][0] if len(rst['links']['blockchain_site']) > 0 else "n/a",
                    'name': rst.get('name'),
                    'symbol': rst.get('symbol'),
                    'image': rst.get('image'),
                    'contract': rst.get('contract_address'),
                    'id': rst.get('id'),
                    'circulating_suply': rst.get('circulating_suply'),
                    'total_suply': rst.get('total_supply'),
                    'market_cap': rst.get('market_cap'),
                    "current_price": rst.get('current_price'),
                    "high_24h": rst.get('high_24h'),
                    "low_24h": rst.get('low_24h')
                })
                #print(formatted_msg)
                client.tele.send(formatted_msg, True)
            else:
                pass
        threading.Timer(60, _timer, [client]).start()
    except Exception as e:
        print(e)

def main():
    client = CoinGeckoClient()
    _timer(client)


if __name__ == "__main__":
    main()

