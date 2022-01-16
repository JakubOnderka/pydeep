from setuptools import setup, Command, Extension

import os
import sys
import os.path as op


def get_version():
    with open(os.path.join(os.path.dirname(__file__), 'pydeep.c'), 'r') as f:
        for line in f:
            if "#define PYDEEP_VERSION" in line:
                return line.split()[-1].strip('"')


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        os.chdir(op.join(op.dirname(op.abspath(__file__)), "tests"))
        errno = subprocess.call([sys.executable, 'test.py'])
        if errno != 0:
            raise SystemExit(errno)
        else:
            os.chdir("..")


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydeep2",
    author="Kiran Bandla",
    author_email="kbandla@in2void.com",
    license="BSD",
    version=get_version(),
    description="Python bindings for ssdeep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/JakubOnderka/pydeep",
    ext_modules=[Extension(
        "pydeep",
        sources=["pydeep.c"],
        libraries=["fuzzy"],
        library_dirs=["/usr/local/lib/"],
        include_dirs=["/usr/local/include/"],
    )],
    cmdclass={
        'test': TestCommand
    },
)
