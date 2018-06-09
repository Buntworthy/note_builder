from collections import namedtuple
from glob import glob
import os
import subprocess

Note = namedtuple('Note', ['name', 'content'])

def find_notes(directory):
    """Find all notes in a given directory."""
    return glob(os.path.join(directory, '*.md'))

def make_note(note_path):
    """Create a note from a path to a file."""
    name = name_from_path(note_path)
    content = read_content(note_path)
    return Note(name, content)

def name_from_path(path):
    """Convert path to note name."""
    (_, filename) = os.path.split(path)
    return filename.strip('.md' )

def read_content(path):
    """Read contents of note file at location path."""
    with open(path) as note_file:
        return note_file.read()

def load_notes(note_files):
    """Iterate over note paths and make note from each."""
    return [make_note(note_file) for note_file in note_files]

class HtmlRenderer(object):

    def __init__(self, output_directory):
        self.output_directory = output_directory

    def render(self, notes):
        for note in notes:
            note_destination = os.path.join(self.output_directory, note.name + '.html')
            self.render_to_file(note.content, note_destination)

    def render_to_file(self, content, filename):
        """Convert note content to html file."""
        result = subprocess.run(['pandoc',
                        '-f', 'markdown',
                        '-t', 'html',
                        '-s', '-o', filename],
                        input=content,
                        encoding='utf-8',
                        stdout=subprocess.PIPE)
