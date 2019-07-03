'''
	This module fascilitates the user to avoid calling brace-remover and ncec separately (which is the case with eclipse plug-in). 
'''

import brace_remover.removeBraces as br
import ncec.main as nc
def run():
	br.remove()	#	This will remove braces.
	nc.main()		#	It will extract SDG and apply segmentation algorithm.
	
if __name__=="__main__":
	run()	
