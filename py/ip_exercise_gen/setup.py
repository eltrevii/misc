from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("ip_data_manip.pyx")
)
