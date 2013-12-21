from setuptools import setup, find_packages
import LogDefer

setup(
    name='LogDefer',
    version=LogDefer.__version__,
    description='Structured Logging for Python',
    long_description=open('README.md').read(),
    classifiers=[],
    keywords='structured logging log logdefer',
    author='Michael Pucyk',
    author_email='michael.pucyk@gmail.com',
    url='https://github.com/mikep/LogDefer',
    py_modules=['LogDefer'],
    include_package_data=True,
    install_requires=[],
    entry_points={},
    zip_safe=True,
)

