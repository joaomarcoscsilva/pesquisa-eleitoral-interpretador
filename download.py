from kinto_http import Client

client = Client(server_url="https://kinto-pesquisa.herokuapp.com/v1",
                auth=('Joao', 'Joao'))
                
collections = client.get_collections(bucket = 'pesquisa')

class Voto:
    def __init__(this):
        this.pesquisador = ''
        
        this.genero = 0
        this.classe = 0
        
        this.candidato = 0
        this.rejeita = []
        
        this.hora = ''
        
    def __tojson__(this):
        r = '{'
        r += '\n"pesquisador": "' + str(this.pesquisador)
        r += '",\n"genero": "' + str(this.genero)
        r += '",\n"classe": "' + str(this.classe)
        r += '",\n"candidato": "' + str(this.candidato)
        r += '",\n"rejeita": ' + json.dumps(this.rejeita)
        r += ',\n"hora": "' + this.hora
        r += '"\n}'
        
        return r
votos = []

        
def getVotosString():
    result = '[\n'
    
    i = 0
    
    for voto in votos:
        result += voto.__tojson__()
        if i < len(votos) - 1:
            result += ','
        result += '\n'
        
        i += 1
    
    result += ']'
    
    return result

for collection in collections:
    name = collection['id']
    
    print(name + '...')
        
    record_list = client.get_records(collection=name, bucket='pesquisa')
    records = record_list[0]['info']
    
    if len(record_list) > 1:
        print ('found ' + str(len(record_list)) + ' entries.')
    
    for record in records:
        voto = Voto()
        
        voto.pesquisador = name
        
        voto.genero = record['genero']
        voto.classe = record['classe_social']
        
        voto.candidato = record['candidato']
        voto.rejeita = record['rejeita']
        
        voto.hora = record['criado_em']
        
        votos.append(voto)
        
import json

file = open('resultados.txt', 'w')
file.write(getVotosString())
file.close()