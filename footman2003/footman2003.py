import csv
import random
 

#variável global diasMes : organização de todos os meses acabados no dia 30 e no dia 31
global diasMes
diasMes = {
    31 : [1,3,5,6,8,10,12],
    30 : [4,7,9,11]
}

#varíavel global data: uma lista que guarda todas as datas do calendario de jogos. 
#data: [inicio, Ultima Data Gerada(U.D.G)] -> inicio, U.D.G: [dia, mes, ano]
global data
data = [0,0,0]

#varíavel global selecoes : uma lista com todas as selecoes existentes
global selecoes
selecoes = []

global numJogo
numJogo = [0]

#Dicionario com contagem de selecoes por continente apuradas para o torneio
global continentes
continentes = {
    "America" : 0,
    "Europa" : 0,
    "Oceania" : 0,
    "Asia": 0,
    "Africa" : 0,
    "Antártida" : 0
}
#golosMarcados : biblioteca que associa ao nome da equipa, os golos que eles marcaram
global golosMarcados
golosMarcados = {}
#golosMarcados : biblioteca que associa ao nome da equipa, os golos que eles sofreram
global golosSofridos
golosSofridos = {}
    
#varíavel global equipasFase: Dicionario que guarda a informação de todas as equipas que passam cada fase do campeonato
global equipasFase
equipasFase = {
    "oitavos" : [], 
    "quartos" : [], 
    "meias" : [], 
    "final" : []
}
#varíavel global jogosFase: Dicionario que guarda as informações de cada jogo em cada fase do campeonato
global jogosFase
jogosFase = {
    0 : [], 
    1 : [], 
    2 : [], 
    3 : []
}

# a nossa main. Contém uma funcao que lê o ficheiro equipas e a execução do menu princi
def main():
    count = False
    with open("equipas.csv", 'r') as equipas:
        reader = csv.reader(equipas)
        for row in reader:   
            if (count == True):
                selecoes.append(row)
            count = True
    mainMenu()

#addSelecao : função que adiciona uma seleção à lista de seleções
def addSelecao():
    nome = input("Introduza o nome da seleção: ") 
    pais = input("Introduza o país da sua seleção: ")
    continente = input("Introduza o continente da seleção: ") 
    ranking =int(input("Introduza o ranking da seleção: "))
    selecoes.append([nome, pais, continente, ranking])

#remSelecao : função que remove uma equipa da lista de seleções
def remSelecao():
    selecaoRemovida = input("Qual equipa vai ser removida: ")
    for x in selecoes:
        if selecaoRemovida == x[0]:
            selecoes.remove(x)
            break
        
#anoBissexto : função que testa se um ano é ou não bissexto.
def anoBissexto(ano):
    if((ano % 400 == 0) or (ano % 100 != 0) and (ano% 4 == 0)):  
        return True
    else:
        return False

#incrementarData : função que adiciona n dias (incremento) à data global
def incrementarData(incremento):
    data[0] += incremento
    if((data[1] in diasMes[31] and data[0] > 31) or (data[1] in diasMes[30] and data[0] > 30)):
        data[0] = incremento
        data[1] += 1
    elif((data[1] == 2 and anoBissexto(data[2]) == False and data[0] > 28) or (data[1] == 2 and anoBissexto(data[2]) == True and data[0] > 29)):
        data[0] = incremento
        data[1] += 1
    if(data[1] > 12):
        data[1] = 1
        data[2] += 1
    return data
    
#randJogo: simula todos os jogos de uma certa fase, retornando a lista de todas as equipas vencedoras (e apuradas para a proxima fase).
def randJogo(listaEquipa, fase):
    ret = []
    flipflop = False
    while(len(listaEquipa) != 0):
        random.shuffle(listaEquipa)
        if(flipflop == True):
            hora = "16:00"
            flipflop = False
        else:
            hora = "14:00"
            flipflop = True
        tempoUtil = int(90 * ((random.randrange(60, 70)/100)))
        casa = listaEquipa[0]
        listaEquipa.pop(0)
        fora = listaEquipa[0]
        listaEquipa.pop(0)
        resCasa = random.randint(0, 6)
        resFora = random.randint(0, 6)
        if(resCasa == resFora):
            resFora += 1
        if(resCasa > resFora):
            equipaApurada = casa
        else:
            equipaApurada = fora
        ret.append(equipaApurada)
        adicionarGolosMarcados(casa[0], resCasa)
        adicionarGolosMarcados(fora[0], resFora)
        adicionarGolosSofridos(casa[0], resFora)
        adicionarGolosSofridos(fora[0], resCasa)
        numJogo[0] = numJogo[0] + 1
        jogosFase[fase].append([numJogo[0], casa[0], fora[0], data.copy(), hora, resCasa, resFora, tempoUtil, equipaApurada[0]])
        if(flipflop == False):
            incrementarData(1)
    return ret

