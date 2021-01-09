# -*- coding: utf-8 -*-
import psycopg2
from configuration import *
import webscraping
from controller import Controller
from dbconnection import Connection


def construir_busqueda_filtro(carga, filtro):
    carga["busqueda"] = filtro
    busqueda = ""
    if carga["busqueda"] is not None:
        busqueda = "-busqueda-" + carga["busqueda"].replace(" ", "-")

    busqueda_area = ""
    if carga["busqueda_area"] not in ("", None):
        busqueda_area = "-area-" + carga["busqueda_area"].replace(" ", "-")

    total = ""
    if busqueda == "" and busqueda_area == "":
        total = ""
    carga["url_principal"] = WS_PORTAL_LABORAL_URL
    urlbusqueda = "/ofertas-de-trabajo/empleos-lima/?q=analista%20programador"
    paginado = "&start="

    extension = ""
    ordenado = ""
    carga["url_prefix"] = carga["url_principal"] + urlbusqueda + paginado
    carga["url_sufix"] = extension + ordenado

    carga["url_pagina"] = carga["url_principal"]
    carga["url_busqueda"] = urlbusqueda

def set_url_busqueda(carga):

    carga["url_principal"] = WS_PORTAL_LABORAL_URL
    urlbusqueda = "/ofertas-de-trabajo/empleos-lima/?q=analista%20programador"
    #hiro cambio en paginado
    #https://www.mipleo.com.pe/ofertas-de-trabajo/empleos-lima/?q=analista%20programador&page=3&pag=3
    paginado = "&page=^&pag=^"

    carga["url_prefix"] = carga["url_principal"] + urlbusqueda + paginado
    carga["url_sufix"] = ""

    carga["url_busqueda"] = carga["url_principal"] + urlbusqueda    

def connect_bd():
    con = Connection(DB_HOST, DB_SERVICE, DB_USER, DB_PASSWORD)
    con.connect()
    return con

#def delati_indeed()


if __name__ == "__main__":
    controller = Controller()
    con = connect_bd()

    carga = {}
    carga["pagina"] = WS_PORTAL_LABORAL
    carga["cant_paginas"] = WS_PAGINAS
    carga["pagina_inicial"] = WS_PAGINA_INICIAL
    carga["cant_ofertas"] = WS_OFERTAS
    carga["busqueda_area"] = WS_AREA
    carga["busqueda"] = ""

    set_url_busqueda(carga)


    #id_carga es el id_webscraping
    carga["id_carga"] = controller.registrar_webscraping(con, carga)


    #print("----control de datos-----")
    #print(carga)
    #print(carga["url_principal"])
    #print(carga["url_prefix"])
    #print(carga["url_sufix"])
    #print(carga["pagina_inicial"])
    #print(carga["cant_paginas"])
    #print(carga["cant_ofertas"])
    #print(carga["id_carga"])







    listaOferta = webscraping.scraping_ofertas(con, carga["url_principal"], carga["url_prefix"], carga["url_sufix"],
                                               carga["pagina_inicial"], carga["cant_paginas"], carga["cant_ofertas"],
                                               carga["id_carga"])


    print('hiro')
    #for i in range(len(listaOferta)):
        #print(listaOferta[i])
    print(listaOferta[0]["url"])
        #print(listaOferta[i]["url"])
        #print("/n")
    print("/n")
    #print('hiro')

    


    webscraping.scraping_ofertadetalle(con,listaOferta)


    #print(listaOferta)