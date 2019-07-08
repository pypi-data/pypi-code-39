import __init__ as main
from apihelper import Authentication, make_request
from exceptions import Unauthenticated

class CreateLead:
	def __init__(self):
		try:
			self.__userdata = Authentication(main.accessKey, main.secretKey, 'api.leadsquared.com')
			self._api = self.__userdata['LSQCommonServiceURLs']['api']
			self.params = {"accessKey": main.accessKey, "secretKey": main.secretKey}
			print("\033[1;92mAuthentication Details :"\
					"\n Name : "+self.__userdata["Name"]+\
					"\n Email : "+self.__userdata["PassPhrase"]+\
					"\033[00m")
		except Exception as e:
			raise Unauthenticated(e)

	def capture(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Lead.Capture"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to capture lead\
						\nException Message : "+str(e)+"\n\n\033[00m"

	def convert(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Lead.Convert"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Convert a lead\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def create(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Lead.Create"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Create a lead\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def createbulk(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Lead/Bulk/Create"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Create leads in Bulk\
						\nException Message : "+str(e)+"\033[00m\n\n"
	
	def createorupdate(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Lead.CreateOrUpdate"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to create or update a lead\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def createorupdatebulk(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Lead/Bulk/CreateOrUpdate"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to create or update leads in bulk\
						\nException Message : "+str(e)+"\033[00m\n\n"
	
	def customfield(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/CreateLeadField"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to create a Custom Lead Field\
						\nException Message : "+str(e)+"\033[00m\n\n"
	
	def leadandactivity(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/CreateCustom"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to create a lead and activity\
						\nException Message : "+str(e)+"\033[00m\n\n"
	
	def note(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/createnote"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to create a Note\
						\nException Message : "+str(e)+"\033[00m\n\n"

class RetriveLead:
	def __init__(self):
		try:
			self.__userdata = Authentication(main.accessKey, main.secretKey, 'api.leadsquared.com')
			self._api = self.__userdata['LSQCommonServiceURLs']['api']
			self.params = {"accessKey": main.accessKey, "secretKey": main.secretKey}
			print("\033[1;92mAuthentication Details :"\
					"\n Name : "+self.__userdata["Name"]+\
					"\n Email : "+self.__userdata["PassPhrase"]+\
					"\033[00m")
		except Exception as e:
			raise Unauthenticated(e)

	def metadata(self, schemaName=None):
		try:
			if schemaName is not None:
				self.params["schemaName"] = schemaName
			self.endpoint = "/v2/LeadManagement.svc/LeadsMetaData.Get"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='GET', url=self.url, params=self.params))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Get Lead Metadata\
						\nException Message : "+str(e)+"\033[00m\n\n"
	

	def leadid(self, id):
		try:
			self.params["id"] = id
			self.endpoint = "/v2/LeadManagement.svc/Leads.GetById"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='GET', url=self.url, params=self.params))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Get Lead by leadid\
						\nException Message : "+str(e)+"\033[00m\n\n"
	

	def leadidbulk(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Leads/Retrieve/ByIds"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Get Lead by bulk leadid\
						\nException Message : "+str(e)+"\033[00m\n\n"
	

	def leademail(self, emailaddress):
		try:
			self.params["emailaddress"] = emailaddress
			self.endpoint = "/v2/LeadManagement.svc/Leads.GetByEmailaddress"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='GET', url=self.url, params=self.params))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Get Lead by Email\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def leadphone(self, phone):
		try:
			self.params["phone"] = phone
			self.endpoint = "/v2/LeadManagement.svc/RetrieveLeadByPhoneNumber"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='GET', url=self.url, params=self.params))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Get Lead by Phone\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def quicksearch(self, key):
		try:
			self.params["key"] = key
			self.endpoint = "/v2/LeadManagement.svc/Leads.GetByQuickSearch"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='GET', url=self.url, params=self.params))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
		
	def criteria(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Leads.Get"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
		
	def daterange(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Leads.RecentlyModified"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def note(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/RetrieveNote"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def leadowner(self, LeadIdentifier, value):
		try:
			self.params["LeadIdentifier"] = LeadIdentifier
			self.params["value"] = value
			self.endpoint = "/v2/LeadManagement.svc/LeadOwner.Get"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='GET', url=self.url, params=self.params))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"

class UpdateLead:
	def __init__(self):
		try:
			self.__userdata = Authentication(main.accessKey, main.secretKey, 'api.leadsquared.com')
			self._api = self.__userdata['LSQCommonServiceURLs']['api']
			self.params = {"accessKey": main.accessKey, "secretKey": main.secretKey}
			print("\033[1;92mAuthentication Details :"\
					"\n Name : "+self.__userdata["Name"]+\
					"\n Email : "+self.__userdata["PassPhrase"]+\
					"\033[00m")
		except Exception as e:
			raise Unauthenticated(e)

	def leadid(self, leadid , body):
		try:
			self.params["leadid"] = leadid
			self.endpoint = "/v2/LeadManagement.svc/Lead.Update"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
		
	def leadidbulk(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/Lead/Bulk/Update"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
		
	def leadidbulk(self, masterId, childId):
		try:
			self.params["masterId"] = masterId
			self.params["childId"] = childId
			self.endpoint = "/v2/LeadManagement.svc/Lead.Merge"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
		
	def markemailinvalid(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/MarkEmailInvalid"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
		
	def markemailvalid(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/MarkEmailValid"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
		
	def note(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/UpdateNote"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
	
	def adddropdown(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/LeadField/Dropdown/Options/Push"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
				
	def removedropdown(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/LeadField/Dropdown/Options/Remove"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to quicksearch lead\
						\nException Message : "+str(e)+"\033[00m\n\n"
				
class DeleteLead:
	def __init__(self):
		try:
			self.__userdata = Authentication(main.accessKey, main.secretKey, 'api.leadsquared.com')
			self._api = self.__userdata['LSQCommonServiceURLs']['api']
			self.params = {"accessKey": main.accessKey, "secretKey": main.secretKey}
			print("\033[1;92mAuthentication Details :"\
					"\n Name : "+self.__userdata["Name"]+\
					"\n Email : "+self.__userdata["PassPhrase"]+\
					"\033[00m")
		except Exception as e:
			raise Unauthenticated(e)

	def leadid(self, leadId):
		try:
			self.params["leadId"] = leadId
			self.endpoint = "/v2/LeadManagement.svc/Lead/Delete/ById"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='GET', url=self.url, params=self.params))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Get Lead by leadid\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def stagechangehistory(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/DeleteStageChangeHistory"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Get Lead by leadid\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def ownerchangehistory(self, body):
		try:
			self.endpoint = "/v2/LeadManagement.svc/DeleteUserAssignmentChangeHistory"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='POST', url=self.url, params=self.params, data=body))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Get Lead by leadid\
						\nException Message : "+str(e)+"\033[00m\n\n"

	def note(self, prospectId, NoteId):
		try:
			self.params["prospectId"] = prospectId
			self.params["NoteId"] = noteId
			self.endpoint = "/v2/LeadManagement.svc/DeleteNote"
			self.url = 'https://'+ self._api + self.endpoint
			return (make_request(method='GET', url=self.url, params=self.params))
		except Exception as e:
			return "\n\n\033[1;91mAn Exception occoured while trying to Get Lead by leadid\
						\nException Message : "+str(e)+"\033[00m\n\n"

	