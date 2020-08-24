import aos
import os
import numpy as np
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

def infer(x):
    aos_op = ""
    if isinstance(x, int):
        return "int"
    elif isinstance(x, str):
        return "str"
    elif isinstance(x, float):
        return "float"    

    elif isinstance(x, tuple):
        aos_op += "("
        for i in x:
            aos_op += infer(i)
            aos_op += "|"
        aos_op = aos_op[:-1]
        aos_op += ")"
    
    elif isinstance(x, list):
        aos_op += "("
        for i in x:
            aos_op += infer(i)
            aos_op += "|"
        aos_op = aos_op[:-1]
        aos_op += ")"

    elif isinstance(x, dict):
        aos_op += "("
        for i in x.items():
            aos_op += "(" + infer(i[0]) + "&" + infer(i[1]) + ")"
            aos_op += "|"
        aos_op = aos_op[:-1]
        aos_op += ")"

    return aos_op

if __name__ == "__main__":
    d1 = {
        'a': [
            { 
            'x': 1, 'y': 2
            },
            {
            'x': 3, 'y': 4
            },
            {
            'x': 5, 'y': 6
            }
        ]
    }

    d2 = {
        "checked": False,
        "dimensions": {
            "width": 5,
            "height": 10
        },
        "id": 1,
        "name": "A green door",
        "price": 12.5,
        "tags": [
            "home",
            "green"
        ]
    }

    print(infer(d1))
# ((str&(((str&int)|(str&int))|((str&int)|(str&int))|((str&int)|(str&int)))))
    print(infer(d2))
# ((str&int)|(str&((str&int)|(str&int)))|(str&int)|(str&str)|(str&)|(str&(str|str)))



