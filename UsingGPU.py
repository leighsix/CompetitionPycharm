import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy

cuda.init()
print("%d device(s) found." % cuda.Device.count())

for ordinal in range(cuda.Device.count()):
    dev = cuda.Device(ordinal)
    print("Device #%d: %s" % (ordinal, dev.name()))
    print(" Compute Capability: %d.%d" % dev.compute_capability())
    print(" Total Memory: %s KB" % (dev.total_memory() // (1024)))

a = numpy.random.randn(5,5)
a = a.astype(numpy.float32)
a_gpu = cuda.mem_alloc(a.nbytes)
cuda.memcpy_htod(a_gpu, a)
mod = SourceModule("""
__global__ void doubleMatrix(float *a)
{
int idx = threadIdx.x + threadIdx.y*4;
a[idx] *= 2;
}
""")
func = mod.get_function("doubleMatrix")
func(a_gpu, block=(5,5,1))
a_doubled = numpy.empty_like(a)
cuda.memcpy_dtoh(a_doubled, a_gpu)
print("ORIGINAL MATRIX")
print(a)
print("DOUBLED MATRIX AFTER PyCUDA EXECUTION")
print(a_doubled)