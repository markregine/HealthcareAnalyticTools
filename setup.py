from setuptools import setup

exec(compile(open('HealthcareAnalyticTools/version.py').read(),
             'HealthcareAnalyticTools/version.py', 'exec'))

setup(name='HealthcareAnalyticTools',
      version=__version__,
      description='Tools to aid with the cleaning and analysis of medical and pharmacy claims and associated data files.',
      keywords='each word in a different seperated by a space not a comma',
      packages=['HealthcareAnalyticTools'],
      include_package_data=True,
      license='MIT',
      author='Mark Regine, Ph.D.',
      author_email='mregine@betaxanalytics.com',
      url='https://github.com/markregine/HealthcareAnalyticTools',
      classifiers=['Programming Language :: Python :: 3.5'],
      install_requires=['pandas',
                        'numpy'],
      )
