import pymongo
import calculos

#Conexão com o BD
cliente = pymongo.MongoClient("mongodb+srv://administrador:2vUD4tsbjFxm8nZd@clusterc213.pkntv.mongodb.net/controlePID?retryWrites=true&w=majority")
db = cliente["controlePID"] #nome do banco
collection = db["amostras"] #nome da coleção

#Função para salvar a amostra no BD
def sendDB(nome,ts,resp,degrau):
  #Primeiramente, calcula-se os parâmetros a1,b1,k e tal da amostra recebida
  size = len(resp)
  a1,b1= calculos.minimos_quadrados(size,resp,degrau)
  k,tal= calculos.funcao_transferencia(ts,size,a1,b1)
  #Depois, os valores são salvos no BD
  dados = {"nome": nome, "pv" : resp, "sp": degrau[0], "ts":ts, "a1":a1, "b1":b1, "k":k,"tal":tal}
  collection.insert_one(dados)

#Função para retornar as amostras salvas no BD
sample = "sample-select"
select = "select"
importar = "importar"
def searchDB():
  resposta = collection.find() #Busca-se no BD e exibe a lista em html
  Html = "<select id="+select+"  multiple name="+sample+">"
  for data in resposta: 
    Html = Html+"<option value="+ str(data['nome']) + ">" + str(data['nome']) +  "</option>"
  Html = Html + "<input type=submit value=Import id="+importar+">"
  Html = Html+"</select>"
  return Html

#Busca os dados de uma amostra em específico
def searchSampleDB(nome_amostra):
  resposta = collection.find_one({'nome':nome_amostra})
  return resposta

#Salva os resultados do tipo PID em uma coleção a parte específica para a amostra
def sendResultDB(nome_amostra,kp,ki,kd,pico,overshoot,tempo_acomodacao):
  collection = db[nome_amostra] #nome da coleção
  dados = {"kp": kp, "ki" : ki, "kd": kd, "pico":pico, "overshoot":overshoot, "tempo_acomodacao":tempo_acomodacao}
  collection.insert_one(dados)