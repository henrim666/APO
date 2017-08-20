'''
Farming softeware APO
Henri F. van Maarseveen 
release Beta
'''
import argparse
#import datetime
import inspect
import logging
#import os.path
import re
import sys
#import traceback
import configparser


#Import Actions
from actions.adruino import *
from actions.stock import *
from actions.weather import *

def _findCallableActions(aClass, classDescription, validActions):
    for name, data in inspect.getmembers(aClass):
        if re.match('_',name):
            continue

        func = getattr(aClass, name, None)
        if callable(func):
            validActions[name] = (func,classDescription)
    return validActions

def  _readApplicationConfigurationFiles():
    '''
    This function is responsible for initially reading the configuration information for the application
    '''
    config = configparser.RawConfigParser()
    config.read('conf/globals.cfg')
    return config

def _parseCommandLineOptions():
    '''
    Parses command line options.
    '''
        
    parser = argparse.ArgumentParser()

    parser.add_argument("--weather"         , help="Weather information")
    parser.add_argument("--stock"           , help="Stock information")
    parser.add_argument("--adruino"         , help="Andruino data")
    parser.add_argument("--file"            , help="Filename")
    
    #arguments = parser.parse_args()
    args = parser.parse_args()
    print (args)
    return args

def main():

    # Parse command line options
    options = _parseCommandLineOptions()

    # Read global configuration file
    configparser    = _readApplicationConfigurationFiles()


    list_stock              = [9501,2190,3825,2369,3318,2395,8918,7610,7523]
    list_weather            = ['Togane','Tokyo']
    list_warnings           = ['Togane-shi','Chiba-shi']
    list_area               = ['kanto', 'tohoku','shinetsu','shinkansen']
    adruino_samples         = 2
    adruino_sampleTime      = 1
    stk=Stock(options, configparser)
    stk.get_stock(list_stock)
    #Weather().get_weather(list_weather)
    #Weather().get_weather_warning(list_warnings)
    wth=Weather(options, configparser)
    wth.get_train_info(list_area)
    adr=Adruino(options, configparser)
    adr.get_adruino(adruino_samples+1,adruino_sampleTime) 

    ##############################
    # Main process
    ##############################
    # Find all validActions in the Actions class
    validActions    = {}
    stocks         = Stock(options, configparser)
    validActions    = _findCallableActions(stocks, 'Stock Actions', validActions)

    # Find all valid actions in the SpdbEmailActions class
    adruino       =  Adruino(options, configparser)
    validActions    = _findCallableActions(adruino, 'Adruino Actions', validActions)

    # Find all SPDB FTP related actions
    weather          = Weather(options, configparser)
    validActions     = _findCallableActions(weather, 'Weather Actions', validActions)

    print(validActions)
    print(options.action)
    
    # Validate if the action is valid. Print valid actions if no valid action is found
    if (options.action not in validActions):
        logging.warn("%s is not a valid action. Please specify an action from the list below" % (options.action))
        actions = validActions.keys()

        # Group All Actions by their class descriptions
        actionsByClass = {}
        for action in actions:
            classDescription = validActions[action][1]
            if (actionsByClass.has_key(classDescription) == True):
                tmp = actionsByClass[classDescription]
                tmp.append(action)
                actionsByClass[classDescription] = tmp
            else:
                actionsByClass[classDescription] = [action]

        for classDesc in actionsByClass:
            print ("\n%s" % (classDesc))
            print ("----------------------")
            actions = actionsByClass[classDesc]
            actions.sort()
            for action in actions:
                print (action)
        sys.exit(1)



 
main()
'''
todo
earth quackes
argparser


finish
http://traininfo.jreast.co.jp/train_info/e/kanto.aspx

td id="dspdate"    for date/time

table id="traininfo" 

at the link get togane .. and then sindo !!
 
'''
