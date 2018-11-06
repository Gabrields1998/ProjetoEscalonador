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

# --------------------------------Processos----------------------------------------
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
        self.__TTE = 0 #Tempo Total de Espera
    #------------------------------------------------------------------------------
    # Reseta todas as variaveis que são alteradas durante a execução do escalonador
    #------------------------------------------------------------------------------
    def clean(self):
        self.__posIO = 0
        self.__cicloP = 0
        self.__TB = 0
        self.__historico = ""
        self.__TTE = 0

    def getPrio(self):
        return self.__Prio
    #------------------------------------------------------------------------------
    # Imprime os detalhes do processo
    #------------------------------------------------------------------------------
    def printDetail(self):
        print("processo",self.__ID,"DF",self.__DF,"prio",self.__Prio,"TC",self.__TC,"IO",self.__IO,"PosIo",self.__posIO,"cicloP",self.__cicloP,"TB",self.__TB,"historico",self.__historico,"TTE",self.__TTE)
    
    def getID(self):
        return self.__ID

    def getTC(self):
        return self.__TC
    #------------------------------------------------------------------------------
    # Obtem o pico de execução atual
    #------------------------------------------------------------------------------
    def getTempoExec(self):
        if len(self.__IO):
            if self.__posIO < len(self.__IO):
                return self.__IO[self.__posIO] - self.__cicloP
        return self.__DF - self.__cicloP

    def getTTE(self):
        return self.__TTE
    #------------------------------------------------------------------------------
    # Exibe o historico do processo juntamente com seu id
    #------------------------------------------------------------------------------
    def printProcesso(self):
        print("processo[", self.__ID ,"]|", self.__historico.replace('-', INI).replace('b', BLOQ).replace('e', EXEC).replace('s', ESP), sep = "")

    #------------------------------------------------------------------------------
    # Executa um passo do processo bloqueado, grava a ação no historico e retorna 1
    # se for necessario desbloquear, do contrario retorna 0
    #------------------------------------------------------------------------------
    def bloqExecP(self):
        self.__TB += 1
        self.__historico += "b"
        if self.__TB == TIO:
            self.__TB = 0
            return 1
        return 0

    #------------------------------------------------------------------------------
    # Grava um caracter no historico referente a espera para entrar na fila de pro-
    # cessos aptos a execução
    #------------------------------------------------------------------------------
    def espera(self):
        self.__historico += "-"

    #------------------------------------------------------------------------------
    # Grava um caracter no historico referente a espera pela CPU
    #------------------------------------------------------------------------------
    def pronto(self):
        self.__historico += "s"
        self.__TTE += 1

    #------------------------------------------------------------------------------
    # Executa  um passo do processo, grava no historico e retorna 1 caso tenha ter-
    # minado, 2 para I/O e 0 para continuar
    #------------------------------------------------------------------------------
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

