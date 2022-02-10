import asyncio
import json
import websockets
from datetime import datetime, timedelta
import time

file = 'Nuovo_metodo/json_completo.json'
def addResult(new): # FINITO #
    global file
    a_file = open(file, "r")
    json1 = json.load(a_file)
    json1[-2].update(new)
    a_file.close()

    b_file = open(file, "w")
    json.dump(json1, b_file)
    b_file.close()

def addMatch(new): # FINITO #
    global file
    a_file = open(file, "r")
    json1 = json.load(a_file)
    json1.append(new)
    a_file.close()

    b_file = open(file, "w")
    json.dump(json1, b_file)
    b_file.close()




def info_e_orario(data):
    global cod_prog
    global num_avv
    global new
    global ora
    global next_match
    # INFORMAZIONI E ORARIO AVVENIMENTO #
    for list in data['data']['list_menu_gv']:
        if list['sigla_sport'] == 'HGCALS':
            partita = list['menuIppicaBeanArrayList'][0]['des_avvenimento']
            ora = list['menuIppicaBeanArrayList'][0]['orario']
            next_match = list['menuIppicaBeanArrayList'][1]['orario']
            next_match = datetime.strptime(next_match, '%H:%M') - timedelta(minutes=1)
            next_match = next_match.strftime('%H:%M')
            cod_prog = list['menuIppicaBeanArrayList'][0]['cod_programma']
            num_avv = list['menuIppicaBeanArrayList'][0]['num_avvenimento']
            print('partita: ' + partita + '      ' + ora)
            new = {'partita': partita, 'orario': ora}

def quote(data):
    # QUOTE #
    for list in data['data']['cod_tipo_sco_gv']:
        evento = list['des_tipo_sco']
        for scom in list['eventi']:
            desc = scom['des_evento']
            quota = scom['quota']/100
            a = {evento+'-'+desc: quota}
            new.update(a)
            print(new)
            print(evento+'-'+desc+':    '+str(quota))
    addMatch(new)

def risultato(data):
    # RISULTATI #
    esito = data['data']['collpase_list_avvenimenti'][0]['risultato']
    risultato = {'Risultato': esito}
    addResult(risultato)
    print(risultato)

def getNextMatch(data):
    global next_match
    # INFORMAZIONI E ORARIO AVVENIMENTO #
    for list in data['data']['list_menu_gv']:
        if list['sigla_sport'] == 'HGCALS':
            partita = list['menuIppicaBeanArrayList'][1]['des_avvenimento']
            next_match = list['menuIppicaBeanArrayList'][1]['orario']
            next_match = datetime.strptime(next_match, '%H:%M') - timedelta(minutes=1)
            next_match = next_match.strftime('%H:%M')
            print('partita: ' + partita + '      ' + next_match)


async def automatico():
    m_programma = {"event":"list_menu_gv","data":{}}    # 1 richiesta

    async with websockets.connect('wss://wss.snai.it/SNWS/ssockGiochiVirtuali?q=6485d3a0c1bbc56e470f7cb2401a1c32febc1542', origin='https://www.snai.it') as websocket:
        await websocket.recv()
        
        
        await websocket.send(str(m_programma))        ##  PROGRAMMA  ##
        json_programma = await websocket.recv()
        info_e_orario(json.loads(json_programma))


        m_quote = {"event":"detail_avvenimento_gv","data":{"cod_programma":cod_prog,"num_avvenimento":num_avv}}     # 2 richiesta

        await websocket.send(str(m_quote))             ##  QUOTE  ## 
        json_quote = await websocket.recv()
        quote(json.loads(json_quote))
        

        m_risultato = {"event":"collpase_list_avvenimenti","data":{"sigla_sport":"HGCALS","date":oggi_data,"numero_lista":0}}     # 3 richiesta
        
        await websocket.send(str(m_risultato))             ##  RISULTATO  ## 
        json_risultato = await websocket.recv()
        risultato(json.loads(json_risultato))


async def avvio():
    m_programma = {"event":"list_menu_gv","data":{}}    # 1 richiesta

    async with websockets.connect('wss://wss.snai.it/SNWS/ssockGiochiVirtuali?q=6485d3a0c1bbc56e470f7cb2401a1c32febc1542', origin='https://www.snai.it') as websocket:
        await websocket.recv()
        
        
        await websocket.send(str(m_programma))        ##  PROGRAMMA  ##
        json_programma = await websocket.recv()
        getNextMatch(json.loads(json_programma))



asyncio.get_event_loop().run_until_complete(avvio()) # AVVIO PROGRAMMA #

a = True
while a == True:
    now = datetime.now()
    timer = now.strftime("%H:%M")
    if timer==next_match:
        print('in esecuzione')
        oggi_data = int(datetime.now().strftime('%Y%m%d'))    # ANNO MESE GIORNO
        asyncio.get_event_loop().run_until_complete(automatico()) # PROGRAMMA IN ESECUZIONE AUTOMATICA #
        print('FATTO!')
    else:
        print(timer)
        print(next_match)
        time.sleep(20)
        print('-')


#with open('json_data.json', 'w') as outfile:
#    outfile.write(json_risultato)









