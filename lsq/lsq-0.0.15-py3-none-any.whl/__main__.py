import sys
if sys.argv[1].lower() == 'help':
	print("\033[0;95mThank you for installing leadsquared python module.\
		\nProper Documentation on this api can be found at leadsquared apidocs\
		\nhttps://apidocs.leadsquared.com/lead-management/\
	\n\nHere are some options which are available in this \n\n\033[1;92mLead Management API\
		\n\n\033[0;94mCreateLead\t\tTop Level Class to create a lead\n\t\t\tUse lsq CreateLead -help to get more information about CreateLead\
		\n\nRetriveLead\t\tTop Level Class to Retrive a lead\n\t\t\tUse lsq RetriveLead -help to get more information about RetriveLead\
		\n\nDeleteLead\t\tTop Level Class to Delete a lead\n\t\t\tUse lsq DeleteLead -help to get more information about DeleteLead\
		\n\nUpdateLead\t\tTop Level Class to Update a lead\n\t\t\tUse lsq UpdateLead -help to get more information about UpdateLead\
		\n\nThe Module is still under development. Other API's Will be available soon\
		\033[0m")

if sys.argv[1].lower() == 'createlead':
	print("\033[0;95mProper Documentation on this api can be found at leadsquared apidocs\
		\nhttps://apidocs.leadsquared.com/lead-management/\
		\n\nAvailable Functions in this class\
		\n\n\
		\033[0m")
elif sys.argv[1].lower() == 'updatelead':
	pass
elif sys.argv[1].lower() == 'deletelead':
	pass
elif sys.argv[1].lower() == 'retrivelead':
	pass