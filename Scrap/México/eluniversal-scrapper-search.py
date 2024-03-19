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
#import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

headless = False
url='https://activo.eluniversal.com.mx/historico/search/index.php?q=pandemia&anio=&seccion=&opinion=&tipo_contenido=&autor=&tipoedicion=&dia=&mes=&rango_Fechas=&k_rango_fechas=&fecha_ini=&fecha_fin=&editor=&start='
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

'''
current_page=1

headless = True
# Creation of a new instance of Chrome
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
if headless:
    options.add_argument('--headless')
options.add_argument("--window-size=1920,1200")

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
browser.set_page_load_timeout(8)
try:
    browser.get(url+ str(current_page)+query)
except TimeoutException:
    browser.execute_script("window.stop();")
coverpage =  browser.page_source
'''



headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
p_actual = 1817
start_actual = (p_actual-1)*20
page= requests.get(url+str(start_actual)+'&page='+str(p_actual),headers=headers)
coverpage= page.content
    # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
coverpage_news = soup1.find_all('div', class_='moduloNoticia')


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

paginas = soup1.find('div', class_='HojaBusqueda').find('span').get_text()
pattern = r"\(([0-9]*) de ([0-9]*)\)"

p_actual = int(re.search(pattern,paginas).group(1))
p_final=   int(re.search(pattern,paginas).group(2))
#p_final=3

while (p_actual <= p_final):
    print("Página: " + str(p_actual) +"de " +str(p_final))
    for n in np.arange(0, number_of_articles):
    
            #Obtener la volanta
            list_volanta.append('')
            # Obtener el link al artículo
            
            link = coverpage_news[n].find('div', class_='HeadNota').find('a')['href']
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
                    seccion = soup_article.find('div', class_='ce12-DatosArticulo-Tags mb-10').find('a').get_text() 
                    list_secciones.append(seccion)
                except:
                    list_secciones.append('')
                # Obtener el título
                try:
                    if (seccion == 'OPINIÓN'):
                        title = soup_article.find('h1', class_='ceh-Opinion_Titulo').get_text()
                    else:
                        title = soup_article.find('div', class_='Encabezado-Articulo').find('h1').get_text()
                except:
                    title=''

                    # Obtener el bajada
                try:
                    if (seccion == 'OPINIÓN'):
                        bajada = soup_article.find('p', class_='ceh-Opinion_Resumen').get_text()
                    else:
                        bajada = soup_article.find('div', class_='Encabezado-Articulo').find('h').get_text()
                    list_bajadas.append(bajada)
                except:
                    list_bajadas.append('')
               
                try:
                    if (seccion == 'OPINIÓN'):
                        autor = soup_article.find('h2', class_='ceh-Opinion_Autor').get_text()
                    else:
                        autor = soup_article.find('span',class_='ce12-DatosArticulo_autor').get_text()
                    list_autores.append(autor)
                except:
                    list_autores.append('')
                
                try:
                    if (seccion == 'OPINIÓN'):
                        fecha = soup_article.find('a', class_='ce12-DatosArticulo_ElementoFecha').getText()    
                    else:
                        fecha = soup_article.find('span', class_='ce12-DatosArticulo_ElementoFecha').getText()
                except:
                      fecha=''

        
                body = soup_article.find('div', class_='field field-name-body field-type-text-with-summary field-label-hidden')
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
            except:
                print('There is a problem.')
                list_titles.append('')
                news_contents.append('')
                list_fecha.append('')
               
    
    try:
        has_next = soup1.find('div', id='resultdata').find('a',class_='next_btn').get_text()
    except:
        has_next = ''
        
    p_actual= p_actual + 1   
    if (p_actual <= p_final):
            start_actual = (p_actual - 1) * 20
            url2 = url + str(start_actual) + '&page=' + str(p_actual)
            page= requests.get(url2,headers=headers)               
            coverpage= page.content
            soup1 = BeautifulSoup(coverpage, 'html5lib')
            coverpage_news = soup1.find_all('div', class_='moduloNoticia')
            number_of_articles =  len(coverpage_news)

    # df_show_info
df_show_info = pd.DataFrame(
        {'Diario': 'El Universal', 
         'País': 'México',
         'Seccion': list_secciones,
         'fecha': list_fecha,
         'Título Artículo': list_titles,
         'Link a Artículo': list_links,
         'Bajada Artículo': list_bajadas,
         'Autor': list_autores,
         'Contenido': news_contents
         })

workbook = xlsxwriter.Workbook('eluniversal-results.xlsx')
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
