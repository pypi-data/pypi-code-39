import os

from setuptools import Extension, setup

Box2D = [
    'deps/Box2D/Collision/b2BroadPhase.cpp',
    'deps/Box2D/Collision/b2CollideCircle.cpp',
    'deps/Box2D/Collision/b2CollideEdge.cpp',
    'deps/Box2D/Collision/b2CollidePolygon.cpp',
    'deps/Box2D/Collision/b2Collision.cpp',
    'deps/Box2D/Collision/b2Distance.cpp',
    'deps/Box2D/Collision/b2DynamicTree.cpp',
    'deps/Box2D/Collision/b2TimeOfImpact.cpp',
    'deps/Box2D/Collision/Shapes/b2ChainShape.cpp',
    'deps/Box2D/Collision/Shapes/b2CircleShape.cpp',
    'deps/Box2D/Collision/Shapes/b2EdgeShape.cpp',
    'deps/Box2D/Collision/Shapes/b2PolygonShape.cpp',
    'deps/Box2D/Common/b2BlockAllocator.cpp',
    'deps/Box2D/Common/b2Draw.cpp',
    'deps/Box2D/Common/b2Math.cpp',
    'deps/Box2D/Common/b2Settings.cpp',
    'deps/Box2D/Common/b2StackAllocator.cpp',
    'deps/Box2D/Common/b2Timer.cpp',
    'deps/Box2D/Dynamics/b2Body.cpp',
    'deps/Box2D/Dynamics/b2ContactManager.cpp',
    'deps/Box2D/Dynamics/b2Fixture.cpp',
    'deps/Box2D/Dynamics/b2Island.cpp',
    'deps/Box2D/Dynamics/b2World.cpp',
    'deps/Box2D/Dynamics/b2WorldCallbacks.cpp',
    'deps/Box2D/Dynamics/Contacts/b2ChainAndCircleContact.cpp',
    'deps/Box2D/Dynamics/Contacts/b2ChainAndPolygonContact.cpp',
    'deps/Box2D/Dynamics/Contacts/b2CircleContact.cpp',
    'deps/Box2D/Dynamics/Contacts/b2Contact.cpp',
    'deps/Box2D/Dynamics/Contacts/b2ContactSolver.cpp',
    'deps/Box2D/Dynamics/Contacts/b2EdgeAndCircleContact.cpp',
    'deps/Box2D/Dynamics/Contacts/b2EdgeAndPolygonContact.cpp',
    'deps/Box2D/Dynamics/Contacts/b2PolygonAndCircleContact.cpp',
    'deps/Box2D/Dynamics/Contacts/b2PolygonContact.cpp',
    'deps/Box2D/Dynamics/Joints/b2DistanceJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2FrictionJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2GearJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2Joint.cpp',
    'deps/Box2D/Dynamics/Joints/b2MotorJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2MouseJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2PrismaticJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2PulleyJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2RevoluteJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2RopeJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2WeldJoint.cpp',
    'deps/Box2D/Dynamics/Joints/b2WheelJoint.cpp',
    'deps/Box2D/Rope/b2Rope.cpp',
]

platformer_core = Extension(
    name='minigym.envs.core.platformer',
    include_dirs=['deps'],
    libraries=['opengl32'],
    sources=[
        'minigym/envs/core/platformer.cpp',
    ] + Box2D,
)

if os.path.isfile('deps/Box2D/Box2D.lib'):
    platformer_core.library_dirs.append('deps/Box2D')
    platformer_core.libraries.append('Box2D')
    platformer_core.sources = [x for x in platformer_core.sources if x not in Box2D]

with open('README.md') as f:
    long_description = f.read()

setup(
    name='minigym',
    version='0.2.0',
    description='more gym environments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cprogrammer1994/minigym',
    author='Szabolcs Dombi',
    author_email='cprogrammer1994@gmail.com',
    install_requires=[
        'gym',
        'pyprojector',
        'moderngl<6.0.0',
        'numpy',
        'pillow',
    ],
    ext_modules=[
        platformer_core,
    ],
)
