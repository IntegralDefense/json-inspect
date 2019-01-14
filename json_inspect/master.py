import json

from loguru import logger

from json_inspect import minion
from json_inspect import serialize


def _input_type(input_file, input_string):
    """ Helper function to determine input type

    Args:
        input_file (str, None): The file name to be read from.
        input_string (str, None): JSON-serializable string.

    Returns:
        str: 'file' if input type is a file name. 'string' if
            input type is a JSON-serializable string.
        None: If input is neither a file name or JSON-serializable
            string.
    """

    if input_file:
        return "file"
    elif input_string:
        return "string"
    else:
        return None


class MinionGarage:
    """ Holds minions and performs tasks on minions in bulk.

    Attributes:
        _list (list): A list of minions. One minion per log line.
    """

    def __init__(self):
        self._list = []

    def append(self, data):
        """ A wrapper for the 'append' attribute of self._list

        This allows us to take a raw log line and then convert it
        into a minion before appending to the list.

        Args:
            data (list, dict, str, int): The data to be converted into
                a minion and appended to the minion list.
        """

        new_minion = minion.minion_generator(data)
        self._list.append(new_minion)

    def hashes(self, resolution=1):
        """ Returns a set of unique hashes that represent unique log
        models.

        We first filter out the minions based on their tier. We don't
        want to compare hashes for tier 1 and tier 2, because logs
        with a tier 1-only model do not need to be flattend. In the
        same sense, tier 3 logs need to be flattend more than tier 2
        logs.

        Args:
            resolution (int): The tier we wish to pull hashes from.
                This will actually pull hashes from any model that has
                the specified resolution and greater.

        Returns:
            set: Set of MD5 hexdigest strings for each unique log model
        """

        filtered_list = [minion for minion in self._list if minion.depth >= resolution]
        return {minion.hash(resolution) for minion in filtered_list}

    def count(self, tier=1):
        """ Count the number of minions in a tier

        Args:
            tier (int): The minions will only be counted if the minion
                has a depth >= this argument.

        Returns:
            int: The count of the minions filtered out by the tier
                requirement.
        """

        filtered_list = [minion for minion in self._list if minion.depth >= tier]
        return len(filtered_list)

    @property
    def depth(self):
        pass

    @depth.getter
    def depth(self):
        """ Return the deepest tier of all the minions.

        Returns:
            int: The deepest tier of all the minions.
        """

        deepest = 0
        for minion in self._list:
            minion_depth = minion.depth
            if not (minion_depth > deepest):
                continue
            deepest = minion_depth
        return deepest

    def uniques(self, tier=1):
        filtered_list = [minion for minion in self._list if minion.depth >= tier]
        return {minion.hash(tier): minion for minion in filtered_list}

    def __getattr__(self, item):
        return getattr(self._list, item)

    def __len__(self):
        return len(self._list)

    def __str__(self):
        return str(self._list)


