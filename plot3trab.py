import matplotlib
import time
import matplotlib.pyplot as plt
import numpy as np
import re
import calculos


def create_table(modo, a1, b1, sp, p, i, d, pico,os, overshoot,tm, tempo_acomodacao):
    Html = "<table>"
    Html = Html+"<tr><th>     Param.  </th>    <th>Valor                     </th></tr>"
    Html = Html+"<tr><td>     Modo    </th>    <td>" + modo +  "             </td></tr>"
    Html = Html+"<tr><td>     A1      </td>    <td>" + str(a1)+"             </td></tr>"
    Html = Html+"<tr><td>     B1      </td>    <td>" + str(b1)+"             </td></tr>"
    Html = Html+"<tr><td>     SP      </td>    <td>" + str(sp)+"             </td></tr>"
    Html = Html+"<tr><td>     KP       </td>    <td>" + str(p)+"              </td></tr>"
    Html = Html+"<tr><td>     KI       </td>    <td>" + str(i)+"              </td></tr>"
    Html = Html+"<tr><td>     KD       </td>    <td>" + str(d)+"              </td></tr>"
    Html = Html+"<tr><td>     Pico    </td>    <td>" + str(round(pico, 2))+"        </td></tr>"
    if (overshoot>=os):
        Html = Html+'<tr><td>     Overshoot        </td><td class="text-danger">' + str(round(overshoot, 2))+"  </td></tr>"
    else:
        Html = Html+'<tr><td>     Overshoot        </td><td class="text-success">' + str(round(overshoot, 2))+"  </td></tr>"
    if (tempo_acomodacao>=tm):
        Html = Html+'<tr><td>     TS      </td><td class="text-danger">' + str(round(tempo_acomodacao, 2))+"  </td></tr>"
    else:
        Html = Html+'<tr><td>     TS      </td><td class="text-success">' + str(round(tempo_acomodacao, 2))+"  </td></tr>"

    Html = Html+"</table>"
    # <p class="text-success">.text-success</p>
    # vc nao esta vendo errado, isto eh exatamente oque vc pensa que eh
    return Html

def plot(modo, a1, b1, ts, sp, kp, ki, kd, fs, ps, pa, os,tm,k,tal):
    samples = []
    ref_arquivo = open("samples.txt","r")
    linhas = ref_arquivo.readlines()
    for i in range(len(linhas)):
        linhas[i] = re.sub('\n','',linhas[i])
        linhas[i] = float(linhas[i])
        samples.append(linhas[i])
    pv = 0
    pvMA = 0
    pvMF = 0
    tempo = 0
    vetY = []
    vetYMA = []
    vetYMF = []
    vetT = []
    acaoIntegral = 0
    erroAnterior = sp-pv
    tempo_acomodacao = 0
    tempo_analise = 347.1
    if(modo=="Sint"):
        kp,ki = calculos.sintonia (os,tm,k,tal)
    if(pa):
        modo="Comparação"
    
    while (tempo < tempo_analise):
        vetY.append(pv)
        vetT.append(tempo)
        #MODOS:
        if(modo=="Comparação"):
            vetYMA.append(pvMA);
            vetYMF.append(pvMF);
            pvMA = calculos.malha_aberta(sp,pvMA,a1,b1)
            pvMF = calculos.malha_fechada(sp,pvMF,a1,b1)
            pv,acaoIntegral,erroAnterior = calculos.pid(sp,pv,a1,b1,kp,ki,kd,ts,acaoIntegral,erroAnterior)
        elif(modo=="MA"):
            pv = calculos.malha_aberta(sp,pv,a1,b1)
        elif(modo=="MF"):
            pv = calculos.malha_fechada(sp,pv,a1,b1)
        elif(modo=="PID" or modo=="Sint"):
            pv,acaoIntegral,erroAnterior = calculos.pid(sp,pv,a1,b1,kp,ki,kd,ts,acaoIntegral,erroAnterior)
        else:
            modo = '-'
        #TEMPO DE ACOMODAÇÃO:
        if(pv > sp*1.02):  # pv>51 (+2% de variação do valor setado)
            tempo_acomodacao = 0
        elif (pv < sp*0.98):  # pv<49 (-2% de variação do valor setado)
            tempo_acomodacao = 0
        elif(tempo_acomodacao == 0):
            tempo_acomodacao = tempo
        tempo = tempo+ts
        
    #GRÁFICO  
    fig, ax = plt.subplots()
    plt.xlim(xmin=0.0, xmax=tempo)
    if fs: #se a escala for fixa, limita ymax em 120% de sp
        plt.ylim(ymin=0.0, ymax=sp*1.2)
    if(modo=="Comparação"):
        ax.plot(vetT, vetYMA, color='darkorange', label="Malha Aberta")
        ax.plot(vetT, vetYMF, color='forestgreen', label="Malha Fechada")
        ax.plot(vetT, vetY, color='darkblue', label="PID")
        ax.legend()
    else:
        ax.plot(vetT, vetY, color='darkblue', label="Calculado")
    ax.set(xlabel='Tempo[s]', ylabel='Nível[mm]')
    if(ps):
        ax.plot(vetT, samples, color='crimson', label="Amostras")
        ax.legend()
    ax.grid()
    plt.subplots_adjust(top=0.95,)
    #CÁLCULO OVERSHOOT
    pico = max(vetY)
    overshoot = (pico-sp)/sp*100
    if (overshoot<0): 
        overshoot=0
    timestamp = str(int(time.time()*1000.0))
    name_image = "./tmp/Results"+timestamp+".png"
    fig.savefig(name_image)
    
    Html = create_table(modo, a1, b1, sp, kp, ki, kd,
                        pico,os, overshoot, tm,tempo_acomodacao)
    return Html, timestamp


