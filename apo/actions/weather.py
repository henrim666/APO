import time

from conf.config import *
from conf.constants import *
from modules.data_cleaning import *
from modules.data_output import *
from modules.get_internet_data import getInternetData


class Weather(object):

    def __init__(self, options, config):
        self.options = options
        self.config  = config
    
    def get_weather(self,list_weather): 
        proxy_connection=getInternetData()._proxy_settings(PROXY)
        for place in list_weather:
            json_place_weather_data = getInternetData()._get_json_url_data(proxy_connection,URL_WEATHER,place)
            raw_weather_data=dataCleaning()._convert_json_to_weather_data(json_place_weather_data)
            dataOutput()._print_list(raw_weather_data)   
            tag_list=dataCleaning()._split_stock_tags(raw_weather_data) 
        dataOutput()._print_list(tag_list)     
        
    def get_weather_warning(self,list_warnings):
        proxy_connection=getInternetData()._proxy_settings(PROXY)
        raw_table_warning_data =    getInternetData()._get_table_url_data(proxy_connection,URL_WARNING,WARNING_LIST_HTML_TABLE)
        for wanted_place in list_warnings:
            table_warning_data =    dataCleaning()._get_wanted_warning_table(raw_table_warning_data,SPLIT_FOR_URL_WARNING,wanted_place)
            list_of_advisorie = dataCleaning()._get_wanted_advisories_list(table_warning_data,wanted_place,SPLIT_FOR_ADVISORIES)
            dataOutput()._print_list(list_of_advisorie)
            tag_list=dataCleaning()._split_stock_tags(list_of_advisorie)
        dataOutput()._print_list(tag_list)

    def get_train_info(self,list_area):         
        proxy_connection=getInternetData()._proxy_settings(PROXY)
        for area in list_area:
            list_trains=[]
            dataOutput()._print_list(area)
            raw_table_train_time_data = getInternetData()._get_area_time_table_train_data(proxy_connection,URL_TRAIN,TRAIN_TABLE_TIME,area)
            raw_table_train_data = getInternetData()._get_area_info_table_train_data(proxy_connection,URL_TRAIN,TRAIN_TABLE_INFO_NOK,area)
            #dataOutput()._print_list(raw_table_train_data)
            list_trains_in_trouble = dataCleaning()._clean_train_list_in_trouble(raw_table_train_data,list_trains)
            dataOutput()._print_list(list_trains_in_trouble)
            #dataOutput()._print_list(raw_table_train_time_data)
            #dataOutput()._print_list(raw_table_train_data)
        #dataOutput()._print_list(list_trains)    
        #dataOutput()._print_list(list_area)       
            
