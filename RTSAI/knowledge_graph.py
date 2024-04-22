
import os, shutil
from RTSAI.config import DATA_PATH, ASSETS_PATH
from RTSAI.setup_funcs import OBJECT_KEY, RELATIONSHIP_KEY, PROTOTYPE_CHARACTER, NAMED_ENTITY_SYMBOL, PROTOTYPE_SYMBOL, RELATIONSHIP_SYMBOL
from RTSAI.tool_funcs import show_popup_message, new_name_check

debug = 1

'''
named_entity.tsv: 
<named_entity> | <prototype> | #Resource

prototype.tsv: 
<prototype> | <relationship>/is_a | <prototype>/$OBJECT | #Resource
<relationship> | <relationship>/is_a | <prototype>/$RELATIONSHIP | #Resource

relationship.tsv: 
<named_entity> | <relationship> | <named_entity>
<named_entity> | <relationship> | <prototype>
'''

def create_knowledge_graph(graph_name, previous_graph_name = None, showinfo = "print", parent_item = None):
    '''
    Create or rename a Knowledge Graph. 
    Before this function, necessary name checking should be performed. 
    '''
    try: 
        graph_path = os.path.join(DATA_PATH, "knowledge_graphs", graph_name)
        if previous_graph_name:
            previous_graph_path = os.path.join(DATA_PATH, "knowledge_graphs", previous_graph_name)
            if (os.path.exists(previous_graph_path)): 
                os.rename(previous_graph_path, graph_path)
                return 0
            else: 
                if (showinfo == "print"): print(f"Knowledge Graph '{previous_graph_name}' does not exist.")
                else: show_popup_message(f"Knowledge Graph '{previous_graph_name}' does not exist.", parent = parent_item)
                return 1
        else: 
            template_path = os.path.join(ASSETS_PATH, "templates", "template_knowledge_graph")
            shutil.copytree(template_path, graph_path)
            return 0
    except: return 1

def copy_knowledge_graph(existing_graph_name, copied_graph_name, environment_name = None, showinfo = "print", parent_item = None): 
    '''
    Copy an Knowledge Graph. 
    Before this function, necessary name checking should be performed. 
    '''
    if (environment_name): graph_path = os.path.join(DATA_PATH, "environments", environment_name)
    else: graph_path = os.path.join(DATA_PATH, "knowledge_graphs")
    if not os.path.exists(os.path.join(graph_path, existing_graph_name)):
        if (showinfo == "print"): 
            if (environment_name): 
                print(f"Knowledge Graph '{existing_graph_name}' does not exist inside Environment '{environment_name}'. ")
            else: 
                print(f"Knowledge Graph '{existing_graph_name}' does not exist." )
        else: 
            if (environment_name): 
                show_popup_message(f"Knowledge Graph '{existing_graph_name}' does not exist inside Environment '{environment_name}'. ", parent = parent_item)
            else: 
                show_popup_message(f"Knowledge Graph '{existing_graph_name}' does not exist.", parent = parent_item)
        return 1
    elif os.path.exists(os.path.join(graph_path, copied_graph_name)):
        if (showinfo == "print"): 
            if (environment_name): 
                print(f"Knowledge Graph '{copied_graph_name}' already exists inside Environment '{environment_name}'. ")
            else: 
                print(f"Knowledge Graph '{copied_graph_name}' already exists." )
        else: 
            if (environment_name): 
                show_popup_message(f"Knowledge Graph '{copied_graph_name}' already exists inside Environment '{environment_name}'. ", parent = parent_item)
            else: 
                show_popup_message(f"Knowledge Graph '{copied_graph_name}' already exists.", parent = parent_item)
        return 1
    elif (new_name_check(copied_graph_name, graph_path, showinfo = showinfo, parent_item = parent_item) == 0): 
        shutil.copytree(os.path.join(graph_path, existing_graph_name), os.path.join(graph_path, copied_graph_name))
        return 0

def check_knowledge_graph_files(path): 
    if (not os.path.exists(os.path.join(DATA_PATH, path, "named_entity.tsv"))): 
        if (debug == 1): print (f"Knowledge graph {path}'s named_entity.tsv file missing. ")
        return False
    if (not os.path.exists(os.path.join(DATA_PATH, path, "prototype.tsv"))): 
        if (debug == 1): print (f"Knowledge graph {path}'s prototype.tsv file missing. ")
        return False
    if (not os.path.exists(os.path.join(DATA_PATH, path, "relationship.tsv"))): 
        if (debug == 1): print (f"Knowledge graph {path}'s relationship.tsv file missing. ")
        return False
    return True

