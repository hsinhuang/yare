try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "pyre",
    description="Python Regular Expression",
    long_description = """
PYRE is a simple regular expression library implemented in Python.
It is fit for teaching and learning.
It is compatible with both Python 2 and Python 3.
""",
    license="""GPL v2""",
    version = "0.3.0",
    author = "Leonardo Huang",
    author_email = "leon@njuopen",
    maintainer = "Leonardo Huang",
    maintainer_email = "leon@njuopen",
    url = "https://github.com/leon-huang/pyre",
    packages = ['pyre'],
    install_requires = ['ply'],
    classifiers = [
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 2',
    ]
)
