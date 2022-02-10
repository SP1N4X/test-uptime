import requests
import json

def getHash():
    s = requests.get('https://www.snai.it/virtuali')

    if s.url == 'https://www.snai.it/virtuali':
        print('eseguito correttamente')
        #f = open('html.text', 'w')
        #f.write(s.text)
        #f.close
        #f1 = open('html.text', 'r')
        #text = f1.read()
        text = s.text
        for split in text.split('script'):
            if 'hash' in split:
                file = split.replace('jQuery.extend(Drupal.settings, ','').replace(');</','').replace('>','')
                #with open('json_json.json', 'w') as outfile:
                #    outfile.write(file)
                #with open('json_json.json') as json_file:
                #    data = json.load(json_file)
                data = json.loads(file)
                hash = data['snai_angular_integration']['web_socket_url_hash']
                return hash
    else:
        rtext = 'Confermare captcha, url: ' + str(s.url)
        print(rtext)
        return 'CAPTCHA'