named_entity_lines = []; prototype_lines = []
named_entity_file_items = []; prototype_file_items = []; 
def check_knowledge_graph_element_exist(target_item, filename, resource = "", mode = "CHECK", 
                                        named_entity_write = [], prototype_write = []): 
    '''
    Check whether the item (named entity, prototype, relationship) exist in the specified file
    '''

    if (not (filename.endswith('.tsv')) or not os.path.exists(filename)): return False
    if (target_item == OBJECT_KEY or target_item == RELATIONSHIP_KEY): return True
    
    # read the prototype file if it is a relationship
    if (filename.endswith('named_entity.tsv')): filename_to_check = 'named_entity.tsv'
    else: filename_to_check = "prototype.tsv"

    global named_entity_lines, prototype_lines, named_entity_file_items, prototype_file_items
    file_items = []
    if (filename_to_check.endswith("named_entity.tsv")): 
        if (not named_entity_file_items): 
            file = open(filename, 'r'); named_entity_lines = file.readlines(); 
            named_entity_lines = [line.replace('\n', '') for line in named_entity_lines]
            file.close(); named_entity_file_items = [items.split('\t')[0] for items in named_entity_lines]
        file_items = named_entity_file_items
        if (debug == 1): print (f"file_items for named_entity.tsv: {file_items}")
    elif (filename_to_check.endswith("prototype.tsv")): 
        if (not prototype_file_items): 
            file = open(filename, 'r'); prototype_lines = file.readlines(); 
            prototype_lines = [line.replace('\n', '') for line in prototype_lines]
            file.close(); prototype_file_items = [items.split('\t')[0] for items in prototype_lines]
        file_items = prototype_file_items
        if (debug == 1): print (f"file_items for prototype.tsv: {file_items}")

    for item in file_items: 
        if (debug == 1): print (item, target_item, item == target_item)
        if (item == target_item): return True
    if (mode == "UPDATE"): 
        if (resource): resource_field = resource
        else: resource_field = f"{PROTOTYPE_CHARACTER}Resource"
        if (filename.endswith('named_entity.tsv')): 
            named_entity_write.append(f"{target_item}\t{OBJECT_KEY}\t{resource_field}")
        elif (filename.endswith('prototype.tsv')): 
            prototype_write.append(f"{target_item}\tis_a\t{OBJECT_KEY}\t{resource_field}")
        elif (filename.endswith('relationship.tsv')): 
            prototype_write.append(f"{target_item}\tis_a\t{RELATIONSHIP_KEY}\t{resource_field}")
        return True
    else: return False

def fast_update_knowledge_graph(path, mode = "CHECK"): 
    '''
    Update the knowledge graphs based on update.tsv file
    Method: Iterate every item specified in update.tsv file. 
    Remove everything in update.tsv after the operation. 
    '''

    if (not check_knowledge_graph_files(path)): return False
    if (not os.path.exists(os.path.join(DATA_PATH, path, "update.tsv"))): return False
    named_entity_file = open(os.path.join(DATA_PATH, path, "named_entity.tsv"), 'r')
    prototype_file = open(os.path.join(DATA_PATH, path, "prototype.tsv"), 'r')
    update_file = open(os.path.join(DATA_PATH, path, "update.tsv"), 'r+')
    update_file_lines = update_file.readlines()

    num_lines = len(update_file_lines)
    target_keys = [NAMED_ENTITY_SYMBOL, PROTOTYPE_SYMBOL, RELATIONSHIP_SYMBOL]
    for line_id in range (num_lines): 
        line_tokens = update_file_lines[line_id].split('\t')
        # update entry: item, type (named_entity | prototype | relationship), resource (resource | None)
        if (len(line_tokens) != 3 or line_tokens[1] not in target_keys): line_tokens = None
        update_file_lines[line_id] = line_tokens

    global named_entity_lines, prototype_lines
    named_entity_lines = []; prototype_lines = []
    named_entity_write = []; prototype_write = []
    named_entity_file_lines = named_entity_file.readlines()
    named_entity_file_lines = [line.replace('\n', '') for line in named_entity_file_lines]
    prototype_file_lines = prototype_file.readlines()
    prototype_file_lines = [line.replace('\n', '') for line in prototype_file_lines]

    update_file_line_tokens = [line for line in update_file_lines if line != None]
    for line_id, line_tokens in enumerate(update_file_line_tokens): 
        if (line_tokens[1] == NAMED_ENTITY_SYMBOL): 
            check_knowledge_graph_element_exist(line_tokens[0], os.path.join(path, 'named_entity.tsv'), line_tokens[2], mode, named_entity_write, prototype_write)
        elif (line_tokens[1] == PROTOTYPE_SYMBOL): 
            check_knowledge_graph_element_exist(line_tokens[0], os.path.join(path, 'prototype.tsv'), line_tokens[2], mode, named_entity_write, prototype_write)
        elif (line_tokens[1] == RELATIONSHIP_SYMBOL): 
            check_knowledge_graph_element_exist(line_tokens[0], os.path.join(path, 'relationship.tsv'), line_tokens[2], mode, named_entity_write, prototype_write)

    '''
    Remove invalid lines in the previous knowledge graphs
    Remove duplicate entries in the write lists
    Update the knowledge graph files
    '''
    named_entity_write = list(set(named_entity_write))
    prototype_write = list(set(prototype_write))
    if (debug == 1): 
        print (f"named_entity_write: {named_entity_write}")
        print (f"prototype_write: {prototype_write}")
    named_entity_file_lines = [line for line in named_entity_file_lines if line != None]
    prototype_file_lines = [line for line in prototype_file_lines if line != None]
    relationship_file_lines = [line for line in relationship_file_lines if line != None]
    named_entity_file_lines = list(set(named_entity_file_lines + named_entity_write))
    prototype_file_lines = list(set(prototype_file_lines + prototype_write))

    named_entity_file.close(); named_entity_file = open(os.path.join(DATA_PATH, path, "named_entity.tsv"), 'w')
    prototype_file.close(); prototype_file = open(os.path.join(DATA_PATH, path, "prototype.tsv"), 'w')

    named_entity_file.write('\n'.join(named_entity_file_lines)); named_entity_file.close()
    prototype_file.write('\n'.join(prototype_file_lines)); prototype_file.close()
    # No need to write relationship

    update_file.truncate(0)
    update_file.close()
    return True

