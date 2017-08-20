import serial

from errors.url_errors import *

class GetIOData():

    def __init__(self):
        pass
    #test data if serial device is not connected
    TEST_DATA_DHT11_0       = "b'DHT11 test!\r\n'"
    TEST_DATA_DHT11_1       = "b'Humidity: 34.00 %\tTemperature: 23.00 *C\r\n'"

#
# Public functions    
#

    def _get_serial_data(self,com,baudrate,TEST_MODE,TEST_PARAMETER_TELLER_01): 
        if TEST_MODE==False:
            try:
                serial_data=serial.Serial(com,baudrate).readline()
            except:
                return SERIAL_ERROR_0
        if TEST_MODE==True :
            if (TEST_PARAMETER_TELLER_01 != 1):
                serial_data=self.TEST_DATA_DHT11_1
                return serial_data
            if (TEST_PARAMETER_TELLER_01 == 1):
                serial_data=self.TEST_DATA_DHT11_0
                TEST_PARAMETER_TELLER_01+=1
                return serial_data        