# ----------------------------Fim-Processos----------------------------------------
# --------------------------------Escalonador-SJF----------------------------------
class SJF:
    def __init__(self, Processos):
        self.__listaProcess = Processos
        self.__fila = []
        self.__filaBloqueio = []
        self.__ciclo = 0
        self.__indice = 0
        self.__TMaxF = 0
        self.__TMedF = 0
        self.__execucao = 0
    #------------------------------------------------------------------------------
    # Avança um passo todos os processos bloqueados e se necessario desbloqueia
    #------------------------------------------------------------------------------
    def bloqExec(self, indice):
        if len(self.__filaBloqueio) > indice:
            if self.__filaBloqueio[indice].bloqExecP():
                self.__fila.append(self.__filaBloqueio.pop(indice))
                self.bloqExec(indice)
            else:
                self.bloqExec(indice + 1)
    #------------------------------------------------------------------------------
    # Executa o escalonador para os processos recebidos
    #------------------------------------------------------------------------------
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

            self.__TMedF += len(self.__fila)
            if len(self.__fila) > self.__TMaxF:
                self.__TMaxF = len(self.__fila)
            
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

        self.__TMedF = self.__TMedF / self.__ciclo
    #------------------------------------------------------------------------------
    # Imprime as informações resultantes da execução
    #------------------------------------------------------------------------------
    def historico(self):
        print("LEGENDA:---------------------------------------------------------------------\n")
        print("TTE = Tempo Total de Espera")
        print("TME = Tempo Médio de Espera")
        print("Processo a iniciar: |" + INI)
        print("Estado de Execução: |" + EXEC)
        print("Estado de Espera:   |" + ESP)
        print("Estado de Bloqueio: |" + BLOQ)
        
        for i in range(1, len(self.__listaProcess)):
            for j in range(0, i):
                if self.__listaProcess[i].getID() < self.__listaProcess[j].getID():
                    self.__listaProcess[i], self.__listaProcess[j] = self.__listaProcess[j], self.__listaProcess[i]

        TME = 0#Tempo Médio de Espera

        print("DESCRIÇÃO:---------------------------SJF-------------------------------------")
        print()
        for i in range(0, len(self.__listaProcess)):
            print("TTE processo[",str(self.__listaProcess[i].getID()),"] : " + str(self.__listaProcess[i].getTTE()) + " ciclos")
            TME += self.__listaProcess[i].getTTE()
        TME = str(TME/(i+1))
        
        print("TME : " + TME + " ciclos")
        print("THROUGHPUT : " + str(i+1) + " processos executados em "+ str(self.__ciclo) +" ciclos")
        print("THROUGHPUT : "+str((i+1)/self.__ciclo), "processos / ciclo")
        print("Tamanho Máximo da fila:", str(self.__TMaxF))
        print("Tamanho Médio da fila:", str(self.__TMedF))
        print("----------------------------------EXECUÇÃO-----------------------------------")
        for processo in self.__listaProcess:
            processo.printProcesso()
        print()
    #------------------------------------------------------------------------------
    # Passa os processos para a fila de aptos quando o tempo de chegada for equiva-
    # lente ao ciclo atual do escalonador
    #------------------------------------------------------------------------------
    def populaFila(self):
        if len(self.__listaProcess) > self.__indice:
            if self.__listaProcess[self.__indice].getTC() == self.__ciclo:
                self.__fila.append(self.__listaProcess[self.__indice])
                self.__indice+=1
                self.populaFila()

