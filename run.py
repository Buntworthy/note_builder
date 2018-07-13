import note_builder as nb
import os

datadir = '..'
output_dir = '../_build'
note_files = nb.find_notes(datadir)
notes = nb.load_notes(note_files)
renderer = nb.HtmlRenderer(assets=os.path.join(datadir, 'assets'))
quantifier = nb.processors.Quantifier(os.path.join(datadir, 'stats_db'))
tagger = nb.processors.TagIndex()

builder = nb.Builder()

builder.add_processor(quantifier)
builder.add_processor(tagger)

builder.add_renderer(quantifier)
builder.add_renderer(tagger)
builder.add_renderer(renderer)

notes = builder.process(notes)
builder.render(output_dir, notes)
