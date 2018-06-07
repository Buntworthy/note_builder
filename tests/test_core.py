from .context import note_builder
from .fixtures import datadir

import os

def test_find_notes(datadir):

    note_files = note_builder.find_notes(datadir)

    assert note_files[0] == datadir.join('note_1.md')
    assert note_files[1] == datadir.join('note_2.md')


def test_load_notes(datadir):

    note_path = datadir.join('note_1.md')

    note = note_builder.make_note(note_path)

    assert note.name == 'note_1'
    assert note.content == '# Note 1\n\ncontent\n'

def test_html_renderer(datadir):

    note = note_builder.Note(name='note_1', content = '# Note 1\n\ncontent\n')
    expected_name = note.name + '.html'
    expected_filename = datadir.join(expected_name)

    renderer = note_builder.HtmlRenderer(output_directory=datadir)
    renderer.render(note)

    assert os.path.isfile(expected_filename)
