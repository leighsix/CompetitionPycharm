import math
from numba import vectorize, cuda
import numpy as np
from numba import guvectorize

@vectorize(['float32(float32, float32)', 'float64(float64, float64)'], target='cuda')

def gpu_sincos(x, y):
    return math.sin(x) * math.cos(y)

result = gpu_sincos(3.0, 4.0)
print(result)



@guvectorize(..., target='cuda')
def very_complex_kernel(A, B, C):
    ...

very_complex_kernel.max_blocksize = 32  # limits to 32 threads per block

