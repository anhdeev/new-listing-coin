import json
from pycoingecko import CoinGeckoAPI

class CoinGeckoClient:
    _CG_ = CoinGeckoAPI()

    def __init__(self):
        self.api = self._CG_
        self.coinList = []
        self.coinListUpdate= []
        self.coinNumber = 0
        self._refreshCoinList();

    def _refreshCoinList(self):
        try:
            self.coinListUpdate = self.api.get_coins_list()
        except Exception as e:
            raise


    # Get platform, id, symbol,name
    def _composeMessage(self, item):
        msg = json.dumps(item)
        return msg

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
            msg = None
            self._refreshCoinList()
            newCoinNumber = len(self.coinListUpdate)

            if self.coinNumber < newCoinNumber:
                coin = self._extractNewCoin(newCoinNumber)
                if coin:
                    msg = self._composeMessage(coin)
            # update new coin list
            if self.coinNumber != newCoinNumber:
                self.coinList = self.coinListUpdate
                self.coinNumber = newCoinNumber
                print("Updated list:" + str(newCoinNumber))

            print("New token listed:" + str(msg))
            return msg
        except Exception as e:
            print(e)
            return None

########## MAIN #############
import threading

def _timer(client):
    if client:
        client.update()
    threading.Timer(60, _timer, [client]).start()

def main():
    client = CoinGeckoClient()
    _timer(client)


if __name__ == "__main__":
    main()

