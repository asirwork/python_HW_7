from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='0.1',
      description='Sorting files on your folders',
      url='https://github.com/asirwork/python_HW_6',
      author='Andrii',
      author_email='andrii@example.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={
          'console_scripts': ['clean-folder = clean_folder.clean:main']
      })
