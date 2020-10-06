from flask import Flask,request,send_from_directory
import os
#https://matplotlib.org/tutorials/text/text_intro.html#sphx-glr-tutorials-text-text-intro-py
#
#https://getbootstrap.com/docs/4.5/layout/grid/
#
#https://flask.palletsprojects.com/en/1.1.x/quickstart/#accessing-request-data

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 

@app.route('/')
def index():
  return '<h2>Main</h2> <br> redirecting to /control... <meta http-equiv = "refresh" content = "2; url = /control/" />'

@app.route('/control/')
def control():
    #print("screen got hit")
    #print("request GET")
    file = open("control.html", "r")
    html = file.read()

    Penable= str(request.args.get('P__' , ""))
    Ienable= str(request.args.get('PI_' , ""))
    Denable= str(request.args.get('PID' , ""))

    a1 = str(request.args.get('A1' , "" ))
    b1 = str(request.args.get('B1' , ""))
    ts = str(request.args.get('Amostragem' , ""))

    sp= str(request.args.get('SetPoint'      , ""))
    p = str(request.args.get('Proporcional'  , ""))
    i = str(request.args.get('Integral'      , ""))
    d = str(request.args.get('Derivativo'    , ""))

    fs = str(request.args.get('fixed_scale'    , ""))
    
    ps = str(request.args.get('plot_sample'    , ""))

    modo=""
    if Denable:
        modo="PID"
    else:
        if Ienable:
            modo="PI"
            d = 0
        else:
            modo="P"
            d = 0
            i = 0

    if a1=="":
        a1=0.9930900
    if b1=="":
        b1 = 0.0058096
    if ts=="":
        ts=0.3
    if sp=="":
        sp = 50
    if p=="":
        p = 0
    if i=="":
        i = 0
    if d=="":
        d = 0
    if fs=="":
        fs=0
    if ps=="":
        ps=0

    
    
    print (request.headers)
    #print( app.Request.user_agent)
    print("EQ  [",a1,b1,ts,"]\nVAR [",modo,sp,p,i,d,fs,ps,"]")

    #print (request.args)
    #import  prolabs_flask
    #resp=resp+str(prolabs_flask.main(0,p9))
    import plot3trab
    retorno=plot3trab.plot(modo,float(a1),float(b1),float(ts),float(sp),float(p),float(i),float(d),int(fs),int(ps))
    html=html.replace("table_placeholder",retorno)
    print("now sending...")
    return html 

 
@app.route('/tmp/<path:path>')
def send_file(path):
    return send_from_directory('tmp', path)

if __name__ == '__main__':
  app.run(debug=True)    #Localhost
  #app.run(host= '0.0.0.0',debug=True)    #LAN