class Master:
    """ This is the class used as an interface into the
    minions / minion garage.

    Attributes:
        input (str): Input file name or a string containing logs in
            json-serializable format.
        input_type (str): Indicates what type of input is being used.
        minions (MinionGarage): The MinionGarage that will be where
            we store Minions which represent the input logs.
    """

    def __init__(self, input_file=None, input_string=None):
        """ Init the Master class

        Args:
            input_file (str, None): The filename containing logs to
                parse and convert to Minions.
            input_string (str, None): A json-serializable string.
        """

        self.input = input_file or input_string
        self.input_type = _input_type(input_file, input_string)
        self.minions = MinionGarage()
        self.focus = []
        logger.info(
            f"Configured for input type {self.input_type}. "
            f"Don't forget to run Master.make() to generate the log models!"
        )

    def make(self, input_file=None, input_string=None):
        """ Generates minions based on the input type.

        This method allows the user to manually change the input file
        upon making the minions.

        If no input file or input string is used during this method
        call, the method will generate minions from the input already
        assigned to the 'input' attribute.

        Args:
            input_file (str): The name of the file to read from.
            input_string (str): JSON-serializable string to be parsed.
        """

        if input_file or input_string:
            self.input = input_file or input_string
            self.input_type = _input_type(input_file, input_string)
        if self.input_type == "file":
            self._make_file()
        if self.input_type == "string":
            self._make_string()

    def _make_file(self):
        """ Helper method to generate minions from a file and then
            append them to the minions list.
        """

        json_items = serialize.json_transform_from_file(self.input)
        [self.minions.append(json_) for json_ in json_items]

        logger.info(f"Made models/minions from {len(json_items)} source logs events.")


    def _make_string(self):
        """ Helper method to generate minions from a JSON-serializable
            string.
        """

        json_items = serialize.json_transform(self.input)
        [self.minions.append(json_) for json_ in json_items]

        logger.info(f"Made models/minions from {len(json_items)} source logs events.")

    def count(self, tier=1):
        """ Get the count of minions contained in the MinionGarage """

        return self.minions.count(tier=tier)

    @property
    def depth(self):
        pass

    @depth.getter
    def depth(self):
        return self.minions.depth

    def unique_count(self, resolution=1):
        """ Get the count of unique log models for a any tier >= the
            resolution specified.

        Args:
            resolution (int): The hashes will be pulled from any tier
                that is >= this argument.

        Returns:
            int: The number of unique hashes (representing unique log
                models) for the specified resolution/tier.
        """

        return len(self.minions.hashes(resolution=resolution))

    def print_unique_models(self, resolution=0, indent=None):
        """Prints the hash and model of unique logs for the specified
        resolution
        """

        uniques = self._gather_uniques(resolution)
        unique_models = {
            hash_: minion.model(resolution) for hash_, minion in uniques.items()
        }
        logger.info(f"Model data:\n {json.dumps(unique_models, indent=indent)}")
    
    def print_unique_data(self, resolution=0, indent=None):
        """Prints the hash and data of unique logs for the specified
        resolution.
        """

        uniques = self._gather_uniques(resolution)
        unique_data = {
            hash_: minion.data(resolution) for hash_, minion in uniques.items()
        }
        logger.info(json.dumps(unique_data, indent=indent))

    def write_unique_models(self, output_file, resolution=0, indent=None):
        """Writes the hash and model of unique logs for the specified
        resolution to file.
        """

        with open(output_file, "w+") as wf:
            uniques = self._gather_uniques(resolution)
            unique_models = {
                hash_: minion.model(resolution) for hash_, minion in uniques.items()
            }
            wf.write(json.dumps(unique_models, indent=indent))
            logger.info(f"Wrote {len(uniques)} unique log models to {output_file}.")

    def write_unique_data(self, output_file, resolution=0, indent=None):
        """Writes the hash and data of unique logs for the specified
        resolution to file.
        """

        with open(output_file, "w+") as wf:
            uniques = self._gather_uniques(resolution)
            unique_data = {
                hash_: minion.data(resolution) for hash_, minion in uniques.items()
            }
            wf.write(json.dumps(unique_data, indent=indent))
            logger.info(f"Wrote {len(uniques)} unique log data to {output_file}.")

    def write_unique_data_recursive(self, output_file, resolution=0, indent=None):
        """Writes unique logs to file from the resolution specified.
        
        This will start with the specified resolution, log
        the uniques, and then do one for resolution -= 1. This should
        write only logs that were found to be unique in at least one
        tier. This also prevents duplicating logs that are unique on
        multiple tiers.
        """

        if resolution < 0:
            raise ValueError(
                "Resolution for this function must be greater than or equal to 0."
            )

        master_uniques = dict()

        with open(output_file, "w+") as wf:

            for i in range(resolution, 0, -1):
                uniques = self._gather_uniques(i)
                fresh_uniques = {
                    hash_: model
                    for hash_, model in uniques.items()
                    if hash_ not in master_uniques.keys()
                }
                master_uniques = {**master_uniques, **fresh_uniques}
            
            logger.info(f"Printing {len(master_uniques.values())} unique log data.")

            for minion in master_uniques.values():
                json_string = json.dumps(minion.data(resolution), indent=indent)
                wf.write("{}\n".format(json_string))

    def _gather_uniques(self, resolution=0):
        return self.minions.uniques(resolution)
