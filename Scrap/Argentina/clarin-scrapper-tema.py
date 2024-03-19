# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 14:29:33 2021

@author: Marcos Buccellato
"""

#scrapeo solo hasta 12/06/2020 probar https://www.google.com/search?q=coronavirus+ciencia+site%3Aclarin.com&num=100&biw=1536&bih=760&source=lnt&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2020%2Ccd_max%3A6%2F12%2F2020&tbm=
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import xlsxwriter
from webdriver_manager.chrome import ChromeDriverManager
import clarin as cl

parser = cl.clarin_parser
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
time.sleep(8)
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

df_show_info = pd.DataFrame()

for n in np.arange(0, number_of_articles):

       
        # Obtener el link al artículo
        link = 'https://www.clarin.com/' + coverpage_news[n].find('a')['href']
      
        rslt = parser(link)
        if (rslt != ''):
            df_show_info = df_show_info.append(rslt, ignore_index = True)
           

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
