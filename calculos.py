import cmath
import math
import numpy as np

def malha_aberta(sp,pv,a1,b1):
     pv = a1*pv+ b1*sp
     return pv
 
def malha_fechada(sp,pv,a1,b1):
    erro = sp - pv
    pv = a1*pv+ b1*erro
    return pv

def pid(sp,pv,a1,b1,kp,ki,kd,ts,acaoIntegral,erroAnterior):
    erro = sp - pv
    acaoProporcional = kp * erro
    acaoIntegral = acaoIntegral + ki*ts*erro
    acaoDerivativa = ((erro - erroAnterior)/ts)*kd
    acaoControlador = acaoProporcional + acaoIntegral + acaoDerivativa
    pv = a1*pv + b1*acaoControlador
    erroAnterior = erro
    return pv,acaoIntegral,erroAnterior

def sintonia(mp,ts,k,tal): #Cálculos do modelo Resposta em Frequência para controlador do tipo PI
    mp = mp/100
    csi=math.sqrt((math.pow(((math.log(mp))/math.pi),2))/(1+(math.pow(((math.log(mp))/math.pi),2))))
    wn=4/(csi*ts)
    wcg=wn
    MF=2*math.degrees(math.asin(csi))
    G=k/(complex(1,(tal*wcg)))
    modG=abs(G)
    faseG=math.degrees(cmath.phase(G))
    modC=1/modG
    faseC=-180+MF-faseG
    Kp=math.sqrt((math.pow(modC,2))/(1+math.pow((math.tan(math.radians(faseC))*(-1)),2)))
    Ki=math.tan(math.radians(faseC))*(-1)*(wcg)*Kp
    return round(Kp,4),round(Ki,4)

def minimos_quadrados(size,resp,degrau):
    transpostaF = [resp[0:size-1],degrau[0:size-1]]
    F = np.transpose(transpostaF)
    J = resp[1:size]
    Theta = np.linalg.inv(transpostaF@F)@transpostaF@J
    a1 = round(Theta[0],5)
    b1 = round(Theta[1],5)
    return a1,b1

#Como não foi encontrada uma função correlata ao d2c para python, utilizou-se da lógica da análise gráfica
def funcao_transferencia(ts,size,a1,b1):
    vetY = []
    vetY2 = []
    vetT = []
    tempo_analise = ts*size
    tempo = 0
    pv = 0
    while (tempo<tempo_analise): #Gera-se os valores de pv para um tempo x
        vetY.append(round(pv,3))
        vetY2.append(round(pv,2))
        vetT.append(tempo)
        pv = a1*pv+ b1 
        tempo=tempo+ts
    k = round(max(vetY),5) #k é o maior valor dentre os valores de pv
    try: #Encontra-se o valor de pv que corresponde a 1 tal 
        pv_tal = round(0.632*k,3) 
        #Procura no vetor de tempo, o valor de tempo cujo índice é igual ao índice de pv(tal) 
        tal = vetT[vetY.index(pv_tal)]
        #Contudo, como a função não é contínua, o valor nem sempre será encontrada
        #Então, utiliza-se da aproximação de casas decimais para buscar um valor próximo
        #e a estrutura try-expect para evitar a falha de execução
    except ValueError:
        try:
            pv_tal = round(0.632*k,2)
            tal = vetT[vetY2.index(pv_tal)]
        except ValueError:
            print('Não foi possível encontrar tal.')
            tal = 0
    tal = round(tal,3)
    return k,tal