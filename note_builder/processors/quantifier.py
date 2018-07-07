from .. import core

from collections import namedtuple
from collections import defaultdict
import re
import os
from datetime import datetime

import tinydb
import pygal
from jinja2 import Environment, PackageLoader, select_autoescape

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


class MeasurementDb(object):

    def __init__(self, db_path):
        self.db_path = db_path
        self.db = tinydb.TinyDB(self.db_path)
        self.time_format = '%Y-%m-%d %H:%M:%S'

    def record(self, measurement):
        now = datetime.now()
        self.db.insert({
            'time': now.strftime(self.time_format),
            'notes': measurement.notes,
            'lines': measurement.lines,
            'words': measurement.words,
        })

    def load(self):
        db_contents = self.db.all()
        all_measurements = []

        for entry in db_contents:
            time = datetime.strptime(entry['time'], self.time_format)
            measurement = Measurement(entry['notes'],
                                      entry['lines'],
                                      entry['words'])
            all_measurements.append((time, measurement))

        return all_measurements


class Quantifier(object):

    def __init__(self, db_path):
        self.output_name = 'statistics.html'
        self.db = MeasurementDb(db_path)

        self.statistics = {
            'Total Notes':
                lambda data: [(t, x.notes) for (t, x) in data],
            'Total Lines':
                lambda data: [(t, x.lines) for (t, x) in data],
            'Lines per Note':
                lambda data: [(t, x.lines/x.notes) for (t, x) in data],
            'Total Words':
                lambda data: [(t, x.words) for (t, x) in data],
            'Words per note':
                lambda data: [(t, x.words/x.notes) for (t, x) in data],
        }

    def process(self, notes):
        measurement = measure_notes(notes)
        self.db.record(measurement)
        return notes

    def render(self, directory, _):
        data = self.db.load()
        graph_names = []

        for (name, func) in self.statistics.items():
            filepath = os.path.join(directory, name + '.svg')
            graph_names.append(filepath)
            self._make_chart(filepath, name, func(data))

        self._make_html(directory, graph_names)

    def _make_chart(self, filepath, title, data):
        datetimeline = pygal.DateTimeLine(
            x_label_rotation=35,
            truncate_label=-1,
            x_value_formatter=lambda dt: dt.strftime('%d, %b %Y'))
        datetimeline.title = title
        datetimeline.add('', data)
        datetimeline.render_to_file(filepath)

    def _make_html(self, directory, graph_names):
        output_path = os.path.join(directory, self.output_name)
        with open(output_path, 'w') as out_file:
            env = Environment(
                loader=PackageLoader('note_builder', 'templates'),
                autoescape=select_autoescape(['html', 'xml'])
            )
            template = env.get_template('statistics.html')
            out_file.write(template.render(graphs=graph_names))