# ----------------------------Fim-Escalonador-SJF----------------------------------
# --------------------------------Escalonador-Round-Robin--------------------------
class RoundRobin:
    def __init__(self, Processos):
        self.__listaProcess = Processos
        self.__fila = []
        self.__filaBloqueio = []
        self.__ciclo = 0
        self.__quantum = 2
        self.__indice = 0
        self.__TMaxF = 0
        self.__TMedF = 0
        self.__execucao = 0
    #------------------------------------------------------------------------------
    # Avança um passo todos os processos bloqueados e se necessario desbloqueia
    #------------------------------------------------------------------------------
    def bloqExec(self, indice):
        if len(self.__filaBloqueio) > indice:
            if self.__filaBloqueio[indice].bloqExecP():
                self.__fila.append(self.__filaBloqueio.pop(indice))
                self.bloqExec(indice)
            else:
                self.bloqExec(indice + 1)
    #------------------------------------------------------------------------------
    # Imprime as informações resultantes da execução
    #------------------------------------------------------------------------------
    def historico(self):
        for i in range(1, len(self.__listaProcess)):
            for j in range(0, i):
                if self.__listaProcess[i].getID() < self.__listaProcess[j].getID():
                    self.__listaProcess[i], self.__listaProcess[j] = self.__listaProcess[j], self.__listaProcess[i]

        TME = 0#Tempo Médio de Espera

        print("DESCRIÇÃO:-----------------------ROUND-ROBIN---------------------------------")
        print()
        for i in range(0, len(self.__listaProcess)):
            print("TTE processo[",str(self.__listaProcess[i].getID()),"] : " + str(self.__listaProcess[i].getTTE()) + " ciclos")
            TME += self.__listaProcess[i].getTTE()
        TME = str(TME/(i+1))
        
        print("TME : " + TME + " ciclos")
        print("THROUGHPUT : " + str(i+1) + " processos executados em "+ str(self.__ciclo) +" ciclos")
        print("THROUGHPUT : "+str((i+1)/self.__ciclo), "processos / ciclo")
        print("Tamanho Máximo da fila:", str(self.__TMaxF))
        print("Tamanho Médio da fila:", str(self.__TMedF))
        print("-----------------------------------EXECUÇÃO----------------------------------")
        for processo in self.__listaProcess:
            processo.printProcesso()
        print()
    #------------------------------------------------------------------------------
    # Passa os processos para a fila de aptos quando o tempo de chegada for equiva-
    # lente ao ciclo atual do escalonador
    #------------------------------------------------------------------------------
    def populaFila(self):
        if len(self.__listaProcess) > self.__indice:
            if self.__listaProcess[self.__indice].getTC() == self.__ciclo:
                self.__fila.append(self.__listaProcess[self.__indice])
                self.__indice+=1
                self.populaFila()
    #------------------------------------------------------------------------------
    # Executa o escalonador para os processos recebidos
    #------------------------------------------------------------------------------
    def executa(self):
        Verdade = 1
        while Verdade:
            self.populaFila()
            if len(self.__fila):
                if self.__execucao == 0:
                    self.__execucao = self.__fila.pop(0)
            
            self.__TMedF += len(self.__fila)
            if len(self.__fila) > self.__TMaxF:
                self.__TMaxF = len(self.__fila)
            
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
                self.__quantum -= 1 
                aux = self.__execucao.executaP()
                if aux == 1:
                    self.__execucao = 0
                elif aux == 2:
                    self.__filaBloqueio.append(self.__execucao)
                    self.__execucao = 0
                elif self.__quantum == 0:
                    self.__fila.append(self.__execucao)
                    self.__execucao = 0
            self.__ciclo += 1
                       
            if self.__execucao == 0:
                self.__quantum = 2

            ## codigo para RR
            if len(self.__listaProcess) == self.__indice:
                if self.__execucao == 0:
                    if len(self.__fila) == 0:
                        if len(self.__filaBloqueio) == 0:
                            Verdade = 0
        self.__TMedF = self.__TMedF / self.__ciclo

# ----------------------------Fim-Escalonador-Round-Robin--------------------------

