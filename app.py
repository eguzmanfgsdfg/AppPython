from flask import Flask, jsonify, request
from datetime import datetime,timedelta
app = Flask(__name__)
from Modelo import *
from flask import Flask, request,json
from db import *
import jwt
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

@app.route('/v1/', methods=['GET'])
def handle_jlogin_():
  print ('++++++++++++++++++hola++++++++++')
  return  ({'status':'ok'})
   
@app.route('/v1/login', methods=['GET'])
def handle_jlogin():
  content_type = request.headers.get('Content-Type')
  #if (content_type == 'application/json'):
  #data = json.loads(request.data)
 # print (request.data)
  print (request.headers.get('username'))  
  print (request.headers.get('password'))  
  resp = sp(request.headers.get('username'),request.headers.get('password'))
  print ('el sp devolvio ',resp)

  #decoder_jwt=jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
  #print(decoder_jwt)
  encoded_jwt =getToken(request.headers.get('username'),resp)
  return  ({'jwt':encoded_jwt})

@app.route('/v1/riskLevel', methods=['POST'])
def handle_json():
  print ('token re4cibido ',request.headers.get('token'))  
  print (setToken(request.headers.get('token')))
  content_type = request.headers.get('Content-Type')
  #if (content_type == 'application/json'):
  data = json.loads(request.data)
  print (request.data)
  print (data['date'])  
  id= '0fa2b371-1017-4859-98bf-61a63ca34eac'
  #valores = [[id,get(data,'merchant'),get(data,'subMerchant'),'',get(data,'amount'),get(data,'additionalAmount'),get(data,'currency'),'','',get(data,'date'),'0',get(data,'serial'),get(data,'merchantName'),'',get(data,'card'),get(data,'promoMonths'),get(data,'months'),'MC-13379191',get(data,'entryMode'),get(data,'serial'),'0',get(data,'bin'),'US','65101','JEFFERSON CITY','MO','OTHER','Visa','0','0','0','0',40,get(data,'email'),get(data,'cardholderName'),'0','0','0'   ]]
  #valores = [[id,get(data,'merchant'),get(data,'subMerchant'),'',get(data,'amount'),get(data,'additionalAmount'),get(data,'currency'),'','',get(data,'date'),'0',get(data,'serial'),get(data,'merchantName'),'',get(data,'card'),get(data,'promoMonths'),get(data,'months'),'MC-13379191',get(data,'entryMode'),get(data,'serial'),'0',get(data,'bin'),'US','65101','JEFFERSON CITY','MO','OTHER','Visa','0','0','0','0',40,get(data,'email'),get(data,'cardholderName'),'0','0','0'   ]]
  valores = [[
     id                           ,get(data,'merchant') , get(data,'subMerchant')  ,                          '',int(get(data,'amount'))         ,
     get(data,'additionalAmount') ,get(data,'currency') , get(data,'promoMonths')  ,get(data,'months')          ,'',
     get(data,'entryMode')        ,get(data,'serial')   , get(data,'merchantName') ,get(data,'bankName')        ,'',
     ''                           ,''                   , ''                       ,''                          ,get(data,'descriptor'),
     get(data,'operation')        ,get(data,'bin')      , get(data,'countryClient'),get(data,'postalCodeClient'), get(data,'cityClient'),
     get(data,'stateClient')      ,get(data,'cardType') , get(data,'cardBrand')
  ]]
  
  
#          [[input[0][1] , input[0][2],rango       ,input[0][5] ,input[0][6] , #'Afiliacion', 'SubAffiliation','Amount', 'additionalAmount', 'currency',
#            input[0][7] , input[0][8],input[0][10],input[0][11],input[0][12], #'Promo Months','months','entryMode','IPAddress','Merchant Account Name',
#            input[0][13],input[0][19],input[0][20],input[0][21],input[0][22], #'Bank Account Name','Descriptor','operation', 'Bin8', 'Customer Country',
#            input[0][23],input[0][24],input[0][25],input[0][26],input[0][27], #'Customer Zip Code', 'Customer City','Customer State','Credit Card Type', 'Credit Card Brand',
#            rango_in_bank_currency]] #'Amount Charged in Bank Currency'
  print ('data ',valores)
  val= model(valores)   
  

  query=  "INSERT INTO public.transaccion("
  query+=  "    id, merchant, \"subMerchant\", amount, currency, \"promoMonths\", months, date, \"entryMode\", serial, acquirer, card, \"expYear\", \"expMonth\", reference, reference2, \"merchantName\", operation, bin, country, mcc, authentication, account, trigger, \"respCode\", \"authorization\", \"cardholderName\", email, score, \"CreationDate\""
  #query+=  " \"acquirer\", \"card\", \"expYear\", \"expMonth\", \"reference\", \"reference2\", \"merchantName\", \"operation\", \"bin\", \"country\","
 # query+=  "  \"mcc\", \"authentication\", \"account\", \"trigger\", \"respCode\", \"authorization\", \"cardholderName\", \"email\", \"score\", \"CreationDate\""
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

  sp_all()
  return  ({'data':data,'porce':val})
    #response = client.post('/data_extraction'), data=json.dumps(payload), headers=(accept_json)
    #return{'foo': 'bar'}

    #return {'aas':11,'as':122}
  #else:
   # return "Content type is not supported."



