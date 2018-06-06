from .context import note_builder
from .fixtures import datadir


def test_find_notes(datadir):

    note_files = note_builder.find_notes(datadir)
    note_list = [note for note in note_files]
    assert(len(note_list) == 2)
    assert(note_list[0] == datadir.join('note_1.md'))
    assert(note_list[1] == datadir.join('note_2.md'))
