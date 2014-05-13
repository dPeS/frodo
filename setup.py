from distutils.core import setup

setup(
    name='Frodo',
    version='0.1.0',
    author='dPeS',
    author_email='dpeees@gmail.com',
    packages=['frodo', 'frodo.test'],
    scripts=['',],
    url='http://pypi.python.org/pypi/Frodo/',
    license='LICENSE.txt',
    description='Generic resource blocking engine.',
    long_description=open('README.md').read(),
    install_requires=[
        "psycopg2 >= 2.5.2",
    ],
)
