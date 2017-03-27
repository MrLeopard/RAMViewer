#coding=utf8

# from time import ctime
# print ctime()

from modules import adbbox
from time import sleep
import re,sys

class meminfo():  
      
    list_package_command = 'adb shell pm list package '        
    filter = re.compile('(Java Heap.*)Objects', re.S) 
    count = 0
    
    def __init__(self,package):
        
        meminfo.count += 1
        self.adb = adbbox()
        self.package = package
        
        if not self.package_exist():
            sys.exit()
            
        if meminfo.count == 1 and self.Is_app_running() == False:
            print "{%s} not running.Don't forget it. " %self.package
            self.wait_for_app()
            
    def package_exist(self):
        _return = self.adb.returnlines(self.list_package_command)
        for i in _return:
            i = i.replace('package:', '').replace('\r', '').replace('\n', '')
            if self.package == i:
                return True            
        print 'Package: {%s} not exist!' %self.package
        
    def get_meminfo(self):
        
        meminfo_command = 'adb shell dumpsys meminfo ' + self.package
        _return = self.adb.returnread(meminfo_command)
        return _return
    
    def Is_app_running(self):
        
        _return = self.get_meminfo()
        
        if "Uptime" in _return:
            return _return
        else:
            return False
         
    def wait_for_app(self):
        
        while not self.Is_app_running():
#             print '....wait_for_app()'
            sleep(1)
            
    def app_meminfo_preocessor(self):                
        ram_item, ram_value  = [], []
        _return = self.Is_app_running()
        
        if _return == False:
            if not self.adb.device():
                print 'Device disconnected.'
                return                
            else:
                print 'waiting for app running again..'
                self.wait_for_app()
                _return = self.Is_app_running()
                          
        _text = self.filter.findall(_return)[0]        
        _meminfo_list = _text.replace(r' ', '').replace('TOTAL', '\nTOTAL').\
                         replace('\n\n', '\n').replace('\r', '').split('\n') 
                                
        while '' in _meminfo_list:
            _meminfo_list.remove('')
         
        for i in _meminfo_list:
            ram_item.append(i.split(':')[0])
            ram_value.append(i.split(':')[1])
              
        meminfo={'ram_item': ram_item,'ram_value': ram_value}
        
        return meminfo
    
    def app_ram_item(self):
        
        return self.app_meminfo_preocessor()['ram_item']   
    
    def app_ram_value(self):
        
        _return = self.app_meminfo_preocessor()['ram_value']
        app_ram_value = []
        
        for i in _return:
            app_ram_value.append(int(i))
            
        return app_ram_value  
    
if __name__ == '__main__':
    mem = meminfo('com.qiyi.video')
    for i in mem.app_ram_item():
        print i + '\t\t',
    print '\n'    
    for i in range(10):
        for i in mem.app_ram_value():
            print str(i) + '\t\t\t',
        print '\n'
        sleep(1)
