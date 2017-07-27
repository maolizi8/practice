'''
Created on 2017年7月27日

@author: geqiuli
'''
def get_info_from_txt(file_name):
    arr=[]
    with open(file_name,'r') as f:
        for line in f.readlines():
            arr.append(line.strip())
    return arr



if __name__ == '__main__':
    pass