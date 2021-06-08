from Crawler.Crawler.processing_func import normalize_data

# Read Data in multi folder
objects = ['iphone', 'ipad', 'applewatch', 'macbook']
folder_path = r'Crawler/Data/'
for obj in objects:
    data = normalize_data(folder_path + obj)
    data.to_csv(folder_path + "data_normalized.csv")







