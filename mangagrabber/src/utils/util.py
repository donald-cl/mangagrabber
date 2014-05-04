from os.path import expanduser
from os.path import isfile

HOME = expanduser("~")
PROJ = "mangagrabber"

def get_mangagrabber_dir():
    path = "%s/%s/"
    return path % (HOME, PROJ)
