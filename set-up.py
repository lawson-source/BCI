from setuptools import setup
from Cython.Build import cythonize
import os
os.environ.get('WPDPACK_BASE')
basedir=os.path.abspath(os.path.dirname(__file__))

setup(
    name='test',
    ext_modules=cythonize(basedir+'/NEXEED_DA.py'),
)