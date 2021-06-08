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


def get_status(df):
    for i in range(0, len(df['name'])):
        try:
            b = re.findall('99%', df['name'][i])
            c = re.findall('97%', df['name'][i])
            a = (re.findall('cũ|98%|96%|95%|90%|likenew|Cũ|Likenew|LIKENEW', df['name'][i]))
            if b != []:
                df['status'][i] = '99%'
            elif c != []:
                df['status'][i] = '97%'
            elif a == []:
                df['status'][i] = 'mới'
            else:
                df['status'][i] = 'cũ'
        except:
            continue
    return df


def normalize_color(df):
    # explode exist color
    df['color'] = df['color'].str.split(",")
    df = df.explode('color', ignore_index=True)

    # get color of product from name

    for i in range(0, len(df['name'])):
        if df['color'][i] is None:
            try:
                a = re.findall('(bạc|tím|trắng|vàng|xanh|đỏ|lục|lam|đen|xám|gold|graphite|silver|blue|gray)',
                               df['name'][i].lower())
                if a:
                    df['color'][i] = ','.join(a)
            except:
                continue

    # explode exist color lan 2
    df['color'] = df['color'].str.split(",")
    df = df.explode('color', ignore_index=True)

    # regex to remove special string color
    for i in range(0, len(df['color'])):
        try:
            df['color'][i] = re.sub('(nhôm nguyên khối|vỏ nguyên khối)', '', df['color'][i].lower())
            df['color'][i] = re.sub('\(.+', '', df['color'][i].lower())
        except:
            continue

    # explode color lan chot
    df['color'] = df['color'].str.split("-")
    df = df.explode('color', ignore_index=True)

    df['color'] = df['color'].str.split("/")
    df = df.explode('color', ignore_index=True)

    for i in range(0, len(df['color'])):
        try:
            df['color'][i] = re.sub('^ +', '', df['color'][i].lower())
            df['color'][i] = re.sub(' +$', '', df['color'][i].lower())
            df['color'][i] = re.sub(' +', ' ', df['color'][i].lower())
        except:
            continue

    for i in range(0, len(df['color'])):
        try:
            if df['color'][i] == 'black':
                df['color'][i] = 'đen'
            elif df['color'][i] == 'blue':
                df['color'][i] = 'xanh'
            elif df['color'][i] == 'gold':
                df['color'][i] = 'vàng'
            elif re.findall('(grey|gray)', df['color'][i]):
                df['color'][i] = 'xám'
            elif df['color'][i] == 'silver':
                df['color'][i] = 'bạc'
            elif re.findall('(rose)', df['color'][i]):
                df['color'][i] = 'hồng'
            elif re.findall('(graphite)', df['color'][i]):
                df['color'][i] = 'vàng đồng'
            elif re.findall('(xanh lá cây)', df['color'][i]):
                df['color'][i] = 'xanh lục'
            elif re.findall('(xanh dương)', df['color'][i]):
                df['color'][i] = 'xanh'
            elif re.findall('(bạc trắng)', df['color'][i]):
                df['color'][i] = 'bạc'
        except:
            continue

    for i in range(0, len(df['color'])):
        if df['color'][i] == 'undefined':
            df['color'][i] = 'chưa rõ'

    df['color'] = df['color'].fillna(value='chưa rõ')
    return df


def normalize_tech(df):
    # Fill ram and rom
    df['ram'] = df['ram'].fillna("1GB")
    df['rom'] = df['rom'].fillna("16GB")

    # regex form of ram and explode ram
    for i in range(0, len(df['ram'])):
        try:
            a = (re.findall('(\d+)(?=(?:\/\d+)*\s*([MG]B))', df['ram'][i]))
            for j in range(0, len(a)):
                a[j] = ''.join(a[j])
            df['ram'][i] = a
        except:
            continue
    df = df.explode('ram', ignore_index=True)

    # regex form of rom and explode rom
    for i in range(0, len(df['rom'])):
        try:
            a = (re.findall('(\d+)(?=(?:\/\d+)*\s*([MG]B))', df['rom'][i]))
            for j in range(0, len(a)):
                a[j] = ''.join(a[j])
            df['rom'][i] = a
        except:
            continue
    df = df.explode('rom', ignore_index=True)

    # regex rear cam and front cam. after regex, things will only contain MP
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

    # sim regex
    for i in range(0, len(df['name'])):
        a = (re.findall('wifi|WIFI|Wifi', df['name'][i]))
        b = (re.findall('4G|3G', df['name'][i]))
        if a and b:
            df['sim'][i] = 'e-sim'
        elif a and not b:
            df['sim'][i] = 'wifi only'

    return df


def normalize_prize(df):
    # pricing regex
    for i in range(0, len(df['price'])):
        if not df['price'][i] is None:
            a = (re.findall('[0-9]', df['price'][i]))
            df['price'][i] = ''.join(a)
    return df


def convert_name(name):
    try:
        t_name = name.lower()
    except:
        return name
    if 'macbook' in t_name:
        # Pro or air
        f_name = 'MACBOOK'
        if 'air' in t_name:
            f_name += ' AIR'
        elif 'pro' in t_name:
            f_name += ' PRO'

        # M1 or not
        if 'm1' in t_name:
            f_name += ' M1'

        # inch
        if 'air' in t_name:
            f_name += ' 13'
        elif '13' in t_name or '13"' in t_name or '13.3' in t_name:
            f_name += " 13"
        elif '15' in t_name:
            f_name += " 15"
        elif '16' in t_name:
            f_name += ' 16'
        elif '12' in t_name:
            f_name += ' 12'

        # touchbar
        if 'touchbar' in t_name:
            f_name += ' TOUCHBAR'

        # year
        x = re.findall(r'.*([1-3][0-9]{3})', t_name)
        if len(x) > 0:
            if int(x[0]) <= 2021:
                f_name += (' ' + x[0])

        return f_name
    else:
        return name


