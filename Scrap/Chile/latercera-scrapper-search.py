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
import re

headless = False
url = 'https://www.latercera.com/etiqueta/coronavirus/page/'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page= requests.get(url+'1/',headers=headers)               
coverpage= page.content
    # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('div', class_='art-container')


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

paginas = soup1.find('li', class_='pagination-info').get_text()
pattern = r".{5}([0-9]{1,3}).{4}([0-9]{1,3})"

p_actual =1
p_final=int(re.search(pattern,paginas).group(2))
#p_final= 2

while (p_actual <= p_final):
    for n in np.arange(0, number_of_articles):
        
                #Obtener la volanta
                list_volanta.append('')
                # Obtener el link al artículo
                try:
                    link = coverpage_news[n].find('div', class_='headline').find('h3').find('a')['href']
                    list_links.append('https://www.latercera.com/'+link) 
                except:
                    try:
                        link = coverpage_news[n].find('div', class_='headline').find('h5').find('a')['href']
                        list_links.append('https://www.latercera.com/'+link) 
                    except:
                        list_links.append('')
               # Ir al artículo (it is divided in paragraphs)
                print('https://www.latercera.com/'+link)
        
                #article
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                article = requests.get('https://www.latercera.com/'+link,headers=headers)
                article_content = article.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
                
                try:
                    seccion = soup_article.find('ul', class_='list-cat-y-tags').find('li').find('a').find('div').get_text()              
                    list_secciones.append(seccion)
                except:
                    list_secciones.append('')
             
                try:
                    title = soup_article.find('div', class_='hl').find('h1').find('div').get_text()
                    list_titles.append(title)
                except:
                      list_titles.append('')
                    
                try:
                    bajada = soup_article.find('h2', class_='story-header__news-summary').get_text()
                    list_bajadas.append(bajada)
                except:
                    list_bajadas.append('')
               
                try:
                    autor = soup_article.find('div', class_='name').get_text()
                    list_autores.append(autor)
                except:
                    list_autores.append('')
                
                try:
                    fecha = soup_article.find('time')['datetime']   
                    list_fecha.append(fecha)
                except:
                    fecha=''

                try:
                    body = soup_article.find('div',class_='single-content')
                    x = body.findAll('p')
                
                    # Unifying the paragraphs
                    list_paragraphs = []
            
                    #Este diario tiene un parrafo introductorio separado
            
                    for p in np.arange(0, len(x)):
                        paragraph = x[p].get_text()
                        list_paragraphs.append(paragraph)
                        final_article = " ".join(list_paragraphs)
    
                    news_contents.append(final_article)
                except:
                    news_contents.append('')
            
                
               
    
        
    p_actual= p_actual + 1   
    if (p_actual <= p_final):
            url2 =url+str(p_actual)+'/'
            page= requests.get(url2,headers=headers)               
            coverpage= page.content
            soup1 = BeautifulSoup(coverpage, 'html5lib')
            coverpage_news = soup1.find_all('div', class_='art-container')
            number_of_articles =  len(coverpage_news)

    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'La Tercera', 
         'País': 'Chile',
         'Seccion': list_secciones,
         'fecha': list_fecha,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Autor': list_autores,
         'Contenido': news_contents
         })

workbook = xlsxwriter.Workbook('Chile-LaTercera-results.xlsx')
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
