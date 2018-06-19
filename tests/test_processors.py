from .context import note_builder

import os

def test_measure():

    content = 'Note 1\nThe content\n'

    measurements = note_builder.processors.measure(content)

    assert measurements.notes == 1
    assert measurements.lines == 2
    assert measurements.words == 4

def test_remove_special_characters():

    content = '# Note 1\n\n*&*!\nThe content! []\n'

    measurements = note_builder.processors.measure(content)

    assert measurements.notes == 1
    assert measurements.lines == 2
    assert measurements.words == 4

def test_measure_notes():

    note1 = note_builder.Note(name='note_1',
                                content = '# Note 1\n\ncontent\n')
    note2 = note_builder.Note(name='note_2',
                                content = '# Second Note\nSome new content\n')
    note_list = [note1, note2]

    measurements = note_builder.processors.measure_notes(note_list)
    assert measurements.notes == 2
    assert measurements.lines == 4
    assert measurements.words == 8

def test_quantifier(tmpdir):
    note1 = note_builder.Note(name='note_1',
                                content = '# Note 1\n\ncontent\n')
    note2 = note_builder.Note(name='note_2',
                                content = '# Second Note\nSome new content\n')
    note_list = [note1, note2]
    test_db = tmpdir.mkdir('db').join('test.db')
    quantifier = note_builder.processors.Quantifier(test_db)

    quantifier.process(note_list)

    assert quantifier.db_path == test_db
    assert os.path.isfile(quantifier.db_path)