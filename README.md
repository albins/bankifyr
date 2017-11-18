# bankifyr
Figuring out where your money went. With Science.

# Development instructions

1. Set up a virtual environment

```
$ conda create -n bankifyr python=3 matplotlib nltk # For mac users
$ source activate bankifyr
$ mkvirtualenv --python=python3 bankifyr-env # For everyone else
$ source bankifyr-env/bin/activate
```
2. Install dependencies
```
$ pip install -r requirements.txt
```
3. Set up the project using setup.py in development mode (this will make sure all the modules are where they should be and all binaries are in the virtual environment's PATH):

```
$ python setup.py develop
```
