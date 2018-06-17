from collections import namedtuple
import re

Measurement = namedtuple('Measurement', ['num_lines', 'num_words'])

pattern = re.compile('[^a-zA-Z\d\s:]+', re.UNICODE)

def measure(content):
    num_lines = 0
    num_words = 0

    for line in content.splitlines():
        line = pattern.sub('', line)

        words = line.split()
        if len(words) > 0:
            num_lines += 1
            num_words += len(words)

    return Measurement(num_lines, num_words)

def measure_notes(notes):
    all_lines = 0
    all_words = 0

    for note in notes:
        note_measurement = measure(note.content)
        all_lines += note_measurement.num_lines
        all_words += note_measurement.num_words

    return Measurement(all_lines, all_words)
