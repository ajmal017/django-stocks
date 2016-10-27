from distutils.core import setup

setup(
    name='django-stocks',
    version='0.1.0',
    description='Django app that provides a ReST API with Stock Market information',
    author='Ramon Moraes',
    author_email='vyscond@gmail.com',
    url='https://github.com/vyscond/django-stocks',
    license='MIT',
    packages=['stocks'],
    install_requires=[
        'Django==1.10.1',
        '-e git://github.com/vyscond/django-stocks.git@0.1.0#egg=django-stocks'
    ]
)
