from collections import namedtuple
import re

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
