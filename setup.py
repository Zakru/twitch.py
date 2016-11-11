from setuptools import setup
import twitch

setup(name='twitch.py',
	  description='Twitch API for Python',
	  author='Zakru',
	  authir_email='sakari.leukkunen@gmail.com',
	  url='https://github.com/Zakru/twitch.py',
	  version=twitch.__version__,
	  packages=['twitch'],
	  license='MIT')
