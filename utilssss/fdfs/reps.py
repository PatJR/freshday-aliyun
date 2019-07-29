import re

data = 'http://192.168.3.5:8888group1\M00/00/00/wKgDBV00bnCAZPZlAAAmv27pX4k4596892.jpg'


ret = re.sub(r'\\', r'/', data)
print(ret)
print('\\')