#distContinente : listar a distribuição de equipas por continente
def distContinente():
    for continente, contagem in continentes.items():
        print(continente + ": " + str(contagem)) 

#updateContinente : função que atualiza a distribuicao das equipas por continente 
def updateContinente(selecoes):
    for continente in continentes.keys():   #reset de cada vez
        continentes[continente] = 0
    for selecao in selecoes:
        for continente in continentes.keys():
            if (continente.lower() == selecao[2].lower()):
                continentes[continente] += 1

#checkMenuOptions : verifica se a opção introduzida é válida em cada menu
def checkMenuOption(toCheck, max):
    if(toCheck.isdigit()):
        ret = int(toCheck)
        if(ret >= 0 and ret < max):
            return ret
    print("\n<==============================================>")
    print("!!opção não existe, introduza um número válido!!")
    print("<==============================================>\n")
    return -1
            
#apuramento : seleciona todas as equipas apuradas para o torneio.
def apuramento():
    organiza = selecoes.copy()
    random.shuffle(organiza)
    count = 0
    ret = []
    while( len(ret) <= 12 and  count != len(organiza)):
        if(int(organiza[count][3]) <= 30):
            ret.append(organiza[count])
            organiza.pop(count)
            continue  
        count += 1
    for x in range(3):
        ret.append(organiza[x])
    return ret


#printCalendario : função que representa graficamente o calendario dos jogos de cada fase
def printCalendario(fase, filtro):  #fase -> 0 a 3
        fases = ["Oitavos de Final", "Quartos de Final", "Meias de Final", "Final"]
        toPrint = [
            "<=================",
            " |  dia/mes/ano  |",
            " |  hora:        |",
            " |  casa:        |",
            " |  visitante:   |",
            "<=================",
        ]
        print("\n<" + fases[fase] + ">")
        for jogo in jogosFase[fase]:
            if(filtro == 0 or filtro == jogo[1] or filtro == jogo[2]):
                toPrint[0] += "=============="
                if(jogo[3][1] > 9 and jogo[3][0] > 9):
                    toPrint[1] += "  "+str(jogo[3][0]) + "/" + str(jogo[3][1]) + "/" + str(jogo[3][2]) +" |"
                elif((jogo[3][1] > 9 and jogo[3][0] < 10) or (jogo[3][1] < 10 and jogo[3][0] > 9)):
                    toPrint[1] += "   "+str(jogo[3][0]) + "/" + str(jogo[3][1]) + "/" + str(jogo[3][2]) +" |"
                else:
                    toPrint[1] += "   "+str(jogo[3][0]) + "/" + str(jogo[3][1]) + "/" + str(jogo[3][2]) +"  |"
                toPrint[2] += "     " + str(jogo[4])+ "   |"
                toPrint[3]+= "     " + str(jogo[1]) + "     |"
                toPrint[4]+= "     " + str(jogo[2]) + "     |"
                toPrint[5] += "=============="
        toPrint[0] += ">"
        toPrint[5] += ">"  
        if(len(toPrint[0]) != 18):
            for line in toPrint:
                print(line)
        else:
            print("\n!!Horário inexistente!!\n")\

#validaData : função que verifica se uma certa data é válida
def validaData(aValidar):
    if(aValidar[0].isnumeric() and aValidar[1].isnumeric() and aValidar[2].isnumeric()):
        aValidar[0] = int(aValidar[0])
        aValidar[1] = int(aValidar[1])
        aValidar[2] = int(aValidar[2])
    else:
        return False
    if(aValidar[1] <= 12 and aValidar[0] > 0 and aValidar[1] > 0 and aValidar[2] >= 0):
        if((aValidar[1] in diasMes[31] and aValidar[0] <= 31) or (aValidar[1] in diasMes[30] and aValidar[0] <= 30)):
            return True
        elif((aValidar[1] == 2 and anoBissexto(aValidar[2]) == False and aValidar[0] <= 28) or (aValidar[1] == 2 and anoBissexto(aValidar[2]) == True and data[0] <= 29)):
            return True    
    return False

