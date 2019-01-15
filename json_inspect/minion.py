import collections
import hashlib
import json


def minion_generator(data, tier=0):
    """Generates a minion of the proper subclass based on data type.
    
    Returns:
        Minion subclass based on the data type.
    """

    if isinstance(data, dict):
        return DictMinion(data, tier=tier)
    if isinstance(data, list):
        return ListMinion(data, tier=tier)
    return EdgeMinion(data, tier=tier)


def build_model(data, tier=0):
    """Builds data model based on data type.

    Args:
        data: The data to be built into a model.
        tier: Optional tier value that will be passed down through
            the model/minion creation process.
    
    Note:
        The use of OrderedDict is required for proper hashing of the
        model. Dict objects do not have a guarantee of order which
        means the object could hash differently depending on key order.
        Notice that we use OrderedDict and then add the keys in a
        sorted order to preserve consistent hashing for comparisons.

    Returns:
        The appropriate minion based on data type.

    """

    if isinstance(data, dict):
        sorted_keys = sorted(data.keys())
        ordered_dict = collections.OrderedDict()  # For consistent hashing
        for key in sorted_keys:
            ordered_dict[key] = minion_generator(data[key], tier=tier)
        return ordered_dict

    if isinstance(data, list):
        return [minion_generator(item, tier=tier) for item in data]
    return minion_generator(data, tier=tier)


def hasher(data):
    """Hashes a json-valid object so that it can be compared to others.
    
    Args:
        data: A JSON-serializable structure.
    
    Returns:
        MD5 Hex Digest of the json-data.
    """

    json_ = json.dumps(data)
    bytes_ = json_.encode("utf-8")  # Bytes equired for use with hashlib.mmd5()
    return hashlib.md5(bytes_).hexdigest()


class Minion:
    """Base class for all minions.

    Attributes:
        _data (str, list, dict): Data that will be converted to a
            Minion. This should be any data pulled from a JSON log.
        edge (bool): True if this is an edge minion. False if this is
            a ListMinion or DictMinion, and therefore, not an edge.
        tier (int): The tier this Minion is part of. For example:
            {
                'object_1': {
                    'where': 'I would be in tier 1',
                    'object_2': {
                        'where': 'I would be in tier 2',
                    }
                }
            }
        label (str): The string to be displayed in the model. 'LIST',
            'DICT', or 'edge'.
        _model (dict, list, str): The actual structure containing
            child minions. For example, if current minion is a LIST
            minion:
                [EdgeMinion, DictMinion, ListMinion, EdgeMinion]
            DICT minion:
                {'first': 'EdgeMinion', 'second': 'ListMinion', etc}
    """

    def __init__(self, data=None, label=None, tier=0):
        # Holds base value if an Edge minion
        if label == "edge":
            self._data = data
            self.edge = True
        else:
            self._data = None
            self.edge = False
        self.tier = tier
        self.label = label
        # List or Dict holding child minions unless data will generate
        # an EdgeMinion
        if not self.edge:
            next_tier = self.tier + 1
            self._model = build_model(data, tier=next_tier)

    def data(self, resolution=1):
        """ Look to the specified tier and pull back all data at that
            tier.

            example:
                >>> log = {
                        'key1': 'value1',
                        'key2': {
                            'key3': {
                                'key4': 'value2',
                            }
                        },
                        'key5': ['hello', 'world'],
                    }
                >>> minion = Minion(data=log)
                >>> minion_data = minion.data(tier=1)
                >>> print(json.dumps(minion_data, indent=4))
                {
                    'key1': 'value1',
                    'key2': {
                        'key3': 'DICT',
                    },
                    'key5': ['hello', 'world']
                }

        Args:
            tier (int): The tier that we want data from. If there is
                more data past the tier specificed, then we will
                return a label for the non-edge minions. See example
                above.

        Returns:
            list, dict, str: The actual dict, list, or string that
                contains relevant log data or label
        """

        if resolution == -1:
            resolution = self.depth
        return self._recursive_data(resolution)

    def model(self, resolution=1):
        if resolution == -1:
            resolution = self.depth
        return self._recursive_model(resolution)

    @property
    def depth(self):
        """ Deepest tier from this Minion's child Minions """
        pass

    @depth.getter
    def depth(self):
        """ Returns the tier of the current Minion

        This method should be overridden if you wish to return
        anything other than the curren tier."""
        return self._recursive_depth()

    def hash(self, resolution=1):
        model = self.model(resolution=resolution)
        return hasher(model)

    def _recursive_depth(self):
        """ Returns the tier of the current Minion

        This method should be overridden if you wish to return
        anything other than the curren tier.
        """
        return self.tier

    def _recursive_data(self, tier):
        """ Returns the data that this Minion represents.

        This method should be overriden if you wish to return anything
        other than the literal data within this Minion.
        """

        return self._data

    def _recursive_model(self, resolution):
        """ Returns the lable as representation of the current Minion's
        model.

        This method should be overriden if you wish to return anything
        other than the label of the current Minion
        """

        return self.label

    def __str__(self):
        return str(self.model(-1))


