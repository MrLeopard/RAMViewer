#coding=utf-8  
import xlsxwriter, time, os
from modules import *
      
class data_processor():
        
    def __init__(self, package):
        
        adb = adbbox()        
        self.package = package
        self.file_name = adb.deviceinfo()[1]+'_'+self.package+time.strftime("_%Y_%m_%d_%H_%M")+'.xlsx'
        
        self.workbook = xlsxwriter.Workbook(self.file_name)
        self.chart_sheet = self.workbook.add_worksheet('Chart')  
        self.data_sheet = self.workbook.add_worksheet(self.package) 
        self.bold = self.workbook.add_format({'bold': 1}) 
        
    def head_writer(self, head):        
        
        self.data_sheet.write_row('B1', head, self.bold) 
    
    def value_writer(self, row_no, ram_value):
        
        content = [time.ctime()] + ram_value        
        self.data_sheet.write_row('A%s' %row_no, content)
    
    def chart_creater(self, row_no, column_titles):
        
        stub = ['JavaHeap', 'NativeHeap', 'Code', 'Stack', 'Graphics',
                      'PrivateOther', 'System', 'TOTAL', 'TOTALSWAP(KB)']
        
        if column_titles != stub:
            print 'Warning: items of APP ram info has changed.'
        
        chart = self.workbook.add_chart({'type': 'area', 'subtype': 'stacked'})  
           
        # It's hard to understand.
        #add all data to chart except 'TOTAL' & 'TotalSWAP(KB)' 
        #With Android version upgrade,if the ram info change ,it will print a warning.
         
        numbers_of_series = len(column_titles) - 2
        
        for i in  range(numbers_of_series):
            chart.add_series({  
                'name':        '=%s!$%s$1'         %(self.package, chr(66+i)),  
                'categories':  '=%s!$A$2:$A$%s'    %(self.package, row_no-1),  
                'values':      '=%s!$%s$2:$%s$%s'  %(self.package, chr(66+i), chr(66+i), row_no-1),  
            })          

  
        chart.set_title ({'name': 'RAM trend of %s'  %self.package})  
        chart.set_x_axis({'name': 'Time'})  
        chart.set_y_axis({'name': 'RAM(KB)'})  
           
        chart.set_style(2) 
        chart.set_size({'width': 1200, 'height': 700})     
            
        self.chart_sheet.insert_chart('A1', chart) 
        
    def close(self):
        
        self.workbook.close() 
        return self.file_name
    
if __name__ == '__main__': 
    import os
    os.chdir(r'C:\\')
    data_processor.package = 'com.qiyi.video' 
    rp = data_processor()
    print rp.file_name