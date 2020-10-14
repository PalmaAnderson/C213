import matplotlib
import time
import matplotlib.pyplot as plt
import numpy as np
import re
import cmath
import math


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

def sintonia(mp,ts,k,tal):
    mp = mp/100
    csi=math.sqrt((math.pow(((math.log(mp))/math.pi),2))/(1+(math.pow(((math.log(mp))/math.pi),2))))
    wn=4/(csi*ts)
    wcg=wn;
    MF=2*math.degrees(math.asin(csi));
    G=k/(complex(1,(tal*wcg)));
    modG=abs(G);
    faseG=math.degrees(cmath.phase(G));
    modC=1/modG;
    faseC=-180+MF-faseG;
    Kp=math.sqrt((math.pow(modC,2))/(1+math.pow((math.tan(math.radians(faseC))*(-1)),2)))
    Ki=math.tan(math.radians(faseC))*(-1)*(wcg)*Kp
    
    return round(Kp,4),round(Ki,4)

def plot(modo, a1, b1, ts, sp, kp, ki, kd, fs, ps, os,tm,k,tal):
    samples = []
    ref_arquivo = open("samples.txt","r")
    linhas = ref_arquivo.readlines()
    for i in range(len(linhas)):
        linhas[i] = re.sub('\n','',linhas[i])
        linhas[i] = float(linhas[i])
        samples.append(linhas[i])
    pv = 0
    tempo = 0
    vetY = []
    vetT = []
    acaoIntegral = 0
    erroAnterior = sp-pv
    tempo_acomodacao = 0
    tempo_analise = 347.1
    if(modo=="Sint"):
        kp,ki = sintonia (os,tm,k,tal) 
    
    while (tempo < tempo_analise):
        vetY.append(pv)
        vetT.append(tempo)
        if(modo=="MA"):
             pv = a1*pv+ b1*sp
        elif(modo=="MF"):
            erro = sp - pv; 
            pv = a1*pv+ b1*erro; 
        elif(modo=="PID" or modo=="Sint"):
            erro = sp - pv
            acaoProporcional = kp * erro
            acaoIntegral = acaoIntegral + ki*ts*erro
            acaoDerivativa = ((erro - erroAnterior)/ts)*kd
            acaoControlador = acaoProporcional + acaoIntegral + acaoDerivativa
            pv = a1*pv + b1*acaoControlador
            erroAnterior = erro
        else:
            modo = '-'
        if(pv > sp*1.02):  # pv>51 (+2% de variação do valor setado)
            tempo_acomodacao = 0
        elif (pv < sp*0.98):  # pv<49 (-2% de variação do valor setado)
            tempo_acomodacao = 0
        elif(tempo_acomodacao == 0):
            tempo_acomodacao = tempo
        tempo = tempo+ts
    fig, ax = plt.subplots()
    plt.xlim(xmin=0.0, xmax=tempo)
    # plt.xlim(xmin=0.0,xmax=350)

    if fs:
        plt.ylim(ymin=0.0, ymax=sp*1.2)
    ax.plot(vetT, vetY, color='darkblue', label="Calculado")
    ax.set(xlabel='Tempo[s]', ylabel='Nível[mm]')
    if(ps):
        ax.plot(vetT, samples, color='crimson', label="Amostras")
        ax.legend()
    ax.grid()
    plt.subplots_adjust(top=0.95,)
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


