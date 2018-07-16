from .. import core

import re
import os

from jinja2 import Environment, PackageLoader, select_autoescape

class Gallery(object):

    def __init__(self):
        self.images = []
        self.env = Environment(
            loader=PackageLoader('note_builder', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def process(self, notes):
        for note in notes:
            self._find_images(note)
        return notes

    def render(self, directory, _):
        self._make_gallery_html(directory)

    def _find_images(self, note):
        for line in note.content.splitlines():
            if '![' in line:
                match = re.search(r'\((.*)\)', line)
                self.images.append((match.group(1), note))

    def _make_gallery_html(self, directory):
        output_path = os.path.join(directory, 'gallery.html')
        with open(output_path, 'w') as out_file:
            template = self.env.get_template('gallery.html')
            out_file.write(template.render(images=self.images))