class DictMinion(Minion):
    """ Minion that is structured as an OrderedDict

    DictMinion is generated from a JSON object.  self._model will be
    an OrderedDict of key:value pairse where the values will be a
    Minion-derived object.

    Example:
        >>> log = {
                'key1': 'value1',
                'key2': {
                    'key3': {
                        'key4': 'value2',
                    }
                },
                'key5': ['hello', 'world'],
            }
        >>> minion = DictMinion(data=log)
        >>> minion._model
        {'key1': EdgeMinion, 'key2': DictMinion, 'key5': ListMinion}
    """

    def __init__(self, dictionary, tier=1):
        """ See Minion class """
        super().__init__(data=dictionary, label="DICT", tier=tier)

    def _recursive_depth(self):
        """ Returns the deepest tier associated with the current
        Minion.

        Return the deepest tier returned from the child Minions.

        The return value is first set to the current Minion's tier so
        that if there are no child Minions, the current Minion's will
        be returned.

        Returns:
            int: The deepest tier found from the child minions. If no
                child minions, then the tier of the current minion.
        """

        # Default deepest tier is the current Minion's tier
        deepest = self.tier
        # Get deepest tier from all child Minions
        for v in self._model.values():
            depth = v.depth
            if depth > deepest:
                deepest = depth
        return deepest

    def _recursive_data(self, resolution):
        """ Overrides super()._recursive_data to be specific for a
        dict.

        Since this object is considered an OrderedDict, we will
        perform dict comprehension to pull out the data values from
        the values within the dictionary.

        If this object is actually in the tier which we are stopping on,
        then, we just return a label instead.

        Args:
            resolution (int): How deep you want to traverse the data
                for results

        Returns:
            dict: Dictionary of the data
            str: Label of the current Minion
        """

        if not (resolution < self.tier):
            return {k: v.data(resolution) for k, v in self._model.items()}
        return self.label

    def _recursive_model(self, resolution):
        """ Overrides super()._recursive_model to be specific for a
        dict.

        Since the current object is a dict of key:value pairs where the
        values are Minions, we may need to return the model of the
        Minions if the resolution specified requires it.

        If this object is actually in the tier which we are stopping
        on, then we just return a label instead.

        Args:
            resolution (int): How deep you want to traverse the model
                for results

        Returns:
            dict: Dictionary of the model
            str: Label of the current Minion
        """

        if not (resolution < self.tier):
            for v in self._model.values():
                if not v.edge:
                    return {k: v.model(resolution) for k, v in self._model.items()}
            # If the dict has nothing but edges as values, just return
            # a string of the keys.
            if not self._model:
                return "EMPTY_{}".format(self.label)
            return "DICT_KEYS: {}".format(str(list(self._model.keys())))
        return self.label


