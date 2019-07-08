import nep
import simplejson
import sys
import time
import nep
import rize

class nodes_manager():
        
    def __init__(self, middleware = "ZMQ"):
        
        node = nep.node("rize_manager","ZMQ",False)
        # Publish in /nep_node topic (enable to kill other nodes)
        conf = node.direct("127.0.0.1", "12345", "one2many") 
        self.pub_exit  = node.new_pub("/nep_node", "json", conf)
        # Get feedback from other nodes
        sub_config = node.broker("many2one")
        self.status_sub  = node.new_sub("/node_status","json" ,sub_config)

    # ------------------------------------ onStopRobots ----------------------------
    # Description: Send signal to stop a list of robots
    def onStopNodeList(self,node_name, options_= ""): #TODO puy in NEP core

        if node_name is list:

            for name in node_name:
                dic = {'node': name}
                print ("kill " + name )
                self.pub_exit.send_json(dic)
                time.sleep(.2)
        else:
            dic = {'node': node_name}
            print ("kill " + node_name )
            self.pub_exit.send_json(dic)
            time.sleep(.2)


        return {'state': "success"}

    # ------------------------------- onRobotLaunch ---------------------------
    # Description: Launch robot and it sensors (if external)
    def onLaunchRobots(self,input_, options_ = {"debug":True}):
        print ("Robot to launch " + str(input_))
        if type(input_) is str:
            robot = input_
            try:
                s, options = rize.getRobotConfiguration(robot)
                if s:
                    if sys.version_info[0] == 3:
                        middleware = options['middleware']
                        ip = options['ip']
                        name = options['name']
                        port = options['port']
                        type_ = options['type']
                        python_version = options['python']

                    else:
                        # Get info
                        middleware = options['middleware'].encode("UTF-8")
                        ip = options['ip'].encode("UTF-8")
                        name = options['name'].encode("UTF-8")
                        port = str(options['port']).encode("UTF-8")
                        type_ = options['type'].encode("UTF-8")
                        python_version = options['python'].encode("UTF-8")

                    parameters = " " + str(name) + " " + str(ip) +  " " + str(port) + " " + str(middleware)
                    nep.neprun(type_,name, parameters, python_version)

                else:
                    return "failure"
            except:
                print ("Robot configuration for *** " + robot + " *** not found")
                return "failure"


    # ------------------------------- onLaunchNode ---------------------------
    # Description: Launch robot and it sensors (if external)
    def onLaunchNode(self,input_, options_ = {"debug":True}):
        print ("Robot to launch " + str(input_))
        if type(input_) is str:
            node = input_
            try:
                s, options = rize.getNodeConfiguration(node)
                if s:
                    parameters = " "
                    nep.neprun(node,node, parameters, "default")
                else:
                    return "failure"
            except:
                print ("Node configuration for *** " + node + " *** not found")
                return "failure"