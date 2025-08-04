# Примеры использования стандартной библиотеки
import sys
print("Python path:", sys.path[:3])

import json
data = {"name": "Анна", "age": 25}
json_str = json.dumps(data)
print(json_str)

import datetime
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

import collections
counter = collections.Counter(['a', 'b', 'a', 'c', 'b', 'a'])
print(counter) 