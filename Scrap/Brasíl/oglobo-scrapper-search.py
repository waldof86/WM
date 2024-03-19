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
import re

url='https://oglobo.globo.com/busca/?q=covid+"sociologa"&page='
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page= requests.get(url+'1',headers=headers)               
coverpage= page.content
    # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('li', class_='species-materia')


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
try:
    has_next = soup1.find('a', class_='proximo fundo-cor-produto')['href']
except:
    has_next = ''


current = 1
while (has_next != ''):
    for n in np.arange(0, number_of_articles):
    
            #Obtener la volanta
            list_volanta.append('')
            # Obtener el link al artículo
            
            link = coverpage_news[n].find('a', class_='cor-produto')['href']
            pattern =r'(https)(.*)&'
            link = re.search(pattern,link).group(2)
            link = link.replace('%3A','').replace('%2F', '/').split('&')[0]
            list_links.append('https:' +link) 
            
    
    
            # Ir al artículo (it is divided in paragraphs)
            print('https:' +link)
        
            try:
                #article = 
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                article = requests.get('https:' +link,headers=headers)
                #time.sleep(2)
                article_content = article.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
                
                try:
                    seccion = soup_article.find('div', class_='site-header__section-name').find('a').get_text() 
                   
                except:
                    seccion = ''
                # Obtener el título
                try:
                    title = soup_article.find('h1', class_='article__title').get_text().replace('\n','')
                except:
                    title=''

                    # Obtener el bajada
                try:
                    bajada = soup_article.find('div', class_='article__subtitle').get_text().replace('\n','')
                    
                except:
                    bajada=''
               
                try:
                    autor = soup_article.find('div', class_='article__author').get_text()
                    
                except:
                    autor=''
                
                try:
                    fecha = soup_article.find('div', class_='article__date').getText().replace('\n','').split(' - ')[0]   
                except:
                    fecha=''

        
                body = soup_article.find('main', class_='main-content')
                x = body.findAll('p')
                
                # Unifying the paragraphs
                list_paragraphs = []
                for p in np.arange(0, len(x)):
                    paragraph = x[p].get_text()
                    list_paragraphs.append(paragraph)
                    final_article = " ".join(list_paragraphs)
    
                news_contents.append(final_article)
                list_titles.append(title)
                list_fecha.append(fecha)
                list_autores.append(autor)
                list_bajadas.append(bajada)
                list_secciones.append(seccion)
            except:
                print('There is a problem.')
                list_secciones.append('')
                list_titles.append('')
                news_contents.append('')
                list_fecha.append('')
                list_autores.append('')
                list_bajadas.append('')
    try:
        has_next = soup1.find('a', class_='proximo fundo-cor-produto')['href']
    except:
        has_next = ''      
    
    if (has_next != ''):
            current = current + 1
            print("página:" + str(current))
            url2 ='https://oglobo.globo.com/busca/' + has_next
            page= requests.get(url2,headers=headers)               
            coverpage= page.content
            soup1 = BeautifulSoup(coverpage, 'html5lib')
            coverpage_news = soup1.find_all('li', class_='species-materia')
            number_of_articles =  len(coverpage_news)

    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'O Globo', 
         'País': 'Brasil',
         'Seccion': list_secciones,
         'fecha': list_fecha,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Autor': list_autores,
         'Contenido': news_contents
         })




workbook = xlsxwriter.Workbook('oglobo-results.xlsx')
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
