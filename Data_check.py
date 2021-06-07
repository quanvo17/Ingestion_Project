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


# get status of product. now have 2 status: cu, moi



