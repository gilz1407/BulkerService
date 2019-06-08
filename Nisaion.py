import os
import sys

sys.path.append(os.path.abspath('../CrossInfra'))
from RedisManager import connect


r=connect()
data = r.lpop('TemplateList')
print(str(data))