# Simulador de Algoritmos de Escalonamento

  Trabalho implementado na disciplina de Sistemas Operacionais, com o objetivo de colocar em pratíca os conceitos vistos em aula.

  Para executar a implementação é necessário ter o `Python3` instalado e rodar o comando no padrão abaixo em um terminal.

  ````console
  foo@bar$ python3 escalonador.py ArquivoDeProcessos
  ````

  Onde `escalonador.py` é o arquivo com o código implementado e `ArquivoDeProcessos` é o arquivo com a descrição dos processos.

  > Formato do Arquivo de processos </br> ID - DF - PRI - TC - FIO </br> 0 10 4 0 3 5 7  # Onde Processo id = 0, Tamanho = 10, Prioridade = 4, Tempo de chegada = 0 e Fila de I/O = [3, 5, 7] </br> 1 5 2 1 # Onde Processo id = 1, Tamanho = 5, Prioridade = 2, Tempo de chegada = 1 e Fila de I/O = Vazio

Grupo: Everton, Gabriel David Sacca e Lucas Santana de Rocha