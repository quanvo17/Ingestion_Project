import re

import numpy as np
from Crawler.items import SchemaItems


# Hàm : transform(text): convert các trường về tên trường chuẩn
# Hàm : normalize(text): chuẩn hoá dữ liệu
# Hàm : get_name(text): dùng để trả về tên sản phẩm


def levenshtein_ratio_and_distance(s, t, ratio_calc=False):
    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows, cols), dtype=int)
    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0  # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row - 1][col] + 1,  # Cost of deletions
                                     distance[row][col - 1] + 1,  # Cost of insertions
                                     distance[row - 1][col - 1] + cost)  # Cost of substitutions
    if ratio_calc == True:
        Ratio = ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))
        return Ratio
    else:
        return "The strings are {} edits away".format(distance[row][col])


def normalize(text):
    normal_text = text.lower()
    normal_text = re.sub(r'[^\w\s]', '', normal_text)
    normal_text = re.sub(' +', ' ', normal_text)
    normal_text = re.sub(r'\n+|\r+|\t+', '', text)
    return normal_text


def get_name(text):
    x = re.findall("Mac.*20[0-9][0-9]", text)
    if (x):
        temp = ''.join(x)
        temp = re.sub('\((.*?)\)', '', temp)
        temp = re.sub('\(|\)', '', temp)
        temp = re.sub(' +', ' ', temp)
    else:
        temp = text
    return temp


def transform(text):
    text = text.lower()
    status = ["status", "loại"]
    name = ["name", "tên", "tên sản phẩm"]
    resolution = ["resolution", "độ phân giải", "độ phân giải màn hình"]
    screentech = ["screentech", "màn hình", "công nghệ màn hình"]
    screensize = ["screensize", "kích thước màn hình"]
    cpu = ["cpu", "chip", "chipset", "Bộ vi xử lý"]
    rom = ["rom", "bộ nhớ trong", "Ổ cứng"]
    ram = ["ram", "Ram"]
    pin = ["pin", "PIN", "dung lượng pin"]
    gpu = ["gpu", "đồ hoạ", "vga", "card hình"]
    size = ["size", "kích thước", "kích thước (rộng x dài x cao)"]
    rear_cam = ["rear_cam", "camera sau", "camera chính", "cam sau"]
    front_cam = ["front_cam", "camera trước", "camera selfie", "cam trước", "camera phụ", "webcam"]
    sim = ["sim", "thẻ sim"]
    tech = ["tech", "bảo mật", "công nghệ khác", "Bảo mật, Công nghệ"]
    wifi = ["wifi", "Giao tiếp không dây"]
    bluetooth = ["bluetooth"]
    weight = ["weight", "trọng lượng", "cân nặng"]
    os = ["os", "hệ điều hành"]
    port = ["port", "cổng sạc", "cổng kết nối", "cổng giao tiếp", "khe cắm"]
    price = ["price", "giá", "giá sản phẩm", "price_sale", "sale_price"]
    color = ["color", "màu", "màu sắc"]
    link = ["link", "url"]
    feature_list = []
    feature_list = [link, pin, color, status, name, resolution, screensize, screentech, cpu, rom, ram, gpu, size,
                    rear_cam, front_cam, sim, tech, wifi, bluetooth, weight, os, port, price]
    for feature in feature_list:
        for num in range(len(feature)):
            Distance = levenshtein_ratio_and_distance(text, feature[num], ratio_calc=True)
            # print(Distance)
            if Distance >= 0.77:
                text = feature[0]
    return text


def convert(data):
    schema = SchemaItems()
    feature_list = "link,color,status,name,resolution,screensize,screentech,cpu,rom,ram,gpu,size,rear_cam,front_cam," \
                   "sim,tech,wifi,bluetooth,weight,os,port,price".split(",")
    l = []
    for col in data:
        l.append(col)
    l = set(l)
    for col in l:
        data[transform(col)] = data.pop(col)
    for feature in feature_list:
        try:
            if feature == 'name':
                schema[feature] = get_name(data[feature])
            else:
                schema[feature] = data[feature]
        except:
            schema[feature] = ''
    return schema
