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
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

url='https://www.milenio.com/buscador/page/'
query='?text=pandemia'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
current_page=1

headless = False
# Creation of a new instance of Chrome
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
if headless:
    options.add_argument('--headless')
options.add_argument("--window-size=1920,1200")

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
browser.set_page_load_timeout(10)
try:
    browser.get(url+ str(current_page)+query)
except TimeoutException:
    browser.execute_script("window.stop();")
coverpage =  browser.page_source


browser.find_element_by_link_text("SIGUIENTE").send_keys(Keys.RETURN)
time.sleep(15)
browser.find_element_by_link_text("SIGUIENTE").send_keys(Keys.RETURN)
time.sleep(15)
browser.find_element_by_link_text("SIGUIENTE").send_keys(Keys.RETURN)
time.sleep(15)
browser.find_element_by_link_text("SIGUIENTE").send_keys(Keys.RETURN)
#browser.close()
#page= requests.get(url+ str(current_page)+query,headers=headers)               
#coverpage= page.content
    # Soup creation

soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('div', class_='item-news-container')

print(coverpage_news)
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
    has_next = soup1.find('div',class_='number-pages-container').findAll('a', class_='link-pagination')[-1].get_text().replace('\n','').replace(' ','')
except:
    has_next = ''



while (has_next == 'SIGUIENTE'):
    print('pagina: '+str(current_page))
    for n in np.arange(0, number_of_articles):
    
             
            link = coverpage_news[n].find('div', class_='title').find('a')['href']
            
            list_links.append('https://www.milenio.com' +link) 
            print('https://www.milenio.com' +link)
            
            try:
                fecha = coverpage_news[n].find('div', class_='hour').find('span').get_text().split('/')[0]
                list_fecha.append(fecha)
            except:
                fecha=''
                list_fecha.append('')
       

            try:
                title = coverpage_news[n].find('div', class_='title').find('h2').get_text()
                list_titles.append(title)
            except:
                list_titles.append('')
    
               
          
        
            try:
                #article = 
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                article = requests.get('https://www.milenio.com/' +link,headers=headers)
                
                article_content = article.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
                try:
                    seccion = link.split('/')[1]
                    list_secciones.append(seccion)
                except:
                    list_secciones.append('')
                   
                try:
                    bajada = soup_article.find('h2', class_='summary').get_text() 
                    list_bajadas.append(bajada)
                except:
                    list_bajadas.append('')
                             
                try:
                    autor = soup_article.find('article',class_='contenedor-detail-block').find('div',class_='nd-content-body').find('span',class_='author').get_text()
                    list_autores.append(autor)
                except:
                    list_autores.append('')
   
                body = soup_article.find('div', id='content-body')
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
                has_next = soup1.find('div',class_='number-pages-container').findAll('a', class_='link-pagination')[-1].get_text().replace('\n','').replace(' ','')
            except:
                has_next = ''
                
   
    current_page = current_page + 1
    #url2 =url+ str(current_page)+query
    try:
        try:    
            link = browser.find_element_by_link_text("SIGUIENTE")
            link.send_keys(Keys.RETURN)
            #browser.find_element_by_link_text(" SIGUIENTE").send_keys('\n')
            #browser.find_element_by_link_text(" SIGUIENTE").click()
            time.sleep(5)  
            browser.execute_script("window.stop();")
  
            coverpage_news= browser.page_source
            soup1 = BeautifulSoup(coverpage, 'html5lib')
            coverpage_news = soup1.find_all('div', class_='item-news-container')
            number_of_articles =  len(coverpage_news)
        except:
            print("Error en Siguiente")
    except:     
        has_next=''
        print('END')
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



browser.quit()
workbook = xlsxwriter.Workbook('elmilenio-results.xlsx')
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
