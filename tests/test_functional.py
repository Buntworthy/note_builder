from .context import note_builder
from .fixtures import datadir

import os


def test_end_to_end(datadir):
    output_dir = datadir.join('output')
    test_db = datadir.mkdir('db').join('test.db')

    note_files = note_builder.find_notes(datadir)
    notes = note_builder.load_notes(note_files)
    quantifier = note_builder.processors.Quantifier(test_db)
    note_renderer = note_builder.HtmlRenderer(assets='assets')

    builder = note_builder.Builder()
    builder.add_processor(quantifier)
    builder.add_renderer(quantifier)
    builder.add_renderer(note_renderer)

    notes = builder.process(notes)
    builder.render(output_dir, notes)

    assert os.path.isfile(datadir.join('output').join('statistics.html'))
