
import json
import collections

import cowstrap.machine

class MachineDictionary(collections.MutableMapping):
    """
    Special case of a dictionary with extra methods for saving and loading.

    The file stores each of the Machines in a nice, editable json format.

    :ivar _file_name: the path to save and load the machine dictionary from
    :type _file_name: local_absolute_path

    :ivar _store: the actual dictionary of data
    :type _store: dict
    """

    def __init__(self, file_name):
        self._store = dict()
        self._file_name = file_name
        self._load()

    def _save(self):
        """
        Save all Machines to our file
        """
        with open(self._file_name, 'wb') as out_file:
            json.dumps(self._store, out_file, sort_keys=True, indent=4, \
                       separators=(',', ': '))

    def _load(self):
        """
        Load all Machines from our file
        """
        with open(self._file_name, 'rb') as in_file:
            obj = json.load(in_file)
            for name, json_dict in obj.viewitems():
                self._store[name] = cowstrap.machine.Machine\
                    .from_dict(json_dict)

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value
        self._save()

    def __delitem__(self, key):
        del self._store[key]
        self._save()

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)
