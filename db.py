
import psycopg2
def sp(name,pass_) -> str:
    print('name ',name,' pass ',pass_)
    conexion1 = psycopg2.connect(host="db-dmrzl-bzpnac.cry7lrrhvglg.us-east-2.rds.amazonaws.com",port='5432'  , user="postgres", password="G3n3r42023!.", database="transaccion_api")
    print ('sdfgsdfffgff')
    cursor1=conexion1.cursor()
    query ="SELECT * FROM public.usertest where username='" + name + "' and password ='" +  pass_ + "'"
    print ('[',query,']')
    cursor1.execute(query)
#    cursor1.execute("update articulos set precio=50 where codigo=3")
    #conexion1.commit()
    #cursor1.execute("select codigo, descripcion, precio from articulos")
    retur=''    
    for fila in cursor1:
        print(fila)
        print(fila[0])
        retur=fila[0]
    conexion1.close()   
    print('responde')
    return retur

def sp_insert(query) -> str:
    print('dentro sdfwe wert query ',query)
    conexion1 = psycopg2.connect(host="db-dmrzl-bzpnac.cry7lrrhvglg.us-east-2.rds.amazonaws.com",port='5432'  , user="postgres", password="G3n3r42023!.", database="transaccion_api")
    print ('sdfgsdfffgff')
    cursor1=conexion1.cursor()
    print ('[',query,']')
    varrr= cursor1.execute(query)
#    cursor1.execute("update articulos set precio=50 where codigo=3")
    #conexion1.commit()
    #cursor1.execute("select codigo, descripcion, precio from articulos")
    retur=''    
    print('fila ',cursor1)
    print('varrr ',varrr)
    #for fila in cursor1:
    #    print(fila)
    #conexion1.close()   
    #print('responde')
    return retur


def sp_all() -> str:
    query ='select * from public.transaccion'
    print('all ')
    conexion1 = psycopg2.connect(host="db-dmrzl-bzpnac.cry7lrrhvglg.us-east-2.rds.amazonaws.com",port='5432'  , user="postgres", password="G3n3r42023!.", database="transaccion_api")
    print ('sdfgsdfffgff')
    cursor1=conexion1.cursor()
    print ('[',query,']')
    cursor1.execute(query)
#    cursor1.execute("update articulos set precio=50 where codigo=3")
    #conexion1.commit()
    #cursor1.execute("select codigo, descripcion, precio from articulos")
    retur=''   
    print('registros ',cursor1.rowcount)
    #for fila in cursor1:
    #    print(fila)
    conexion1.close()   
    print('responde')
    return retur