def verify_knowledge_graph(path, mode = "CHECK", round = 0): 
    '''
    Check whether the specified knowledge graph is valid
    Input path: relative path to the knowledge graph under DATA_PATH
    '''

    if (not check_knowledge_graph_files(path)): return False
    if (os.path.exists(os.path.join(DATA_PATH, path, "update.tsv")) and mode == "UPDATE"): 
        update_file = open(os.path.join(DATA_PATH, path, "update.tsv"), 'r+')
        update_file_lines = update_file.readlines()
        if (len(update_file_lines) == 0): return True # kg is up-to-date
        else: fast_update_knowledge_graph(path, mode)

    '''
    Check the validity each .tsv files. Each entity should be verified. 
    For invalid entities/prototypes/relationships: Remove them (CHECK mode), or define them (i.e., increment the original graph) (UPDATE) mode

    named_entity.tsv: 
    <named_entity> | <prototype> | #Resource
     
    prototype.tsv: 
    <prototype> | <relationship>/is_a | <prototype>/$OBJECT | #Resource
    <relationship> | <relationship>/is_a | <prototype>/$RELATIONSHIP | #Resource
    '''
    named_entity_file = open(os.path.join(DATA_PATH, path, "named_entity.tsv"), 'r')
    prototype_file = open(os.path.join(DATA_PATH, path, "prototype.tsv"), 'r')
    relationship_file = open(os.path.join(DATA_PATH, path, "relationship.tsv"), 'r')

    '''
    _lines store the original file lines
    _write to store the lines to add
    '''
    global named_entity_lines, prototype_lines, named_entity_file_items, prototype_file_items
    named_entity_lines = []; prototype_lines = []
    named_entity_file_items = []; prototype_file_items = []
    named_entity_write = []; prototype_write = []
    named_entity_file_lines = named_entity_file.readlines()
    named_entity_file_lines = [line.replace('\n', '') for line in named_entity_file_lines]
    prototype_file_lines = prototype_file.readlines()
    prototype_file_lines = [line.replace('\n', '') for line in prototype_file_lines]
    relationship_file_lines = relationship_file.readlines()
    relationship_file_lines = [line.replace('\n', '') for line in relationship_file_lines]

    # 1. Check named_entity.tsv
    num_lines = len(named_entity_file_lines)
    for line_id in range(num_lines): 
        line_tokens = named_entity_file_lines[line_id].split('\t')
        if (len(line_tokens) != 3): 
            if (debug == 1): print (f"Knowledge Graph {path}: named_entity.tsv: line {line_id}: {line_tokens} length is not 3 | INVALID")
            named_entity_file_lines[line_id] = None; continue  # invalid line; discard despite the mode
        token_1_valid = check_knowledge_graph_element_exist(line_tokens[0], os.path.join(path, 'named_entity.tsv'), line_tokens[2], mode, named_entity_write, prototype_write)
        token_2_valid = check_knowledge_graph_element_exist(line_tokens[1], os.path.join(path, 'prototype.tsv'), line_tokens[2], mode, named_entity_write, prototype_write)
        line_valid = token_1_valid and token_2_valid
        if (debug == 1): print (f"Knowledge Graph {path}: named_entity.tsv: line {line_id} check: {token_1_valid, token_2_valid}")
        if (mode == "CHECK" and not line_valid): named_entity_file_lines[line_id] = None; # Discard the line under the check mode if not valid
    
    # 2. Check prototype.tsv
    num_lines = len(prototype_file_lines)
    for line_id in range(num_lines): 
        line_tokens = prototype_file_lines[line_id].split('\t')
        if (len(line_tokens) != 4): 
            if (debug == 1): print (f"Knowledge Graph {path}: prototype.tsv: line {line_id}: {line_tokens} length is not 4 | INVALID")
            prototype_file_lines[line_id] = None; continue  # invalid line; discard despite the mode
        token_1_valid = check_knowledge_graph_element_exist(line_tokens[0], os.path.join(path, 'prototype.tsv'), line_tokens[3], mode, named_entity_write, prototype_write)
        token_2_valid = check_knowledge_graph_element_exist(line_tokens[1], os.path.join(path, 'relationship.tsv'), line_tokens[3], mode, named_entity_write, prototype_write)
        token_3_valid = check_knowledge_graph_element_exist(line_tokens[2], os.path.join(path, 'prototype.tsv'), line_tokens[3], mode, named_entity_write, prototype_write)
        line_valid = token_1_valid and token_2_valid and token_3_valid
        if (debug == 1): print (f"Knowledge Graph {path}: prototype.tsv: line {line_id} check: {token_1_valid, token_2_valid, token_3_valid}")
        if (mode == "CHECK" and not line_valid): prototype_file_lines[line_id] = None; # Discard the line under the check mode if not valid

    # 3. Check relationship.tsv
    num_lines = len(relationship_file_lines)
    for line_id in range(num_lines): 
        line_tokens = relationship_file_lines[line_id].split('\t')
        if (len(line_tokens) != 4): 
            if (debug == 1): print (f"Knowledge Graph {path}: relationship.tsv: line {line_id}: {line_tokens} length is not 4 | INVALID")
            relationship_file_lines[line_id] = None; continue  # invalid line; discard despite the mode
        token_1_valid = check_knowledge_graph_element_exist(line_tokens[0], os.path.join(path, 'named_entity.tsv'), line_tokens[3], mode, named_entity_write, prototype_write)
        token_2_valid = check_knowledge_graph_element_exist(line_tokens[1], os.path.join(path, 'relationship.tsv'), line_tokens[3], mode, named_entity_write, prototype_write)
        token_3_valid = check_knowledge_graph_element_exist(line_tokens[2], os.path.join(path, 'named_entity.tsv'), line_tokens[3], "CHECK") or \
                        check_knowledge_graph_element_exist(line_tokens[2], os.path.join(path, 'prototype.tsv'), line_tokens[3], mode, named_entity_write, prototype_write) # issue: cannot know it is named_entity or prototype. Default: prototype
        line_valid =  token_1_valid and token_2_valid and token_3_valid
        if (debug == 1): print (f"Knowledge Graph {path}: relationship.tsv: line {line_id} check: {token_1_valid, token_2_valid, token_3_valid}")
        if (mode == "CHECK" and not line_valid): prototype_file_lines[line_id] = None; # Discard the line under the check mode if not valid

    '''
    Remove invalid lines in the previous knowledge graphs
    Remove duplicate entries in the write lists
    Update the knowledge graph files
    '''
    named_entity_write = list(set(named_entity_write))
    prototype_write = list(set(prototype_write))
    if (debug == 1): 
        print (f"named_entity_write: {named_entity_write}")
        print (f"prototype_write: {prototype_write}")
    named_entity_file_lines = [line for line in named_entity_file_lines if line != None]
    prototype_file_lines = [line for line in prototype_file_lines if line != None]
    relationship_file_lines = [line for line in relationship_file_lines if line != None]
    named_entity_file_lines = list(set(named_entity_file_lines + named_entity_write))
    prototype_file_lines = list(set(prototype_file_lines + prototype_write))

    print  ("\n\n")
    print (named_entity_file_lines)
    print (prototype_file_lines)
    print (relationship_file_lines)

    named_entity_file.close(); named_entity_file = open(os.path.join(DATA_PATH, path, "named_entity.tsv"), 'w')
    prototype_file.close(); prototype_file = open(os.path.join(DATA_PATH, path, "prototype.tsv"), 'w')
    relationship_file.close(); relationship_file = open(os.path.join(DATA_PATH, path, "relationship.tsv"), 'w')

    named_entity_file.write('\n'.join(named_entity_file_lines)); named_entity_file.close()
    prototype_file.write('\n'.join(prototype_file_lines)); prototype_file.close()
    relationship_file.write('\n'.join(relationship_file_lines)); relationship_file.close()

    '''
    verify the knowledge graph again
    '''
    if (round < 1): verify_knowledge_graph(path, mode, round + 1)

    '''
    Create a new update file to allow fast update in the future
    '''
    update_file = open(os.path.join(DATA_PATH, path, "update.tsv"), 'w')
    update_file.close()

    return True