@app.route('/v1/update', methods=['POST'])
def handle_json_update():
  print ('token re4cibido ',request.headers.get('token'))  
  print (setToken(request.headers.get('token')))
  content_type = request.headers.get('Content-Type')
  #if (content_type == 'application/json'):
  data = json.loads(request.data)
  print (request.data)
  print (data['id'])  
  print (data['response'])
  print (data['date'])    
  id= '0fa2b371-1017-4859-98bf-61a63ca34eac'
  #valores = [[id,get(data,'merchant'),get(data,'subMerchant'),'',get(data,'amount'),get(data,'additionalAmount'),get(data,'currency'),'','',get(data,'date'),'0',get(data,'serial'),get(data,'merchantName'),'',get(data,'card'),get(data,'promoMonths'),get(data,'months'),'MC-13379191',get(data,'entryMode'),get(data,'serial'),'0',get(data,'bin'),'US','65101','JEFFERSON CITY','MO','OTHER','Visa','0','0','0','0',40,get(data,'email'),get(data,'cardholderName'),'0','0','0'   ]]
  #valores = [[id,get(data,'merchant'),get(data,'subMerchant'),'',get(data,'amount'),get(data,'additionalAmount'),get(data,'currency'),'','',get(data,'date'),'0',get(data,'serial'),get(data,'merchantName'),'',get(data,'card'),get(data,'promoMonths'),get(data,'months'),'MC-13379191',get(data,'entryMode'),get(data,'serial'),'0',get(data,'bin'),'US','65101','JEFFERSON CITY','MO','OTHER','Visa','0','0','0','0',40,get(data,'email'),get(data,'cardholderName'),'0','0','0'   ]]
  valores = [[
     id                           ,get(data,'merchant') , get(data,'subMerchant')  ,                          '',int(get(data,'amount'))         ,
     get(data,'additionalAmount') ,get(data,'currency') , get(data,'promoMonths')  ,get(data,'months')          ,'',
     get(data,'entryMode')        ,get(data,'serial')   , get(data,'merchantName') ,get(data,'bankName')        ,'',
     ''                           ,''                   , ''                       ,''                          ,get(data,'descriptor'),
     get(data,'operation')        ,get(data,'bin')      , get(data,'countryClient'),get(data,'postalCodeClient'), get(data,'cityClient'),
     get(data,'stateClient')      ,get(data,'cardType') , get(data,'cardBrand')
  ]]
  
  
#          [[input[0][1] , input[0][2],rango       ,input[0][5] ,input[0][6] , #'Afiliacion', 'SubAffiliation','Amount', 'additionalAmount', 'currency',
#            input[0][7] , input[0][8],input[0][10],input[0][11],input[0][12], #'Promo Months','months','entryMode','IPAddress','Merchant Account Name',
#            input[0][13],input[0][19],input[0][20],input[0][21],input[0][22], #'Bank Account Name','Descriptor','operation', 'Bin8', 'Customer Country',
#            input[0][23],input[0][24],input[0][25],input[0][26],input[0][27], #'Customer Zip Code', 'Customer City','Customer State','Credit Card Type', 'Credit Card Brand',
#            rango_in_bank_currency]] #'Amount Charged in Bank Currency'
  print ('data ',valores)
  val= model(valores)   
  

  query=  "INSERT INTO public.transaccion("
  query+=  "    id, merchant, \"subMerchant\", amount, currency, \"promoMonths\", months, date, \"entryMode\", serial, acquirer, card, \"expYear\", \"expMonth\", reference, reference2, \"merchantName\", operation, bin, country, mcc, authentication, account, trigger, \"respCode\", \"authorization\", \"cardholderName\", email, score, \"CreationDate\""
  #query+=  " \"acquirer\", \"card\", \"expYear\", \"expMonth\", \"reference\", \"reference2\", \"merchantName\", \"operation\", \"bin\", \"country\","
 # query+=  "  \"mcc\", \"authentication\", \"account\", \"trigger\", \"respCode\", \"authorization\", \"cardholderName\", \"email\", \"score\", \"CreationDate\""
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


  sp_all()
  return  ({'data':data,'porce':val})
    #response = client.post('/data_extraction'), data=json.dumps(payload), headers=(accept_json)
    #return{'foo': 'bar'}

    #return {'aas':11,'as':122}
  #else:
   # return "Content type is not supported."

if __name__ == '__main__':
    app.run(debug=False, port=8000)
