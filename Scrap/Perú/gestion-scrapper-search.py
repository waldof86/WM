# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 14:29:33 2021

@author: Marcos Buccellato
"""

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import xlsxwriter
#import time

headless = False
url = 'https://gestion.pe/buscar/pandemia/todas/descendiente/'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page= requests.get(url+'1/',headers=headers)               
coverpage= page.content
    # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('div', class_='story-item')


number_of_articles =  len(coverpage_news)

    # Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []
list_volanta = []
list_bajadas = []
list_fecha = []
list_secciones = []
list_autores = []

paginas = soup1.findAll('a', class_='pagination__page')


p_actual =1
p_final=int(paginas[len(paginas)-2].get_text())
#p_final= 2

while (p_actual <= p_final):
    
    print("página " + str(p_actual)) 
   
    for n in np.arange(0, number_of_articles):
    
            #Obtener la volanta
            list_volanta.append('')
            # Obtener el link al artículo
            
            link = coverpage_news[n].find('a', class_='story-item__title')['href']
            list_links.append('https://gestion.pe/'+link) 
            
    
    
            # Ir al artículo (it is divided in paragraphs)
            print('https://gestion.pe/'+link)
        
            try:
                #article
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                article = requests.get('https://gestion.pe/'+link,headers=headers)
                #time.sleep(2)
                article_content = article.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
                try:
                    seccion = soup_article.find('div', class_='story-header__share').find('div').get_text() 
                    list_secciones.append(seccion)
                except:
                    list_secciones.append('')
                
                # Obtener el título
                try:
                    title = soup_article.find('h1', class_='sht__title').get_text()
                except:
                    try:
                         title = soup_article.find('h1', class_='story-header__news-title').get_text()
                    except:
                        title=''

                    # Obtener el bajada
                try:
                    bajada = soup_article.find('h2', class_='sht__summary').get_text()
                    list_bajadas.append(bajada)
                except:
                    try:
                        bajada = soup_article.find('h2', class_='story-header__news-summary').get_text()
                        list_bajadas.append(bajada)
                    except:
                        list_bajadas.append('')
               
                try:
                    autor = soup_article.find('a', class_='story-content__author-link').get_text()
                    list_autores.append(autor)
                except:
                    list_autores.append('')
                
                try:
                    fecha = soup_article.find('time')['datetime'].split('T')[0]   
                except:
                    fecha=''

        
                body = soup_article.find('section')
                x = body.findAll('p')
                
                # Unifying the paragraphs
                list_paragraphs = []
            
                #Este diario tiene un parrafo introductorio separado
            
                for p in np.arange(0, len(x)):
                    paragraph = x[p].get_text()
                    list_paragraphs.append(paragraph)
                    final_article = " ".join(list_paragraphs)
    
                news_contents.append(final_article)
                list_titles.append(title)
                list_fecha.append(fecha)
            except:
                print('There is a problem.')
                list_titles.append('')
                news_contents.append('')
                list_fecha.append('')
               
    
    
    p_actual= p_actual + 1   
    if (p_actual <= p_final):
            url2 =url+str(p_actual)+'/'
            page= requests.get(url2,headers=headers)               
            coverpage= page.content
            soup1 = BeautifulSoup(coverpage, 'html5lib')
            coverpage_news = soup1.find_all('div', class_='story-item')
            number_of_articles =  len(coverpage_news)

    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'Gestión', 
         'País': 'Perú',
         'Seccion': list_secciones,
         'fecha': list_fecha,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Autor': list_autores,
         'Contenido': news_contents
         })

workbook = xlsxwriter.Workbook('gestion-results.xlsx')
worksheet = workbook.add_worksheet()

# Headers
headers = ['diario', 'País','Sección','Fecha', 'Título','Link','Bajada','Autor','artículo']
for h in range(len(headers)):
    worksheet.write(0, h, headers[h])

# Content
for i in range(len(df_show_info)):

    for j in range(df_show_info.iloc[i].size):
        
        worksheet.write(i + 1, j, df_show_info.iloc[i][j])

workbook.close()
