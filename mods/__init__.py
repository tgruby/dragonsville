import logging
from os.path import dirname, basename, isfile, join
import glob

# list used to store all monster mods
all_definitions = []

monster_definitions = []

# list used to store all character mods
character_definitions = []

# list use to store all item definitions
item_definitions = []

# Load definitions (dictionary objects) from a file directory.  This is used to add additional characters, mods,
# and items.
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

# Load all the monster definitions (dictionary objects) from the mods directory.
for m in __all__:
    if m.object_definition == "monster":
        monster_definitions.append(m.object_definition)
    elif m.object_definition == "character":
        character_definitions.append(m.object_definition)
    elif m.object_definition == "item":
        item_definitions.append(m.object_definition)

logger = logging.getLogger('dragonsville')
logger.debug(monster_definitions)
logger.debug(character_definitions)
logger.debug(item_definitions)
