from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Sudoku solver',
    ext_modules=cythonize("solvercython.pyx"),
    zip_safe=False,
    compiler_directives={'language_level' : "3"}
)