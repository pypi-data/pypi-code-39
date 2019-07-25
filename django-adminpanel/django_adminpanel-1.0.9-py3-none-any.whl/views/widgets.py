from .autoload import *
def widgets(request):
	widget_tabs = configuration('admin_widget')
	return render(request,"adminpanel/widgets.html",{'widget_tabs':widget_tabs})

