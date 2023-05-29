import os, shutil
from bs4 import BeautifulSoup as bs
import requests
import csv
import pandas as pd

with open("test.html", "r") as f:
    htmlCode = f.read()a