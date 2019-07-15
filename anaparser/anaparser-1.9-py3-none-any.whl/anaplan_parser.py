
# coding: utf-8

# In[24]:


import pandas as pd
import numpy as np
import xlrd
import csv
import os



#%%
def csv_from_excel(input_file, output_file):

    wb = xlrd.open_workbook(input_file)
    sh = wb.sheet_by_name('Sheet 1')
    your_csv_file = open(output_file, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()




# In[25]:






# In[26]:



    



# In[27]:


#Проверить наличие Applies To


# In[28]:


#Проверить формат item
def check_format(string):
    if type(string) == float:
            return False
    elif len(string) < 10:
        return 'NONE'
        
    elif string.split(':')[-1].find('ENTITY') == 1:
        return 'someth'
    
    elif string.split(':')[-1].find('NUMBER') == 1:
        return 'NUMBER'
    
    elif string.split(':')[-1].find('NONE') == 1:
        return 'NONE'

    else:
        return 'someth'


# In[29]:


#Проверить на тип расчетной характеристики
def check_referenced(string):
    #print(string)
    if type(string) == float:
        return 'Interm'
    else:
        if string.find('М60.01 CONS')!= -1:
            return 'Final'
        else:
            return 'Interm'


# In[30]:


#Проверить на тип item
def check_formula(string):
    if type(string) == float:
        return 'intro'
    else:
        return 'calc'


# In[31]:


def check_time(string):
    if string.find('Not Applicable') == -1:
        return 'Time'
    else:
        return ''


# In[32]:


def check_version(string):
    if string.find('Not Applicable')== -1:
        return 'Versions'
    else:
        return ''


# In[33]:


ex = "'М60.01 CONS'.'# Изменения ОНА, Расходы (без НДС), руб.', 'М60.01 CONS'.'# Текущий налог на прибыль, Расходы (без НДС), руб.', 'M80.03 Проверка расходов в CONS и источниках'.Расходы из источников"


# In[34]:


def unique(list1): 
    list_set = set(list1) 
    return (list(list_set)) 
    
def find_all_substrings(string):
    base = 'М60.01 CONS'
    a = 0
    b = len(ex)
    poses = []
    while a < (b - len(base)):
        pos = string.find(base, a, b)
        if pos != -1:
            poses.append(pos)
        a += 1
    poses = unique(poses)
    for pos in poses:
        print(pos)
        


# In[35]:


#Найти к каким CONS ведет финальный показатель
def find_conses(string, cons):
   # print(string[23], '\n')
    conses = []
    string = string[23]
    for elem in cons['Unnamed: 0']:
        if (string.find(elem)!= -1) and (elem != 'М60.01 CONS'):
            conses.append(elem)
    return conses


# In[36]:


all_essences = np.array(['Расходы без НДС в руб.',  
                         'Потребность с НДС, руб.', 'Потребность (без НДС) в руб.', 
                         'Ввод в эксплуатацию, руб.', 'Платежи с НДС, руб.', 
                        'НДС по закупкам, руб.',
                         'НДС с авансов, руб.'])


# In[37]:


#для поиска сущностей CONS
def find_essences(string):
    out = ''
    if type(string) == float:
        return '-'
    else:
        for ess in all_essences:
            if string.find(ess) != -1:
                out = out + ess + ' '

    return out
        


# In[38]:


def cons_staff(string, cons):
    #print(type(string))
    conses = find_conses(string, cons)
    Apto = []
    Essencies = []
    for item in conses:
        #это Referenced By в CONS
        refby = cons[cons['Unnamed: 0'] == item]['Referenced By'].item()
        #это Applies To в CONS
        apto = cons[cons['Unnamed: 0'] == item]['Applies To'].item()
        
        essencies = find_essences(refby).replace('-', '')
        #print(essencies)
        
        Essencies.append(essencies)
        if apto != '-':
            Apto.append(apto)   
    return [x for x in Essencies if len(x)>0], Apto



# In[39]:


#Основная часть алгоритма:
    
class file_parser:
    """
    Класс для обработки файлов из Анаплан.
    При создании объекта этого класса по желанию можно задать:
        Input_path = "тут может быть путь к обрабатываемому файлу"
        Output_path = "тут может быть путь, по которому будет сохранен результат обработки"
    В ином случае взятие и сохранение будут производиться в текущей директории (если это возможно).
    """
    
    def __init__(self, dict_name, **args):
    
        
        if 'Input_path' in args:
            self.Input_path = args['Input_path']
        else:
            self.Input_path = -1
            
        if 'Output_path' in args:
            self.Output_path = args['Output_path']
        else: 
            self.Output_path = -1
         
        
            
            
        self.cons = pd.read_csv(dict_name, sep = ';')
            
    def parse_file(self, fname):
     """
     Функция парсинга файлов Анаплан. Принимает имя файла (csv или xls). 
     Создает по выбранному ранее адресу три файла: 1.Входные данные, 2.Итоговые показатели, 3.Промежуточные показатели.
     
     """
     cons = self.cons
     
     if fname.endswith('.xls') or fname.endswith('.csv'):
        self.fname = fname
     else:
        raise Exception('Это не Excel или csv файл, давайте другой.')
        
     fname = self.fname
     
     origin = ''
     fname_csv = fname
     separator  = ';'
     base_name = ''
     
      #Если это НЕ csv файл 
      
     if fname.find('csv') == -1:
         
         base_name = fname.replace('.xls', '')
         #fname_csv = '/Users/deniszagorodnev/Desktop/anaplan_parse/' + fname
        # fname_csv = fname_csv.replace('xls', 'csv')
         if self.Input_path != -1:
             fname = self.Input_path + fname
         #separator = ','
         origin = pd.read_excel(fname, header = 0)
         
         
      #Если это csv файл   
     if fname.find('csv') != -1:
         if self.Input_path != -1:
             fname = self.Input_path + fname
         origin = pd.read_csv(fname_csv, sep = separator)
         base_name = fname.replace('.csv', '')
         
     base_module_dimension = ''
     
     if type(origin['Applies To'][0]) != float:
       base_module_dimension = origin['Applies To'][0]
     else:
        None
        
     def check_dimension(string):
        if type(string) == float:
            return '' 
        else:
            if string == '-':
                return base_module_dimension
            else:
                return string
      
     Intro_data = []
     insert_module_name = []
     insert_input_data = []
     insert_cutup = []
    
     Interm_data = []
     Interm_marker = []
     Interm_module_name = []
    
    
     Final_data = []
     Final_marker = []
     Final_module_name = []
     Final_applies = []
     Final_essence = []
    
     for raw in origin.values:
        #Формула есть?
        if check_formula(raw[1]) == 'intro':
            #если показатель вводный
            if check_format(raw[4]) == 'NUMBER' or check_format(raw[4]) == 'someth':
                #если это item, а не подзаголовок
                insert_module_name.append(base_name)
                insert_input_data.append(raw[0])
                insert_cutup.append(check_time(raw[6]) + ' ' + check_version(raw[8]) + ' '+ check_dimension(raw[5]))
    
            else:
                #Строка таблицы оказалась пустой
                None
        else:
            #если показатель расчетный
            
            if check_referenced(raw[23]) == 'Interm':
                #Показатель промежуточный
                Interm_marker.append(raw[0])
                Interm_module_name.append(base_name)
            
            else:
    
                #Показатель финальный
                #print(raw[23], '/n')
                if check_format(raw[4]) == 'someth':
                    #если формат айтема не числовой, а какой-то - это все равно промежуточный показатель
                    Interm_marker.append(raw[0])
                    Interm_module_name.append(base_name)
                else:
                    Final_marker.append(raw[0])
                    Final_module_name.append(base_name)
                    essencies, apto = cons_staff(raw, cons)
                    Final_applies.append(str(list(set(apto))).strip("[]"))
                    Final_essence.append(str(essencies).strip("[]"))
    
     if self.Output_path != -1:
         
        
         Intro_data = pd.DataFrame({'Module': insert_module_name,'Input data': insert_input_data,'Cutup': insert_cutup})
         Intro_data.to_excel(self.Output_path + "Вводные_данные.xlsx")
         
         Final_data = pd.DataFrame({'Рассчетный показатель': Final_marker,
                                    'Модуль': Final_module_name,'Подмножество CONS': Final_applies,
                                    'Сущность CONS': Final_essence})
         Final_data.to_excel(self.Output_path + "Итоговые_показатели.xlsx")
        
         Interm_data = pd.DataFrame({'Рассчетный показатель': Interm_marker, 'Модуль': Interm_module_name})
         Interm_data.to_excel(self.Output_path + "Промежуточные_показатели.xlsx")
         
     else:
         Intro_data = pd.DataFrame({'Module': insert_module_name,'Input data': insert_input_data,'Cutup': insert_cutup})
         Intro_data.to_excel("Вводные_данные.xlsx")
         
         Final_data = pd.DataFrame({'Рассчетный показатель': Final_marker,
                                    'Модуль': Final_module_name,'Подмножество CONS': Final_applies,
                                    'Сущность CONS': Final_essence})
         Final_data.to_excel("Итоговые_показатели")
        
         Interm_data = pd.DataFrame({'Рассчетный показатель': Interm_marker, 'Модуль': Interm_module_name})
         Interm_data.to_excel("Промежуточные_показатели.xlsx")

#%% 
class cons_parser(file_parser):
    def __init__(self, **args):
            
            if 'Input_path' in args:
                self.Input_path = args['Input_path']
            else:
                self.Input_path = -1
                
            if 'Output_path' in args:
                self.Output_path = args['Output_path']
            else: 
                self.Output_path = -1                
    

    def parse_file(self, fname):
     if fname.endswith('.xls') or fname.endswith('.csv'):
        self.fname = fname
     else:
        raise Exception('Это не Excel или csv файл, давайте другой.')
        
     fname = self.fname
     
     origin = ''
     fname_csv = fname
     separator  = ';'
     base_name = ''
     
      #Если это НЕ csv файл 
      
     if fname.find('csv') == -1:
         
         base_name = fname.replace('.xls', '')
         #fname_csv = '/Users/deniszagorodnev/Desktop/anaplan_parse/' + fname
        # fname_csv = fname_csv.replace('xls', 'csv')
         if self.Input_path != -1:
             fname = self.Input_path + fname
         #separator = ','
         origin = pd.read_excel(fname, header = 0)
         
         
      #Если это csv файл   
     if fname.find('csv') != -1:
         if self.Input_path != -1:
             fname = self.Input_path + fname
         origin = pd.read_csv(fname_csv, sep = separator)
         base_name = fname.replace('.csv', '')
         
     base_module_dimension = ''
     
     if type(origin['Applies To'][0]) != float:
       base_module_dimension = origin['Applies To'][0]
     else:
        None
        
     def check_dimension(string):
        if type(string) == float:
            return '' 
        else:
            if string == '-':
                return base_module_dimension
            else:
                return string
            
     Item_name = []
     Item_formula = []
     Applies_to = []
     Comment = []
     
     for raw in origin.values:
         if check_formula(raw[1]) == 'intro' and check_format(raw[4]) == 'NONE':
             Item_name.append(raw[0])
             Item_formula.append('')
             Applies_to.append('')
             Comment.append('Подзаголовок!')
             
         elif check_formula(raw[1]) == 'intro' and check_format(raw[4]) != 'NONE':
              Item_name.append(raw[0])
              Item_formula.append('')
              Applies_to.append(check_time(raw[6]) + ' ' + check_version(raw[8]) + ' '+ check_dimension(raw[5]))
              Comment.append('')
              
         elif check_formula(raw[1]) != 'intro':
             Item_name.append(raw[0])
             Item_formula.append(raw[1])
             Applies_to.append(check_time(raw[6]) + ' ' + check_version(raw[8]) + ' '+ check_dimension(raw[5]))
             Comment.append('')
             
        
         
     
     if self.Output_path != -1:
         
        
         Intro_data = pd.DataFrame({'Item': Item_name,'Cut up': Applies_to, 'Formula': Item_formula, 'Comment': Comment})
         Intro_data.to_excel(self.Output_path + "CONS.xlsx")
         
         
         
     else:
         Intro_data = pd.DataFrame({'Item': Item_name,'Cut up': Applies_to, 'Formula': Item_formula, 'Comment': Comment})
         Intro_data.to_excel("CONS.xlsx")
         
            
            
            
            
            