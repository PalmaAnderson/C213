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

    sp= str(request.args.get('SetPoint'      , ""))
    p = str(request.args.get('Proporcional'  , ""))
    i = str(request.args.get('Integral'      , ""))
    d = str(request.args.get('Derivativo'    , ""))

    modo=""
    if Denable:
        modo="PID"
    else:
        if Ienable:
            modo="PI"
        else:
            modo="P"

    if a1=="":
        a1=0.9930900
    if b1=="":
        b1 = 0.0058096
    if sp=="":
        sp = 50
    if p=="":
        p = 1
    if i=="":
        i = 1
    if d=="":
        d = 1
    
    print (request.headers)
    #print( app.Request.user_agent)
    print("EQ  [",a1,b1,"]\nVAR [",modo,sp,p,i,d,"]")

    #print (request.args)
    #import  prolabs_flask
    #resp=resp+str(prolabs_flask.main(0,p9))
    import plot3trab
    aaa=plot3trab.plot(modo,float(a1),float(b1),float(sp),float(p),float(i),float(d))
    html=html.replace("yyyy",aaa)
    print("now sending...")
    return html 

 
@app.route('/tmp/<path:path>')
def send_file(path):
    return send_from_directory('tmp', path)

if __name__ == '__main__':
  app.run(debug=True)