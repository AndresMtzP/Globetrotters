import cProfile
import time
from teleportapi import *
from trottersDB import *

print "Timing started:"
time1 = time.time()
getAll('Jamaica')
time2 = time.time()
print (time2-time1)*1000.0
print "--- Timing ended ---"
'''
def timing(f):
	def wrap(*args):
		time1 = time.time()
		ret = f(*args)
		time2 = time.time()
		print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
return wrap

@timing
getAll('Jamaica')
'''