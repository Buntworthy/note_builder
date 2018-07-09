import note_builder as nb

datadir = '..'
output_dir = '/mnt/c/Temp'
note_files = nb.find_notes(datadir)
notes = nb.load_notes(note_files)
renderer = nb.HtmlRenderer(assets='../assets')
quantifier = nb.processors.Quantifier('test_db')
tagger = nb.processors.TagIndex()

builder = nb.Builder()

builder.add_processor(quantifier)
builder.add_processor(tagger)

builder.add_renderer(quantifier)
builder.add_renderer(tagger)
builder.add_renderer(renderer)

notes = builder.process(notes)
builder.render(output_dir, notes)
