
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
    #for i in range(pagina_inicial, cant_paginas):
    for i in range(pagina_inicial, cant_paginas):
        print('xd')
        print(prefix_url)
        print('xd página')
        #hiro
        url_pagina = prefix_url.replace('^',str(i))
        print(url_pagina)
        print('xd')

        #print("------------------for i in range(pagina_inicial, cant_paginas)-------------------")
        #print(i) 

        req = requests.get(url_pagina)
        soup = BeautifulSoup(req.text, "lxml")


        #avisos = soup.find_all("div", {"class": "aviso-simple"})
        avisos=soup.find("div", {"id":"content"}).find("div", {"class": "col_rt"}).findAll("div", {"class": "item_list"})                    
        #print("----------------------")
        #print("----------------------")
        #print(avisos[0])
        #print("----------------------")
        #print("----------------------")
        #print("----------------------")
        #cont = 0       
        lista_oferta = []
        for er in avisos:
            #print("-------avisos--------")
            #print(len(avisos))
            el = er.find("div", {"class": "infoAd"})
            #print(el)  -> Esto es para verificar 
            oferta = {}    
            #cont = cont + 1
            #if cant_ofertas is not None:
            #    if cont > cant_ofertas:
            #        break
            # Obtiene el link para poder ver el detalle de la oferta
            href = el.find("a")['href']

            oferta["id_carga"] = id_carga
            # Almacena la url de la pagina
            oferta["url_pagina"] = url_pagina
            # Almacena la url de la oferta
            oferta["url"] = href

            oferta["puesto"]  =el.find("span", {"class": "titleAd"}).get_text()
            
            empresa= el.find("span", {"class": "dateAd"})  
            if empresa!=None:                            
                oferta["empresa"]=empresa.get_text()
            else:
                oferta["empresa"]=''
            
            lugar   = el.find("span", {"class": "zoneAd"})
            if lugar!=None:                                            
                oferta["lugar"]=lugar.get_text()
            else:
                oferta["lugar"]=''                

            salario = el.find("span", {"class": "salaryText"})            
            if salario!=None:                                            
                oferta["salario"]=salario.get_text()
            else:
                oferta["salario"]='' 

            # Accede al contenido HTML del detalle de la oferta
            reqDeta = requests.get(oferta["url"])            
            soup_deta = BeautifulSoup(reqDeta.text, "lxml")


            #con esto hago un find de los div 

            #aviso_deta = soup_deta.find("div", {"id": "vjs-desc"})
            #aviso_deta = soup_deta.find("div", {"id": "description_item"})

            aviso_deta = soup_deta.find("div", {"class": "description_item"})
            if aviso_deta!=None:                                            
                oferta["detalle"]=aviso_deta.get_text()




            #Nueva implementacion de la profe clase del 2 de enero
            #aviso_deta_div=soup_deta.find("div",{"id":"description_item"}).find_all("div") 
            #for el_div in aviso_deta_div:
            #    print(el_div)






                      


#Esto lo voy acomentar para no hacer ingresos a la bd 
#Modificar ojo hiro 8/01/2021
            
            #esto lo puedo añadir a la oferta y asu vez esto va a la lista oferta y ya con eso se puede trabajar-







            #--> descomentar esta linea para que se realice la insercion
            oferta["id_oferta"]=controller.registrar_oferta(con, oferta)







            lista_oferta.append(oferta)  



                  
    return lista_oferta

#Existe una lógica oferta detalles que nos puede ayudar a evaluar el contenido



