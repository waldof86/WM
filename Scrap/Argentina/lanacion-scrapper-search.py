# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 09:03:21 2021

@author: Marcos Buccellato
"""

import time
from selenium import webdriver
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import xlsxwriter
from webdriver_manager.chrome import ChromeDriverManager
import re

headless = True
url = "https://www.lanacion.com.ar/buscador/?query=pandemia"
#url = 'https://www.lanacion.com.ar/buscador/?query=coronavirus%20antropolog%C3%ADa'

# Creation of a new instance of Chrome
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
if headless:
    options.add_argument('--headless')
options.add_argument("--window-size=1920,1200")
browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

browser.get(url)

coverpage =  browser.page_source

    # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('div', class_='queryly_item_row')


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

has_next = 'Siguiente'
page =1
while (has_next == "Siguiente"):
    print('Página: ' +str(page))
    page = page + 1
    for n in np.arange(0, number_of_articles):
    
            #Obtener la volanta
            list_volanta.append('')
            # Obtener el link al artículo
            link = coverpage_news[n].find('a')['href']
            
            if((link.find("sociedad/coronavirus-en")> 0)):
               #print('Salteando: '+ link)
               continue
            
            list_links.append('https://www.lanacion.com/' + link) 
            
           # Ir al artículo (it is divided in paragraphs)
            print('https://www.lanacion.com' + link)
            try:
                article = requests.get('https://www.lanacion.com' + link)
                article_content = article.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
                # Obtener el título
                title = soup_article.find('h1', class_='com-title').get_text()
                
               
                #Obtener la fecha
                fecha = soup_article.find('time', class_='com-date')['datetime']
           
                body = soup_article.find_all('p', class_='com-paragraph')
                x = body
                
                # Unifying the paragraphs
                list_paragraphs = []
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
      
            try:
                # Obtener el bajada
                bajada = soup_article.find('h2',class_='com-subhead').get_text()
                list_bajadas.append(bajada)
            except:
                list_bajadas.append('')
                
                  
            try:
               sec_array = soup_article.find('nav', class_='com-breadcrumb').findAll('a') 
               seccion= sec_array[len(sec_array)-1].get_text() 
               list_secciones.append(seccion[1:])
            except:
                list_secciones.append('')
                
            try:  
                autor = soup_article.find('a', class_='com-link --autor').get_text()
                list_autores.append(autor)
            except:
                #jsjsj
                list_autores.append('')
                
    
    try:
        has_next = soup1.find('div', id='resultdata').find('a',class_='next_btn').get_text()
    except:
        has_next = ''
    if (has_next == 'Siguiente'):
            browser.find_element_by_class_name('next_btn').click()
            time.sleep(2)
            coverpage =  browser.page_source
            soup1 = BeautifulSoup(coverpage, 'html5lib')
            coverpage_news = soup1.find_all('div', class_='queryly_item_row')
            number_of_articles = len(coverpage_news)

    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'La Nación', 
         'País': 'Argentina',
         'Seccion': list_secciones,
         'fecha': list_fecha,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Autor': list_autores,
         'Contenido': news_contents
         })

browser.quit()
workbook = xlsxwriter.Workbook('lanacion-results.xlsx')
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

