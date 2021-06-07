import re
import numpy as np
import recordlinkage
import os
import glob
import pandas as pd

# Read Data in multi folder
folder_path = r'Crawler/Data'
subFolder_path = glob.glob(folder_path + "/*")
seq = []
for paths in subFolder_path:
    fileNames = glob.glob(paths + "/*.csv")
    dfs = []
    for filename in fileNames:
        dfs.append(pd.read_csv(filename))
    # Concatenate all data into one DataFrame
    seq.append(pd.concat(dfs, ignore_index=True))

data_df = pd.concat(seq, ignore_index=True)

new_df = data_df
new_df['color'] = new_df['color'].str.split(",")
new_df = new_df.explode('color', ignore_index=True)
new_df['ram'] = new_df['ram'].fillna("1GB")
new_df['rom'] = new_df['rom'].fillna("16GB")

# regex form of ram and explode ram

for i in range(0, len(new_df['ram'])):
    a = (re.findall('(\d+)(?=(?:\/\d+)*\s*([MG]B))', new_df['ram'][i]))
    for j in range(0, len(a)):
        a[j] = ''.join(a[j])
    new_df['ram'][i] = a
new_df = new_df.explode('ram', ignore_index=True)

# regex form of rom and explode rom

for i in range(0, len(new_df['rom'])):
    a = (re.findall('(\d+)(?=(?:\/\d+)*\s*([MG]B))', new_df['rom'][i]))
    for j in range(0, len(a)):
        a[j] = ''.join(a[j])
    new_df['rom'][i] = a
new_df = new_df.explode('rom', ignore_index=True)

# get status of product. now have 2 status: cu, moi

for i in range(0, len(new_df['name'])):
    a = (re.findall('cũ|99%|98%|97%|96%|95%|90%|likenew|Cũ|Likenew|LIKENEW', new_df['name'][i]))
    if not a:
        new_df['status'][i] = 'mới'
    else:
        new_df['status'][i] = 'cũ'

# pricing regex

for i in range(0, len(new_df['price'])):
    if not new_df['price'][i]:
        a = (re.findall('[0-9]', new_df['price'][i]))
        new_df['price'][i] = ''.join(a)

new_df['price'] = new_df['price'].replace('From', 'Liên hệ')

# sim regex

for i in range(0, len(new_df['name'])):
    a = (re.findall('wifi|WIFI|Wifi', new_df['name'][i]))
    b = (re.findall('4G|3G', new_df['name'][i]))
    if a and b:
        new_df['sim'][i] = 'e-sim'
    elif a and not b:
        new_df['sim'][i] = 'wifi only'

# name regex
for i in range(0, len(new_df['name'])):
    a1 = re.search('(.+(GB|Gb))', new_df['name'][i])
    a2 = re.search('(.+\()', new_df['name'][i])
    result1 = a1.group(0) if a1 else ""
    result2 = a2.group(0)[:-1] if a2 else ""
    if result1 == "" or result2 == "":
        result = result1 + result2
        if result != "":
            new_df['name'][i] = result
    else:
        if len(result1) > len(result2):
            new_df['name'][i] = result2
        else:
            new_df['name'][i] = result1
    new_df['name'][i] = re.sub('Điện thoại', '', new_df['name'][i])
    new_df['name'][i] = re.sub('Apple', '', new_df['name'][i])
    new_df['name'][i] = re.sub(' +', ' ', new_df['name'][i])

# screen size and tech regex
for i in range(0, len(new_df['screensize'])):
    if not new_df['screentech'][i] and not new_df['screensize'][i]:
        text = re.search("\d+(\.|\,)?\d+( inch|\")", new_df['screensize'][i])
        if text:
            new_df['screentech'][i] = re.sub("\d+(\.|\,)?\d+( inch|\")", '', new_df['screensize'][i])
            new_df['screensize'][i] = text.group(0)
        else:
            new_df['screentech'][i] = new_df['screensize'][i]
            new_df['screensize'][i] = ''
for i in range(0, len(new_df['name'])):
    if not new_df['screensize'][i] or new_df['screensize'][i] == '':
        text = re.search("\d+(\.|\,)?\d+( inch)", new_df['name'][i])
        if text:
            new_df['screensize'][i] = text.group(0)

for i in range(0, len(new_df['screentech'])):
    if not new_df['screentech'][i]:
        if len(new_df['screentech'][i]) > 2:
            text = re.search('\d+(\.|\,)?\d+( inch|")', new_df['screentech'][i])
            print(text)
            if text:
                new_df['screensize'][i] = text.group(0)
                new_df['screentech'][i] = re.sub('\d+(\.|\,)?\d+( inch|"|-inch| inches| ")', '',
                                                 new_df['screentech'][i])

for field in list(new_df):
    new_df[field] = new_df[field].str.strip()


new_df.to_csv('test.csv')
