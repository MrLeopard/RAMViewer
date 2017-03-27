#coding=utf8
from subprocess import Popen, PIPE, STDOUT, call
import re,sys

class adbbox():
    '''
    rules: 
    adb version ,@Function __init__
    
    adb devices ,@Function devices,
                2 lines 0 device, 3 lines 1 devices over 4 lines 2 or 
                more devices.
                when output 2 lines,device/offline/unauthorized 
                as key words.
                
    adb devices -l,@Function deviceinfo
                use re module to filte deivice info,output like below:    
    1019351a      device product:E76mini model:Hisense_E76mini device:HS8937QC
    
    '''
    error_code = \
    {
        'AE01':'Error:\n\tadb.exe not found.',\
        'AE02':'Error:\n\tno device found.',\
        'AE03':'Error:\n\tdevice unauthorized',\
        'AE04':'Error:\n\tdevice offline',\
        'AE05':'Error:\n\ttwo or more device.',\
        'AE06':'Error:\n\tunknow error',\
        'AE07':"Error:ADB server didn't ACK",\
    }
    count = 0
    def __init__(self):
        
        adbbox.count += 1
        
        if adbbox.count == 1:
            _text = self.returnlines('adb version')[0]
            _result = re.findall('version', _text)
            
            if bool(_result):
                print _text,
                call('adb devices -l', stdout = PIPE)  
            else:
                print self.error_code['AE01']
                sys.exit()
                
            device_info = self.device()
            
            if bool(device_info):
                print 'Device: {%s} connected .\n' %device_info[1]
            else:
                print 'Check you adb device.Test has stoped.'  
                sys.exit() 
                             
        else:pass 
              
    def wait_for_device(self):
        call('adb wait-for-device')
                
    def get_output(self, command):
        file_out = Popen(command, shell = True, stdout = PIPE, stderr = STDOUT)        
        return file_out
            
    def returnlines(self, command):
        '''return a list when command executed'''
        list_text=self.get_output(command).stdout.readlines()        
        return list_text
    
    def returnread(self, command):
        '''return a string when command executed'''
        text = self.get_output(command).stdout.read()        
        return text
    
    def deviceinfo(self):
        
        _text = self.returnlines('adb devices -l')      
        _serial_no =_text[1].split(' ')[0]
        _device_name = re.findall(r'model:(.+?) device', _text[1])[0]        
        return _serial_no, _device_name
        
    def device(self):
        _text = self.returnlines('adb devices')
        _len = len(_text)
        
        if  _len == 2:
            error_code = self.error_code['AE02']    
             
        elif _len == 3:
            if 'unauthorized' in _text[1]:
                error_code = self.error_code['AE03']
                
            elif 'offline' in _text[1]:
                error_code = self.error_code['AE04']
                
            elif 'device' in _text[1]:
                return self.deviceinfo()            
            else:
                error_code = self.error_code['AE06']                 
                
        elif _len >= 4:
            if _len == 5:
                for i in _text:
                    if "ADB server didn't ACK" in i:
                        error_code = self.error_code['AE07']
                        if adbbox.count > 2:
                            print 'adb is blocking,wait 30 seconds.'
                            import time
                            time.sleep(30)
                    else:
                        error_code = self.error_code['AE05']                         
            else:    
                error_code = self.error_code['AE05']              
        else:
            error_code = self.error_code['AE06']
            
        if adbbox.count == 1:
            print error_code
                    
if __name__ == '__main__':
    adb = adbbox()
    df = adb.device()
    if df != None:
        print df[0],df[1]
    else:
        print 'no device'