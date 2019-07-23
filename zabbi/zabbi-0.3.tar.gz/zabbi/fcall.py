import sys
import json

def func(self,attr,*args, **kwargs):

	out=self.parent.do_request(
                '{0}.{1}'.format(self.name, attr),
                args or kwargs
            )['result']


	if((kwargs.get("host") is not None) and self.name == "host"):
			host=self.parent.do_request(
                                '{0}.{1}'.format(self.name, "get"),
                                args or kwargs
                                )['result']

			hostin=self.parent.do_request(
                                '{0}.{1}'.format("hostinterface", "get"),
                                )['result']

			hj = []
			for h in host:
				for hip in hostin:
					if( h["host"] == kwargs.get("host") and h['hostid']==hip['hostid']):
						h.update(hip)
						hj.append(h)
			return hj

	if(self.name == "host"):
			host=self.parent.do_request(
                		'{0}.{1}'.format(self.name, "get"),
                		args or kwargs
            			)['result']

			hostin=self.parent.do_request(
                                '{0}.{1}'.format("hostinterface", "get"),
                                args or kwargs
                                )['result']
			
			hj = []
			for h in host:
				for hip in hostin:
					if( h["hostid"] == hip["hostid"]):
						h.update(hip)
						hj.append(h)
			return hj


	if((kwargs.get("ip") is not None) and self.name == "hostinterface"):
		host=self.parent.do_request(
                                '{0}.{1}'.format("host", "get"),
                                )['result']

		hostin=self.parent.do_request(
                                '{0}.{1}'.format("hostinterface", "get"),
                                args or kwargs
                                )['result']

		hj = []
		for hip in hostin:
			for h in host:
				if( hip['ip']==kwargs.get("ip") and hip['hostid']==h['hostid']):	
					h.update(hip)
					hj.append(h)
		return hj		

	if(self.name == "hostinterface"):
		host=self.parent.do_request(
                                '{0}.{1}'.format(self.name, "get"),
                                args or kwargs
                                )['result']

		hostin=self.parent.do_request(
                                '{0}.{1}'.format("hostinterface", "get"),
                                args or kwargs
                                )['result']

		hj = []
		for hip in hostin:
			for h in host:
				if( h["hostid"] == hip["hostid"]):
					hip.update(h)
					hj.append(hip)
		return hj

