# Track which plots are active, which to draw in. 
# Derek Fujimoto
# June 2019

import matplotlib.pyplot as plt

# =========================================================================== #
class PltTracker(object):
    """
        active:         id number of active plot {data:0,fitting:0,param:0}
        bfit:           main object 
        plots:          dictionary for plots drawn {data:[],fitting:[],param:[]}
    """
    
    # ======================================================================= #
    def __init__(self,parent):
        """
            Parent: pointer to bfit object
        """
        self.bfit = parent
        
        # lists for tracking all plots 
        self.plots = {'data':[],'fitting':[],'param':[]}
        
        # track the active plot 
        self.active = {'data':0,'fitting':0,'param':0}
    
    # ======================================================================= #
    def figure(self,style):
        """Make new figure"""
        
        # make figure
        fig = plt.figure()
        
        # make events and save as canvas attribute
        fig.canvas.user_close = fig.canvas.mpl_connect('close_event', self.close_figure)
        fig.canvas.user_active = fig.canvas.mpl_connect('button_press_event', self.update_active)
        
        # set style
        fig.canvas.style = style
        
        # update lists
        self.plots[style].append(fig.number)
        self.active[style] = fig.number

    # ======================================================================= #
    def close_figure(self,event):
        """Remove figure from list"""
        
        # get number and style
        number = event.canvas.figure.number
        style = event.canvas.style
        
        # disconnect events
        event.canvas.mpl_disconnect(event.canvas.user_close)
        event.canvas.mpl_disconnect(event.canvas.user_active)
        
        # close the winow
        plt.close(number)
        
        # remove from list 
        self.plots[style].remove(number)
        
        # reset active
        try:
            self.active[style] = self.plots[style][-1]
        except IndexError:
            self.active[style] = 0
                    
    # ======================================================================= #
    def update_active(self,event):
        """
            Update the active figure id based on click event.
        """
        number = event.canvas.figure.number
        style = event.canvas.style
        self.active[style] = number
