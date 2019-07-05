from distutils.core import setup 
setup ( 
name='HQChart',     # 这个是最终打包的文件名 
version='1.0.6', 
author='jones2000',
url='https://github.com/jones2000/HQChart',
install_requires=['requests'],
#打包.py文件， 
py_modules=[  
    '__init__',              
    'umychart_complier_data',
    'umychart_complier_help',
    'umychart_complier_job',
    'umychart_complier_jsalgorithm',
    'umychart_complier_jscomplier',
    'umychart_complier_jsexecute',
    'umychart_complier_jsparser',
    'umychart_complier_jssymboldata',
    'umychart_complier_scanner',
    'umychart_complier_testcase',
    'umychart_complier_util'
    ], 
license='MIT',
)