import note_builder as nb

import os
import json
import click

@click.command()
@click.option('--stats/--no-stats', default=True)
def build(stats):
    try:
        config = nb.parse_config()
    except FileNotFoundError:
        print('No config file in current directory.')
        return

    note_files = nb.find_notes(config['datadir'])
    notes = nb.load_notes(note_files)
    renderer = nb.HtmlRenderer(assets=config['assets'], css=config['css'])
    quantifier = nb.processors.Quantifier(os.path.join(config['datadir'], 'stats_db'))
    tagger = nb.processors.TagIndex()
    gallery = nb.processors.Gallery()

    builder = nb.Builder()

    if stats:
        builder.add_processor(quantifier)

    builder.add_processor(tagger)
    builder.add_processor(gallery)

    if stats:
        builder.add_renderer(quantifier)

    builder.add_renderer(tagger)
    builder.add_renderer(gallery)
    builder.add_renderer(renderer)

    notes = builder.process(notes)
    builder.render(config['output_dir'], notes)

if __name__ == '__main__':
    build()
