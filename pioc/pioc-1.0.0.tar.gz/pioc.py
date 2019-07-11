import inspect

__author__ = 'xwann'
__version__ = '1.0.0'
__license__ = ''

# 所有配置的bean
__appBeanMap = {}


def getBean(cls):
    """
    获取bean
    :param cls: beanName或者class
    :return:
    """
    return __appBeanMap.get(cls)


def setBean(name, obj):
    """
    设置bean
    :param name: beanName
    :param obj:
    :return:
    """
    __appBeanMap[name] = obj


def component(name=None):
    """
    定义组件装饰器
    :param name: beanName可省略
    :return:
    """
    def decorator(cls):
        if name is None or name == "":
            __appBeanMap[cls] = cls()
        else:
            __appBeanMap[name] = cls()
        return cls

    if inspect.isclass(name):
        return decorator(name)
    else:
        return decorator


def auto(name=None):
    """
    组件注入装饰器
    :param name: beanName可省略
    :return:
    """
    def decorator(fun):
        def t(*args):
            if name is None or name == "":
                beanname = fun(*args)
            elif inspect.isfunction(name):
                beanname = fun(*args)
            else:
                beanname = name
            if beanname is None:
                raise Exception("bean name Can't be None")
            bean = getBean(beanname)
            if bean is None:
                raise Exception("bean {} not found!".format(beanname))
            return bean

        return t

    if inspect.isfunction(name):
        return decorator(name)
    else:
        return decorator