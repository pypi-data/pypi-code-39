"""A starter tutorial to learn about biseau scripting in python.

"""


TUTORIAL_NAME = 'Python scripting of biseau: a primer'
LANGUAGE = 'Python'
ORDERED_TUTO = (
'''
# Hello !
# Welcome in this tutorial.
# You will learn how to script biseau using python.

# The central principle is the following:

# A python script for biseau is made of a `run_on` function, that takes
#  a parameter `context`, which is the current context of the programe,
#  and should return a string that will be appended to the context.

# Let's make an example:
def run_on(context):
    return 'link(a,b).'

# This script will simply add an edge linking 'a' to 'b' in the graph.
$run
$pause

# This is the very basic principle. There is now lot of details
#  that enables a fine control of many aspects of scripting.

# Let's explore that !
$end
''','''$title Arguments

# We saw the basic run_on function. But you can also put more arguments !

def run_on(context, *, source:str='a', target:str='b'):
    return f'link({source},{target}).'

$run
# Now there is an options tab, in which you can set the values
#  for source and target.

# Play around with this, and go to next stage.
$end
''','''$title Many types of arguments

# 
''','''$title Metadata

# 
''','''$title Last details

# You are ready to play with scripting !
'''
)
