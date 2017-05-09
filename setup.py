try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'description': 'Tlb Simulator',
  'author': 'Panitan Wongse-ammat',
  #'url': 'URL to get it at.',
  #'download_url': 'Where to download it.',
  'author_email': 'mr.panitan.w@gmail.com',
  'version': '0.1',
  'install_requires': [],
  'packages': ['NAME'],
  'scripts': [],
  'name': 'Tlb Simulator'
}

setup(**config)
