# Zalando Textmining

### NLTK Installation Guide (Windows)
1. make sure python is installed
2. pip install nltk
3. (optional) downloading nltk data by opening python and run:
```
    >>> import nltk
    >>> nltk.download()
```
4. have fun

### NLTK Installation Guide (Debian/Ubuntu Linux)
1. pip install nltk
2. make sure in downloader.py line 370 in "/usr/lib/python2.7/dist-packages/nltk/" the DEFAULT_URL is set to "http://nltk.github.com/nltk_data/"
3. download nltk data by executing this command:
```
    $ sudo python -m nltk.downloader -d /usr/local/share/nltk_data all
```
4. have fun