#obterData : função que pede a data ao utilizador
def obterData():
    check = True
    while(check != False):
        dia = input("Introduza um dia: ")
        mes = input("Introduza um mês: ")
        ano = input("Introduza um ano: ")
        if(validaData([dia, mes, ano]) == True):
            return [int(dia), int(mes), int(ano)]
        print("\n<====================================================>")
        print("!!Data invalida, por favor introduza uma data válida!!")
        print("<====================================================>\n")
        option = input("(prima (0) para cancelar ou [enter] para continuar)")
        if(option == "0"):
            return -1

#resDia : função que retorna os resultados de uma equipa num certo dia.           
def resDia(dia):       
    ret = []
    if(dia == -1):
        return ret
    for fase in jogosFase.keys():
        for jogo in jogosFase[fase]:
            if(jogo[3][0] == dia[0] and jogo[3][1] == dia[1] and jogo[3][2] == dia[2]):
                ret.append(jogo)
    return ret               

#validaSelecao : função que verifica se uma selecao existe e é válida.
def validaSelecao(selecao):
    for fase in jogosFase.keys():
        for jogo in jogosFase[fase]:
            if(jogo[1] == selecao or jogo[2] == selecao):
                return True

#obterSeleção: função que pede ao utilizador o nome de uma certa seleção.
def obterSeleção():
    check = True
    while(check != False):
        selecao = input("Introduza o nome de uma selecão: ")
        if(validaSelecao(selecao) == True):
            return selecao
        print("\n<=========================================================>")
        print("!!Seleção invalida, por favor introduza uma seleção válida!!")
        print("<==========================================================>\n")
        option = input("(prima (0) para cancelar ou [enter] para continuar)")
        if(option == "0"):
            return -1

#limparCampeonato : função que limpa todos os dados que foram acumulados  
def limparCampeonato():
    numJogo[0] = 0
    for fase in jogosFase.keys():
        jogosFase[fase] = []
    for fase in equipasFase.keys():
        equipasFase[fase] = []
    for continente in continentes.keys():
        continentes[continente] = 0
    golosMarcados.clear()
    golosSofridos.clear()

#maisUtil : função que retorna a lista com o jogo que tem o tempo mais util.
def maisUtil(fase):
    max = 0
    for jogo in jogosFase[fase]:
        if(jogo[7] > max):
            max = jogo[7]
            ret = jogo.copy()
    return ret

#adicionarGolosSofridos: função que adiciona os dados ao dicionario de golosSofridos
def adicionarGolosSofridos(nome, golos):
    for equipa in golosSofridos.keys():
        if(equipa == nome):
            golosSofridos[equipa] = golosSofridos[equipa] + golos

#adicionarGolosSofridos: função que adiciona os dados ao dicionario de golosMarcados
def adicionarGolosMarcados(nome, golos):
    for equipa in golosMarcados.keys():
        if(equipa == nome):
            golosMarcados[equipa] = golosMarcados[equipa] + golos

#printDef : função retorna a lista da equipa que tem melhor defesa.
def printDef():
    min = 24
    ret = 0
    for golo in golosSofridos.values():
        if(golo < min):
            min = golo
    for equipa in golosSofridos.keys():
        if(golosSofridos[equipa] == min):
            ret = equipa
    return ret
            
#printAtk : função retorna a lista da equipa que tem melhor ataque.
def printAtk():
    max = 0
    ret = -1
    for golos in golosMarcados.values():
        if(golos > max):
            max = golos
    for equipa in golosMarcados.keys():
        if(golosMarcados[equipa] == max):
            ret = equipa
    return ret

 #menuGerirEquipa : representação grafica do menu que gere as equipas no terminal.
def menuGerirEquipa():
    check = True
    while(check != False):
        print("<===============================>")
        print("<         Gerir Equipas         >")
        print("<===============================>")
        print("|                               |")
        print("|0)Sair                         |")
        print("|1)Adicionar Equipa             |")
        print("|2)Remover Equipa               |")
        print("|                               |")
        print("<===============================>")
        option = input(">?")
        option = checkMenuOption(option ,3)
        if(option == 0):
            check = False
        elif(option == 1):
            addSelecao()
        elif(option == 2):
            remSelecao()

