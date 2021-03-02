#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 10:23:40 2021

@author: mutt
"""

from file_opera import list_dir_files as ldf
import os
import pandas as pd
import sqlalchemy
from pprint import pprint

def many_excel_to_sql(sql_tabel_name,base_path = None,fill_na = "nodata"):
    if base_path:
        basic_path = base_path
    else:   
        basic_path      =  os.path.abspath(os.path.dirname(__file__))
    file_path , file_name = ldf(basic_path,[".xls",".xlsx"])
    file_name = [name.split(".")[0] for name in file_name]
    file_list = zip(file_path,file_name)
    
    #sql配置
    engine = sqlalchemy.create_engine('mysql+pymysql://root:loveying1211@localhost:3306/%s'%sql_tabel_name)
    error_file = []
    
    
    for detail in file_list :
        #print("写入路径",detail[0],"文件名",detail[1])
        try:
            path = detail[0]
            name = detail[1]
            
            df = pd.read_excel(path,header = 1)
            df.fillna(fill_na,inplace = True)
            df.to_sql(
                name = name,
                con = engine,
                index = False,
                if_exists = 'append'
            )
        except BaseException as e:
            #print("文件写入错误：路径>>%s"%path,"文件名>>%s"%name)
            error_file.append(detail)
            #error_file.append(str(e))
    
    if error_file:    
        print("SQL写入失败，失败列表")
        pprint(error_file)
        
        
if __name__ == "__main__":
    #for example
    
    many_excel_to_sql("hfqdq")
    
    
    