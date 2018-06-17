from .context import note_builder

def test_measure():

    content = 'Note 1\nThe content\n'

    measurements = note_builder.processors.measure(content)

    assert measurements.num_lines == 2
    assert measurements.num_words == 4


def test_remove_special_characters():

    content = '# Note 1\n\n*&*!\nThe content! []\n'

    measurements = note_builder.processors.measure(content)

    assert measurements.num_lines == 2
    assert measurements.num_words == 4

def test_measure_notes():

    note1 = note_builder.Note(name='note_1',
                                content = '# Note 1\n\ncontent\n')
    note2 = note_builder.Note(name='note_2',
                                content = '# Second Note\nSome new content\n')
    note_list = [note1, note2]

    measurements = note_builder.processors.measure_notes(note_list)
    assert measurements.num_lines == 4
    assert measurements.num_words == 8
