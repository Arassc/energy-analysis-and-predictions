from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as file:
    content = file.readlines()

requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='energyanalysis',
      version='0.0.1',
      description='Analyze and predict german energy prices and production',
      author='Araceli Sebastian',
      author_email='sebasarsan@protonmail.com',
      install_requires=requirements,
      packages=find_packages(),
      #packages=['energyanalysis'],
      include_package_data=True, # to install data from manifest
      zip_safe=False)