class ListMinion(Minion):
    """ Minion that is structured as a list.

    ListMinion is generated from a JSON list.  self._model will be
    an list of Minion derived objects.

    Example:
        >>> log = ['hello', {'key': 'value'}, ['inner', 'list']]
        >>> minion = ListMinion(data=log)
        >>> minion._model
        [EdgeMinion, DictMinion, ListMinion]
    """

    def __init__(self, list_, tier=0):
        super().__init__(data=list_, label="LIST", tier=tier)

    def _recursive_depth(self):
        """ Returns the deepest tier associated with the current
        Minion.

        Return the deepest tier returned from the child Minions.

        The return value is first set to the current Minion's tier so
        that if there are no child Minions, the current Minion's will
        be returned.

        Returns:
            int: The deepest tier found from the child minions. If no
                child minions, then the tier of the current minion.
        """

        # Default deepest tier is the current Minion's tier
        deepest = self.tier
        # Get deepest tier from all child Minions
        for item in self._model:
            depth = item.depth
            if depth > deepest:
                deepest = depth
        return deepest

    def _recursive_data(self, resolution):
        """ Overrides super()._recursive_data to be specific for a
        list.

        Since this object is a list of Minions, we will need to pull
        out the data from each minion if data is needed in the tier
        below the current Minion.

        Args:
            resolution (int): How deep you want to traverse the data
                for results

        Returns:
            list: List of the data
            str: Label of the current Minion
        """
        if resolution >= self.tier:
            # Only summarize if the next tier is the final tier.
            if resolution == self.tier:
                return self.get_summary()
            # If resolution is >2 from this tier, return the data
            # like normal.
            return [item.data(resolution) for item in self._model]
        
        # Base case - no more children
        return self.label

    def _recursive_model(self, resolution):
        """ Overrides super()._recursive_model to be specific for a
        list.

        Since the current object is a list of Minions, we will need to
        pull out the models from each minion if the model is needed in
        the tier below the current Minion. However, since we need to
        identify unique models based on nesting throughout the program,
        we do not care about the quantity of EdgeMinions in the list:
            - If the list contains all EdgeMinions, return
              ["empty_list"] because we want a list of 2 EdgeMinions to
              produce the same hash as a list of 20 EdgeMinions for
              flattening purposes.
            - If the list contains at least 1 dict or list, then we
              return the actual model because we want to consider this
              unique from a list of all EdgeMinions for flattening
              purposes.

        If this object is actually in the tier which we are stopping
        on, then we just return a label instead.

        Args:
            resolution (int): How deep you want to traverse the model
                for results

        Returns:
            list: List of the model children or surrogate string
            str: Label of the current Minion
        """

        if resolution >= self.tier:
            for minion in self._model:

                if not minion.edge:
                    # Only summarize if the next tier is the final tier
                    if resolution == self.tier:
                        return self.get_summary()
                    # If resolution is >2 from this tier, return the
                    # models like normal.
                    return [item.model(resolution) for item in self._model]

            if not self._model:
                return "EMPTY_{}".format(self.label)
            return ["edges_only"]

        # Base case - no more children.
        return self.label
    
    def get_summary(self):
        types = set()
        for minion in self._model:
            if isinstance(minion, DictMinion):
                types.add("DICT(s)")
            elif isinstance(minion, ListMinion):
                types.add("LIST(s)")
            else:
                types.add("edge(s)")
        return sorted(list(types))


class EdgeMinion(Minion):
    """Minion that represents an edge of the JSON object.

    This means there is no child data of this value in the JSON object.

    For example, in the dictionary,
    {"hello": {"somekey": 'edge-value'}, "world": "usa"} the values
    "edge-value" and "usa" would be edges.
    """

    def __init__(self, edge_item, tier=1):
        super().__init__(data=edge_item, label="edge", tier=tier)
        self.edge = True
