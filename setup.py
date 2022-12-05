#  python setup.py build_ext --inplace

from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Sudoku solver',
    ext_modules=cythonize("solverc.pyx"),
    zip_safe=False,
)