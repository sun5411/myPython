#!/usr/bin/env python
import re

str = '123&&sdfsfdsdfsf;123s9d9fsdf12315677a1'

number_list = re.findall(r"\d+",str)
string_list = re.findall(r"[a-z]+",str)

### 字符串排序
max_num = sorted(number_list,key=lambda x: len(x))[-1]
max_str = sorted(string_list,key=lambda x: len(x))[-1]
print max_num,max_str

