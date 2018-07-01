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

def test_measurement_db(tmpdir):
    test_db = tmpdir.mkdir('db').join('test.db')
    measurement = note_builder.processors.Measurement(1, 2, 3)
    db = note_builder.processors.MeasurementDb(test_db)

    db.record(measurement)
    loaded = db.load()

    assert len(loaded) == 1

    (_, loaded_measurement) = loaded[0]
    assert loaded_measurement == measurement

def test_measurement_db_existing(tmpdir):
    test_db = tmpdir.mkdir('db').join('test.db')
    measurement1 = note_builder.processors.Measurement(1, 2, 3)
    measurement2 = note_builder.processors.Measurement(30, 20, 10)
    db = note_builder.processors.MeasurementDb(test_db)
    db.record(measurement1)

    del db

    new_db = note_builder.processors.MeasurementDb(test_db)
    new_db.record(measurement2)

    loaded = new_db.load()

    assert len(loaded) == 2

    (_, loaded_measurement1) = loaded[0]
    (_, loaded_measurement2) = loaded[1]
    assert loaded_measurement1 == measurement1
    assert loaded_measurement2 == measurement2


def test_quantifier(tmpdir):
    note1 = note_builder.Note(name='note_1',
                                content = '# Note 1\n\ncontent\n')
    note2 = note_builder.Note(name='note_2',
                                content = '# Second Note\nSome new content\n')
    note_list = [note1, note2]
    test_db = tmpdir.mkdir('db').join('test.db')
    quantifier = note_builder.processors.Quantifier(test_db)

    quantifier.process(note_list)
    quantifier.render(tmpdir, [])

    assert os.path.isfile(tmpdir.join('statistics.html'))
