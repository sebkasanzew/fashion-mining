# Zalando Textmining

## Installation instructions for Windows

### NLTK Installation
1. make sure python is installed
2. pip install nltk
3. (optional) downloading nltk data by opening python and run:
```
    >>> import nltk
    >>> nltk.download()
```
4. have fun

### GENSIM installation (coming soon)
---

## Installation instructions for Debian Linux (Ubuntu)

### NLTK Installation Guide (Debian/Ubuntu Linux)
1. pip install nltk
2. make sure in downloader.py line 370 in "/usr/lib/python2.7/dist-packages/nltk/" the DEFAULT_URL is set to "http://nltk.github.com/nltk_data/"
3. download nltk data by executing this command:
```
	~$ sudo python -m nltk.downloader -d /usr/local/share/nltk_data all
```
4. have fun

### GENSIM installation

#### Dependencies

	1. Python >= 2.7
	2. NumPy >= 1.10
	3. Scipy >= 0.16

#### Installation
```
	~$ sudo apt-get install libamd2.* libblas3gf libc6 libgcc1 \
	libgfortran3 liblapack3gf libumfpack5.* libstdc++6 \
	build-essential gfortran python-all-dev \
	libatlas-base-dev 

	~$ sudo apt-get install python-setuptools

	~$ sudo easy_install pip

	~$ pip install --upgrade gensim
	(NumPy and SciPy would be downloaded automatically)

```

All dependencies should be resolved and installation is complete to use *GENSIM*
