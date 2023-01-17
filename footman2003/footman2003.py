import csv
import random
 

#variável global dias_mes : organização de todos os meses acabados no dia 30 e no dia 31
global dias_mes
dias_mes = {
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

global num_jogo
num_jogo = [0]

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
#golos_marcados : biblioteca que associa ao nome da equipa, os golos que eles marcaram
global golos_marcados
golos_marcados = {}
#golos_sofridos : biblioteca que associa ao nome da equipa, os golos que eles sofreram
global golos_sofridos
golos_sofridos = {}
    
#varíavel global equipas_fase: Dicionario que guarda a informação de todas as equipas que passam cada fase do campeonato
global equipas_fase
equipas_fase = {
    "oitavos" : [], 
    "quartos" : [], 
    "meias" : [], 
    "final" : []
}
#varíavel global jogos_fase: Dicionario que guarda as informações de cada jogo em cada fase do campeonato
global jogos_fase
jogos_fase = {
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
    main_menu()

#add_selecao : função que adiciona uma seleção à lista de seleções
def add_selecao():
    nome = input("Introduza o nome da seleção: ") 
    pais = input("Introduza o país da sua seleção: ")
    continente = input("Introduza o continente da seleção: ") 
    ranking =int(input("Introduza o ranking da seleção: "))
    selecoes.append([nome, pais, continente, ranking])

#rem_selecao : função que remove uma equipa da lista de seleções
def rem_selecao():
    selecaoRemovida = input("Qual equipa vai ser removida: ")
    for x in selecoes:
        if selecaoRemovida == x[0]:
            selecoes.remove(x)
            break
        
#ano_bissexto : função que testa se um ano é ou não bissexto.
def ano_bissexto(ano):
    if((ano % 400 == 0) or (ano % 100 != 0) and (ano% 4 == 0)):  
        return True
    else:
        return False

#incrementar_data : função que adiciona n dias (incremento) à data global
def incrementar_data(incremento):
    data[0] += incremento
    if((data[1] in dias_mes[31] and data[0] > 31) or (data[1] in dias_mes[30] and data[0] > 30)):
        data[0] = incremento
        data[1] += 1
    elif((data[1] == 2 and ano_bissexto(data[2]) == False and data[0] > 28) or (data[1] == 2 and ano_bissexto(data[2]) == True and data[0] > 29)):
        data[0] = incremento
        data[1] += 1
    if(data[1] > 12):
        data[1] = 1
        data[2] += 1
    return data
    
#rand_jogo: simula todos os jogos de uma certa fase, retornando a lista de todas as equipas vencedoras (e apuradas para a proxima fase).
def rand_jogo(lista_equipa, fase):
    ret = []
    flip_flop = False
    while(len(lista_equipa) != 0):
        random.shuffle(lista_equipa)
        if(flip_flop == True):
            hora = "16:00"
            flip_flop = False
        else:
            hora = "14:00"
            flip_flop = True
        tempo_util = int(90 * ((random.randrange(60, 70)/100)))
        casa = lista_equipa[0]
        lista_equipa.pop(0)
        fora = lista_equipa[0]
        lista_equipa.pop(0)
        res_casa = random.randint(0, 6)
        res_fora = random.randint(0, 6)
        if(res_casa == res_fora):
            res_fora += 1
        if(res_casa > res_fora):
            equipa_apurada = casa
        else:
            equipa_apurada = fora
        ret.append(equipa_apurada)
        adicionar_golos_marcados(casa[0], res_casa)
        adicionar_golos_marcados(fora[0], res_fora)
        adicionar_golos_sofridos(casa[0], res_fora)
        adicionar_golos_sofridos(fora[0], res_casa)
        num_jogo[0] = num_jogo[0] + 1
        jogos_fase[fase].append([num_jogo[0], casa[0], fora[0], data.copy(), hora, res_casa, res_fora, tempo_util, equipa_apurada[0]])
        if(flip_flop == False):
            incrementar_data(1)
    return ret

#dist_continente : listar a distribuição de equipas por continente
def dist_continente():
    for continente, contagem in continentes.items():
        print(continente + ": " + str(contagem)) 

#update_continente : função que atualiza a distribuicao das equipas por continente 
def update_continente(selecoes):
    for continente in continentes.keys():   #reset de cada vez
        continentes[continente] = 0
    for selecao in selecoes:
        for continente in continentes.keys():
            if (continente.lower() == selecao[2].lower()):
                continentes[continente] += 1

#check_menu_options : verifica se a opção introduzida é válida em cada menu
def check_menu_option(to_check, max):
    if(to_check.isdigit()):
        ret = int(to_check)
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


#print_calendario : função que representa graficamente o calendario dos jogos de cada fase
def print_calendario(fase, filtro):  #fase -> 0 a 3
        fases = ["Oitavos de Final", "Quartos de Final", "Meias de Final", "Final"]
        to_print = [
            "<=================",
            " |  dia/mes/ano  |",
            " |  hora:        |",
            " |  casa:        |",
            " |  visitante:   |",
            "<=================",
        ]
        print("\n<" + fases[fase] + ">")
        for jogo in jogos_fase[fase]:
            if(filtro == 0 or filtro == jogo[1] or filtro == jogo[2]):
                to_print[0] += "=============="
                if(jogo[3][1] > 9 and jogo[3][0] > 9):
                    to_print[1] += "  "+str(jogo[3][0]) + "/" + str(jogo[3][1]) + "/" + str(jogo[3][2]) +" |"
                elif((jogo[3][1] > 9 and jogo[3][0] < 10) or (jogo[3][1] < 10 and jogo[3][0] > 9)):
                    to_print[1] += "   "+str(jogo[3][0]) + "/" + str(jogo[3][1]) + "/" + str(jogo[3][2]) +" |"
                else:
                    to_print[1] += "   "+str(jogo[3][0]) + "/" + str(jogo[3][1]) + "/" + str(jogo[3][2]) +"  |"
                to_print[2] += "     " + str(jogo[4])+ "   |"
                to_print[3]+= "     " + str(jogo[1]) + "     |"
                to_print[4]+= "     " + str(jogo[2]) + "     |"
                to_print[5] += "=============="
        to_print[0] += ">"
        to_print[5] += ">"  
        if(len(to_print[0]) != 18):
            for line in to_print:
                print(line)
        else:
            print("\n!!Horário inexistente!!\n")\

#valida_data : função que verifica se uma certa data é válida
def valida_data(a_validar):
    if(a_validar[0].isnumeric() and a_validar[1].isnumeric() and a_validar[2].isnumeric()):
        a_validar[0] = int(a_validar[0])
        a_validar[1] = int(a_validar[1])
        a_validar[2] = int(a_validar[2])
    else:
        return False
    if(a_validar[1] <= 12 and a_validar[0] > 0 and a_validar[1] > 0 and a_validar[2] >= 0):
        if((a_validar[1] in dias_mes[31] and a_validar[0] <= 31) or (a_validar[1] in dias_mes[30] and a_validar[0] <= 30)):
            return True
        elif((a_validar[1] == 2 and ano_bissexto(a_validar[2]) == False and a_validar[0] <= 28) or (a_validar[1] == 2 and ano_bissexto(a_validar[2]) == True and data[0] <= 29)):
            return True    
    return False

#obter_data : função que pede a data ao utilizador
def obter_data():
    check = True
    while(check != False):
        dia = input("Introduza um dia: ")
        mes = input("Introduza um mês: ")
        ano = input("Introduza um ano: ")
        if(valida_data([dia, mes, ano]) == True):
            return [int(dia), int(mes), int(ano)]
        print("\n<====================================================>")
        print("!!Data invalida, por favor introduza uma data válida!!")
        print("<====================================================>\n")
        option = input("(prima (0) para cancelar ou [enter] para continuar)")
        if(option == "0"):
            return -1

#res_dia : função que retorna os resultados de uma equipa num certo dia.           
def res_dia(dia):       
    ret = []
    if(dia == -1):
        return ret
    for fase in jogos_fase.keys():
        for jogo in jogos_fase[fase]:
            if(jogo[3][0] == dia[0] and jogo[3][1] == dia[1] and jogo[3][2] == dia[2]):
                ret.append(jogo)
    return ret               

#valida_selecao : função que verifica se uma selecao existe e é válida.
def valida_selecao(selecao):
    for fase in jogos_fase.keys():
        for jogo in jogos_fase[fase]:
            if(jogo[1] == selecao or jogo[2] == selecao):
                return True

#obter_seleção: função que pede ao utilizador o nome de uma certa seleção.
def obter_seleção():
    check = True
    while(check != False):
        selecao = input("Introduza o nome de uma selecão: ")
        if(valida_selecao(selecao) == True):
            return selecao
        print("\n<=========================================================>")
        print("!!Seleção invalida, por favor introduza uma seleção válida!!")
        print("<==========================================================>\n")
        option = input("(prima (0) para cancelar ou [enter] para continuar)")
        if(option == "0"):
            return -1

#limpar_campeonato : função que limpa todos os dados que foram acumulados  
def limpar_campeonato():
    num_jogo[0] = 0
    for fase in jogos_fase.keys():
        jogos_fase[fase] = []
    for fase in equipas_fase.keys():
        equipas_fase[fase] = []
    for continente in continentes.keys():
        continentes[continente] = 0
    golos_marcados.clear()
    golos_sofridos.clear()

#mais_util : função que retorna a lista com o jogo que tem o tempo mais util.
def mais_util(fase):
    max = 0
    for jogo in jogos_fase[fase]:
        if(jogo[7] > max):
            max = jogo[7]
            ret = jogo.copy()
    return ret

#adicionar_golos_sofridos: função que adiciona os dados ao dicionario de golos_sofridos
def adicionar_golos_sofridos(nome, golos):
    for equipa in golos_sofridos.keys():
        if(equipa == nome):
            golos_sofridos[equipa] = golos_sofridos[equipa] + golos

#adicionar_golos_sofridos: função que adiciona os dados ao dicionario de golos_marcados
def adicionar_golos_marcados(nome, golos):
    for equipa in golos_marcados.keys():
        if(equipa == nome):
            golos_marcados[equipa] = golos_marcados[equipa] + golos

#print_def : função retorna a lista da equipa que tem melhor defesa.
def print_def():
    min = 24
    ret = 0
    for golo in golos_sofridos.values():
        if(golo < min):
            min = golo
    for equipa in golos_sofridos.keys():
        if(golos_sofridos[equipa] == min):
            ret = equipa
    return ret
            
#print_atk : função retorna a lista da equipa que tem melhor ataque.
def print_atk():
    max = 0
    ret = -1
    for golos in golos_marcados.values():
        if(golos > max):
            max = golos
    for equipa in golos_marcados.keys():
        if(golos_marcados[equipa] == max):
            ret = equipa
    return ret

 #menu_gerir_equipa : representação grafica do menu que gere as equipas no terminal.
def menu_gerir_equipa():
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
        option = check_menu_option(option ,3)
        if(option == 0):
            check = False
        elif(option == 1):
            add_selecao()
        elif(option == 2):
            rem_selecao()

#menu_simulacoes : representação grafica do menu de simulações. Também utilizada para chamar as funções apresentadas.
def menu_simulacoes(equipas, fase):
    if(len(equipas) == 0):
        limpar_campeonato()
        return []
    elif(fase == 0):
        update_continente(equipas)
        for x in equipas:
            golos_marcados[x[0]] = 0
            golos_sofridos[x[0]] = 0
    fases = ["<       Oitavos de Final        >", "<       Quartos de Final        >", "<        Meias de Final         >", "<            Final              >"]
    vencedores = rand_jogo(equipas, fase)
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
            option = check_menu_option(option ,3)
        else:
            option = check_menu_option(option ,5)
        if(option == 0):
            return []
        elif(option == 1):
            print_calendario(fase,0)
        elif(option == 2):
            for equipa in vencedores:
                print(equipa)
        elif(option == 3):
            print(mais_util(fase))
        elif(option == 4):
            incrementar_data(2)
            return vencedores
        if(option != 0):
            input("(prima qualquer tecla para continuar)")

#menu_estatisticas_campeonato : representação gráfica do menu que apresenta as  Estatisticas do Campeonato.    
def menu_estatisticas_campeonato():
    if(len(jogos_fase[0]) == 0 ):
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
        option = check_menu_option(option ,9)
        if(option == 0):
            check = False
        elif(option == 1):
            for x in range(4):
                print_calendario(x,0)
        elif(option == 2):
            selec =obter_seleção()
            for x in range(4):
                print_calendario(x,selec)
        elif(option == 3):
            print(res_dia(obter_data()))        
        elif(option == 4):
            dist_continente()
        elif(option == 5):
            for participante in golos_marcados.keys():
                print(participante)
        elif(option == 6):
            mais_uteis = []
            for x in range(4):
                mais_uteis.append(mais_util(x))
            sorted(mais_uteis, key = lambda x : x[7], reverse=True)
            print(mais_uteis[0])
        elif(option == 7):
            print(print_def())
        elif(option == 8):
            print(print_atk())
        if(option != 0):
            input("(prima qualquer tecla para continuar)")

#main_menu : representação gráfica do menu principal.    
def main_menu():
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
        option = check_menu_option(option ,4)
        if(option == 0):
            check = False
        elif(option == 1):
            menu_gerir_equipa()
        elif(option == 2):
            limpar_campeonato()
            dataTemp = obter_data()
            data[0] = dataTemp[0]
            data[1] = dataTemp[1]
            data[2] = dataTemp[2]
            menu_simulacoes(menu_simulacoes(menu_simulacoes(menu_simulacoes(apuramento(), 0), 1), 2),3)
        elif(option == 3):
            menu_estatisticas_campeonato()

#execução da main.
if __name__ == "__main__":
    main()