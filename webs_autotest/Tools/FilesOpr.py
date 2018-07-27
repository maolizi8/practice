'''
Created on 2017年7月27日

@author: geqiuli
'''
import os
from os import path
from conftest import root_dir


def get_info_from_txt(file_name):
    arr=[]
    with open(file_name,'r') as f:
        for line in f.readlines():
            arr.append(line.strip())
    return arr

def get_newest_file(file_path='Reports'):
    file_dir=root_dir+file_path
    print(file_dir)
    file_list=os.listdir(file_dir)
    sort_list=sorted(file_list,key=lambda f:path.getmtime(path.join(file_dir, f)),reverse=True)
    return path.join(file_dir, sort_list[0])



if __name__ == '__main__':
    print(get_newest_file())