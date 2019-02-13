# HealthcareAnalyticTools  

# Modules:  
## lookups  
## raw_data_files  


## Things learned along the way when building the module.
### this statment builds the wheels and eggs
* ### python setup.py sdist bdist_wheel
### documentation says to do this...
* ### python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
### because i have dependencies AND i'm using TestPyPi I need to do this
* ### pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/pypi MODULENAME
### needed to update, but still not working
* ### pip install -i https://testpypi.python.org/pypi --extra-index-url https://pypi.python.org/pypi test_mark_0001 --upgrade
