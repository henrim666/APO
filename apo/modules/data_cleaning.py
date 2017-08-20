from datetime import datetime


class dataCleaning():
    
    def __init__(self):
        pass

#
# Public functions    
#
    
    def _convert_json_to_stock_data(self,stock_data):
        List_of_stock_data=[]
        str_data=str(stock_data)
        str_data=str_data.replace('" : "',':').replace('":"',':').replace('": "',':')
        words=str_data.split('"')
        word_counter=-1
        for word in words:
            word_counter+=1
            if word_counter > 1 :
                if (word_counter % 2 != 0):
                    filtered_word=str(word)
                    List_of_stock_data.append(filtered_word)
        return List_of_stock_data           
    
    def _convert_json_to_weather_data(self,weather_data):
        str_weather_data= str(weather_data)  
        str_weather_data=str_weather_data[3:][:-3].replace('{',' ').replace(',',' ').replace('}','')
        str_weather_data=str_weather_data.replace('[','').replace('{','').replace(']','').replace('  ',' ').replace('":"',':').replace('":',':')
        str_weather_data=str_weather_data.replace(' "','" "').replace('""','"')
        str_weather_data=str_weather_data[3:-2] 
        List_of_weather_data = str_weather_data.split('" "')
        return List_of_weather_data 

    def _add_column_to_train_list(self,list_trains_in_trouble):
        
        return list_trains_in_trouble
    
    def _get_wanted_warning_table(self,raw_table_warning_data,split_chars,wanted_place):
        str_raw_table_warning_data=str(raw_table_warning_data)
        table_warning_data=str_raw_table_warning_data.split(split_chars)
        for table in table_warning_data:
            a=str(table)
            correct_place=a.find(wanted_place)
            if correct_place>-1:
                return table 

    def _get_wanted_advisories_list(self,table_warning_data,wanted_place,find_advisories):
        span_split=table_warning_data.split('span')
        tag_place='city:'+wanted_place
        list_of_advisorie=[tag_place]
        for span in span_split:
            advisories=str(span)
            advisories_wanted=advisories.find(find_advisories)
            if advisories_wanted>-1:
                advisorie = str(advisories[advisories.find('>')+1:]).replace('</','')
                tag_advisorie = 'advisorie:'+advisorie
                list_of_advisorie.append(tag_advisorie)
        return list_of_advisorie     
    
    def _get_sensor_data(self,raw_serial_data,list_sensor_data):
        cleaner_serial_data=raw_serial_data.replace("\r\n'","").replace(': ',':').replace("b'","")
        cleaner_serial_data=' '.join(cleaner_serial_data.split())
        cleaner_serial_data=cleaner_serial_data.replace('0 %','0%').replace('0 *C','0*C')
        sensor_serial_data=cleaner_serial_data.split(' ')
        for sensor_data in sensor_serial_data:
            non_data=sensor_data.find(':')
            if non_data==-1:
                sensor_data='metadata:'+sensor_data
            list_sensor_data.append(sensor_data)
        return list_sensor_data   
            
    #read structure and create a table if table does exist skip (parameter create).
    def _clean_stock_data(self,stock_data):
        clean_stock_data = []
        for tages in stock_data:
            tag = str(tages[:tages.find(':')])
            value = str(tages[tages.find(':')+1:])
            #remove the first 4 char because of unicode yen symbol
            if tag == 'l_cur':
                value=value[3:]
            #2:41PM GMT+9 remove the timezone
            if tag == 'ltt':
                value=value[:-6]
                date_time=datetime.strptime(value,'%I:%M%p')
                value=date_time.strftime('%H:%M:%S')
            #Mar 11, 2:41PM GMT+9 remove the timezone   
            if tag == 'lt':
                value=value[:-6]
                date_time=datetime.strptime(value,'%b %d, %I:%M%p')
                year=str(datetime.now().strftime('%Y'))
                value=date_time.strftime(year+'-%m-%d %H:%M:%S')
            parameter= tag + ':' + value
            clean_stock_data.append(parameter)        
        return clean_stock_data
    
    def _clean_train_list_in_trouble(self,raw_table_train_data,list_trains):
        raw_html_data = str(raw_table_train_data)
        raw_html_data=raw_html_data.split('<')
        for lines in raw_html_data:
            lines_ok=1
            line1='td id="dspdate" class="text-m r">'
            line2='td class="head-m2">'
            line3='align="center" class="td-w2">'
            line4='td class="td-w-dot">'
            line5='td class="td-w">'
            line_ok1=lines.find(line1)
            if line_ok1>-1:
                lines_ok=0
            line_ok2=lines.find(line2)
            if line_ok2>-1:
                lines_ok=0
            line_ok3=lines.find(line3)
            if line_ok3>-1:
                lines_ok=0
            line_ok4=lines.find(line4)
            if line_ok4>-1:
                lines_ok=0
            line_ok5=lines.find(line5)
            if line_ok5>-1:
                lines_ok=0
            if lines_ok==0: 
                word_counter=1
                toomany_lines=lines.split('>')
                for wanted_lines in toomany_lines:
                    word_counter+=1
                    if (word_counter % 2 != 0):
                        filtered_word=str(wanted_lines)
                        list_trains.append(filtered_word)
        return list_trains
    
    def _split_stock_tags(self,stock_data):
        name_list=[]
        for tags in stock_data:
            #if : is last char then drop element (because it is a sub header)
            tag = str(tags[:tags.find(':')])
            setlist = set(name_list)
            if tag not in setlist:
                name_list.append(tag)
        return  name_list
