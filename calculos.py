import cmath
import math

def malha_aberta(sp,pv,a1,b1):
     pv = a1*pv+ b1*sp
     return pv
 
def malha_fechada(sp,pv,a1,b1):
    erro = sp - pv; 
    pv = a1*pv+ b1*erro;
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