# --------------------------------Escalonador-Prioridade---------------------------
class Prioridade:
    def __init__(self, Processos):
        self.__listaProcess = Processos
        self.__fila = []
        self.__filaBloqueio = []
        self.__ciclo = 0
        self.__quantum = 2
        self.__indice = 0
        self.__TMaxF = 0
        self.__TMedF = 0
        self.__execucao = 0
    #------------------------------------------------------------------------------
    # Avança um passo todos os processos bloqueados e se necessario desbloqueia
    #------------------------------------------------------------------------------
    def bloqExec(self, indice):
        if len(self.__filaBloqueio) > indice:
            if self.__filaBloqueio[indice].bloqExecP():
                self.__fila.append(self.__filaBloqueio.pop(indice))
                self.bloqExec(indice)
            else:
                self.bloqExec(indice + 1)
    #------------------------------------------------------------------------------
    # Imprime as informações resultantes da execução
    #------------------------------------------------------------------------------
    def historico(self):
        for i in range(1, len(self.__listaProcess)):
            for j in range(0, i):
                if self.__listaProcess[i].getID() < self.__listaProcess[j].getID():
                    self.__listaProcess[i], self.__listaProcess[j] = self.__listaProcess[j], self.__listaProcess[i]

        TME = 0#Tempo Médio de Espera

        print("DESCRIÇÃO-------------------------PRIORIDADE---------------------------------")
        print()
        for i in range(0, len(self.__listaProcess)):
            print("TTE processo[",str(self.__listaProcess[i].getID()),"] : " + str(self.__listaProcess[i].getTTE()) + " ciclos")
            TME += self.__listaProcess[i].getTTE()
        TME = str(TME/(i+1))
        
        print("TME : " + TME + " ciclos")
        print("THROUGHPUT : " + str(i+1) + " processos executados em "+ str(self.__ciclo) +" ciclos")
        print("THROUGHPUT : "+str((i+1)/self.__ciclo), "processos / ciclo")
        print("Tamanho Máximo da fila:", str(self.__TMaxF))
        print("Tamanho Médio da fila:", str(self.__TMedF))
        print("-----------------------------------EXECUÇÃO----------------------------------")
        for processo in self.__listaProcess:
            processo.printProcesso()
        print()
    #------------------------------------------------------------------------------
    # Passa os processos para a fila de aptos quando o tempo de chegada for equiva-
    # lente ao ciclo atual do escalonador
    #------------------------------------------------------------------------------
    def populaFila(self):
        if len(self.__listaProcess) > self.__indice:
            if self.__listaProcess[self.__indice].getTC() == self.__ciclo:
                self.__fila.append(self.__listaProcess[self.__indice])
                self.__indice+=1
                self.populaFila()
    #------------------------------------------------------------------------------
    # Executa o escalonador para os processos recebidos
    #------------------------------------------------------------------------------
    def executa(self):
        Verdade = 1
        while Verdade:
            self.populaFila()
            if len(self.__fila):
                if self.__execucao == 0:
                    maxP = self.__fila[0].getPrio()
                    ind = 0
                else:
                    maxP = self.__execucao.getPrio()
                    ind = -1
                for i in range(0, len(self.__fila)):
                    if(maxP < self.__fila[i].getPrio()):
                        maxP = self.__fila[i].getPrio()
                        ind = i
                if self.__execucao == 0:
                    self.__execucao = self.__fila.pop(ind)
                elif ind != (-1):
                    self.__fila.append(self.__execucao)
                    self.__execucao = self.__fila.pop(ind)

            
            self.__TMedF += len(self.__fila)
            if len(self.__fila) > self.__TMaxF:
                self.__TMaxF = len(self.__fila)
            
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
            
            ## codigo para RR
            if len(self.__listaProcess) == self.__indice:
                if self.__execucao == 0:
                    if len(self.__fila) == 0:
                        if len(self.__filaBloqueio) == 0:
                            Verdade = 0
        
        self.__TMedF = self.__TMedF / self.__ciclo

# ----------------------------Fim-Escalonador-Prioridade---------------------------

#---------------------------------Organiza-Processos-------------------------------
# Limpa os variaveis que são utilizadas durante a execução do escalonador e ordena
# os processos pelo TC (Tempo de Chegada)
#----------------------------------------------------------------------------------
def organizaProcessos(listaP):
    for proc in listaP:
        proc.clean()
    for i in range(1,len(listaP)):
        for j in range(i):
            if listaP[j].getTC() > listaP[i].getTC(): 
                listaP[j],listaP[i] = listaP[i],listaP[j]

# --------------------------------Main---------------------------------------------
    #-----------------------------abre-arquivo-------------------------------------
    # Abre e faz a leitura do arquivo de descrição dos processos
    #------------------------------------------------------------------------------
arquivo = open(sys.argv[1],'r')
if arquivo == None:
    print("Erro na Leitura")
    exit(1)
processos = arquivo.readlines()
    #-----------------------------organiza-Processos-------------------------------
    # Cria e organiza os processos para a execução
    #------------------------------------------------------------------------------
listaP = []
for processo in processos:
    listaP.append(Processo(processo.split()))
organizaProcessos(listaP)
    #-----------------------------Executa-SJF--------------------------------------
sjf = SJF(listaP)
sjf.executa()
sjf.historico()

organizaProcessos(listaP)
    #-----------------------------Executa-Roud-Robin-------------------------------
rr = RoundRobin(listaP)
rr.executa()
rr.historico()

organizaProcessos(listaP)
    #-----------------------------Executa-Prioridade-------------------------------
prio = Prioridade(listaP)
prio.executa()
prio.historico()
#-----------------------------Fim-Main---------------------------------------------