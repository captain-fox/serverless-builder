import abc
from collections import OrderedDict

import stringcase
import yaml


class YamlOrderedDict(OrderedDict, yaml.YAMLObject):
    yaml_tag = "!YamlOrderedDict"

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self.get(item)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_dict(data)


class SmartString:
    def __init__(self, val, prefix="", suffix=""):
        self.val = val
        self.prefix = prefix
        self.suffix = suffix

    def __str__(self):
        if not self.val:
            return ""

        return f"{self.prefix}{self.val}{self.suffix}"

    def __call__(self, prefix="", suffix=""):
        return SmartString(self.val, prefix=prefix, suffix=suffix)


class Identifier(yaml.YAMLObject):
    yaml_tag = "Identifier"

    def __init__(self, identifier):
        super().__init__()
        self.identifier = identifier

    @property
    def camel(self):
        return stringcase.camelcase(self.identifier)

    @property
    def pascal(self):
        return stringcase.pascalcase(self.identifier.replace("-", "_"))

    @property
    def snake(self):
        return stringcase.snakecase(self.identifier)

    @property
    def spinal(self):
        return stringcase.spinalcase(self.identifier)

    def __str__(self):
        return self.identifier

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_str(str(data.identifier))


class ProviderMetadata(type(YamlOrderedDict), type(abc.ABC)):
    pass


class Provider(YamlOrderedDict, abc.ABC, metaclass=ProviderMetadata):
    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self.get(item)

    @abc.abstractmethod
    def configure(self, service):
        pass


class Feature(abc.ABC):
    @abc.abstractmethod
    def enable(self, service):
        pass


class Integration(abc.ABC):
    @abc.abstractmethod
    def enable(self, service):
        pass


class PluginMetadata(type(YamlOrderedDict), type(abc.ABC)):
    pass


class Plugin(YamlOrderedDict, abc.ABC, metaclass=PluginMetadata):
    @abc.abstractmethod
    def enable(self, service):
        pass
