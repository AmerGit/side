
def createHairSystemControl(hairSystemNodes=None):
    """
        function that goes over the given hair system nodes and creates controllers for each of them

        @param hairSystemNodes: list containing hairSystem nodes to add controllers two
    """
    # define lists for all different attribute categories, which will be separated in the channelbox
    dynamicAttrs = ['stretchResistance', 'compressionResistance', 'bendResistance','twistResistance', 'extraBendLinks',
                    'restLengthScale']
    collisionAttrs = ['collideStrength', 'collisionLayer', 'maxSelfCollisionIterations','bounce', 'friction',
                      'stickiness']
    forceAttrs = ['startCurveAttract', 'attractionDamp', 'mass', 'drag', 'tangentialDrag', 'damp',
                  'dynamicsWeight']
    turbulenceAttrs = ['turbulenceStrength', 'turbulenceFrequency', 'turbulenceSpeed']

    if hairSystemNodes is None:
        hairSystemNodes = cmds.ls('hairSystem')


'''
	quick script to easily copy selected attributes and their properites from one node
	to another and connecting deselected
	attributes from one to another
	
	primary use: creating a control that plugs into another node's attributes, usually
	useful to control and animate deformers with a control
	
	future updates:
	    a. fix bugs with enums
	    b. fix range fetching bugs
	
	possible ideas:
	    a. UI
	    b. feature to plug simple operators to attributes(multipliers, dividers, offsets)
	    c. attribute multipliers
	    d. simple categorization
	    c. choose between existing or new controller
'''

from maya import cmds, mel


# fetch selected attributes from channelBox
selectedNode = 'mpcNoiseDeformer3'
targetNode = 'preSwallowNoise_CTRL'

mainAttrs = cmds.channelBox('mainChannelBox', query=True, selectedMainAttributes=True)
shapeAttrs = cmds.channelBox('mainChannelBox', query=True, selectedShapeAttributes=True)
inputAttrs = cmds.channelBox('mainChannelBox', query=True, selectedHistoryAttributes=True)
outputAttrs = cmds.channelBox('mainChannelBox', query=True, selectedOutputAttributes=True)


# loop over selected attributes

print mainAttrs
print shapeAttrs
print inputAttrs
print outputAttrs

for attr in selectedAttrs:
	
	# get attribute long name and properties
	attrName = cmds.attributeQuery(attr, node=selectedNode, longName=True)
	attrType = cmds.attributeQuery(attr, node=selectedNode, attributeType=True)
	
	'''-----------------------FIX THIS SHIT----------------------------'''
	# adress special kinds of attributes
	
	
	# case: enum
	
	
	# case: string
	
	
	
	# get range information from the attribute
	hasMin = cmds.attributeQuery(attr, node=selectedNode, minExists=True)
	hasMax = cmds.attributeQuery(attr, node=selectedNode, maxExists=True)
	
	min = None
	max = None
	
	if hasMin:
	    min =cmds.attributeQuery(attr, node=selectedNode, minimum=True)[0]
	    
	if hasMax:
	    max = cmds.attributeQuery(attr, node=selectedNode, maximum=True)[0]
	
	'''----------------------------------------------------------------'''    
	# add attribute to the target node
	cmds.addAttr(targetNode, attributeType=attrType, longName=attrName, shortName=attr, keyable=True)
	
	# fetch attribute values from source node and connect destination node to it
	currentValue = cmds.getAttr('%s.%s'%(selectedNode,attr))
	cmds.setAttr('%s.%s'%(targetNode,attr), currentValue)
	cmds.connectAttr('%s.%s'%(targetNode,attr),'%s.%s'%(selectedNode,attr))
	
	

	
