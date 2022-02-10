const test_server = 'https://spina3.herokuapp.com/'
const host = 'https://www.sisal.it'
const url_alberatura = '/api-betting/vrol-api/vrol/palinsesto/getAlberaturaEventiSingoli/1'
const url_eventoSingolo =	'/api-betting/vrol-api/vrol/palinsesto/getDettaglioEventiSingoli/1/'

async function esegui(){
    document.getElementById("partita").innerHTML = 'Partita: Caricamento...'
    document.getElementById("ora").innerHTML = 'Orario di inizio: Caricamento...'
    document.getElementById("prob_1").innerHTML = '1: Caricamento...'
    document.getElementById("prob_X").innerHTML = 'X: Caricamento...'
    document.getElementById("prob_2").innerHTML = '2: Caricamento...'
    document.getElementById('best_match').innerHTML = '<div style="margin-top: 1rem;">Migliori partite da giocare:</div>'
    const avventimento = await getEvento()
    palinsesto = avventimento[0]
    evento = avventimento[1]
    url_evento = host + url_eventoSingolo +  palinsesto + '/' + evento
    json_odds = await getOdds(url_evento)
    json = await apiCall(json_odds) 
    
    document.getElementById("partita").innerHTML = 'Partita: ' + json.casa + ' - ' + json.ospite
    document.getElementById("ora").innerHTML = 'Orario di inizio: ' + json.orario
    if(json.pred != 0){
        document.getElementById("risultato").innerHTML = 'Risultato: ' + json.pred
    } else {
        document.getElementById("risultato").innerHTML = 'Risultato: X'
    }    
    document.getElementById("prob_1").innerHTML = '1: ' + (json.prob_1 * 100).toFixed(2) + '%'
    document.getElementById("prob_X").innerHTML = 'X: ' + (json.prob_X * 100).toFixed(2) + '%'
    document.getElementById("prob_2").innerHTML = '2: ' + (json.prob_2 * 100).toFixed(2) + '%'
    
    console.clear()
    
    result = await getOddsNextMatch(url_evento)
    for(array of result){
        if(array.prob_1 >= 0.6 || array.prob_2 >= 0.6 || array.prob_X >= 0.6){
            if(array.pred != 0){
                document.getElementById('best_match').innerHTML += '<div style="margin-top: 1rem;"> ' + array.orario + ' ' + array.casa + ' - ' + array.ospite + ' : ' + array.pred + '</div>'
            } else {
                document.getElementById('best_match').innerHTML += '<div style="margin-top: 1rem;"> ' + array.orario + ' ' + array.casa + ' - ' + array.ospite + ' : X</div>'
            }    
        }
        console.log(prob_1, prob_2, prob_X)
        
        
    }
    
    
}

async function apiCall(json_odds){
    url = 'https://spina3.herokuapp.com/post'
    console.log(json_odds)
    response = await fetch(
        url, {
            method: 'POST',
            headers: {  
                'Content-Type': 'application/json', 
            },
            body: JSON.stringify(json_odds) 
        }
        )
        
        return response.json()
    }
    
async function getEvento(){
    response = await fetch(host+url_alberatura)
    data = await response.json()
    data.forEach(
        element => {
            if(element.descrdisc == 'Football'){
                dati_1 = element.sogeicodpalinsesto
                dati_2 = element.sogeicodevento
                
            }
        }
    )
    return [dati_1, dati_2]
}

async function getOddsNextMatch(url){
    response = await fetch(url)
    data = await response.json()
    array = []
    data.forEach( element => {
        squadra_casa = element.playerVirtualeList[0].name
        squadra_ospite = element.playerVirtualeList[1].name
        orario = element.formattedOrario
        json_odds = [{'casa': squadra_casa, 'ospite': squadra_ospite, 'orario': orario}]
        element.scommessaVirtualeBaseList.forEach(
            element => {
                descrizione = element.descrizione
                element.esitoVirtualeList.forEach(
                    element => {
                        desc = element.descrizione
                        quota = element.quota / 100
                        quota_desc = descrizione+desc
                        json_odds[0][quota_desc] = quota
                    }
                )
            }
        )
        array.push(json_odds) 
    })

    array_result = []
    for (match of array){
        quota_1 = match[0]['1X2 Finale1']
        quota_X = match[0]['1X2 FinaleX']
        quota_2 = match[0]['1X2 Finale2']
        json = await apiCall(match)
        if(json.pred == '1'){
            quota = quota_1
        }else if(json.pred == '0'){
            quota = quota_X
        }else if(json.pred == '2'){
            quota = quota_2
        }
        if(quota >= 2){
            json['quota'] = quota
            array_result.push(json)
        }
    }
    
    return array_result
}
        
async function getOdds(url){
    response = await fetch(url)
    data = await response.json()
    squadra_casa = data[0].playerVirtualeList[0].name
    squadra_ospite = data[0].playerVirtualeList[1].name
    orario = data[0].formattedOrario
    json_odds = [{'casa': squadra_casa, 'ospite': squadra_ospite, 'orario': orario}]
    data[0].scommessaVirtualeBaseList.forEach(
        element => {
            descrizione = element.descrizione
            element.esitoVirtualeList.forEach(
                element => {
                    desc = element.descrizione
                    quota = element.quota / 100
                    quota_desc = descrizione+desc
                    json_odds[0][quota_desc] = quota
                }
            )
        }
    )
       
    return json_odds 
}
                
                
                
                
async function test(){
    response = await fetch(test_server)

    if(response.status === 200){
        document.getElementById("status").innerHTML = 'ONLINE'
        console.log('ONLINE')
    }else{
        document.getElementById("status").innerHTML = 'OFFLINE'
        console.log('OFFLINE')
    }
}