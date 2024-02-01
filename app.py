from flask import Flask, jsonify, request
from datetime import datetime,timedelta
app = Flask(__name__)
from Modelo import *
from flask import Flask, request,json
from db import *
import jwt
import uuid
# ...

def get(data,nombre,str1=True) -> str:
   try:
      dat= data[nombre] #if str1 else f'{}'
      print ('val ',nombre,' = ',dat)
      return    f'{dat}'
   except KeyError:
      return ''
def getToken(username,id) -> str:
   fecha = datetime.today()
   print(fecha)
   dias_a_sumar = timedelta(days=30)
   print(dias_a_sumar)
   fecha_nueva = (fecha + dias_a_sumar).strftime('%Y-%m-%d')
   print(fecha_nueva)
   resp ={"username": username,"id":id,"date": fecha_nueva}
   print(resp)
   encoded_jwt = jwt.encode(resp, "secret", algorithm="HS256")
   print(encoded_jwt)
   
   #print(dencoded_jwt)
   return encoded_jwt

def setToken(encoded_jwt) -> str:
   dencoded_jwt = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
  # dencoded_jwt = jwt.decode (encoded_jwt, "secret1", algorithm=["HS256"])
   print(dencoded_jwt)
   return dencoded_jwt

@app.route('/v1/token', methods=['GET'])
def handle_jlogin():
  content_type = request.headers.get('Content-Type')
  print (request.headers.get('username'))  
  print (request.headers.get('password'))  
  resp = sp(request.headers.get('username'),request.headers.get('password'))
  print ('+++++++++++++++++el sp devolvio  [',resp,']')
  if resp=='' :
    return  ({'error':'Datos Invalidos'})
  encoded_jwt =getToken(request.headers.get('username'),resp)
  return  ({'token':encoded_jwt})

@app.route('/v1/riskLevel', methods=['POST'])
def handle_json():
  print ('token re4cibido ',request.headers.get('token'))  
  print (setToken(request.headers.get('token')))
  content_type = request.headers.get('Content-Type')
  data = json.loads(request.data)
  print (request.data)
  print (data['date'])  
  id= str( uuid.uuid4())#'0fa2b371-1017-4859-98bf-61a63ca34eac'
  
  valores = [[
     id                           ,get(data,'merchant') , get(data,'subMerchant')  ,                          '',int(get(data,'amount'))         ,
     get(data,'additionalAmount') ,get(data,'currency') , get(data,'promoMonths')  ,get(data,'months')          ,'',
     get(data,'entryMode')        ,get(data,'serial')   , get(data,'merchantName') ,get(data,'bankName')        ,'',
     ''                           ,''                   , ''                       ,''                          ,get(data,'descriptor'),
     get(data,'operation')        ,get(data,'bin')      , get(data,'countryClient'),get(data,'postalCodeClient'), get(data,'cityClient'),
     get(data,'stateClient')      ,get(data,'cardType') , get(data,'cardBrand')
  ]]
  

  print ('data ',valores)
  val= model(valores)   
  print ('data .') 

  query=  "INSERT INTO public.transaccion("
  query+=  "    id, merchant, \"subMerchant\", amount, currency, \"promoMonths\", months, date, \"entryMode\", serial, acquirer, card, \"expYear\", \"expMonth\", reference, reference2, \"merchantName\", operation, bin, country, mcc, authentication, account, trigger, \"respCode\", \"authorization\", \"cardholderName\", email, score, \"CreationDate\""
  query+=  " ,   \"postalCodeClient\",\"cityClient\",\"stateClient\",\"additionalAmount\""
  query+=  "   )    VALUES "
  query+=  "       ("
  query+=   "'"+id  +"'"+",'"+ get(data,'merchant')+"','"+ get(data,'subMerchant')+"',"
  query += get(data,'amount',False)  +"," 
  query+= get(data,'currency')  +", '"+ get(data,'promoMonths') +"',"+  get(data,'months') +", TO_TIMESTAMP('"+ get(data,'date')  +"', 'dd-mm-yyyy hh24:mi:ss'), '"+get(data,'entryMode')  +"' , '"+ get(data,'serial')  +"' ,"
  query+= " '"+ get(data,'acquirer') +"' , "+ get(data,'card') +" , "+get(data,'expYear')  +" , "+  get(data,'expMonth') +" ,"+ get(data,'reference',False)  +", '"+ get(data,'reference2',False)  +"' , '"+ get(data,'merchantName')  +"' , '"
  query+=  get(data,'operation') +"' ,"+get(data,'bin')  +", '"+ get(data,'countryClient')  +"' ,"
  query+=     " "+  get(data,'mcc')  +" ,'"+ get(data,'authentication')  +"' , "+ get(data,'account')  +" , '"+get(data,'trigger')   
  query+= "' ,"+ ( get(data,'respCode')  if get(data,'respCode')  else '99') +","+(get(data,'authorization')  if  get(data,'authorization') else '0')  +", '" + get(data,'cardholderName') +"' , '"+get(data,'email')  +"',"+ f'{val}' +", TO_TIMESTAMP('"+  get(data,'date')+"', 'dd-mm-yyyy hh24:mi:ss')  "
  query+=     " , '"+  get(data,'postalCodeClient') +"' ,'"+ get(data,'cityClient') +"' , '"+  get(data,'stateClient') +"' , "+( get(data,'additionalAmount') if get(data,'additionalAmount') else null)    +""
  query+=      " );"
        
  print("query ["+query+"]")
  sp_insert (query)
  return  ({'id':id,'porce':val})


@app.route('/v1/update', methods=['POST'])
def handle_json_update():
  print ('token re4cibido ',request.headers.get('token'))  
  print (setToken(request.headers.get('token')))
  content_type = request.headers.get('Content-Type')
  #if (content_type == 'application/json'):
  data = json.loads(request.data)
  print (request.data)
  print (data['id'])  
  print (data['authorization'])    
  print (data['respCode'])
 
  query=  "update public.transaccion "
  query+=  " set  \"respCode\"= " +str(data['respCode'])+ " , \"authorization\"= "+str(data['authorization'])

  query+=  "       where id= '"+str(data['id']+"'")

  print("query ["+query+"]")
  sp_update (query)


  return  ({'resp':'ok'})
    #response = client.post('/data_extraction'), data=json.dumps(payload), headers=(accept_json)
    #return{'foo': 'bar'}

    #return {'aas':11,'as':122}
  #else:
   # return "Content type is not supported."


if __name__ == '__main__':
    app.run(debug=False, port=8000)
