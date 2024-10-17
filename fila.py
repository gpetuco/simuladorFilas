import random

class Fila:
    perdas = 0
    estadoAtual = 0
    tempoUltimoEvento = 0
    
    def __init__(self, nomeFila, probProxFila, probMesmaFila, probSairFila, numeroServidores, capacidade, chegada, tempoSaida, timer):
        self.nomeFila = nomeFila
        self.probProxFila = float(probProxFila)
        self.probMesmaFila = float(probMesmaFila)
        self.probSairFila = float(probSairFila)
        self.numeroServidores = int(numeroServidores)
        self.capacidade = int(capacidade)
        self.estados = {i: 0 for i in range(self.capacidade + 1)}
        self.tempoMinimoChegada = int(chegada[0])
        self.tempoMaximoChegada = int(chegada[1])
        self.tempoMinimoSaida = int(tempoSaida[0])
        self.tempoMaximoSaida = int(tempoSaida[1])
        self.perdas = 0
        self.estadoAtual = 0
        self.timer = timer

    def getNome(self):
        return self.nomeFila
       
    def getEstados(self):
        return self.estados

    def getPerdas(self):
        return self.perdas
        
    ##########################################################

    def probabilidade(self):
        return random.uniform(0,1)
  
    def calculaTempoChegada(self,geraNumeros):
        return (self.tempoMaximoChegada - self.tempoMinimoChegada) * geraNumeros.geraNumero() + self.tempoMinimoChegada
    
    def calculaTempoSaida(self,geraNumeros):
        return (self.tempoMaximoSaida - self.tempoMinimoSaida) * geraNumeros.geraNumero() + self.tempoMinimoSaida
      
    def agendarChegada(self,time,incremento_tempo,eventos):
        if self.nomeFila == 'F1':
            eventos.append({'Fila':self.nomeFila,
                           'evento':'chegada',
                           'time':time + incremento_tempo,
                           'incremento_tempo':incremento_tempo})
    
    def agendarSaida(self,time,incremento_tempo,eventos):
        eventos.append({'Fila':self.nomeFila,
                       'evento':'saida',
                       'time':time + incremento_tempo,
                       'incremento_tempo':incremento_tempo})
        if(self.probabilidade() < self.probProxFila):
            string = self.nomeFila
            new = int(string.replace('F',''))
            new += 1
            new = 'F'+str(new)
            eventos.append({'Fila':new,
                           'evento':'chegada',
                           'time':time + incremento_tempo,
                           'incremento_tempo':incremento_tempo})
        elif(self.probMesmaFila > 0):
            eventos.append({'Fila':self.nomeFila,
                           'evento':'chegada',
                           'time':time + incremento_tempo,
                           'incremento_tempo':incremento_tempo})
 
    def chegada(self, evento, eventos, geraNumeros):
        print('--------------Chegada--------------')
        print(f'A Fila {self.nomeFila} tinha {self.estadoAtual} pessoas')
        if self.estadoAtual < self.capacidade:
            elapsed_time = evento['time'] - self.tempoUltimoEvento
            self.estados[self.estadoAtual] += elapsed_time
            self.timer.set_time(elapsed_time)
            self.tempoUltimoEvento = evento['time']
            self.estadoAtual += 1
            print(f'Agora a Fila {self.nomeFila} tem {self.estadoAtual} pessoas')
            if self.estadoAtual <= self.numeroServidores:
                incremento_tempo = self.calculaTempoSaida(geraNumeros)
                self.agendarSaida(evento['time'], incremento_tempo, eventos)
        else:
            self.perdas += 1
            print('!!!!!!!!!!! >>> Perda <<< !!!!!!!!!!!!')
        incremento_tempo = self.calculaTempoChegada(geraNumeros)
        self.agendarChegada(evento['time'], incremento_tempo, eventos)

    def saida(self, evento, eventos, geraNumeros):
        print('--------------Saída--------------')
        print(f'Fila {self.nomeFila} tinha {self.estadoAtual} pessoas')
        elapsed_time = evento['time'] - self.tempoUltimoEvento
        self.estados[self.estadoAtual] += elapsed_time
        self.timer.set_time(elapsed_time)
        self.tempoUltimoEvento = evento['time']
        self.estadoAtual -= 1
        print(f'Agora a Fila {self.nomeFila} tem {self.estadoAtual} pessoas')
        if self.estadoAtual >= self.numeroServidores:
            incremento_tempo = self.calculaTempoSaida(geraNumeros)
            self.agendarSaida(evento['time'], incremento_tempo, eventos)