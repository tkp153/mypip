from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
from setuptools import setup, Extension

import numpy as np

sourcefiles = ['my_yolox_fnc.pyx']

setup(
    name='my_yolox_fnc',
    version='1.0.2',
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("my_yolox_fnc", sourcefiles, include_dirs=[np.get_include()],language="c++", extra_compile_args=["-std=c++11"],define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")])],
)