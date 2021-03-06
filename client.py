import requests  # pip install requests
import json
import hashlib
import hmac
import time #for nonce
import os

class BitfinexClient(object):
    BASE_URL = "https://api.bitfinex.com/"
    KEY = os.getenv('BF_API_KEY')
    SECRET = os.getenv('BF_API_SECRET')


    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(int(round(time.time() * 1000)))


    def _headers(self, path, nonce, body):

        signature = "/api/" + path + nonce + body
        print("Signing: " + signature)
        h = hmac.new(self.SECRET.encode('utf8'), signature.encode('utf8'), hashlib.sha384)
        signature = h.hexdigest()

        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.KEY,
            "bfx-signature": signature,
            "content-type": "application/json"
        }


    def active_orders(self):
        """
        Fetch active orders
        """
        nonce = self._nonce()
        body = {}
        rawBody = json.dumps(body)
        path = "v2/auth/r/orders"


        print(self.BASE_URL + path)
        print(nonce)


        headers = self._headers(path, nonce, rawBody)

        print(headers)
        print(rawBody)


        print("requests.post("+self.BASE_URL + path + ", headers=" + str(headers) + ", data=" + rawBody + ", verify=True)")
        r = requests.post(self.BASE_URL + path, headers=headers, data=rawBody, verify=True)

        if r.status_code == 200:
          return r.json()
        else:
          print(r.status_code)
          print(r)
          return ''


    def funding_offers(self,symbol):
        """
        Fetch funding offers
        """
        nonce = self._nonce()
        body = {}
        rawBody = json.dumps(body)
        path = "v2/auth/r/funding/offers/" + str(symbol)

        headers = self._headers(path, nonce, rawBody)

        print("requests.post("+self.BASE_URL + path + ", headers=" + str(headers) + ", data=" + rawBody + ", verify=True)")
        r = requests.post(self.BASE_URL + path, headers=headers, data=rawBody, verify=True)

        if r.status_code == 200:
          return r.json()
        else:
          print(r.status_code)
          print(r)
          return ''


    def submit_funding_offer(self,funding_type,symbol,amount,rate,period,flags):
        """
        Fetch funding offers
        """
        nonce = self._nonce()
        body: {
                'type': funding_type,
                'symbol': symbol,
                'amount': amount,
                'rate': rate,
                'period': period,
                'flags': flags
            }
        rawBody = json.dumps(body)
        path = "v2/auth/r/funding/offers/submit"

        print(self.BASE_URL + path)
        print(nonce)

        headers = self._headers(path, nonce, rawBody)

        print(headers)
        print(rawBody)

        print("requests.post("+self.BASE_URL + path + ", headers=" + str(headers) + ", data=" + rawBody + ", verify=True)")
        r = requests.post(self.BASE_URL + path, headers=headers, data=rawBody, verify=True)

        if r.status_code == 200:
          return r.json()
        else:
          print(r.status_code)
          print(r)
          return ''


if __name__ == "__main__":
    # print(BitfinexClient().active_orders())
    print(BitfinexClient().funding_offers('USD'))
    # print(BitfinexClient().submit_funding_offer(' LIMIT','fUSD','30','0.001',2,0))