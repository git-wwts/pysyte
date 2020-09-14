"""Classes for configuration"""

from configparser import ConfigParser as IniParser
from dataclasses import dataclass

from yamlreader import yaml_load

from pysyte.types import paths
from pysyte.types.dictionaries import NameSpaces
from pysyte.types.paths import FileTypes


class PysyteConfiguration(NameSpaces):
    def __init__(self, stem):
        self.path = self.as_path(stem)
        self.data = self.load(self.path) if self.path else {}
        super().__init__(self.data)

    def extensions(self):
        raise NotImplementedError

    def as_path(self, stem_):
        stem = paths.path(stem_)
        for extension in self.extensions():
            try:
                file = stem.extend_by(extension)
                if file.isfile():
                    return file
            except TypeError:
                pass
            return paths.path(None)


class YamlConfiguration(PysyteConfiguration):
    """Read a yaml config file and parse it to attributes"""

    def load(self, path):
        return yaml_load(path)

    def extensions(_):
        return ('yml', 'yaml')

class ModuleConfiguration(YamlConfiguration):
    def extensions(_):
        return ('yaml', )


class YamlParser:
    """This exists to mimic IniParser"""
    def __init__(self, path_):
        pass

    def read(self, string):
        pass


class IniConfiguration(PysyteConfiguration):

    def load(self, string):
        parser = IniParser()
        parser.read(string)
        data = {}
        for section in parser.sections():
            section_key = section.replace('-', '_')
            data[section_key] = {}
            for option in parser.options(section):
                option_key = option.replace('-', '_')
                data[section][option_key] = parser[section][option]
        result = NameSpaces(data)
        return data

    def extensions(_):
        return ('ini', 'cfg')


@dataclass
class ConfigPathsData:
    paths: list


class ConfigPaths(ConfigPathsData):
    def __init__(self, paths):
        super().__init__([_ for _ in paths if _])
        self.file_types = FileTypes([
            (YamlConfiguration, 'yml'),
            (YamlConfiguration, 'yaml'),
            (IniConfiguration, 'ini'),
        ])


    def configs(self, name):
        for path_ in self.paths:
            path__ = path_ / name
            for typed in list(self.file_types.typed(path__)):
                if not typed:
                    continue
                yield typed

    def files(self, name):
        for path_ in self.paths:
            path__ = path_ / name
            for file in list(self.file_types.files(path__)):
                if not file:
                    continue
                yield file

    def config(self, name):
        result = {}
        for config in self.configs(name):
            result.update(config)
        return result

    def append(self, path_):
        if path_ in self.paths:
            return self
        return ConfigPaths(self.paths + [path_])
