#Criação da tabela em html
def create_table(modo, a1, b1, sp, p, i, d, pico,os, overshoot,tm, tempo_acomodacao):
    Html = "<table>"
    Html = Html+"<tr><th>     Param.  </th>    <th>Valor                     </th></tr>"
    Html = Html+"<tr><td>     Modo    </th>    <td>" + modo +  "             </td></tr>"
    Html = Html+"<tr><td>     A1      </td>    <td>" + str(a1)+"             </td></tr>"
    Html = Html+"<tr><td>     B1      </td>    <td>" + str(b1)+"             </td></tr>"
    Html = Html+"<tr><td>     SP      </td>    <td>" + str(sp)+"             </td></tr>"
    Html = Html+"<tr><td>     KP      </td>    <td>" + str(p)+"              </td></tr>"
    Html = Html+"<tr><td>     KI      </td>    <td>" + str(i)+"              </td></tr>"
    Html = Html+"<tr><td>     KD      </td>    <td>" + str(d)+"              </td></tr>"
    Html = Html+"<tr><td>     Pico    </td>    <td>" + str(round(pico, 2))+"        </td></tr>"
    #Caso o valor real do overshoot, seja maior que o máx. desejado, o texto é exibido em vermelhor
    overshoot = round(overshoot, 2)
    tempo_acomodacao = round(tempo_acomodacao, 2)
    if (overshoot>os): 
        Html = Html+'<tr><td> Overshoot </td><td class="text-danger">' + str(overshoot)+"  </td></tr>"
    else: #Caso contrário em verde
        Html = Html+'<tr><td> Overshoot </td><td class="text-success">' + str(overshoot)+"  </td></tr>"

    #O mesmo ocorre para o tempo de acomodação
    if (tempo_acomodacao>tm):
        Html = Html+'<tr><td> TS </td><td class="text-danger">' + str(tempo_acomodacao)+"  </td></tr>"
    else:
        Html = Html+'<tr><td> TS </td><td class="text-success">' + str(tempo_acomodacao)+"  </td></tr>"
        
    Html = Html+"</table>"
    return Html