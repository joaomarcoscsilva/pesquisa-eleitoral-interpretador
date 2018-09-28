import numpy as np
import matplotlib.pyplot as plt
import json

candidatos = {
    '0': 'Álvaro Dias',
    '1': 'Cabo Daciolo',
    '2': 'Ciro Gomes',
    '3': 'Eymael',
    '4': 'Fernando Haddad',
    '5': 'Geraldo Alckmin',
    '6': 'Guilherme Boulos',
    '7': 'Henrique Meirelles',
    '8': 'Jair Bolsonaro',
    '9': 'João Amoedo',
    '10': 'João Goulart Filho',
    '11': 'Marina Silva',
    '12': 'Vera Lúcia',
    '13': 'Branco/Nulo',
    '14': 'Não sabe/Não quis responder'
}

with open('resultados.txt') as file:
    votos = json.load(file)
    
total = {}


explode = (0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05)
    
for voto in votos:
    
    if voto['hora'][1] == '7':
        continue
    
    if candidatos[voto['candidato']] in total:
        total[candidatos[voto['candidato']]] += 1
    else:
        total[candidatos[voto['candidato']]] = 1

plt.pie(total.values(), labels = total.keys(), explode=explode, autopct='%1.1f%%', wedgeprops=dict(width=1))
plt.show()
