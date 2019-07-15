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

	text = 	getText().decode('utf-8')

	text = ',\r\n'.join([':'.join(map(repr,map(lambda x:x.strip(),line.split(':',1)))) for line in text.split('\r\n')])

	print(text)

	setText(text.encode('utf-8'))

