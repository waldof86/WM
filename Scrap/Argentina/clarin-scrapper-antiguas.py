# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 14:29:33 2021

@author: Marcos Buccellato
"""
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

#def get_news_clarin():

# url notar que aca lo que hay que hacer es determinar la url por la fecha
url = "https://www.clarin.com/ediciones-anteriores/20211105"

#Otra opción es buscar en https://www.clarin.com/tema/pandemia.html ahi lo 
#unico que hay que tener cuidado es en hacer scroll hasta el fondo

    # Request
r1 = requests.get(url)
r1.status_code

    # We'll save in coverpage the cover page content
coverpage = r1.content

    # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('article')


number_of_articles =  len(coverpage_news)

    # Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []
list_volanta = []
list_bajadas = []
list_secciones = []

for n in np.arange(0, number_of_articles):

        #Obtener la volanta
        seccion = coverpage_news[n].find('p', class_='section').getText()
        list_secciones.append(seccion)
        
        #Obtener la volanta
        volanta = coverpage_news[n].find('p', class_='volanta').getText()
        list_volanta.append(volanta)

        # Obtener el link al artículo
        link = coverpage_news[n].find('a')['href']
        list_links.append('https://www.clarin.com/' + link)

        # Obtener el título
        title = coverpage_news[n].find('h2').get_text()
        list_titles.append(title)

        # Ir al artículo (it is divided in paragraphs)
        article = requests.get('https://www.clarin.com/' + link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html5lib')

        # Obtener el título
        bajada = coverpage_news[n].find('h2').get_text()
        list_bajadas.append(bajada)

        body = soup_article.find_all('div', class_='body-nota')
        x = body[0].find_all('p')

        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)

        news_contents.append(final_article)


    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'Clarin', 
         'Seccion': list_secciones,
         'Volanta Artículo': list_volanta,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Contenido': news_contents
         })

    #return (df_features, df_show_info)

#get_news_clarin()