
import os, shutil
from RTSAI.config import DATA_PATH, ASSETS_PATH
from RTSAI.setup_funcs import OBJECT_KEY, RELATIONSHIP_KEY, PROTOTYPE_CHARACTER, NAMED_ENTITY_SYMBOL, PROTOTYPE_SYMBOL, RELATIONSHIP_SYMBOL
from RTSAI.tool_funcs import show_popup_message, new_name_check

debug = 1

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

def check_knowledge_graph_element_exist(target_item, filename, resource = None, mode = "CHECK"): 
    '''
    Check whether the item (named entity, prototype, relationship) exist in the specified file
    '''

    if (not (filename.endswith('.tsv'))): 
        if (debug == 1): print (f"Check {target_item} in file: Filename {filename} not ends with .tsv")
        return False
    if (not os.path.exists(filename)): 
        if (debug == 1): print (f"Check {target_item} in file: Filename {filename} does not exist. ")
        return False
    if (filename.endswith('relationship.tsv')): # read the prototype file if it is a relationship
        filename = filename[:(-1*len('relationship.tsv'))] + 'prototype.tsv'

    file = open(filename, '+a')
    file_lines = file.readlines()
    file_items = [items.split('\t')[0] for items in file_lines]
    for item in file_items: 
        if (item == target_item): break
    else: 
        if (mode == "UPDATE"): 
            if (filename.endswith('named_entity.tsv')): 
                if (resource): file.write(f"{target_item}\t{OBJECT_KEY}\t{resource}{PROTOTYPE_CHARACTER}Resource")
                else: file.write(f"{target_item}\t{OBJECT_KEY}\t{PROTOTYPE_CHARACTER}Resource")
            elif (filename.endswith('prototype.tsv')): 
                if (resource): file.write(f"{target_item}\tis_a\t{OBJECT_KEY}\t{resource}{PROTOTYPE_CHARACTER}Resource")
                else: file.write(f"{target_item}\tis_a\t{OBJECT_KEY}\t{PROTOTYPE_CHARACTER}Resource")
            elif (filename.endswith('relationship.tsv')): 
                if (resource): file.write(f"{target_item}\tis_a\t{RELATIONSHIP_KEY}\t{resource}{PROTOTYPE_CHARACTER}Resource")
                else: file.write(f"{target_item}\tis_a\t{RELATIONSHIP_KEY}\t{PROTOTYPE_CHARACTER}Resource")
            file.close()
            return True
        else: 
            file.close()
            return False

def fast_update_knowledge_graph(path, mode = "CHECK"): 
    '''
    Update the knowledge graphs based on update.tsv file
    Method: Iterate every item specified in update.tsv file. 
    Remove everything in update.tsv after the operation. 
    '''

    if (not check_knowledge_graph_files(path)): return False
    if (not os.path.exists(os.path.join(DATA_PATH, path, "update.tsv"))): return False
    update_file = open(os.path.join(DATA_PATH, path, "update.tsv"), 'r+')
    update_file_lines = update_file.readlines()
    num_lines = len(update_file_lines)
    target_keys = [NAMED_ENTITY_SYMBOL, PROTOTYPE_SYMBOL, RELATIONSHIP_SYMBOL]
    for line_id in range (num_lines): 
        line_tokens = update_file_lines[line_id].split('\t')
        if (len(line_tokens) != 3): # item, type (named_entity | prototype | relationship), resource (resource | None)
            if (debug == 1): print (f"Knowledge graph {path}'s update.tsv's line {line_id}: {line_tokens}'s length is not 3 | SKIPPED")
            line_tokens = None
        if (line_tokens[1] not in target_keys): 
            if (debug == 1): print (f"Knowledge graph {path}'s update.tsv's line {line_id}: {line_tokens}'s key is invalid | SKIPPED")
            line_tokens = None
        update_file_lines[line_id] = line_tokens

    update_file_line_tokens = [line for line in update_file_lines if line != None]
    for line_id, line_tokens in enumerate(update_file_line_tokens): 
        if (line_tokens[1] == NAMED_ENTITY_SYMBOL): 
            check_knowledge_graph_element_exist(line_tokens[0], os.path.join(path, 'named_entity.tsv'), line_tokens[2], mode)
        elif (line_tokens[1] == PROTOTYPE_SYMBOL): 
            check_knowledge_graph_element_exist(line_tokens[0], os.path.join(path, 'prototype.tsv'), line_tokens[2], mode)
        elif (line_tokens[1] == RELATIONSHIP_SYMBOL): 
            check_knowledge_graph_element_exist(line_tokens[0], os.path.join(path, 'relationship.tsv'), line_tokens[2], mode)
    
    update_file.truncate(0)
    update_file.close()
    return True

