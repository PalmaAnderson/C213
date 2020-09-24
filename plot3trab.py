import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#oi
def create_table(modo,a1,b1,sp,p,i,d,pico):
    Html=     "<table>"
    Html=Html+"<tr><th>     Param.  </th>    <th>Valor                   </th></tr>"
    Html=Html+"<tr><td>     Modo    </th>    <td>"+modo+   "             </td></tr>"
    Html=Html+"<tr><td>     A1      </td>    <td>"+str(a1)+"             </td></tr>"
    Html=Html+"<tr><td>     B1      </td>    <td>"+str(b1)+"             </td></tr>"
    Html=Html+"<tr><td>     SP      </td>    <td>"+str(sp)+"             </td></tr>"
    Html=Html+"<tr><td>     P       </td>    <td>"+str(p)+"              </td></tr>"
    Html=Html+"<tr><td>     I       </td>    <td>"+str(i)+"              </td></tr>"
    Html=Html+"<tr><td>     D       </td>    <td>"+str(d)+"              </td></tr>"
    tol=sp*1.03
    Html=Html+"<tr><td>     3% Tol. </td>    <td>"+str(tol)+"        </td></tr>"
    if(pico<tol):
        Html=Html+'<tr><td>     Pico    </td><td class="text-success">'+str(round(pico,2))+"  </td></tr>"
    else:
        Html=Html+'<tr><td>     Pico    </td><td class="text-danger">'+str(round(pico,2))+"  </td></tr>"
    Html=Html+"</table>"
    #<p class="text-success">.text-success</p>
    #vc nao esta vendo errado, isto eh exatamente oque vc pensa que eh
    return Html

def plot(modo,a1,b1,sp,p,i,d):
    
    
    #for x in range(0, len(samples)):
    #    print (samples[x])

    #limite = len(samples)      # 600 amostras (10 minutos)
    limite=1200
    amostragem = 1  # intervalo entre amostras
    leituras = []     # valor vazio
    tempo = np.arange(0, limite*amostragem, amostragem)
    #tempo2 = np.arange(0, (limite)*3, amostragem)

    # preenche o vetor com 6000 amostras
    # entre 0 e 599.9
    #a1 = 0.9930900
    #b1 = 0.0058096
    kp = float(p)  #ganho proporcional
    ki = float(i)  #ganho integral



    #setpoint = 0
    saida = 0
    #alvo = 50
    alvo=float(sp)
    leituras.append(saida)  # instante zero vale zero

    erro = 50  # erro inicial
    acao_int=0
    for cont in tempo:
        acao_int=acao_int+ki*amostragem*erro
        acao_pro=kp*erro

        acao_controle=acao_int+acao_pro
        erro = alvo-leituras[int(cont)]
        #print (round(cont,1))
        # esta string feia quer dizer erro = (alvo)-(ultima saida)
        if modo=="P":
            leituras.append(( a1*leituras[int(cont)] + b1*alvo)) #Q1
        else:
            leituras.append(( a1*leituras[int(cont)] + kp*b1*acao_controle))  #Q2
        #leituras.append(( a1*leituras[int(cont)] + b1*kp*erro))  #Q3

    #   if cont >= 344.3:
        if cont >= (tempo.max()-1*amostragem):
            break


    #for leitura in leituras:
    #    print(leitura)

    #t = tempo
    #v = leituras

    #for t in range(0,len(tempo)):
    #    a=tempo[t]*0.3
    #    print(a)
    #    tempo[t]=a

    fig, ax = plt.subplots()
    #plt.xlim(xmin=0.0,xmax=len(samples))
    plt.xlim(xmin=0.0,xmax=1200)
    plt.ylim(ymin=0.0,ymax=60)

    pico=max(leituras)
    
    ax.plot(tempo, leituras, color='darkblue', label="Equação")
    #ax.plot(tempo, samples , color='crimson' , label="Leitura" )

    ax.legend()
    titulo = "Grafico de amostras vs tempo"
    ax.set(xlabel='Amostras', ylabel='Valores', title=titulo)
    ax.grid()
    #plt.show()
    fig.savefig("./static/Results.png")

    
    Html=create_table(modo,a1,b1,sp,p,i,d,pico)
    return Html
