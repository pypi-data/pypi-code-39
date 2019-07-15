import win32con
import win32clipboard as w
def HeadersFormatter():
	def getText():
		w.OpenClipboard()
		d = w.GetClipboardData(win32con.CF_TEXT)
		w.CloseClipboard()
		return d
	 
	def setText(aString):
		w.OpenClipboard()
		w.EmptyClipboard()
		w.SetClipboardData(win32con.CF_TEXT, aString)
		w.CloseClipboard()

	try: 
		text = 	getText().decode('utf-8')
	except:
		print('读取剪贴板失败')
		return 1

	if ':' not in text:
		print('未在剪贴板中找到Headers')
		return 2
        
	text = ',\r\n'.join([':'.join(map(repr,map(lambda x:x.strip(),line.split(':',1)))) for line in text.split('\r\n')])

	print('格式化结果如下：')
	print(text)

	try:
		setText(text.encode('utf-8'))
	except:
		print('剪贴板写入失败')
		return 3
	
	return 0

