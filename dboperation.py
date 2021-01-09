import psycopg2


class DBWebscraping:
    def __init__(self):
        pass

    def insert_webscraping(self, connection, carga):
        try:
          mydb = connection.connect()         
          cur = mydb.cursor() 

          sql = "insert into webscraping (busqueda, busqueda_area, pagina_web, url_pagina, url_busqueda,fecha_creacion,fecha_modificacion) values (%s,%s,%s,%s,%s,current_date,current_date)"
          params = (carga["busqueda"], carga["busqueda_area"], carga["pagina"], carga["url_principal"],carga["url_busqueda"])
                    
          cur.execute(sql, params)                 

          mydb.commit()

          sql = "SELECT last_value FROM webscraping_id_webscraping_seq"
          cur.execute(sql)  
          row_id = int(cur.fetchone()[0])

          cur.close()
          mydb.close()      
        except (Exception, psycopg2.DatabaseError) as error:                
                print (error)
                mydb.close()
        return row_id


class DBOferta:
    def __init__(self):
        pass

    def insert_oferta(self, connection, oferta):        
        try:
            mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "insert into Oferta (id_webscraping, titulo,empresa,lugar,salario,oferta_detalle,url_oferta,url_pagina,fecha_creacion,fecha_modificacion) values (%s,%s,%s,%s,%s,%s,%s,%s,current_date,current_date)"            
            params = (oferta["id_carga"], oferta["puesto"].strip(), oferta["empresa"].strip(), oferta["lugar"].strip(),oferta["salario"].strip(),oferta["detalle"].strip(), oferta["url"], oferta["url_pagina"])
            cur.execute(sql, params)        
            mydb.commit()  

            sql = "SELECT last_value FROM Oferta_id_oferta_seq"
            cur.execute(sql)  
            row_id = int(cur.fetchone()[0])

            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
                print ("-------------Exception, psycopg2.DatabaseError-------------------")
                print (error)
                mydb.close()        
     
            
        return row_id


class DBOfertadetalle:
    def __init__(self):
        pass

    def insert_ofertadetalle(self, connection, oferta_detalle):        
        try:
            mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "INSERT INTO OFERTA_DETALLE (id_oferta,descripcion,fecha_creacion,fecha_modificacion) VALUES (%s,%s,current_date,current_date)"            
            params = (oferta_detalle["id_oferta"],oferta_detalle["descripcion_tupla"])
            cur.execute(sql, params)        
            mydb.commit()  

            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
                print ("-------------Exception, psycopg2.DatabaseError-------------------")
                print (error)
                mydb.close()        

            
        return 1
  
