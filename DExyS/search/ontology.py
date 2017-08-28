from owlready import *

import config

print(config.ROOT_DIR+config.ontology['path'])
# onto_path.append(config.ROOT_DIR)
onto = get_ontology('file://'+config.ROOT_DIR+config.ontology['path'])
onto.load()