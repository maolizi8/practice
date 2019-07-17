# coding:utf-8
'''
    库版本：
        Python  3.7.0
        opencv+contrib  3.4.2
        numpy   1.16.3
'''
import sys
import os
import time
#from cv2 import cv2
import cv2
from six import PY3
import numpy as np


# SIFT识别特征点匹配，参数设置:
FLANN_INDEX_KDTREE = 0
FLANN = cv2.FlannBasedMatcher({'algorithm': FLANN_INDEX_KDTREE, 'trees': 5}, dict(checks=50))
# SIFT参数: FILTER_RATIO为SIFT优秀特征点过滤比例值(0-1范围，建议值0.4-0.6)
FILTER_RATIO = 0.6
# SIFT参数: SIFT识别时只找出一对相似特征点时的置信度(confidence)
ONE_POINT_CONFI = 0.5
# 图像相似阈值
THRESHOLD = 0.95

def cal_rgb_confidence(img_src_rgb, img_sch_rgb):
    '''同大小彩图计算相似度.'''
    # BGR三通道心理学权重:
    weight = (0.114, 0.587, 0.299)
    src_bgr, sch_bgr = cv2.split(img_src_rgb), cv2.split(img_sch_rgb)

    # 计算BGR三通道的confidence，存入bgr_confidence:
    bgr_confidence = [0, 0, 0]
    for i in range(3):
        res_temp = cv2.matchTemplate(src_bgr[i], sch_bgr[i], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_temp)
        bgr_confidence[i] = max_val

    # 加权可信度
    weighted_confidence = bgr_confidence[0] * weight[0] + bgr_confidence[1] * weight[1] + bgr_confidence[2] * weight[2]
    return weighted_confidence

def find_sift(img_source,img_search,ratio=FILTER_RATIO):
    '''基于sift进行图像识别'''
    #检测图片是否正常
    if not check_image_valid(img_source,img_search):
        raise Exception(img_source,img_search,"空图像")
    #获取特征点集，匹配特征
    kp1, kp2, matches = _get_key_points(img_source, img_search, ratio)
    #关键点匹配数量，匹配掩码
    (matchNum,matchesMask)=getMatchNum(matches,ratio)
    #关键点匹配置信度
    matcheRatio = matchNum/len(matchesMask)
    if matcheRatio >= 0 and matcheRatio <=1:
        return matcheRatio 
    else:
        raise Exception("SIFT Score Error",matcheRatio)

def _init_sift():
    '''Make sure that there is SIFT module in OpenCV.'''
    if cv2.__version__.startswith("3."):
        # OpenCV3.x, sift is in contrib module, you need to compile it seperately.
        try:
            sift = cv2.xfeatures2d.SIFT_create(edgeThreshold=10)
        except:
            print("to use SIFT, you should build contrib with opencv3.0")
            raise Exception("There is no SIFT module in your OpenCV environment !")
    else:
        # OpenCV2.x, just use it.
        sift = cv2.SIFT(edgeThreshold=10)   #对于3.4.2.16版本的，请忽略此处报错

    return sift

def _get_key_points(im_source, im_search, ratio):
    ''' 根据传入图像，计算所有的特征点并匹配特征点对 '''
    #初始化sift算子
    sift = _init_sift()
    # 获取特征点集
    kp_sch, des_sch = sift.detectAndCompute(im_search, None)
    kp_src, des_src = sift.detectAndCompute(im_source, None)
    # When apply knnmatch , make sure that number of features in both test and
    #       query image is greater than or equal to number of nearest neighbors in knn match.
    if len(kp_sch) < 2 or len(kp_src) < 2:
        raise Exception("Not enough feature points in input images !")
    
    # 匹配两个图片中的特征点集，k=2表示每个特征点取出2个最匹配的对应点:
    matches = FLANN.knnMatch(des_sch, des_src, k=2)
    return kp_sch, kp_src, matches

def check_image_valid(im_source, im_search):
    '''Check if the input images valid or not.'''
    if im_source is not None and im_source.any() and im_search is not None and im_search.any():
        return True
    else:
        return False

def imread(filename):
    '''根据图片路径，将图片读取为cv2的图片处理格式.'''
    if not os.path.isfile(filename):
        raise Exception("File not exist: " ,filename)
    if PY3:
        img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    else:
        filename = filename.encode(sys.getfilesystemencoding())
        img = cv2.imread(filename, 1)
    return img

def getMatchNum(matches,ratio):
    '''返回特征点匹配数量和匹配掩码'''
    matchesMask=[[0,0] for i in range(len(matches))]
    matchNum=0
    for i,(m,n) in enumerate(matches):
        #将距离比率小于ratio的匹配点删选出来
        if m.distance<ratio*n.distance: 
            matchesMask[i]=[1,0]
            matchNum+=1
    return (matchNum,matchesMask)

def resize_image(image,size):
    ''' 
    裁剪图像    
        image:图片路径
        size：裁剪尺寸
    '''
    img= imread(image)  #读取图像
    if img is None or not img.any():
        raise Exception("空图像",image)
    shape = img.shape   #图像尺寸,通道
    print('image shape: ',shape)
    if len(set(size)) == 1:
        raise Exception("Size can't be same",size)
    if size[0] >= size[1] or size[2] >= size[3]:
        #图像重置尺寸是否合理
        raise Exception("y1 应大于 y0 ，x1 应大于 x0",size)
    for i in size:  #参数合法检查
        if i < 0.0 or i > 1.0:
            raise Exception("Size shoud be 0~1",i,size)
    print('int(size[0]*shape[0]): ',int(size[0]*shape[0]))
    print('int(size[1]*shape[0]): ',int(size[1]*shape[0]))
    print('int(size[2]*shape[1]): ',int(size[2]*shape[1]))
    print('int(size[3]*shape[1]): ',int(size[3]*shape[1]))
    image = img[int(size[0]*shape[0]):int(size[1]*shape[0]), int(size[2]*shape[1]):int(size[3]*shape[1])]    #裁剪图像
    return image

def image_compare(img_source, img_search, size=[0,0,0,0]):
    '''
    传入对比图像判别相似度
        img_source:样本图像
        img_search:查询图像
        size:图像裁剪尺寸 #[y0,y1,x0,x1] 相对坐标，取值区间[0~1]
    '''
    if size!=[0,0,0,0]:
        img_source = resize_image(img_source,size)
        img_search = resize_image(img_search,size)
    else :
        img_source = imread(img_source)
        img_search = imread(img_search)
        check_image_valid(img_source,img_search)
    threshold = find_sift(img_source,img_search)
    resize_img = cv2.resize(img_search, (img_source.shape[1], img_source.shape[0]))
    threshold_conf = cal_rgb_confidence(resize_img,img_source)  #基于特征匹配的阈值
    threshold_conf=(threshold_conf+1)/2     #置信度需要放水
    result=threshold,threshold_conf, threshold_conf > THRESHOLD and threshold > THRESHOLD
    print('result: ',result)
    return result

if __name__=='__main__':
    img_source=r'E:\test1.png'
    img_search=r'E:\test2.png'
    image_compare(img_source, img_search, size=[0.2,0.9,0.2,0.9])

