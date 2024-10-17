import sys
from fila import Fila

class Temporizador:
    def __init__(self):
        self.temporizador = 0
    def set_time(self, incrementadorTempo):
        self.temporizador += incrementadorTempo
    def get_time(self):
        return self.temporizador

class PseudoAleatorios:
    # sementeAtual irá variar, o resto não
    sementeAtual = 50
    a = 55
    M = 2500
    c = 5.8
    def geraNumero(self):
        self.proximaSemente = ((self.a * self.sementeAtual) + self.c) % self.M
        self.sementeAtual = self.proximaSemente
        return (self.proximaSemente / self.M)

def entradaFila():
    try:
        with open('entrada.yaml', 'r') as f:
            filaTamanho = int(f.readline().strip().replace('Tamanho ',''))
            
            filasList = []
            
            for i in range(1, filaTamanho + 1):
                
                f.readline()

                filaAtual = {}

                linha = f.readline().strip()
                filaAtual['id'] = linha

                linha = f.readline().strip().replace('ProxFila ','')
                filaAtual['proxFila'] = linha
                
                linha = f.readline().strip().replace('MesmaFila ','')
                filaAtual['mesmaFila'] = linha
                
                linha = f.readline().strip().replace('Sair ','')
                filaAtual['sair'] = linha
                
                linha = f.readline().strip().replace('Servidores ','')
                filaAtual['server'] = linha
                
                linha = f.readline().strip().replace('Capacidade ','')
                filaAtual['capacidade'] = linha
                
                linha = f.readline().strip().replace('Chegada ','')
                filaAtual['arrival'] = linha.split('..')
                
                linha = f.readline().strip().replace('Saida ','')
                filaAtual['exit'] = linha.split('..')
                
                filasList.append(filaAtual)
        
        return filasList
        
    except:
        print('Erro!')
        sys.exit()

def simulador():
    temporizador = Temporizador()
    filas = entradaFila()
    tempoAtual = 2
    iteracoes = 100000
    geraNumeros = PseudoAleatorios()
    rodadaAtual = 0
    eventos = [{'Fila': 'F1', 
                'evento': 'chegada', 
                'time': tempoAtual, 
                'incremento_tempo': 0}]
    filasList = []

    for i in filas:
        filaNew = Fila(i['id'].replace('\n', ''),i['proxFila'],i['mesmaFila'],i['sair'],i['server'],i['capacidade'],i['arrival'],i['exit'],temporizador)
        filasList.append(filaNew)

    while True:
        try:
            if rodadaAtual >= iteracoes:
                break
            rodadaAtual += 1
            print('\n')
            evento = buscaEvento(eventos)
            tempoAtual = evento['time'] + evento['incremento_tempo']
            temporizador.set_time(evento['incremento_tempo'])  
            # Evento (Chegada ou Saída)
            selectedFila = None
            for fila in filasList:
                if fila.getNome() == evento['Fila']:
                    selectedFila = fila
                    break

            if selectedFila is None:
                print(f"Fila {evento['Fila']} não encontrada!")
                continue

            if evento['evento'] == 'chegada':
                selectedFila.chegada(evento, eventos, geraNumeros)
            elif evento['evento'] == 'saida':
                selectedFila.saida(evento, eventos, geraNumeros)
        except Exception as e:
            print(f'Erro: {e}')
            sys.exit(1)

    print('\n\n\n******Resultados*******\n')
    tempo(filasList, temporizador)
    print('\n')
    resultados(filasList)

def resultados(filasList):
    print('------------------Distribuição e Perdas------------------\n')
    
    for fila in filasList:
        nome_fila = fila.getNome()
        estados = fila.getEstados()
        soma_total = sum(estados.values())
        
        print(f'Fila {nome_fila}:')
        
        if soma_total == 0:
            print("Nenhuma contagem de estado disponível.")
        else:
            for estado, contagem in estados.items():
                porcentagem = (contagem / soma_total) * 100
                print(f'  Estado {estado}: {porcentagem:.2f}%')

        perdas = fila.getPerdas()
        print(f'  Perdas: {perdas}')
        print()

def tempo(filasList, temporizador):
    print('---> Tempos de Execução')
    for fila in filasList:
        print(f'\n------------Fila {fila.getNome()}---------------', end=' ')
        estados = fila.getEstados()
        tempoAcumulado = sum(estado * count for estado, count in estados.items())
        print(f'\nTempo acumulado ---> {tempoAcumulado}')
        for estado, tempo in estados.items():
            print(f'  Estado {estado}: {tempo}')
    print('\n\n---> Tempo de simulação =', temporizador.get_time())

# Prioridade: menor tempo       
def buscaEvento(eventos):
    eventoProcessado = 0
    time = sys.maxsize
    for evento in eventos:
        if evento['time'] < time: time = evento['time']
    for evento in eventos:
       if evento['time'] == time:
           eventoProcessado = evento
           eventos.remove(evento)
    return eventoProcessado
            
if __name__ == "__main__":
    simulador()