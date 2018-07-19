import os
import shutil


class Builder(object):

    def __init__(self):
        self.processors = []
        self.renderers = []

    def add_processor(self, processor):
        self.processors.append(processor)

    def add_renderer(self, renderer):
        self.renderers.append(renderer)

    def process(self, notes):
        for processor in self.processors:
            notes = processor.process(notes)

        return notes

    def render(self, directory, notes):
        self._clean(directory)

        for renderer in self.renderers:
            renderer.render(directory, notes)

    def _clean(self, directory):
        if os.path.isdir(directory):
            shutil.rmtree(directory)
        os.mkdir(directory)
