# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 02:28:36 2021

@author: Marcos Buccellato
"""
import requests
from bs4 import BeautifulSoup
import numpy as np

def clarin_accepted(url):
    ex_l = ['tema']
    url_parts= url.split('/')
    if (url_parts[3] in  ex_l):
        return False
    return True

    
def clarin_parser(url):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # Empty lists for content, links and titles
    contenido = ''
    titulo = ''
    bajada = ''
    fecha = ''
    seccion = ''
    autor = ''
    print('Intentando: '+ url)
    soup_article =''
    if (clarin_accepted(url)):
        try:
            article = requests.get(url,headers)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')
        except:
             print('Problema accediendo al link')
    
        try:
            titulo = soup_article.find('h1',  {"id": "title"}).get_text()
        except:
             print('Problema con el título')
        try:
            body = soup_article.find_all('div', class_='body-nota')
            x = body[0].find_all('p')
            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                contenido= " ".join(list_paragraphs)
        except:
            print('Problema con el contenido')
        try:
            seccion = soup_article.find('div',class_='breadcrumb').findAll('li', itemprop='itemListElement')[1].find('a').find('span').get_text()
        except:
             print('Problema con la sección')
        try:
            autor = soup_article.find('p', itemprop='author').get_text()
        except:
             print('Problema con el autor')
        try:
            bajada = soup_article.find('div',class_='bajada').find('h2').get_text()
        except:
             print('Problema con la bajada')
        try:
            fecha = soup_article.find('div',class_='breadcrumb').find('span', class_='publishedDate').get_text().replace('\n','').split(' ')[0]
        except:
             print('Problema con la fecha')
    else:
       return ''

    row = {'Diario': 'Clarín', 
         'País': 'Argentina',
         'Seccion': seccion,
         'fecha': fecha,
         'Título Artículo': titulo,
         'Link a Artículo': url,
         'Bajada Artículo': bajada,
         'Autor': autor,
         'Contenido': contenido
         }
    return row