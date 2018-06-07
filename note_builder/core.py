from collections import namedtuple
from glob import glob
import os
import subprocess

Note = namedtuple('Note', ['name', 'content'])

def find_notes(directory):
    return glob(os.path.join(directory, '*.md'))

def make_note(note_path):
    name = name_from_path(note_path)
    content = read_content(note_path)
    return Note(name, content)

def name_from_path(path):
    (_, filename) = os.path.split(path)
    return filename.strip('.md' )

def read_content(path):
    with open(path) as note_file:
        return note_file.read()

def load_notes(note_files):
    for note_file in note_files:
        yield make_note(note_file)

def render_to_file(content, filename):
    result = subprocess.run(['pandoc',
                    '-f', 'markdown',
                    '-t', 'html',
                    '-s', '-o', filename],
                    input=content,
                    encoding='utf-8',
                    stdout=subprocess.PIPE)
    return result.stdout

class HtmlRenderer(object):

    def __init__(self, output_directory):
        self.output_directory = output_directory

    def render(self, note):
        note_destination = os.path.join(self.output_directory, note.name + '.html')
        render_to_file(note.content, note_destination)
