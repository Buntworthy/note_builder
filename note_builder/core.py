from glob import glob
import os

def find_notes(directory):
    return glob(os.path.join(directory, '*.md'))
