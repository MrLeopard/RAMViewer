#coding=utf8
from modules import *
import threading
from time import sleep
import sys,time

class controller():
    
    def __init__(self, package, cycle, interval):
        
        self.package = package
        self.mem = meminfo(package)        
        self.adb = adbbox()
                
        self.cycle_seconds = cycle*60*60 #total test time, [hour]
        self.interval = interval # time between every time to get ram value,[ second]
        
        self.xls = data_processor(package)          
        self.basic_head = self.mem.app_ram_item()        
        self.xls.head_writer(self.basic_head)
        self.value_row_no = 2 
        print 'Starting:',time.ctime()
        
                 
    def adb_device_watcher(self):
        
        sleep(self.cycle_seconds) 
                     
    def exerciser(self):  
              
        try:
            meminfo = self.mem.app_ram_value()
            print time.ctime(),'     TOTAL:',meminfo[7],'KB'
            self.xls.value_writer(self.value_row_no, meminfo)
            self.value_row_no += 1 
            
        except (IndexError,TypeError):
            "That's make no sense to print or get this exception,\
            but for better user experience,hide it."
            pass       
                
            
    def round_off(self): #insert chart and close workbook      
        self.xls.chart_creater(self.value_row_no, self.basic_head)
        print '\n',self.xls.close()
                            
    def commander(self):
        
        thread_watcher = threading.Thread(target = self.adb_device_watcher) 
        thread_watcher.start()
        
        while thread_watcher.isAlive() and self.adb.device():
            thread_exerciser = threading.Thread(target = self.exerciser)
            thread_exerciser.start()
            thread_exerciser.join() #It seams that timeout is useless?
            sleep(self.interval - 0.8) #because 1 round need 'almost' 1 second 
#             print datetime.datetime.now().second + float(datetime.datetime.now().microsecond) / 1000000
                       
        self.round_off()        
        print 'Finished: ',time.ctime()
        os._exit(0)       
                 

            
if __name__ == "__main__":
    os.chdir(r'F:\\ram_view')
    ctr = controller('com.qiyi.video', 24, 5)
    ctr.commander()    