def scraping_ofertadetalle(con,oferta_detalle):
    controller = Controller()
    lista_ofertadettalle = []  
    oferta = {}
    i=0
    for i in range(len(oferta_detalle)):
        oferta_detalle[i]["url"]
        oferta_detalle_re = requests.get(oferta_detalle[i]["url"])
        bea = BeautifulSoup(oferta_detalle_re.text, "lxml")


        parrafo=bea.find('div',attrs={'class':'description_item'}).find_all('p')

        texto_pre=parrafo[0].text

        #print('----------------')
        #print('----------------')
        #print('----------------')
        #print('id_oferta')
        #print(oferta_detalle[i]["id_oferta"])
        oferta["id_oferta"]=oferta_detalle[i]["id_oferta"]
        #print('---')
        #print(oferta_detalle[i]["url"])
        lista_a_llenar=texto_pre.split(sep='-')
        for i in range(len(lista_a_llenar)):
            oferta["descripcion_tupla"]=lista_a_llenar[i].strip()
            controller.registrar_oferta_detalle(con,oferta)
            #descripcion_tupla
            #print(lista_a_llenar[i].strip())
        #print('----------------')
        #print('----------------')
        #print('----------------')

        #controller.registrar_oferta_detalle(con,oferta)






   
    #title=bsObj.find_all("div", {"class": "summary"})


    # Accede al contenido HTML del detalle de la oferta
    #reqDeta = requests.get(oferta["url"])
    #print(oferta["url"])
    #soup_deta = BeautifulSoup(reqDeta.text, "lxml")
    # Obtiene el nombre del puesto de trabajo
    #oferta["puesto"] = soup_deta.find("div", {"id": "vjs-jobtitle"})
    # Obtiene el nombre de la empresa
    #oferta["empresa"] = soup_deta.find("span", {"id": "vjs-cn"})
    #oferta["lugar"] = soup_deta.find("span", {"id": "vjs-loc"})
    #oferta["salario"] = soup_deta.find("div", {})
    # Obtiene los div z-group en el cual esta contenido los datos resumen de la oferta, tales como:
    # Lugar, Tiempo de Publicacion, Salario, Tipo de Puesto, Area
    #aviso_deta = soup_deta.find("div", {"id": "vjs-desc"})
    #aviso_deta1= aviso_deta
    #for ed in aviso_deta:
        # Obtiene el titulo del dato resumen
        #cabecera_deta = ed.find("div", {"class": "spec_attr"})
        # Obtiene el contenido del dato resumen
        #children_descripcion_deta = ed.find("div", {"class": "spec_def"}).findChildren()
        #descripcion_deta = children_descripcion_deta[len(children_descripcion_deta) - 1].text.strip()
        #if cabecera_deta.find("h2", {"class": "lugar"}) is not None:
        #    oferta["lugar"] = descripcion_deta
        #elif cabecera_deta.find("h2", {"class": "fecha"}) is not None:
        #    oferta["tiempoPublicado"] = descripcion_deta
        #elif cabecera_deta.find("h2", {"class": "salario"}) is not None:
        #    oferta["salario"] = descripcion_deta
        #elif cabecera_deta.find("h2", {"class": "tipo_puesto"}) is not None:
        #    oferta["tipoPuesto"] = descripcion_deta
        #elif cabecera_deta.find("h2", {"class": "area"}) is not None:
        #    oferta["area"] = descripcion_deta
    #oferta["prop_area"] = soup_deta.find('input', {'id': 'area'}).get("value")
    #oferta["prop_subarea"] = soup_deta.find('input', {'id': 'subarea'}).get("value")
    # Obtiene la descripcion de la Oferta(Requisitos)
    # Almacena lo contenido en etiquetas <p> y <li>
    # Extrae informacion de etiquetas <p>
    #aviso_descripcion = soup_deta.find("div", {"class": "aviso_description"})
    #descripcion_deta_p = aviso_descripcion.find_all("p")
    #lista_detalle = []
    #for ed in descripcion_deta_p:
    #    content = ed.contents
    #    if content is not None and contain_br(content):
    #        lista_detalle.extend(get_content(content))
    #    else:
    #        if ed.text is not None and ed.text.strip() != "":
    #            lista_detalle.append(ed.text)

    # Extrae informacion de etiquetas <li>
    #descripcion_deta_ul = aviso_descripcion.find_all("ul")
    #for ed in descripcion_deta_ul:
    #    descripcion_deta_ul_li = ed.find_all("li")
    #    for edc in descripcion_deta_ul_li:
    #        children = edc.findChildren()
    #        descripcion = {}
    #        if len(children) > 0:
    #            text = children[len(children) - 1].text.strip()
    #            descripcion["descripcion"] = text
    #            if text is not None and text.strip() != "":
    #                lista_detalle.append(text)
    #       else:
    #            text = edc.text
    #            descripcion["descripcion"] = text
    #            if text is not None and text.strip() != "":
    #                lista_detalle.append(text)
    #lista_detalle.append(aviso_deta.get_text())                    
    #lista_detalle=aviso_deta.get_text()
    #oferta["listaDescripcion"] = replace_quote(lista_detalle)
    #oferta["listaDescripcion"] = aviso_deta1
    #oferta["id_carga"] = id_carga

   #print(oferta)
    return oferta


def replace_quote(list):
    new_list = []
    for el in list:
        el = el.replace("'", "''")
        new_list.append(el)
    return new_list
