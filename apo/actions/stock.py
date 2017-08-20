from conf.config import *
from conf.constants import *
from modules.data_cleaning import *
from modules.data_output import *
from modules.get_internet_data import getInternetData


class Stock():

    def __init__(self, options, config):
        self.options = options
        self.config  = config

#
# Public functions    
#

    def get_stock(self,list_stock): 
        proxy_connection=getInternetData()._proxy_settings(PROXY)
        for quote in list_stock:
            json_quote_data = getInternetData()._get_json_url_data(proxy_connection,URL_STOCK,quote)
            raw_stock_data=dataCleaning()._convert_json_to_stock_data(json_quote_data)
            tag_list=dataCleaning()._split_stock_tags(raw_stock_data)
            clean_stock_data=dataCleaning()._clean_stock_data(raw_stock_data)
            dataOutput()._print_list(clean_stock_data)
        dataOutput()._print_list(tag_list)      