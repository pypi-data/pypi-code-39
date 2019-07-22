from setuptools import setup

setup(
    name='flask-test-requests-client',
    version='0.2.1',
    description='A Flask test client which replicates the requests interface.',
    long_description="""Instead of using the flask test client, you can use this package
which does a similar job. This wrapper to the flask test client has an API based on the
'requests' HTTP client library. This means that you can write tests or monitoring which
works with either requests (for when you want to test against a real web server) and this
package, for when you want to run your tests using the built-in capabilities of flask.""",
    url='http://github.com/jwg4/flask-test-requests-client',
    author='Jack Grahl',
    author_email='jack.grahl@gmail.com',
    license='MIT',
    packages=['frtc'],
    zip_safe=False,
    install_requires=['chardet', 'requests'],
    test_suite="tests",
    tests_require=["flask", "requests"]
)
