#coding=utf8

from modules import *
import sys
import argparse

parser = argparse.ArgumentParser()  
  
parser.add_argument(type = str, nargs = 1,  dest = 'package', \
                    help = 'the package name, like com.android.phone.')

parser.add_argument('-cycle' , '-c', type = float, nargs = 1, 
                    default = [12], dest = 'cycle', help = \
                    'total time,default is 12 hours, must > 0.1 and < 720')
 
parser.add_argument('-interval','-i', type = float, nargs = 1, \
                    default = [15], dest = 'interval', help = \
                    'start to test,default is 15 seconds. must >= 5.')

parser.add_argument('-version','-v', action = 'version', \
                    version = '%s' %version)
              
# parameter = parser.parse_args(['com.qiyi.video','-c','12','-i','15'])
parameter = parser.parse_args()

# print parameter
 
package =  parameter.package[0]
cycle = parameter.cycle[0]
interval = parameter.interval[0]
 
if cycle < 0.1 or cycle > 720:
    print 'cycle out of range'
    sys.exit()
     
if interval < 5:
    print 'interval too short.'
    sys.exit()        
    
ctr = controller(package, cycle, interval)
ctr.commander()
