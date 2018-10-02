import numpy as np
import matplotlib.pyplot as plt
import json
import operator

generos = {
    '0': 'Masculino',
    '1': 'Feminino'
}

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
    '14': 'Não sabe/Não quis responder',
    '15': 'Votaria em Qualquer Candidato'
}

classes = {
    '0': 'A',
    '1': 'B',
    '2': 'C',
    '3': 'D',
    '4': 'E',
    '5': 'Não quis responder'
}

with open('resultados.txt') as file:
    votos = json.load(file)

def increment(dict, key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1

entrevistados = len(votos)
        
total = {}
total_generos = {}
total_classes = {}

rej_total = {}
rej_total_generos = {}
rej_total_classes = {}

porc_generos = {}
porc_classes = {}

for voto in votos:
    if voto['hora'][1] == '7':
        continue

    votou = candidatos[voto['candidato']]
    
    increment(total, votou)

    for g in generos:
        genero = generos[g]
        if genero not in total_generos:
            total_generos[genero] = {}
        if voto['genero'] == g:
            increment(total_generos[genero], votou)
            increment(porc_generos, genero)
        
    for c in classes:
        classe = classes[c]
        if classe not in total_classes:
            total_classes[classe] = {}
        if voto['classe'] == c:
            increment(total_classes[classe], votou)
            increment(porc_classes, classe)
            
    
    if len(voto['rejeita']) == 0:
        rejeitado = candidatos['15']
        
        increment(rej_total, rejeitado)
        
        for g in generos:
            genero = generos[g]
            if genero not in rej_total_generos:
                rej_total_generos[genero] = {}
            if voto['genero'] == g:
                increment(rej_total_generos[genero], rejeitado)
            
        for c in classes:
            classe = classes[c]
            if classe not in rej_total_classes:
                rej_total_classes[classe] = {}
            if voto['classe'] == c:
                increment(rej_total_classes[classe], rejeitado)
        
        
    for rejeicao in voto['rejeita']:
        rejeitado = candidatos[str(rejeicao)]
        
        increment(rej_total, rejeitado)
        
        for g in generos:
            genero = generos[g]
            if genero not in rej_total_generos:
                rej_total_generos[genero] = {}
            if voto['genero'] == g:
                increment(rej_total_generos[genero], rejeitado)
            
        for c in classes:
            classe = classes[c]
            if classe not in rej_total_classes:
                rej_total_classes[classe] = {}
            if voto['classe'] == c:
                increment(rej_total_classes[classe], rejeitado)
        

explode = 0.01    

def make_autopct(total):
    def my_autopct(pct):
        val = int(round(pct*total/100.0))
        return '{p:1.1f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct
    
def plot(title, l, size = 5, total = entrevistados, folder = ''):
    fig1, ax1 = plt.subplots()
    plt.title(title, fontsize = 20)
    
    fig1.set_size_inches(size, size, forward = True)
    data = np.transpose([list(elem) for elem in sorted(l.items(), key=operator.itemgetter(1), reverse=True)])
    plt.pie(data[1], labels = data[0], explode = (explode,) * len(data[1]), autopct = make_autopct(total))
    
    path = 'generated\\' + folder + '\\' + title
    
    plt.savefig(path, bbox_inches='tight')

def plotBar(title, l, size = 5, total = entrevistados, folder = ''):
    fig1, ax1 = plt.subplots()
    
    plt.title(title, fontsize = 20)
    
    fig1.set_size_inches(size, size, forward = True)
    data = np.transpose([list(elem) for elem in sorted(l.items(), key=operator.itemgetter(1), reverse=True)])
    
    plt.barh(range(0, len(data[1])), [(int(elem)/total)*100 for elem in data[1]])
    
    ax1.set_yticks(range(0, len(data[0])))
    ax1.set_yticklabels(data[0])    
    
    for i, v in enumerate([(int(elem)/total)*100 for elem in data[1]]):
        ax1.text(v+1, i-0.2, str(int(v)) + '%')
    
    path = 'generated\\' + folder + '\\' + title
    plt.savefig(path, bbox_inches='tight')
    




    
plot('Proporção entre Homens e Mulheres', porc_generos)
plot('Proporção entre Classes Sociais', porc_classes)

plot('Resultados Gerais', total, 9)
plot('Resultados entre os Homens', total_generos['Masculino'], 9, porc_generos['Masculino'], 'genero')
plot('Resultados entre as Mulheres', total_generos['Feminino'], 9, porc_generos['Feminino'], 'genero')

for classe in total_classes:
    if classe == 'Não quis responder':
        continue
    plot('Resultados entre membros da classe ' + classe, total_classes[classe], 9, porc_classes[classe], 'classe')


plotBar('Rejeição Geral', rej_total, folder = 'rejeicao')
plotBar('Rejeição Entre os Homens', rej_total_generos['Masculino'], total = porc_generos['Masculino'], folder = 'rejeicao\\genero')
plotBar('Rejeição Entre as Mulheres', rej_total_generos['Feminino'], total = porc_generos['Feminino'], folder = 'rejeicao\\genero')
    
print('Total de entrevistados: ' + str(entrevistados))

for classe in total_classes:
    if classe == 'Não quis responder':
        continue
    plotBar('Rejeição entre membros da classe ' + classe, rej_total_classes[classe], total = porc_classes[classe], folder = 'rejeicao\\classe')
    