import os

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

    def render(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)
            
        for renderer in self.renderers:
            renderer.render(directory)
