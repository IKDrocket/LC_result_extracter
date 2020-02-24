import sys, os
import glob
from cx_Freeze import setup, Executable

packages = []
includes = []
include_files = glob.glob("/Users/ikdrocket/.local/share/virtualenvs/LC_result_extracter-FIA9FH4V/lib/python3.6/site-packages/*")
buildOptions = dict(packages=packages, excludes=[],
                    includes=includes,
                    include_files=include_files
                    )
base = 'Console'

executables = [
    Executable('LC_result_extracter.py', base=base, targetName='LC_result_extracter')
]

setup(name='LC_result_extracter',
      version='1.0',
      description='',
      author='IKDrocket',
      options=dict(build_exe=buildOptions),
      executables=executables)