def normalize_name(df):
    for i in range(0, len(df['name'])):
        try:
            ip = re.findall('(iphone [0-9][0-9]|iphone [0-9]s|iphone se|iphone xr|iphone xs|iphone x|iphone [0-9])',
                            df['name'][i].lower())
            pro = re.findall('(pro)', df['name'][i].lower())
            max = re.findall('(max)', df['name'][i].lower())
            plus = re.findall('(plus)', df['name'][i].lower())
            year = re.findall('(\([0-9][0-9][0-9][0-9]\)| [0-9][0-9][0-9][0-9] )', df['name'][i].lower())
            if ip:
                new_name = ''.join(ip) + ' ' + ''.join(plus) + ' ' + ''.join(pro) + ' ' + ''.join(max) + ' ' + ''.join(
                    year)
                new_name = re.sub('\(|\)', ' ', new_name)
                new_name = re.sub('^ +', '', new_name)
                new_name = re.sub(' +$', '', new_name)
                new_name = re.sub(' +', ' ', new_name)
                df['name'][i] = new_name.upper()
        except:
            continue

    list_idx = []
    for i in range(0, len(df['name'])):
        try:
            ip = re.findall('(ipad)', df['name'][i].lower())
            ver = re.findall('( [0-9] |gen [0-9]| [0-9]$|m1)', df['name'][i].lower())
            year = re.findall('( [0-9][0-9][0-9][0-9] | [0-9][0-9][0-9][0-9]$)', df['name'][i].lower())
            pro = re.findall('(pro)', df['name'][i].lower())
            mini = re.findall('(mini)', df['name'][i].lower())
            air = re.findall('(air)', df['name'][i].lower())
            screen = re.findall("(11|12\.9|10\.5|9\.7|10\.2)", df['name'][i].lower())
            if ip != []:
                list_idx.append(i)
                new_name = ''.join(ip) + ' ' + ''.join(pro) + ' ' + ''.join(mini) + ' ' + ''.join(air) + ' ' + ''.join(
                    ver) + ' ' + ''.join(screen) + ' ' + ''.join(year)
                new_name = re.sub('\(|\)|\"|\″', ' ', new_name)
                new_name = re.sub('^ +', '', new_name)
                new_name = re.sub(' +$', '', new_name)
                new_name = re.sub(' +', ' ', new_name)
                df['name'][i] = new_name.upper()
        except:
            continue

    for i in list_idx:
        ip = re.findall('(ipad)', df['name'][i].lower())
        ver = re.findall('( [0-9] |gen [0-9]| [0-9]$|m1)', df['name'][i].lower())
        year = re.findall('( [0-9][0-9][0-9][0-9] | [0-9][0-9][0-9][0-9]$)', df['name'][i].lower())
        pro = re.findall('(pro)', df['name'][i].lower())
        mini = re.findall('(mini)', df['name'][i].lower())
        air = re.findall('(air)', df['name'][i].lower())
        screen = re.findall("(11|12\.9|10\.5|9\.7|10\.2)", df['name'][i].lower())
        new_name = ''.join(ip) + ' ' + ''.join(pro) + ' ' + ''.join(mini) + ' ' + ''.join(air) + ' ' + ''.join(
            ver) + ' ' + ''.join(screen) + ' ' + ''.join(year)
        new_name = re.sub('\(|\)|\"|\″', ' ', new_name)
        new_name = re.sub('^ +', '', new_name)
        new_name = re.sub(' +$', '', new_name)
        new_name = re.sub(' +', ' ', new_name)
        df['name'][i] = new_name.upper()

    for i in list_idx:
        if (re.findall("IPAD AIR 3", df['name'][i])):
            df['name'][i] = 'IPAD AIR 3'
        if (re.findall("IPAD AIR 4", df['name'][i])):
            df['name'][i] = 'IPAD AIR 4'
        if (re.findall("IPAD GEN 5", df['name'][i])):
            df['name'][i] = 'IPAD GEN 5'
        if (re.findall("IPAD 2017", df['name'][i])):
            df['name'][i] = 'IPAD GEN 5'
        if (re.findall("IPAD 2018", df['name'][i])):
            df['name'][i] = 'IPAD GEN 6'
        if (re.findall("IPAD GEN 6", df['name'][i])):
            df['name'][i] = 'IPAD GEN 6'
        if (re.findall("IPAD GEN 7", df['name'][i])):
            df['name'][i] = 'IPAD GEN 7'
        if (re.findall("IPAD GEN 8", df['name'][i])):
            df['name'][i] = 'IPAD GEN 8'
        if (re.findall("IPAD MINI 5", df['name'][i])):
            df['name'][i] = 'IPAD MINI 5'
        if (re.findall("IPAD PRO M1 11", df['name'][i])):
            df['name'][i] = 'IPAD PRO M1 11'
        if (re.findall("IPAD PRO M1 12.9", df['name'][i])):
            df['name'][i] = 'IPAD PRO M1 12.9'

    df['name'] = df.apply(lambda row : convert_name(row['name']), axis=1)
    return df


def normalize_data(source):
    df = add_store(source)

    df = get_status(df)

    df = normalize_color(df)

    df = normalize_tech(df)

    df = normalize_prize(df)

    df = normalize_name(df)

    for field in ['name', 'color', 'cpu', 'bluetooth']:
        df[field] = df[field].str.strip()
    return df
