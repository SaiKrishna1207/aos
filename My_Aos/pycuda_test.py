import aos
import os
import numpy as np
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

def cuda_square():
    mod = SourceModule("""
    __global__ void cuda_sqr(float *dest, float* a){
        const int i = threadIdx.x;
        dest[i] = a[i] * a[i];
    }
     """)
    cuda_sq = mod.get_function("cuda_sqr")
    inp = np.ones(400, dtype=np.float32)
    for i in range(0, 400):
        inp[i] = i
    ans = np.zeros_like(inp)
    cuda_sq(drv.Out(ans), drv.In(inp), block = (400, 1, 1), grid = (1, 1))
    print(ans)

if __name__ == "__main__":
    cuda_square()