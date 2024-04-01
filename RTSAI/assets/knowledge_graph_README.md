Each knowledge graph contains three tab separated files. 

named_entity.tsv
Fields: <entity_name> <prototype_name>

prototype.tsv
Fields: <prototype_name_1> <prototype_relationship> <prototype_name_2>

relationship.tsv
Fields: <entity_name_1 OR prototype_name_1> <relationship> <entity_name_2 OR prototype_relationship>, overriding those defined in prototype.tsv