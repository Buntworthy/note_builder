import note_builder as nb
import os

datadir = '..'
assets = os.path.join(datadir, 'assets')
css_relative = ['assets/css/tufte.css',
                'assets/css/custom.css']
css = [os.path.join(datadir, css_file) for css_file in css_relative]
output_dir = '../_build'


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
