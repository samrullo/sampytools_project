from typing import Dict, Any, Union, Optional, Iterable

class NominalToken:
    """
    Nominal token class to represent constant values and can be used as dictionary keys.
    Tokens with the same name are identical in equality comparison.
    """

    def __init__(self, name: str) -> None:
        """
        constructor.

        :param name: Token name
        """
        self._name = name

    @property
    def name(self) -> str:
        """
        Token name

        :return: Token name
        """
        return self._name

    def __eq__(self, other: Any):
        """
        Override '==' and '!=' operator

        :param other: Value to compare with
        :return: True if the other value is a NominalToken with the same name, else False
        """
        if isinstance(other, NominalToken):
            return self._name == other.name
        return False

    def __hash__(self):
        """
        Override hash().
        NominalToken with the same name will have the same hash value

        :return: Hashcode
        """
        return hash('NominalToken' + self.name)

    def __repr__(self):
        """
        String representation

        :return: String representation
        """
        return f'[{self.name}]'


KeyType = Union[str, NominalToken]


class ConfigDict:
    """
    ConfigDict is a dictionary-like data structure to set and store multiple level configuration.
    The dictionary itself can be easily serialized into JSON or string format.
    """

    __slots__ = '__dict__'

    def __init__(self, preset: Optional[Dict[KeyType, Any]] = None):
        """
        constructor.

        :param preset: Optional dictionary to load config from
        """
        if isinstance(preset, ConfigDict):
            preset = preset.flatten()
        if preset is not None:
            for k, v in preset.items():
                self[k] = v

    def flatten(self) -> Dict[KeyType, Any]:
        """
        Create the flat version of itself.

        :return: A single level dictionary that maps dot-connected config path to their values.
        Empty sub-dictionary will be removed
        """
        result: Dict[KeyType, Any] = {}
        for k, v in [*self.__dict__.items()]:
            if isinstance(v, ConfigDict):
                sub = v.flatten()
                if not len(sub):
                    del self.__dict__[k]
                else:
                    for sub_k, sub_v in sub.items():
                        result[f'{k}.{sub_k}'] = sub_v
            else:
                result[k] = v
        return result

    def get(self, key: KeyType, default: Any = None) -> Any:
        """
        Try to get value for a specific config path and return default value if not found or the value is a sub dictionary

        :param key: Dot-connected config path
        :param default: Optional default value, by default is None
        :return: Configuration value
        """
        item = self[key]
        if isinstance(item, ConfigDict):
            return default
        return item

    def update(self, another: 'Union[ConfigDict, Dict[KeyType, Any]]') -> None:
        """
        Update configuration from another ConfigDict or a dictionary

        :param another: Another ConfigDict or a dictionary that maps string to values
        """
        override = another
        if isinstance(another, ConfigDict):
            override = another.flatten()
        for k, v in override.items():
            self[k] = v

    def __getitem__(self, key: KeyType):
        """
        Get the value assigned to the key

        :param key: Key
        :return: Value
        """
        if isinstance(key, str) and '.' in key:
            p = key.split('.')
            if p[0] not in self.__dict__:
                self.__dict__[p[0]] = ConfigDict()
            return self.__dict__[p[0]]['.'.join(p[1:])]
        if key not in self.__dict__:
            self.__dict__[key] = ConfigDict()
        return self.__dict__[key]

    def __setitem__(self, key: KeyType, value):
        """
        Set the value to the key

        :param key: Key
        :param value: Value
        """
        if isinstance(key, str) and '.' in key:
            p = key.split('.')
            if p[0] not in self.__dict__:
                self.__dict__[p[0]] = ConfigDict()
            self.__dict__[p[0]]['.'.join(p[1:])] = value
            return
        self.__dict__[key] = value

    def __delitem__(self, key: KeyType):
        """
        Delete key

        :param key: Key to delete
        """
        if key in self.__dict__:
            del self.__dict__[key]
            return

        if isinstance(key, str) and '.' in key:
            p = key.split('.')
            if p[0] in self.__dict__:
                del self.__dict__[p[0]]['.'.join(p[1:])]

    def __getattr__(self, key: str):
        """
        Get the value assigned to the key

        :param key: Key
        :return: Value
        """
        return self[key]

    def __setattr__(self, key: str, value):
        """
        Set the value to the key

        :param key: Key
        :param value: Value
        """
        self[key] = value

    def __delattr__(self, key: str):
        """
        Delete key

        :param key: Key to delete
        """
        del self[key]

    def __repr__(self):
        """
        String representation

        :return: String representation
        """
        return self.flatten().__repr__()

    def __len__(self):
        """
        override __len__

        :return: Numbers of keys stored
        """
        return len(self.flatten())

    def __contains__(self, key: KeyType):
        """
        override in operator.

        :param key: Key to check
        :return: True if the key exists
        """
        return key in self.__dict__ or key in self.flatten()

    def __dir__(self) -> Iterable[str]:
        """
        override dir()

        :return: Key to existing elements and methods
        """
        yield from ('get', 'flatten', 'update')
        self.flatten()
        for key in self.__dict__:
            yield str(key)
