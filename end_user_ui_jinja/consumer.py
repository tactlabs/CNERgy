'''

Created on 

Course work: 

@author: raja

Source:
    
'''

# Import necessary modules
import requests
# import os

# Local

class Client(object):

    def __init__(self):

        self.api_base = "http://annotator_prediction:5050"

    # def _append_api_key(self, url, s_id = None):

    #     if('?' in url):

    #         url = url + '&' + 'api_key=' + self.api_key
    #         if s_id:

    #             url = url + '&' + 'sid=' + s_id

    #         return url
        
    #     url = url + '?' + 'api_key=' + self.api_key
    #     if s_id:
    #         url = url + '&' + 'sid=' + s_id

    #     return url
        

    def process_get(self, url):

        # url = self._append_api_key(url, s_id)

        final_url = self.api_base + url

        resp = requests.get(final_url)
        
        return resp.json()

    # def process_post(self, url, data, s_id = None):

    #     url = self._append_api_key(url, s_id)

    #     final_url = self.api_base + url

    #     resp = requests.post(final_url, json = data)
        

    #     return resp.json() 