class Builder(object):

    def __init__(self):
        self.processors = []

    def add_processor(self, processor):
        self.processors.append(processor)

    def process(self, notes):
        for processor in self.processors:
            notes = processor.process(notes)

        return notes
