from collections import namedtuple
from glob import glob
import os
import subprocess
import json


class Note(object):

    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.title = self._get_title(content)

    def _get_title(self, content):
        content_line = self.content.splitlines()
        return content_line[0].lstrip('# ')


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
    (note_name, _) = os.path.splitext(filename)
    return note_name


def read_content(path):
    """Read contents of note file at location path."""
    with open(path) as note_file:
        return note_file.read()


def load_notes(note_files):
    """Iterate over note paths and make note from each."""
    return [make_note(note_file) for note_file in note_files]


class HtmlRenderer(object):

    def __init__(self, assets=None, css=None):
        self.assets_path = assets
        self.css = css

    def render(self, output_directory, notes):
        """Render a list of Notes to a particular directory."""
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)

        for note in notes:
            print('Rendering ' + note.name)
            note_destination = os.path.join(output_directory,
                                            note.name + '.html')
            self.render_to_file(note.content, note_destination)
        if self.assets_path:
            self.copy_assets(output_directory)

    def render_to_file(self, content, filename):
        """Convert note content to html file."""
        command = ['pandoc',
                   '-f', 'markdown',
                   '-t', 'html',
                   '-s', ]
        if self.css:
            for css_item in self.css:
                command.extend(['--css', css_item])
        command.extend(['-o', filename])
        result = subprocess.run(command,
                                input=content,
                                encoding='utf-8',
                                stdout=subprocess.PIPE)

    def copy_assets(self, output_directory):
        assets_folder_name = os.path.basename(os.path.normpath(self.assets_path))
        destination_location = os.path.join(output_directory,
                                            assets_folder_name)
        subprocess.run(['cp', '-r', self.assets_path, destination_location])

def parse_config():
    if not os.path.isfile('config.json'):
        raise FileNotFoundError('Config file not found.')

    with open('config.json', 'r') as read_file:
        raw_config = json.load(read_file)

    config = dict()
    config['datadir'] = '.'
    config['assets'] = os.path.join(config['datadir'], raw_config['assets'])
    css_relative = raw_config['css']
    config['css'] = [os.path.join(config['datadir'], css_file) for css_file in css_relative]
    config['output_dir'] = raw_config['output']
    return config
