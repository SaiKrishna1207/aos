import aos
import os
import numpy as np
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

def infer(x, d):
    aos_op = ""
    if isinstance(x, int):
        if(d == 0):
            return "int"
        else:
            return x
    elif isinstance(x, str):
        if(d == 0):
            return "str"
        else:
            return x
    elif isinstance(x, float):
        if(d == 0):
            return "float"    
        else:
            return x

    elif isinstance(x, tuple):
        aos_op += "("
        for i in x:
            aos_op += infer(i, 0)
            aos_op += "|"
        aos_op = aos_op[:-1]
        aos_op += ")"
    
    elif isinstance(x, list):
        aos_op += "("
        for i in x:
            aos_op += infer(i, 0)
            aos_op += "|"
        aos_op = aos_op[:-1]
        aos_op += ")"

    elif isinstance(x, dict):
        aos_op += "("
        for i in x.items():
            aos_op += "(" + infer(i[0], 1) + "&" + infer(i[1], 0) + ")"
            aos_op += "|"
        aos_op = aos_op[:-1]
        aos_op += ")"

    return aos_op

def validate(x, d1):
    if(x == d1):
        print("True")
    else:
        print("False")


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
    x = "((checked&int)|(dimensions&((width&int)|(height&int)))|(id&int)|(name&str)|(price&float)|(tags&(str|str)))"
    print(infer(d1, 0))
    validate(x, infer(d2, 0))
