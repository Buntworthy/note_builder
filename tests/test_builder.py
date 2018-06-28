from .context import note_builder

from unittest import mock

def test_call_one_processor():

    processor = mock.Mock()
    notes = mock.Mock()

    builder = note_builder.Builder()
    builder.add_processor(processor)

    builder.process(notes)

    processor.process.assert_called_once_with(notes)

def test_call_two_processors():

    processor1 = mock.Mock()
    processor1.process.side_effect = lambda x: x
    processor2 = mock.Mock()
    processor2.process.side_effect = lambda x: x
    notes = mock.Mock()

    builder = note_builder.Builder()
    builder.add_processor(processor1)
    builder.add_processor(processor2)

    builder.process(notes)

    processor1.process.assert_called_once_with(notes)
    processor2.process.assert_called_once_with(notes)

def test_transform_notes():
    processor = mock.Mock()
    processor.process.return_value = []
    notes = mock.Mock()

    builder = note_builder.Builder()
    builder.add_processor(processor)

    notes = builder.process(notes)

    assert notes == []


def test_call_one_renderer():
    renderer = mock.Mock()

    builder = note_builder.Builder()
    builder.add_renderer(renderer)

    builder.render('output_directory')

    renderer.render.assert_called_once_with('output_directory')
