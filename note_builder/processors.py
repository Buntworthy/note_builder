from collections import namedtuple
import re
from datetime import datetime

import tinydb

Measurement = namedtuple('Measurement', ['notes', 'lines', 'words'])

pattern = re.compile('[^a-zA-Z\d\s:]+', re.UNICODE)

def measure(content):
    num_lines = 0
    num_words = 0
    num_notes = 1

    for line in content.splitlines():
        line = pattern.sub('', line)

        words = line.split()
        if len(words) > 0:
            num_lines += 1
            num_words += len(words)

    return Measurement(num_notes, num_lines, num_words)

def measure_notes(notes):
    all_lines = 0
    all_words = 0
    all_notes = 0

    for note in notes:
        note_measurement = measure(note.content)
        all_notes += note_measurement.notes
        all_lines += note_measurement.lines
        all_words += note_measurement.words

    return Measurement(all_notes, all_lines, all_words)

class Quantifier(object):

    def __init__(self, db_path):
        self.db_path = db_path

    def process(self, notes):
        measurement = measure_notes(notes)
        self.record(measurement)

    def record(self, measurement):
            db = tinydb.TinyDB(self.db_path)
            now = datetime.now()
            time_format = '%Y-%m-%d %H:%M:%S'
            db.insert({
                'time': now.strftime(time_format),
                'notes': measurement.notes,
                'lines': measurement.lines,
                'words': measurement.words,
            })
