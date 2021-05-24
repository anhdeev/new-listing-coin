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
        time.sleep(30)

    def _refreshCoinList(self):
        try:
            self.coinListUpdate = self.api.get_coins_list()
            #self.coinNumber = len(self.coinListUpdate)
        except Exception as e:
            print(e)


    # Get platform, id, symbol,name
    def _getDetail(self, item):
        tokenId = item['id']
        print ('Get coin data: ' + tokenId)
        # Get data via API
        data1 = self.api.get_coins_markets('usd', ids=tokenId)
        if len(data1) < 1:
            print('Can not get data: ' + tokenId)
            return None
        # Get data via crawler
        cg = CgCrawler(tokenId)
        data2 = cg.getContract()

        if(not data2):
            rst = tokenId + ' is not a token!'
        else:
            rst = {**data1[0], **data2}

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
            print("Updating....")
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
            if type(rst) is dict:
                formatted_msg = formatString({
                    'platform': rst.get('platform'),
                    'platform_image': rst.get('platform_image'),
                    'explorer': rst.get('explorer'),
                    'name': rst.get('name'),
                    'symbol': rst.get('symbol'),
                    'image': rst.get('image'),
                    'contract': rst.get('contract'),
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

