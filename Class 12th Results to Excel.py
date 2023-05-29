import os, shutil
from bs4 import BeautifulSoup as bs
import requests
import csv
import pandas as pd

df = pd.read_csv("Roll No.csv")

try:
    os.mkdir(".Results")
except Exception as e:
    pass

try:
    os.mkdir("Output")
except Exception as e:
    pass

print("-----RBSE Class 12th Results to Excel-----")
# choice = 0
# while choice not in [1, 2, 3]:
#     choice = int(input('[Enter 1 for SCIENCE, 2 for COMMERCE, & 3 for ARTS]: '))
    
# baseUrl = "https://rajeduboard.rajasthan.gov.in/RESULT2023/ARTS/Roll_Output.asp?roll_no="  #Default for ARTS


# if choice == 1:  
#     baseUrl = "https://rajeduboard.rajasthan.gov.in/RESULT2023/SCIENCE/Roll_Output.asp?roll_no="
# elif choice == 2:  
#     baseUrl = "https://rajeduboard.rajasthan.gov.in/RESULT2023/COMM/Roll_Output.asp?roll_no="
# elif choice == 3:  
#     baseUrl = "https://rajeduboard.rajasthan.gov.in/RESULT2023/ARTS/Roll_Output.asp?roll_no="


# streamNames = ["Science","Commerce","Arts"]
# def result(rollno):
r = requests.get("https://rajeduboard.rajasthan.gov.in/RESULT2023/SCIENCE/Roll_Output.asp?roll_no=2653265&B1=Submit")

    
    
# Parse the HTML code
soup = bs(r.content, 'html.parser')
soup.prettify()

# Extracting examinee's name, father's name, mother's name, roll number
examinee_name = soup.select("body > div > center > table > tbody > tr:nth-child(6) > td > div > center > table:nth-child(1) > tbody > tr:nth-child(3) > td:nth-child(1) > font")
print(examinee_name)