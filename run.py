import note_builder as nb

import os
import json

with open('config.json', 'r') as read_file:
    config = json.load(read_file)

datadir = '.'
assets = os.path.join(datadir, config['assets'])
css_relative = config['css']
css = [os.path.join(datadir, css_file) for css_file in css_relative]
output_dir = config['output']


note_files = nb.find_notes(datadir)
notes = nb.load_notes(note_files)
renderer = nb.HtmlRenderer(assets=assets, css=css)
quantifier = nb.processors.Quantifier(os.path.join(datadir, 'stats_db'))
tagger = nb.processors.TagIndex()
gallery = nb.processors.Gallery()

builder = nb.Builder()

builder.add_processor(quantifier)
builder.add_processor(tagger)
builder.add_processor(gallery)

builder.add_renderer(quantifier)
builder.add_renderer(tagger)
builder.add_renderer(gallery)
builder.add_renderer(renderer)

notes = builder.process(notes)
builder.render(output_dir, notes)
