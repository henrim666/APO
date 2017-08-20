from urllib.request import build_opener, install_opener, ProxyHandler, \
    HTTPHandler

from errors.url_errors import *
import conf.constants
import urllib.request as request


#from bs4 import BeautifulSoup
#import unicodedata 
class getInternetData():
    
    def __init__(self):
        pass

#
# Public functions    
#
    def _proxy_settings(self,proxy):
        proxies = {"http":"http://%s" % proxy}
        proxy_support = ProxyHandler(proxies)
        return proxy_support
    
    #getdata factory
    def _get_json_url_data(self,proxy_support,url,list_element):    
        opener = build_opener(proxy_support, HTTPHandler(debuglevel=1))
        install_opener(opener)
        try:
            lines = request.urlopen(url.format(list_element)).readlines()
            return lines
        except:
            return URL_ERROR_0        
    
    def _get_table_url_data(self,proxy_support,url,wanted_table):    
        opener = build_opener(proxy_support, HTTPHandler(debuglevel=1))
        install_opener(opener)
        try:
            raw_html_data = request.urlopen(url).readlines()
            for table in raw_html_data:
                correct_table=str(table).find(wanted_table)
                if correct_table>-1:
                    return table 
            return raw_html_data
        except:
            return URL_ERROR_0        
        

    def _get_area_time_table_train_data(self,proxy_support,url,wanted_table,area):    
        opener = build_opener(proxy_support, HTTPHandler(debuglevel=1))
        install_opener(opener)
        url=url.replace('{}',area)
        try:
            raw_html_data = request.urlopen(url).readlines()
            for table in raw_html_data:
                correct_table=str(table).find(wanted_table)
                if correct_table>-1:
                    return table 
            return raw_html_data
        except:
            return URL_ERROR_0        
            
    def _get_area_info_table_train_data(self,proxy_support,url,wanted_tables,area):    
        opener = build_opener(proxy_support, HTTPHandler(debuglevel=1))
        install_opener(opener)
        url=url.replace('{}',area)
        try:
            raw_html_data = request.urlopen(url).read()
            return raw_html_data
            #error=0
        except:
            return URL_ERROR_0