from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Sudoku solver',
    ext_modules=cythonize("solverc.py"),
    zip_safe=False,
)

#  python setup.py build_ext --inplace