#menuSimulacoes : representação grafica do menu de simulações. Também utilizada para chamar as funções apresentadas.
def menuSimulacoes(equipas, fase):
    if(len(equipas) == 0):
        limparCampeonato()
        return []
    elif(fase == 0):
        updateContinente(equipas)
        for x in equipas:
            golosMarcados[x[0]] = 0
            golosSofridos[x[0]] = 0
    fases = ["<       Oitavos de Final        >", "<       Quartos de Final        >", "<        Meias de Final         >", "<            Final              >"]
    vencedores = randJogo(equipas, fase)
    check = True
    while(check != False):
        print("<===============================>")
        print(fases[fase])
        print("<===============================>")
        print("|                               |")
        print("|0)Sair                         |")
        if (fase == 3):
            print("|1)Data da Final                |")
            print("|2)Resultados da Final          |")
        else:
            print("|1)Calendário da Fase           |")
            print("|2)Equipas Apuradas para Fase   |")
            print("|3)Jogo > Tempo Util da Fase    |")
            print("|4)Seguir para a proxima Fase   |")
        print("|                               |")
        print("<===============================>")
        option = input(">?")
        if(fase == 3):
            option = checkMenuOption(option ,3)
        else:
            option = checkMenuOption(option ,5)
        if(option == 0):
            return []
        elif(option == 1):
            printCalendario(fase,0)
        elif(option == 2):
            for equipa in vencedores:
                print(equipa)
        elif(option == 3):
            print(maisUtil(fase))
        elif(option == 4):
            incrementarData(2)
            return vencedores
        if(option != 0):
            input("(prima qualquer tecla para continuar)")

#menuEstatisticasCampeonato : representação gráfica do menu que apresenta as  Estatisticas do Campeonato.    
def menuEstatisticasCampeonato():
    if(len(jogosFase[0]) == 0 ):
        print("\n<========================================================================>")
        print("!!Por favor simule na totalidade um campeonato antes de aceder este menu!!")
        print("<========================================================================>\n")
        return
    check = True
    while(check != False):
        print("<===============================>")
        print("<    Estatisticas Campeonato    >")
        print("<===============================>")
        print("|                               |")
        print("|0)Sair                         |")
        print("|1)Calendário do Campeonato     |")
        print("|2)Calendário da Seleção        |")
        print("|3)Resultados do Dia            |")
        print("|4)Seleções por Continente      |")
        print("|5)Equipas Participantes        |")
        print("|6)Jogo > Tempo Util            |")
        print("|7)Seleção melhor Defesa        |")
        print("|8)Seleção melhor Ataque        |")
        print("|                               |")
        print("<===============================>")
        option = input(">?")
        option = checkMenuOption(option ,9)
        if(option == 0):
            check = False
        elif(option == 1):
            for x in range(4):
                printCalendario(x,0)
        elif(option == 2):
            selec =obterSeleção()
            for x in range(4):
                printCalendario(x,selec)
        elif(option == 3):
            print(resDia(obterData()))        
        elif(option == 4):
            distContinente()
        elif(option == 5):
            for participante in golosMarcados.keys():
                print(participante)
        elif(option == 6):
            maisUteis = []
            for x in range(4):
                maisUteis.append(maisUtil(x))
            sorted(maisUteis, key = lambda x : x[7], reverse=True)
            print(maisUteis[0])
        elif(option == 7):
            print(printDef())
        elif(option == 8):
            print(printAtk())
        if(option != 0):
            input("(prima qualquer tecla para continuar)")

#mainMenu : representação gráfica do menu principal.    
def mainMenu():
    check = True
    while(check != False):
        print("<===============================>")
        print("<             main              >")
        print("<===============================>")
        print("|                               |")
        print("|0)Sair                         |")
        print("|1)Gerir Seleções               |")
        print("|2)Simular Campeonato           |")
        print("|3)Estatisticas Campeonato      |")
        print("|                               |")
        print("<===============================>")
        option = input(">?")
        option = checkMenuOption(option ,4)
        if(option == 0):
            check = False
        elif(option == 1):
            menuGerirEquipa()
        elif(option == 2):
            limparCampeonato()
            dataTemp = obterData()
            data[0] = dataTemp[0]
            data[1] = dataTemp[1]
            data[2] = dataTemp[2]
            menuSimulacoes(menuSimulacoes(menuSimulacoes(menuSimulacoes(apuramento(), 0), 1), 2),3)
        elif(option == 3):
            menuEstatisticasCampeonato()

#execução da main.
if __name__ == "__main__":
    main()