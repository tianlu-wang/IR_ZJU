__author__ = 'wenri'

from Index.IndexableField import IndexableField

class Document(object):
    def __init__(self):
        self.fields = {}

    def add(self, field: IndexableField):
        self.fields[field.name()] = field

    def getField(self, name: str) -> IndexableField:
        return self.fields[name]

    def getFields(self):
        return self.fields
