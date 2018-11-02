import sys

TIO = 2 #tempo em ciclos para IO
red = "\033[41m"
green = "\033[42m"
orange = "\033[100m"
blue = "\033[44m"
yellow = "\033[103m"
clean = "\033[49m"
ESP = orange + "  " + clean + '|'
EXEC = blue + "  " + clean + '|'
BLOQ = red + "  " + clean + '|'
INI = yellow + "  " + clean + '|'

# --------------------------------Processos-------------------------------------
class Processo:
    def __init__(self, processo):
        self.__ID = int(processo[0]) #Id do processo
        self.__DF = int(processo[1]) #duracao de fase de uso
        self.__Prio = int(processo[2]) #prioridade
        self.__TC = int(processo[3]) #tempo de chegada
        self.__IO = list(map(int,processo[4:])) #tempo de inicio do IO
        self.__posIO = 0 #indice do proximo IO
        self.__cicloP = 0 #ciclo atual de execucao do processo
        self.__TB = 0 #tempo bloqueado
        self.__historico = ""
    
    def getID(self):
        return self.__ID

    def getTC(self):
        return self.__TC

    def getTempoExec(self):
        return self.__DF - self.__cicloP

    def printProcesso(self):
        print("processo[", self.__ID ,"]|", self.__historico.replace('-', INI).replace('b', BLOQ).replace('e', EXEC).replace('s', ESP), sep = "")

    def bloqExecP(self):
        self.__TB += 1
        self.__historico += "b"
        if self.__TB == TIO:
            self.__TB = 0
            return 1
        return 0

    def espera(self):
        self.__historico += "-"

    def pronto(self):
        self.__historico += "s"

    def executaP(self):
        self.__cicloP += 1
        self.__historico += "e"
        if self.__DF == self.__cicloP:
            return 1
        elif len(self.__IO) > self.__posIO:
            if self.__cicloP == self.__IO[self.__posIO]:
                self.__posIO += 1
                return 2
        return 0

# --------------------------------Processos-------------------------------------
# --------------------------------Escalonador-SJF-------------------------------
class SJF:
    def __init__(self, Processos):
        self.__listaProcess = Processos
        self.__fila = []
        self.__filaBloqueio = []
        self.__ciclo = 0
        self.__indice = 0
        self.__execucao = 0

    def bloqExec(self, indice):
        if len(self.__filaBloqueio) > indice:
            if self.__filaBloqueio[indice].bloqExecP():
                self.__fila.append(self.__filaBloqueio.pop(indice))
                self.bloqExec(indice)
            else:
                self.bloqExec(indice + 1)

    def executa(self):
        Verdade = 1
        while Verdade:
            self.populaFila()
            ##Reordena os processos aptos
            #self.ordenaTempo()
            ##
            if len(self.__fila):
                if self.__execucao == 0:
                    menor = 0
                    menorTempo = self.__fila[0].getTempoExec()
                    for i in range(len(self.__fila)):
                        if(menorTempo > self.__fila[i].getTempoExec()):
                            menor = i
                    self.__execucao = self.__fila.pop(menor)
            for proc in self.__fila:
                proc.pronto()
            
            if len(self.__filaBloqueio):
                self.bloqExec(0)
            #salva o que aconteceu para cada processo fora do escalonador
            i = self.__indice
            j = len(self.__listaProcess)
            while(i < j):
                self.__listaProcess[i].espera()
                i += 1
            ##
            if self.__execucao != 0:
                aux = self.__execucao.executaP()
                if aux == 1:
                    self.__execucao = 0
                elif aux == 2:
                    self.__filaBloqueio.append(self.__execucao)
                    self.__execucao = 0
            self.__ciclo += 1
            if len(self.__listaProcess) == self.__indice:
                if self.__execucao == 0:
                    if len(self.__fila) == 0:
                        if len(self.__filaBloqueio) == 0:
                            Verdade = 0
            
    def historico(self):
        for i in range(1, len(self.__listaProcess)):
            for j in range(0, i):
                if self.__listaProcess[i].getID() < self.__listaProcess[j].getID():
                    self.__listaProcess[i], self.__listaProcess[j] = self.__listaProcess[j], self.__listaProcess[i]

        for processo in self.__listaProcess:
            processo.printProcesso()

    def populaFila(self):
        if len(self.__listaProcess) > self.__indice:
            if self.__listaProcess[self.__indice].getTC() == self.__ciclo:
                self.__fila.append(self.__listaProcess[self.__indice])
                self.__indice+=1
                self.populaFila()

# --------------------------------Escalonador-SJF-------------------------------

# --------------------------------Main------------------------------------------
#------------abre-arquivo---------------------------------
arquivo = open(sys.argv[1],'r')
if arquivo == None:
    print("Erro na Leitura")
    exit(1)
processos = arquivo.readlines()
#-----------fim-abre-arquivo-----------------------------
#-----------ordena-Processos-----------------------------
listaP = []
for processo in processos:
    listaP.append(Processo(processo.split()))
for i in range(1,len(listaP)):
    for j in range(i):
        if listaP[j].getTC() >= listaP[i].getTC(): 
            listaP[j],listaP[i] = listaP[i],listaP[j]
#------------Fim-Ordena-Processos-------------------------
sjf = SJF(listaP)
sjf.executa()
sjf.historico()