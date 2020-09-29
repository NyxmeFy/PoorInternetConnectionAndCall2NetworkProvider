import speedtest
import datetime
import os
import os.path
import sys
import json
import logging
import pathlib
import time

try:
    if os.name != 'nt':
        _folderlogs = '{}/_LOGs'.format(sys.path[0])
        _mainfolder = '{}'.format(sys.path[0])
    else:
        _folderlogs = '{}\\_LOGs'.format(pathlib.Path().absolute())
        _mainfolder = '{}'.format(pathlib.Path().absolute())
    if not os.path.exists(_folderlogs):os.makedirs(_folderlogs)
    print(_folderlogs)
    print(_mainfolder)
except Exception as E: #se nao conseguir criar, fecha app
    print('erro ao criar pastas!!!!!!!!!')
    exit()

if os.name != 'nt':
    _filename = '{}/internet_log_speed.log'.format(_folderlogs) # o nome do arquivo é composto pela pasta que esta rodando + o nome do arquivo (data + '-googlesearch.log')
    configfile = '{}/config.json'.format(_mainfolder)
else:
    _filename = '{}\\internet_log_speed.log'.format(_folderlogs)
    configfile = '{}\\config.json'.format(_mainfolder)

print(_filename)
print(configfile)

with open(configfile, 'r') as f:
    config = json.load(f)

#write it back to the file
#with open('config.json', 'w') as f:
#    json.dump(config, f)

logging.basicConfig(filename=_filename, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', level=logging.DEBUG)
st = speedtest.Speedtest()
plan = config['download']
minPlan = config['downloadMin']
NetworkProvider = config['NetworkProvider']
arrayMedia = []
mediaTop = 0.0
mediaBottom = 0.0
option = int(1)
try:
    while(option != 0):
        if option == 1:
            download = st.download()
            if download <= plan*minPlan:
                print('internet ruim (<=90Mbps): {}'.format(int(download)))
                logging.info('internet abaixo dos {}% fornecido no contrato da {} (<=90Mbps): {:.2f}Mbps'.format(int(minPlan*100), NetworkProvider, download/1000000))
            else:
                print('internet boa (>90Mbps): {}'.format(int(download)))
                logging.info('internet acima dos {}% fornecido no contrato da {} (>90Mbps): {:.2f}Mbps'.format(int(minPlan*100), NetworkProvider, download/1000000))
            arrayMedia.append('{:.2f}'.format(download/1000000))
            for i in arrayMedia:
                mediaTop = mediaTop + float(i)
            mediaBottom += 1
            media = int(mediaTop)/int(mediaBottom)
            print(media)
        elif option == 2:
            print(st.upload())
        elif option == 3:
            servernames =[]
            st.get_servers(servernames)
            print(st.results.ping)
        else: 
            print("Please enter the correct choice !")
        time.sleep(60)
except KeyboardInterrupt:
    logging.info('A media de internet foi: {:.2f}'.format(media))