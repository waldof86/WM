import json
import sys
import time
import xlsxwriter

import pandas as pd
from json import JSONEncoder
from configparser import ConfigParser

from Scraper import Scraper

# Loading of configurations
from utils import ComplexEncoder, ObjectEncoder 

config = ConfigParser()
config.read('config.ini')

# Setting the execution mode
headless_option = len(sys.argv) >= 2 and sys.argv[1].upper() == 'HEADLESS'

# Loading of input data (LinkedIn Urls)
profiles_urls = []
for entry in open(config.get('profiles_data', 'input_file_name'), "r"):
    profiles_urls.append(entry.strip())

if len(profiles_urls) == 0:
    print("Please provide an input.")
    sys.exit(0)


# Launch Scraper
s = Scraper(
    linkedin_username=config.get('linkedin', 'username'),
    linkedin_password=config.get('linkedin', 'password'),
    profiles_urls=profiles_urls,
    headless=headless_option
)

s.start()

s.join()

scraping_results = s.results




# Generation of XLS file with profiles data
output_file_name = config.get('profiles_data', 'output_file_name')
if config.get('profiles_data', 'append_timestamp').upper() == 'Y':
    output_file_name_split = output_file_name.split('.')
    output_file_name = "".join(output_file_name_split[0:-1]) + "_" + str(int(time.time())) + "." + \
                       output_file_name_split[-1]

workbook = xlsxwriter.Workbook(output_file_name)
worksheet = workbook.add_worksheet()

# Headers
headers = ['Nombre', 'Email','URL Linkedin', 'Habilidades', 'Trabajos','Educación']
for h in range(len(headers)):
    worksheet.write(0, h, headers[h])

# Content
for i in range(len(scraping_results)):
    scraping_result = scraping_results[i]
    if scraping_result.is_error():
        data = ['Error'] * len(headers)
    else:
        p = scraping_result.profile
        data = [
            p.name,
            p.email,
            scraping_results[i].linkedin_url
        ]
        data.append(json.dumps(p.skills, cls=ComplexEncoder))
        data.append(json.dumps(p.jobs, cls=ComplexEncoder))
        data.append(json.dumps(p.degrees, cls=ComplexEncoder))
    for j in range(len(data)):
        worksheet.write(i + 1, j, data[j])

workbook.close()

print("Scraping Ended")
