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


url='https://www.eltiempo.com/buscar/1?q=pandemia&publishedAt%5Bfrom%5D=20-01-01&publishedAt%5Buntil%5D=20-08-01&contentTypes%5B0%5D=article '
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
headers1 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
   
page= requests.get(url,headers=headers)               
coverpage= page.content
    # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('div', class_='listing')


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
    has_next = soup1.find('li', class_='next').find('a')['href']
except:
    has_next = ''



hd= 1
while (has_next != ''):
    for n in np.arange(0, number_of_articles):
         
            if(hd>0):
                head = headers
            else:
                head= headers1
            hd = hd *(-1)
            #Obtener la volanta
            list_volanta.append('')
            # Obtener el link al artículo
            
            link = coverpage_news[n].find('h3', class_='title-container').find('a')['href']

            list_links.append('https://www.eltiempo.com/' +link) 
            
            try:
                seccion = coverpage_news[n].find('div', class_='category').get_text() 
                list_secciones.append(seccion)
            except:
                list_secciones.append('')
            try:
                fecha = coverpage_news[n].find('div', class_='published-at').getText().replace('\n','')   
                list_fecha.append(fecha)
            except:
                fecha=''
                list_fecha.append('')
       
            
       
            try:
                title = coverpage_news[n].find('h3', class_='title-container').find('a').get_text().replace('\n','')
                list_titles.append(title)
            except:
                list_titles.append('')
                title=''
                # Obtener el bajada
            try:
                bajada =  coverpage_news[n].find('div', class_='epigraph-container').find('a').get_text().replace('\n','')
                list_bajadas.append(bajada)
            except:
                list_bajadas.append('')
                             

            # Ir al artículo (it is divided in paragraphs)
            print('https://www.eltiempo.com/' +link)
        
            try:
                #article = 
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                article = requests.get('https://www.eltiempo.com/' +link,headers=head)
                #time.sleep(2)
                article_content = article.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
             
                try:
                    autor = soup_article.find('div', class_='author_data').find('span').find('span').get_text().split('-')[0]
                    list_autores.append(autor)
                except:
                    list_autores.append('')
                

        
                body = soup_article.find('div', class_='articulo-contenido')
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
                

    try:
        has_next= soup1.find('li', class_='next').find('a')['href']
    except:
        has_next = ''      

    if (has_next != ''):
            url2 ='https://www.eltiempo.com/' + has_next
            page= requests.get(url2,headers=headers)               
            coverpage= page.content
            soup1 = BeautifulSoup(coverpage, 'html5lib')
            coverpage_news = soup1.find_all('div', class_='listing')
            number_of_articles =  len(coverpage_news)
            print('Página:' + has_next.split('/')[2].split('?')[0])

    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'El Tiempo', 
         'País': 'Colombia',
         'Seccion': list_secciones,
         'fecha': list_fecha,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Autor': list_autores,
         'Contenido': news_contents
         })




workbook = xlsxwriter.Workbook('eltiempo-results.xlsx')
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
