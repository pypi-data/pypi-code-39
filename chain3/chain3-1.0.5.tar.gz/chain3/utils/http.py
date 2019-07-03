def construct_user_agent(class_name):
    from chain3 import __version__ as chain3_version

    user_agent = 'chain3.py/{version}/{class_name}'.format(
        version=chain3_version,
        class_name=class_name,
    )
    return user_agent
