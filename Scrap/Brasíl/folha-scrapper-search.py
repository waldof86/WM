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

url='https://search.folha.uol.com.br/search?q=pandemia&site=todos&periodo=todos&sd=01%2F01%2F2020&ed=26%xm2F03%2F2020&periodo=personalizado&sr='
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
current = 1
page= requests.get(url+str(current),headers=headers)               
coverpage= page.content
    # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('li', class_='c-headline c-headline--newslist')

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

has_next = True


while (has_next):
    for n in np.arange(0, number_of_articles):
    
            #Obtener la volanta
            list_volanta.append('')
            # Obtener el link al artículo
            
            link = coverpage_news[n].find('div', class_='c-headline__content').find('a')['href']
            pattern =r'(https)(.*)&'
            list_links.append(link) 
            
            # Ir al artículo (it is divided in paragraphs)
            print(link)
        
            try:
                #article = 
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                article = requests.get(link,headers=headers)
                #time.sleep(2)
                article_content = article.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
                
                try:
                    seccion = soup_article.find('li', class_='c-site-nav__item--section').find('a').get_text(). rstrip("\n")
                   
                except:
                    try:
                        seccion =link.split('/')[3]
                   
                    except:
                        seccion = ''
                # Obtener el título
                try:
                    title = soup_article.find('h1', class_='c-content-head__title').get_text().replace('\n','').strip()
                except:
                    try:
                         title = soup_article.find('h1', class_='news__title').get_text().replace('\n','').strip()
                    except:
                        try:
                            title = soup_article.find('h1', class_='main_color main_title').get_text().replace('\n','').strip()
                        except:
                            title=''

                    # Obtener el bajada
                try:
                    bajada = soup_article.find('h2', class_='c-content-head__subtitle').get_text().replace('\n','').strip()
                except:
                    try:
                         bajada= soup_article.find('p', class_='news__subtitle').get_text().replace('\n','').strip()
                    except:
                        bajada=''
               
                try:
                    autor = soup_article.find('strong', class_='c-signature__author').get_text().replace('\n','').strip()
                    
                except:
                    try:
                        autor = soup_article.find('div', class_='byline').get_text().replace('\n','').strip()
                    
                    except:
                        autor=''
                
                
                try:
                    fecha = soup_article.find('time', class_='c-more-options__published-date')['datetime'][0:10] 
                except:
                    try:
                        fecha = soup_article.find('time', class_='c-more-options__published-date').get_text()[0:10] 
                    except:
                        try:
                             fecha = soup_article.find('time')['datetime'][0:10] 
                        except:
                            fecha=''

                try:
                    body = soup_article.find('div', class_='c-news__body')
                    x = body.findAll('p')
                
                    # Unifying the paragraphs
                    list_paragraphs = []
                    for p in np.arange(0, len(x)):
                        paragraph = x[p].get_text()
                        list_paragraphs.append(paragraph)
                        final_article = " ".join(list_paragraphs)
                except:
                    try:
                        body = soup_article.find('div', class_='j-paywall news__content js-news-content js-disable-copy js-tweet-selection')
                        x = body.findAll('p')
                    
                        # Unifying the paragraphs
                        list_paragraphs = []
                        for p in np.arange(0, len(x)):
                            paragraph = x[p].get_text()
                            list_paragraphs.append(paragraph)
                            final_article = " ".join(list_paragraphs)
                    except:
                        try:
                            body = soup_article.find('div', class_='column main_content')
                            x = body.findAll('p')
                        
                            # Unifying the paragraphs
                            list_paragraphs = []
                            for p in np.arange(0, len(x)):
                                paragraph = x[p].get_text()
                                list_paragraphs.append(paragraph)
                                final_article = " ".join(list_paragraphs)
                        except:
                             final_article =''
                    
                    
                    
                    
                    
                news_contents.append(final_article.replace('\n',''))
                
                
                
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

    has_next = (current + 25) < 10000
    if (has_next):
            current = current + 25
            print("página:" + str(current))
            url2 =url + str(current)
            page= requests.get(url2,headers=headers)               
            coverpage= page.content
            soup1 = BeautifulSoup(coverpage, 'html5lib')
            coverpage_news = soup1.find_all('li', class_='c-headline c-headline--newslist')
            number_of_articles =  len(coverpage_news)

    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'Folha de S. Paulo', 
         'País': 'Brasil',
         'Seccion': list_secciones,
         'fecha': list_fecha,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Autor': list_autores,
         'Contenido': news_contents
         })




workbook = xlsxwriter.Workbook('folha-results.xlsx')
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
