#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

##############################################################################
# This code is auto generated. DO NOT EDIT FILE!
# Run "./gradlew :Generators:generatePythonImportTools" to generate
##############################################################################


import jpy
import wrapt


_java_type_ = None  # None until the first defineSymbols() call
_builder_type_ = None  # None until the first defineSymbols() call


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_, _builder_type_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.export.jdbc.JdbcLogger")
        _builder_type_ = jpy.get_type("com.illumon.iris.export.jdbc.JdbcLogger$Builder")


# every module method should be decorated with @_passThrough
@wrapt.decorator
def _passThrough(wrapped, instance, args, kwargs):
    """
    For decoration of module methods, to define necessary symbols at runtime

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    defineSymbols()
    return wrapped(*args, **kwargs)


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


@_passThrough
def builder(*args):
    return JdbcLoggerBuilder(*args)


class JdbcLoggerBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form (*args)
        - **kwargs, when provided, should take the form {'builder': *value*}, and is generally 
          meant for internal use
        """
        defineSymbols()
        builder = kwargs.get('builder', None)
        if builder is not None:
            self._builder = builder
        else:
            self._builder = _java_type_.builder(*args)

    @property
    def builder(self):
        """The actual java builder object"""
        return self._builder

    def batchSize(self, batchSize):
        return JdbcLoggerBuilder(builder=self._builder.batchSize(batchSize))

    def build(self):
        return self._builder.build()

    def calendar(self, calendar):
        return JdbcLoggerBuilder(builder=self._builder.calendar(calendar))

    def dataColumn(self, *args):
        return JdbcLoggerBuilder(builder=self._builder.dataColumn(*args))

    def jdbcPassword(self, jdbcPassword):
        return JdbcLoggerBuilder(builder=self._builder.jdbcPassword(jdbcPassword))

    def jdbcUser(self, jdbcUser):
        return JdbcLoggerBuilder(builder=self._builder.jdbcUser(jdbcUser))

    def keyColumns(self, *keyColumns):
        return JdbcLoggerBuilder(builder=self._builder.keyColumns(*keyColumns))

    def logMode(self, logMode):
        return JdbcLoggerBuilder(builder=self._builder.logMode(logMode))

    def operationColumn(self, operationColumn):
        return JdbcLoggerBuilder(builder=self._builder.operationColumn(operationColumn))

    def rowIndexColumn(self, rowIndexColumn):
        return JdbcLoggerBuilder(builder=self._builder.rowIndexColumn(rowIndexColumn))
