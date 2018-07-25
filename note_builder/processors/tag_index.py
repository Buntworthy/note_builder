from .. import core

from collections import defaultdict
import re
import os

from jinja2 import Environment, PackageLoader, select_autoescape


class TagIndex(object):

    def __init__(self):
        self.tags = defaultdict(set)
        self.output_name = 'tag_index.html'
        self.env = Environment(
            loader=PackageLoader('note_builder', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def process(self, notes):
        print(f'Extracting tags from {len(notes)} notes.')

        new_notes = []
        for note in notes:
            note_tags = self._find_tags(note)
            self._add_to_tags(note_tags, note)
            new_note = self._replace_tags(note_tags, note)
            new_notes.append(new_note)
        return new_notes

    def render(self, directory, _):
        print('Rendering tag pages.')

        self._make_index_html(directory)
        self._make_tag_page_html(directory)

    def _find_tags(self, note):
        tags = []
        for line in note.content.splitlines():
            for word in line.split():
                if word.startswith(';;'):
                    tags.append(word[2:])
        return tags

    def _replace_tags(self, tags, note):
        new_content = note.content
        for tag in tags:
            search_string = r';;(' + tag + ')'
            replacement = r'[\1](tagged-\1.html)'
            new_content = re.sub(search_string, replacement, new_content)

        return core.Note(name=note.name, content=new_content)

    def _add_to_tags(self, note_tags, note):
        for tag in note_tags:
            self.tags[tag].add(note)

    def _make_index_html(self, directory):
        output_path = os.path.join(directory, self.output_name)
        with open(output_path, 'w') as out_file:
            template = self.env.get_template('tag_index.html')
            out_file.write(template.render(tags=self.tags))

    def _make_tag_page_html(self, directory):
        for tag in self.tags.keys():
            output_path = os.path.join(directory, 'tagged-' + tag + '.html')
            with open(output_path, 'w') as out_file:
                template = self.env.get_template('tag_page.html')
                out_file.write(template.render(notes=self.tags[tag]))
