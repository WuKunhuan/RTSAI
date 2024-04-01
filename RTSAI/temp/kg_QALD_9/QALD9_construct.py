
import json

current_environment = None
current_knowledge_graph = "QALD_9"

preprocessed_data_location = f"QALD9_train.json"
with open(preprocessed_data_location, 'r') as f:
    data = json.load(f)
    f.close()

all_entity_round_1 = set()
for question_object in data: 
    for uri_object in question_object["answer"]: 
        all_entity_round_1.add(uri_object["uri"].split('/')[-1].replace('_', ' ').strip())

all_entity_round_1 = sorted(list(all_entity_round_1))
print (all_entity_round_1[0:100])
print (f"\nTotal length: {len(all_entity_round_1)}")





################ Stage 2 ################

import csv

# Define the paths to the QALD9 dataset and the countries dataset
qald9_rel_path = f"{current_knowledge_graph}/relationship.tsv"
qald9_named_entity_path = f"{current_knowledge_graph}/named_entity.tsv"
qald9_prototype_path = f"{current_knowledge_graph}/prototype.tsv"
countries_rel_path = "countries/relationship.tsv"
countries_named_entity_path = "countries/named_entity.tsv"
countries_prototype_path = "countries/prototype.tsv"

with open(countries_rel_path, 'r') as countries_rel_file, open(qald9_rel_path, 'a') as qald9_rel_file:
    countries_rel_reader = csv.reader(countries_rel_file)
    qald9_rel_writer = csv.writer(qald9_rel_file)
    for row in countries_rel_reader:
        qald9_rel_writer.writerow(row)

with open(countries_named_entity_path, 'r') as countries_named_entity_file, open(qald9_named_entity_path, 'a') as qald9_named_entity_file:
    countries_named_entity_reader = csv.reader(countries_named_entity_file, delimiter='\t')
    qald9_named_entity_writer = csv.writer(qald9_named_entity_file, delimiter='\t')
    for row in countries_named_entity_reader:
        qald9_named_entity_writer.writerow(row)
    # Add entities from the list
    for entity in all_entity_round_1: 
        qald9_named_entity_writer.writerow([entity, "Object"])

with open(countries_prototype_path, 'r') as countries_prototype_file, open(qald9_prototype_path, 'a') as qald9_prototype_file:
    countries_prototype_reader = csv.reader(countries_prototype_file, delimiter='\t')
    qald9_prototype_writer = csv.writer(qald9_prototype_file, delimiter='\t')
    for row in countries_prototype_reader:
        qald9_prototype_writer.writerow(row)

# Add links between entities in relationship.tsv
with open(qald9_named_entity_path, 'r') as qald9_named_entity_file, open(qald9_rel_path, 'a') as qald9_rel_file:
    qald9_named_entity_reader = csv.reader(qald9_named_entity_file, delimiter='\t')
    qald9_rel_writer = csv.writer(qald9_rel_file, delimiter='\t')
    for row in qald9_named_entity_reader: 
        if (not row): continue
        entity = row[0]
        if entity.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            entity_new = ' '.join(entity.split(" ")[1:])
            if (entity_new.startswith("in ")): 
                entity_new = entity_new [3:]
            qald9_rel_writer.writerow([entity, 'has_num', entity_new])

print("Import completed successfully.")








named_entity_file = (f"{current_knowledge_graph}/named_entity.tsv")


