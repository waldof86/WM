# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 14:29:33 2021

@author: Marcos Buccellato
"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import xlsxwriter
from webdriver_manager.chrome import ChromeDriverManager

'''
DRIVER_PATH = 'C:/Users/marco/Dropbox/Python/CienciaYPandemia/chromedriver.exe'
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)
#driver.get('https://google.com')
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.clarin.com/tema/barrio-chino.html")
'''
headless = True
url = "https://www.clarin.com/tema/pandemia.html"
# Creation of a new instance of Chrome
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
if headless:
    options.add_argument('--headless')
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
driver.get(url)







html = driver.find_element_by_tag_name('html')
html.send_keys(Keys.END)
html.send_keys(Keys.ARROW_UP)
html.send_keys(Keys.ARROW_UP)
html.send_keys(Keys.ARROW_UP)
time.sleep(5)
# Get scroll height.
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        
        html.send_keys(Keys.ARROW_UP)
        html.send_keys(Keys.ARROW_UP)
        html.send_keys(Keys.ARROW_UP)
        time.sleep(5)
        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height
print("fin")


coverpage = driver.page_source
driver.quit()
    # We'll save in coverpage the cover page content


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
list_fecha = []
list_secciones = []
list_autores = []

for n in np.arange(0, number_of_articles):

        
        #Obtener la volanta
        volanta = coverpage_news[n].find('p', class_='volanta').getText()
        list_volanta.append(volanta)
        # Obtener el link al artículo
        link = coverpage_news[n].find('a')['href']
        list_links.append('https://www.clarin.com/' + link) 
        #Obtener la fecha
        fecha = coverpage_news[n].find('div', class_='fecha').find('p').getText()
        list_fecha.append(fecha)


        # Ir al artículo (it is divided in paragraphs)
        print('https://www.clarin.com' + link)
        try:
            article = requests.get('https://www.clarin.com' + link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')
            # Obtener el título
            title = soup_article.find('div', class_='title').find('h1').get_text()
        
            body = soup_article.find_all('div', class_='body-nota')
            x = body[0].find_all('p')
            
            # Unifying the paragraphs
            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)

            try:
                seccion = soup_article.find('div',class_='entry-head').findAll('span', itemprop='name')[1].get_text()
            except:
                seccion = ''
            try:
                autor = soup_article.find('p', itemprop='author').get_text()
            except:
                autor = ''
            try:
                # Obtener el bajada
                bajada = soup_article.find('div', class_='title').find('div',class_='bajada').find('h2').get_text()
            except:
                bajada=''
                
            news_contents.append(final_article)
            list_titles.append(title)
            list_bajadas.append(bajada)
            list_secciones.append(seccion)
            list_autores.append(autor)
        except:
            print('There is a problem.')
            list_titles.append('')
            list_bajadas.append('')
            news_contents.append('')
            list_secciones.append('')
            list_autores.append('')
       
            

    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'Clarín', 
         'País': 'Argentina',
         'Seccion': list_secciones,
         'fecha': list_fecha,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Autor': list_autores,
         'Contenido': news_contents
         })

workbook = xlsxwriter.Workbook('clarin-results.xlsx')
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