def verify_knowledge_graph(path, mode = "CHECK"): 
    '''
    Check whether the specified knowledge graph is valid
    Input path: relative path to the knowledge graph under DATA_PATH
    '''

    if (not check_knowledge_graph_files(path)): return False
    if (os.path.exists(os.path.join(DATA_PATH, path, "update.tsv"))): 
        update_file = open(os.path.join(DATA_PATH, path, "update.tsv"), 'r+')
        update_file_lines = update_file.readlines()
        if (len(update_file_lines) == 0): 
            return True # kg is up-to-date

    '''
    Check the validity each .tsv files. Each entity should be verified. 
    For invalid entities/prototypes/relationships: Remove them (CHECK mode), or define them (i.e., increment the original graph) (UPDATE) mode

    named_entity.tsv: 
    <named_entity> | <prototype> | #Resource
     
    prototype.tsv: 
    <prototype> | <relationship>/is_a | <prototype>/$OBJECT | #Resource
    <relationship> | <relationship>/is_a | <prototype>/$RELATIONSHIP | #Resource
    '''
    named_entity_file = open(os.path.join(DATA_PATH, path, "named_entity.tsv"), 'r+')
    prototype_file = open(os.path.join(DATA_PATH, path, "prototype.tsv"), 'r+')
    relationship_file = open(os.path.join(DATA_PATH, path, "relationship.tsv"), 'r+')

    # 1. Check named_entity.tsv
    named_entity_file_lines = named_entity_file.readlines()
    num_lines = len(named_entity_file_lines)
    for line_id in range(num_lines): 
        line_tokens = named_entity_file_lines[line_id].split('\t')
        if (len(line_tokens) != 3): 
            if (debug == 1): print (f"Knowledge Graph {path}: named_entity.tsv: line {line_id}: {line_tokens} length is not 3 | INVALID")
            named_entity_file_lines[line_id] = None; continue  # invalid line; discard despite the mode
        # line_valid = check_item_exist(line_tokens[0], os.path.join(path, 'named_entity.tsv'), line_tokens[2], mode) and True # The first token (i.e., the current named entity) must exist in named_entity.tsv
        line_valid = check_knowledge_graph_element_exist(line_tokens[1], os.path.join(path, 'prototype.tsv'), line_tokens[2], mode) and line_valid  # The second token (i.e., the prototype) may not exist in prototype.tsv
        if (mode == "CHECK" and not line_valid): named_entity_file_lines[line_id] = None; # Discard the line under the check mode if not valid

    # 2. Check prototype.tsv
    prototype_file_lines = prototype_file.readlines()
    num_lines = len(prototype_file_lines)
    for line_id in range(num_lines): 
        line_tokens = prototype_file_lines[line_id].split('\t')
        if (len(line_tokens) != 4): 
            if (debug == 1): print (f"Knowledge Graph {path}: prototype.tsv: line {line_id}: {line_tokens} length is not 4 | INVALID")
            prototype_file_lines[line_id] = None; continue  # invalid line; discard despite the mode
        # line_valid = check_item_exist(line_tokens[0], os.path.join(path, 'prototype.tsv'), line_tokens[2], mode) and True # The first token (i.e., the current prototype) must exist in prototype.tsv
        line_valid = check_knowledge_graph_element_exist(line_tokens[1], os.path.join(path, 'prototype.tsv'), line_tokens[2], mode) and line_valid  # The second token (i.e., the relationship) may not exist in relationship.tsv
        if (mode == "CHECK" and not line_valid): prototype_file_lines[line_id] = None; # Discard the line under the check mode if not valid

    # 3. Check relationship.tsv
    relationship_file_lines = relationship_file.readlines()


    named_entity_file.close()
    prototype_file.close()
    relationship_file.close()

    '''
    Create a new update file
    This allows fast update in the future
    '''
    update_file = open(os.path.join(DATA_PATH, path, "update.tsv"), 'w')
    update_file.close()

    return True

