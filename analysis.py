# Count number of knowledge base articles and total number of lines
from glob import glob
import os
from  datetime import datetime
import tinydb
import pygal
from build import files_in

def get_counts(filename):
    number_lines = 0
    number_words = 0

    with open(filename) as f:
        for line in f:
            words = line.split()
            if len(words) > 1:
                number_lines += 1
                number_words += len(words)

    return (number_lines, number_words)

def make_chart(filename, title, dates, data):
    datetimeline = pygal.DateTimeLine(
        x_label_rotation=35, truncate_label=-1,
        x_value_formatter=lambda dt: dt.strftime('%d, %b %Y'))
    datetimeline.title = title
    datetimeline.add('', list(zip(dates, data)))
    datetimeline.render_to_file(filename)


if __name__ == '__main__':
    db = tinydb.TinyDB('test.json')
    base_directory = os.path.expanduser('~/notes')
    destination = 'build'
    assets = 'assets'

    num_articles = 0
    line_numbers = []
    word_numbers = []

    for article in glob(os.path.join(base_directory, '*.md')):
        print('Quantifying ' + article)
        (lines, words) = get_counts(article)
        num_articles += 1
        line_numbers.append(lines)
        word_numbers.append(words)

    now = datetime.now()

    total_lines = sum(line_numbers)
    lines_per_article = sum(line_numbers)/num_articles

    total_words = sum(word_numbers)
    words_per_article = sum(word_numbers)/num_articles

    time_format = '%Y-%m-%d %H:%M:%S'
    db.insert({
        'time': now.strftime(time_format),
        'articles': num_articles,
        'lines': total_lines,
        'lines_per': lines_per_article,
        'words': total_words,
        'words_per': words_per_article,
    })

    data = db.all()
    dates = [datetime.strptime(t['time'], time_format) for t in data]
    make_chart('articles.svg', 'articles', dates, [a['articles'] for a in data])
    make_chart('lines.svg', 'lines', dates, [a['lines'] for a in data])
    make_chart('lines_per.svg', 'lines_per', dates, [a['lines_per'] for a in data])
    make_chart('words.svg', 'words', dates, [a['words'] for a in data])
    make_chart('words_per.svg', 'words_per', dates, [a['words_per'] for a in data])
