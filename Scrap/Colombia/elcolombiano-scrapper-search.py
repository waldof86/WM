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


url='https://www.elcolombiano.com/busqueda/-/search/pandemia/false/false/19791109/20211109/date/true/true/0/0/meta/0/0/0/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

current_page=1772
page= requests.get(url+ str(current_page),headers=headers)               
coverpage= page.content
    # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('li', class_='element')


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

has_next= current_page

while (has_next != ''):
    print('pagina: '+str(current_page))
    for n in np.arange(0, number_of_articles):
    
         
            try:
                link = coverpage_news[n].find('div', class_='noticia-resultado').find('div',class_='right').find('a')['href']
            except:
                 try:
                     link = coverpage_news[n].find('div', class_='noticia-resultado').find('div',class_='rightNoFoto').find('a')['href']
                 except:
                     link=''
                
            list_links.append('https://www.elcolombiano.com' +link) 
            print('https://www.elcolombiano.com' +link)
            
            try:
                seccion = coverpage_news[n].find('div', class_='information').find('a').get_text() 
                list_secciones.append(seccion)
            except:
                try:
                    seccion = coverpage_news[n].find('div', class_='information').get_text().split('|')[1].replace(' ','')
                    list_secciones.append(seccion)
                except:
                    list_secciones.append('')
            try:
                fecha = coverpage_news[n].find('div', class_='fecha').find('span').getText().replace(' ','')
                list_fecha.append(fecha)
            except:
                fecha=''
                list_fecha.append('')
       
            
       
            try:
                title = coverpage_news[n].find('h3', class_='titulo-noticia').find('span').get_text()
                list_titles.append(title)
            except:
                list_titles.append('')
                title=''
                # Obtener el bajada
  
            
            try:
                body = coverpage_news[n].find('div', class_='noticia-resultado')
                x = body.findAll('p')
                bajada =''
                # Unifying the paragraphs
                list_paragraphs = []
                for p in np.arange(0, len(x)):
                    paragraph = x[p].get_text()
                    list_paragraphs.append(paragraph)
                    bajada = " ".join(list_paragraphs)
                list_bajadas.append(bajada)
            except:
                list_bajadas.append('')
                             
            try:
                autor = coverpage_news[n].find('span', class_='autor').get_text()
                list_autores.append(autor)
            except:
                list_autores.append('')

        
            try:
                #article = 
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                article = requests.get('https://www.elcolombiano.com' +link,headers=headers)
                #time.sleep(2)
                article_content = article.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
            
                
                try:
                    body = soup_article.find('div', class_='paragraph')
                    x = body.findAll('p')
                    # Unifying the paragraphs
                    list_paragraphs = []
                    for p in np.arange(0, len(x)):
                        paragraph = x[p].get_text()
                        list_paragraphs.append(paragraph)
                        final_article = " ".join(list_paragraphs)
                except:
                    body = soup_article.find('div', class_='text')
                    x = body.findAll('p')
                    # Unifying the paragraphs
                    list_paragraphs = []
                    for p in np.arange(0, len(x)):
                        paragraph = x[p].get_text()
                        list_paragraphs.append(paragraph)
                        final_article = " ".join(list_paragraphs)
                
               
    
                news_contents.append(final_article)
                
            except:
                print('There is a problem.')
                news_contents.append('')
                
    if(current_page == int(soup1.find('div', class_='carrusel').findAll('li')[-1].get_text())):
        has_next = ''
    else:
        has_next=current_page
  
    if (has_next != ''):
            current_page = current_page + 1
            url2 =url+ str(current_page)
            page= requests.get(url2,headers=headers)               
            coverpage= page.content
            soup1 = BeautifulSoup(coverpage, 'html5lib')
            coverpage_news = soup1.find_all('li', class_='element')
            number_of_articles =  len(coverpage_news)

    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'El Colombiano', 
         'País': 'Colombia',
         'Seccion': list_secciones,
         'fecha': list_fecha,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Autor': list_autores,
         'Contenido': news_contents
         })




workbook = xlsxwriter.Workbook('elcolombiano-results.xlsx')
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
