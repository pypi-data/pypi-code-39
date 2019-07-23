###############################################
            
# TODO Current work is exploring deployment of an 'x3d' python package on PyPi for import.
#      This approach will greatly simplify deployment and use, avoiding extra setup.
# TODO Add documentation and stylesheet parameters for enabling/disabling these options.
#
# Developer options for testing source models:

# import x3d # from ../..

from x3d import * # "polluting" version of import that avoids need to prepend "x3d." prefix

###############################################

#  comment preceding root node 
newModel=X3D(profile='Immersive',version='3.3',
  head=head(
    children=[
    meta(content='HelloWorld.x3d',name='title'),
    meta(content='Special test case: simple X3D scene example: Hello World!',name='description'),
    meta(content='30 October 2000',name='created'),
    meta(content='16 April 2018',name='modified'),
    meta(content='Don Brutzman',name='creator'),
    meta(content='images/HelloWorld.tall.png',name='Image'),
    meta(content='http://en.wikipedia.org/wiki/Hello_world',name='reference'),
    meta(content='http://en.wikipedia.org/wiki/Hello#"Hello,_World"_computer_program',name='reference'),
    meta(content='http://en.wikibooks.org/w/index.php?title=Computer_Programming/Hello_world',name='reference'),
    meta(content='http://www.HelloWorldExample.net',name='reference'),
    meta(content='http://www.web3D.org',name='reference'),
    meta(content='http://www.web3d.org/realtime-3d/news/internationalization-x3d',name='reference'),
    meta(content='http://www.web3d.org/x3d/content/examples/HelloWorld.x3d',name='reference'),
    meta(content='http://X3dGraphics.com/examples/X3dForAdvancedModeling/HelloWorldScenes',name='reference'),
    meta(content='http://X3dGraphics.com/examples/X3dForWebAuthors/Chapter01-TechnicalOverview/HelloWorld.x3d',name='identifier'),
    meta(content='http://www.web3d.org/x3d/content/examples/license.html',name='license'),
    meta(content='X3D-Edit 3.3, https://savage.nps.edu/X3D-Edit',name='generator'),
    #  Alternate encodings: VRML97, X3D ClassicVRML Encoding, X3D Compressed Binary Encoding (CBE), X3DOM, JSON 
    meta(content='HelloWorld.wrl',name='reference'),
    meta(content='HelloWorld.x3dv',name='reference'),
    meta(content='HelloWorld.x3db',name='reference'),
    meta(content='HelloWorld.xhtml',name='reference'),
    meta(content='HelloWorld.json',name='reference')
    ]),
  Scene=Scene(
    #  Example scene to illustrate X3D nodes and fields (XML elements and attributes) 
    Group(
      children=[
      Viewpoint(DEF='ViewUpClose',centerOfRotation=(0,-1,0),description='Hello world!',position=(0,-1,7)),
      Transform(DEF='ScaleFeetToMeters',rotation=(0,1,0,3),scale=(0.3048,0.3048,0.3048),
        children=[
        Shape(
          appearance=Appearance(
            material=Material(DEF='MaterialLightBlue',diffuseColor=(0.1,0.5,1)),
            texture=ImageTexture(DEF='ImageCloudlessEarth',url=["earth-topo.png","earth-topo.jpg","earth-topo-small.gif","http://www.web3d.org/x3d/content/examples/Basic/earth-topo.png","http://www.web3d.org/x3d/content/examples/Basic/earth-topo.jpg","http://www.web3d.org/x3d/content/examples/Basic/earth-topo-small.gif"])),
          geometry=Sphere())]
      ),
      Transform(translation=(0,-2,0),
        children=[
        Shape(
          appearance=Appearance(
            material=Material(USE='MaterialLightBlue')),
          geometry=Text(DEF='TextMessage',string=["Hello","world!"],
            fontStyle=FontStyle(justify=["MIDDLE","MIDDLE"])))]
      )]
    ))),
#  comment following root node 
            
print ('     newModel[0]      =',  str(newModel[0]))
print ('type(newModel)        =', type(newModel))
print ('type(newModel[0])     =', type(newModel[0]))
print ('X3D.__name__          =', X3D.__name__)
print ('str(newModel[0].__name__)=', str(newModel[0].__name__))
print ('str(newModel[0].head)    =', str(newModel[0].head))
print ('str(newModel[0].Scene)   =', str(newModel[0].Scene))
