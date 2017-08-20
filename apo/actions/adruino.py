import time

from conf.config import *
from conf.constants import *
from modules.data_cleaning import *
from modules.data_output import *
from modules.get_IO_data import GetIOData


class Adruino(object):

    def __init__(self, options, config):
        self.options = options
        self.config  = config

#
# Public functions    
#
    
    def get_adruino(self,samples,sampletime):
        list_sensor_data=[]
        for sample in range(1,samples):
            time.sleep(sampletime)
            raw_serial_data=GetIOData()._get_serial_data(ADRUINO_COM,ADRUINO_BAUDRATE,MODE,sample)
            sensor_data=dataCleaning()._get_sensor_data(raw_serial_data,list_sensor_data)
            tag_list=dataCleaning()._split_stock_tags(sensor_data)
        dataOutput()._print_list(sensor_data)
        dataOutput()._print_list(tag_list) 