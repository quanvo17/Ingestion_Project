import re
import numpy as np
import recordlinkage
import os
import pandas as pd


# Function add store
def add_store(source):
    stores = []
    dfs = []
    file_name = os.listdir(source)
    for file in file_name:
        if "csv" in file:
            stores.append(file.split(".")[0])
    for store in stores:
        link = source + "/" + store + ".csv"
        df = pd.read_csv(link)
        df['store'] = store
        dfs.append(df)
    df_data = pd.concat(dfs, ignore_index=True)
    return df_data


def normalize_data_iphone(source):
    df = add_store(source)

    # Explode field color
    df['color'] = df['color'].str.split(",")
    df = df.explode('color', ignore_index=True)
    df['color'] = df['color'].fillna(value='chưa rõ')

    # Fill ram and rom
    df['ram'] = df['ram'].fillna("1GB")
    df['rom'] = df['rom'].fillna("16GB")

    # Regex form and explode field ram
    for i in range(0, len(df['ram'])):
        a = (re.findall('(\d+)(?=(?:\/\d+)*\s*([MG]B))', df['ram'][i]))
        for j in range(0, len(a)):
            a[j] = ''.join(a[j])
        df['ram'][i] = a
    df = df.explode('ram', ignore_index=True)

    # Regex form and explode field rom
    for i in range(0, len(df['rom'])):
        a = (re.findall('(\d+)(?=(?:\/\d+)*\s*([MG]B))', df['rom'][i]))
        for j in range(0, len(a)):
            a[j] = ''.join(a[j])
        df['rom'][i] = a
    df = df.explode('rom', ignore_index=True)

    # df['rom'].dropna()
    # df['ram'].dropna()

    # Regex rear cam and front cam. after regex, things will only contain MP
    for i in range(0, len(df['rear_cam'])):
        try:
            a = re.findall('\d+\.?\d+ MP', df['rear_cam'][i])
            df['rear_cam'][i] = '+'.join(a)
        except:
            continue
    for i in range(0, len(df['front_cam'])):
        try:
            a = re.findall('\d+\.?\d+ MP', df['front_cam'][i])
            df['front_cam'][i] = '+'.join(a)
        except:
            continue

    # Get status of product
    for i in range(0, len(df['name'])):
        a = (re.findall('cũ|99%|98%|97%|96%|95%|90%|likenew|Cũ|Likenew|LIKENEW', df['name'][i]))
        if not a:
            df['status'][i] = 'mới'
        else:
            df['status'][i] = 'cũ'

    # Regex pricing
    for i in range(0, len(df['price'])):
        if not df['price'][i]:
            a = (re.findall('[0-9]', df['price'][i]))
            df['price'][i] = ''.join(a)

    df['price'] = df['price'].replace('From', 'Liên hệ')

    # Regex sim
    for i in range(0, len(df['name'])):
        a = (re.findall('wifi|WIFI|Wifi', df['name'][i]))
        b = (re.findall('4G|3G', df['name'][i]))
        if a and b:
            df['sim'][i] = 'e-sim'
        elif a and not b:
            df['sim'][i] = 'wifi only'

    # Regex name
    for i in range(0, len(df['name'])):
        a1 = re.search('(.+(GB|Gb))', df['name'][i])
        a2 = re.search('(.+\()', df['name'][i])
        result1 = a1.group(0) if a1 else ""
        result2 = a2.group(0)[:-1] if a2 else ""
        if result1 == "" or result2 == "":
            result = result1 + result2
            if result != "":
                df['name'][i] = result
        else:
            if len(result1) > len(result2):
                df['name'][i] = result2
            else:
                df['name'][i] = result1
        df['name'][i] = re.sub('Điện thoại', '', df['name'][i])
        df['name'][i] = re.sub('Apple', '', df['name'][i])
        df['name'][i] = re.sub(' +', ' ', df['name'][i])

    for field in ['name', 'color', 'cpu', 'bluetooth']:
        df[field] = df[field].str.strip()
    return df


#
# def matching_data(source):
#     return data


if __name__ == '__main__':
    data_df = normalize_data_iphone(
        "/Users/quanvd/Workspace/HUST/2020-2/Ingestion/crawler/Ingestion_Project/Crawler/Data/iphone")
    data_df.to_csv("test.csv")
