
from urllib.request import urlopen
from urllib.error import HTTPError
import bs4
from bs4 import BeautifulSoup
import requests
from controller import Controller


def contain_br(contents):
    for element in contents:
        if type(element) is bs4.element.Tag:
            if element.name == "br":
                return True
    return False


def get_content(contents):
    lista = []
    for element in contents:
        if type(element) is bs4.element.NavigableString:
            if str(element) is not None and str(element).strip() != "":
                lista.append(str(element))
    return lista


def scraping_ofertas(con, url_principal, prefix_url, sufix_url, pagina_inicial, cant_paginas, cant_ofertas, id_carga):
    controller = Controller()
    lista_oferta = []       
    i=1
    
    for i in range(pagina_inicial, cant_paginas):
        #print('xd')
        #print(prefix_url)
        #print('xd página')
        
        url_pagina = prefix_url.replace('^',str(i))
        #print(url_pagina)
        #print('xd')

         

        req = requests.get(url_pagina)
        soup = BeautifulSoup(req.content.decode('utf-8','ignore'), "lxml")


        
        avisos=soup.find("div", {"id":"content"}).find("div", {"class": "col_rt"}).findAll("div", {"class": "item_list"})                    
              
        lista_oferta = []
        for er in avisos:
            
            el = er.find("div", {"class": "infoAd"})
             
            oferta = {}    
           
            href = el.find("a")['href']

            oferta["id_carga"] = id_carga
            
            oferta["url_pagina"] = url_pagina
            
            oferta["url"] = href

            oferta["puesto"]  =el.find("span", {"class": "titleAd"}).get_text()
            
            empresa= el.find("span", {"class": "dateAd"})  
            if empresa!=None:                            
                oferta["empresa"]=empresa.get_text()
            else:
                oferta["empresa"]=''

            zoneAd = el.find("span", {"class": "zoneAd"})
            
            arrZoneAd = []
            arrZoneAd = zoneAd.get_text().split('|')    
            
            lugar = arrZoneAd[0]
            if lugar!=None:                                            
                oferta["lugar"]=lugar
            else:
                oferta["lugar"]=''                

            salario = arrZoneAd[1].replace('Salario: ','')  
            #print(salario)    
            if salario!=None:                                            
                oferta["salario"]=salario
            else:
                oferta["salario"]='No informado' 

            
            reqDeta = requests.get(oferta["url"])            
            soup_deta = BeautifulSoup(reqDeta.content.decode('utf-8','ignore'), "lxml")


            

            aviso_deta = soup_deta.find("div", {"class": "description_item"})
            if aviso_deta!=None:                                            
                oferta["detalle"]=aviso_deta.get_text()

            oferta["id_oferta"]=controller.registrar_oferta(con, oferta)

            lista_oferta.append(oferta)  
                
    return lista_oferta





def scraping_ofertadetalle(con,oferta_detalle):
    controller = Controller()
    lista_ofertadettalle = []  
    oferta = {}
    i=0
    for i in range(len(oferta_detalle)):
        oferta_detalle[i]["url"]
        oferta_detalle_re = requests.get(oferta_detalle[i]["url"])
        bea = BeautifulSoup(oferta_detalle_re.content.decode('utf-8','ignore'), "lxml")


        parrafo=bea.find('div',attrs={'class':'description_item'}).find_all('p')

        texto_pre=parrafo[0].text

        oferta["id_oferta"]=oferta_detalle[i]["id_oferta"]

        lista_a_llenar=texto_pre.split(sep='-')
        for i in range(len(lista_a_llenar)):
            oferta["descripcion_tupla"]=lista_a_llenar[i].strip()
            controller.registrar_oferta_detalle(con,oferta)

    return oferta


def replace_quote(list):
    new_list = []
    for el in list:
        el = el.replace("'", "''")
        new_list.append(el)
    return new_list
