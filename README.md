# python+selenium 自动化测试练习

## 环境搭建
> ##### 安装Python，此处使用python2.7.13
> * 配置环境变量
> * 安装pip
> * 安装依赖包，pip install selenium
> * 等等

## 练习网站


## 自动化测试脚本
def finddevices():
    rst = util.exccmd('adb devices')
    devices = re.findall(r'(.*?)\s+device',rst)
    if len(devices) > 1:
        deviceIds = devices[1:]
        logger.info('共找到%s个手机'%str(len(devices)-1))
        for i in deviceIds:            
            logger.info('ID为%s'%i)
        return deviceIds
    else:
        logger.error('没有找到手机，请检查')
        return
