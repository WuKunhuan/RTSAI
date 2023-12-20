
import nltk, os, copy, re
import structural_analysis_setting

## Debug Mode
debug = 1



# 0. API Input
# This will be changed, once the API switches
language = "ENGLISH"



# 1. Preparation

# 1.1 Constant list

## Constants defined should not overlap with each other. 
## In our setting, we used numbers to be the constant value, to automatically avoid conflicts
constant_list = []
if (len(set(constant_list)) != len(constant_list)): 
    raise Exception ("ERROR : Constant Setting : No repeating symbols allowed! ")

# 1.2 Pattern
## import Patterns_grammar_ENGLISH
from structural_analysis_setting import Patterns_grammar_ENGLISH
from structural_analysis_setting import language_supported
## 🤓️ SETTING! 
Patterns_grammar = None
if (language in language_supported): 
    if (language == "ENGLISH"): Patterns_grammar = Patterns_grammar_ENGLISH

# 1.3 POS tags
## import English POS to patterns
from structural_analysis_setting import pos_tags_to_Patterns_ENGLISH, POS_key_str
if (debug == 0):
    nltk.download('tagsets')
    print (nltk.help.upenn_tagset())
## 🤓️ SETTING! 
pos_tags_to_Patterns = None
if (language in language_supported): 
    if (language == "ENGLISH"): 
        pos_tags_to_Patterns = pos_tags_to_Patterns_ENGLISH

# 1.4 Global Functions

## Detect whether a text starts with the key ...
from structural_analysis_setting import start_with

## Forbidden sentence start states
from structural_analysis_setting import NOUN_PHRASE_DET, NOUN_PHRASE_NON_DET, NOUN_PHRASE_NON_DET_NON_DEGRADABLE, NOUN_PHRASE_NON_DET_NON_COMPOUND, NOUN_COMPOUND
from structural_analysis_setting import ADJECTIVE_PHRASE_NON_DEGRADABLE, PREPOSITION_PHRASE_NON_DEGRADABLE
forbidden_start_state = None
if (language in language_supported): 
    if (language == "ENGLISH"): 
        forbidden_start_state = [
            f'{NOUN_PHRASE_DET}', 
            f'{NOUN_PHRASE_NON_DET}', 
            f'{NOUN_PHRASE_NON_DET_NON_DEGRADABLE}', 
            f'{NOUN_PHRASE_NON_DET_NON_COMPOUND}', 
            f'{NOUN_COMPOUND}', 
            f'{ADJECTIVE_PHRASE_NON_DEGRADABLE}', 
            f'{PREPOSITION_PHRASE_NON_DEGRADABLE}', 
        ]
        for key, value in POS_key_str.items():
            if (value == "*"): 
                forbidden_start_state.append(key)

## Convert the Patterns_grammar to a string representation
def start_with_forbidden_state(grammar_string): 
    for state in forbidden_start_state: 
        if (start_with(grammar_string, f'{state} ')): 
            return True
    return False
def adjust_grammar_start_state(grammar_string):
    newline_index = grammar_string.index('\n')
    first_part = grammar_string[:newline_index+1]
    second_part = grammar_string[newline_index+1:]
    adjusted_string = second_part + first_part
    return adjusted_string

## translating the keys to values
def key_str_translate(keys, POS_key_str): 
    key_list = keys.split(' ')
    return (' '.join([
        key if key not in POS_key_str.keys()
        else POS_key_str[f'{key}'] 
        for key in key_list]
    ))

## Display the grammar rules
def display_grammar_rules(Patterns_grammar, POS_key_str): 
    grammar_string_display = ""
    for key, value in Patterns_grammar.items():
        value_str = ' | '.join([key_str_translate(item, POS_key_str) for item in value])
        grammar_string_display += f"{key_str_translate(key, POS_key_str)} -> {value_str}\n"
    return grammar_string_display

## Visualize the final grammar tree
def translated_grammar_tree(tree_string, POS_key_str): 
    tree_string_display = tree_string
    for key in POS_key_str.keys(): 
        tree_string_display = tree_string_display.replace (f'({key}\n', f'({POS_key_str[key]}\n')
        tree_string_display = tree_string_display.replace (f'({key} ', f'({POS_key_str[key]} ')
    return tree_string_display

## Return the raw format, in one row, for further structure analysis
def translated_grammar_tree_raw(tree_string, POS_key_str): 
    tree_string_raw = tree_string
    for key in POS_key_str.keys(): 
        tree_string_raw = tree_string_raw.replace (f'({key}\n', f'({POS_key_str[key]}') # no newline
        tree_string_raw = tree_string_raw.replace (f'({key} ', f'({POS_key_str[key]} ')
        tree_string_raw = tree_string_raw.replace (f')\n', f')')
    return tree_string_raw



# 2. Receive and process the input sentence

# 2.1 Receive the input
## Get an input sentence from the user as the input. 
sentence = "Colorless green ideas sleep furiously. " 
input_sentence = input("Sentence: ")
if (input_sentence != ""): 
    sentence = input_sentence

# 2.2 Tokenize the sentence
## Tokenize the sentence and add POS tags
from nltk.tokenize import word_tokenize
tokens = word_tokenize(sentence)

# previous: 
tagged_words = nltk.pos_tag(tokens)

# new: 
try: 
    import os, subprocess
    home_directory = os.path.expanduser("~")

    # Set CLASSPATH environment variable
    class_path = f'{home_directory}/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
    os.environ['CLASSPATH'] = class_path

    # Set STANFORD_MODELS environment variable
    models_path = f'{home_directory}/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
    os.environ['STANFORD_MODELS'] = models_path

    from nltk.tag import StanfordPOSTagger
    st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
    tagged_words = st.tag(tokens)

except Exception as e: print (e)

## force conversion of close quotation marks
for word_id, word in enumerate(tagged_words): 
    if tagged_words[word_id][1] == "''": 
        tokens[word_id] = '"'
        tagged_words[word_id] = ('"', '"')
if (debug == 1): 
    print (f"\ntokens: {tokens}")
    print (f"\ntagged words: {tagged_words}")

# 2.3 Modify the Grammar tree 
## Generate productions dynamically based on POS tags
from structural_analysis_setting import CONJUNCTION_NOUN
forbidden_word_grammar = [
    ('for', f'{CONJUNCTION_NOUN}'), 
    ('but', f'{CONJUNCTION_NOUN}'), 
    ('yet', f'{CONJUNCTION_NOUN}'), 
    ('so',  f'{CONJUNCTION_NOUN}'), 
]
for word, pos in tagged_words:
    if (pos in pos_tags_to_Patterns.keys()): 
        for item in pos_tags_to_Patterns[pos]: 
            if (item not in Patterns_grammar): Patterns_grammar[item] = []
            if ((word, item) not in forbidden_word_grammar and f"\'{word}\'" not in Patterns_grammar[item]): 
                Patterns_grammar[item].append(f"\'{word}\'")
                if (debug == 0): 
                    print (f"grammar item {item} appended word: {word}")
    else: print (f"{word} (POS tagging: {pos}): not defined in the grammar rules. ")

# 2.4 Simplify the Grammar tree
modified = True
while (modified): 
    modified = False
    # Filter out any key with [] as its value
    keys = copy.deepcopy(list(Patterns_grammar.items()))
    for key, value_list in keys:
        if (value_list == []): 
            if (debug == 0): 
                print (f"key {POS_key_str[key]} : removed (value = [])")
            modified = True
            del Patterns_grammar[key]
    # Filter out any value containing a key with [] as its value
    for key, value_list in Patterns_grammar.items():
        for value in value_list: 
            value_list_items = value.split()
            if (not all(item in Patterns_grammar for item in value_list_items) and value[0] != "'"): 
                if (debug == 0): 
                    value_display = ' '.join([POS_key_str[item] for item in value.split(' ')])
                    print (f"key {POS_key_str[key]}'s value {value_display} : removed")
                modified = True
                Patterns_grammar[key].remove(value)

# 2.5 Create the grammar string
grammar_string = ""
for key, value in Patterns_grammar.items(): 
    value_str = ' | '.join(value)
    grammar_string += f"{key} -> {value_str}\n"
if (debug == 1): 
    print (f"\nGrammar Rules: \n{display_grammar_rules(Patterns_grammar, POS_key_str)}") 

# 2.6 Create the CFG grammar from the string representation
def PSR_parse(PSR_dict, tokens): 
    try: 
        grammar = nltk.CFG.fromstring(grammar_string)
        parser = nltk.ChartParser(grammar)
        parse_result = parser.parse(tokens)
        return parse_result
    except Exception as e: 
        return []



# 3. Parsing the sentence

## Representing the tree node
class TreeNode:
    def __init__(self, value, indent_level):
        self.value = value
        self.parent = None
        self.children = []
        self.indent_level = indent_level

## Construct the tree structure
def construct_tree(input_string):

    stack = []
    root = None

    tokens = []
    index = 0; temp = ''
    while (index < len(input_string)): 
        if (input_string[index] == '(' or input_string[index] == ')'): 
            if (temp != ''): 
                tokens.append(temp)
                temp = ''
            tokens.append(input_string[index])
        elif (input_string[index] != ' '): 
            temp += input_string[index]
        else: 
            if (temp != ''): 
                tokens.append(temp)
                temp = ''
        index += 1

    id_token = True
    for token in tokens:
        if token == '(':
            id_token = True
            continue
        elif token == ')':
            node = stack.pop()
            if stack:
                parent = stack[-1]
                parent.children.append(node)
                node.parent = parent
            else:
                root = node
        else:
            node = None
            if (not stack): 
                node = TreeNode(token, 0)
            else: 
                parent = stack[-1]
                node = TreeNode(token, parent.indent_level + 1)
            if (id_token): ## if the node is a structural element
                id_token = False
                stack.append(node)
            else: ## reach the bottom of the tree, no need another closing bracket
                parent = stack[-1]
                parent.children.append(node)

    return root

## Remove unnecessary star layers
def tree_remove_star(tree_string): 
    modified = True
    original_string = tree_string
    new_string = ""
    while (modified): 
        modified = False
        index = 0; new_string = ""
        while (index < len(original_string)): 
            if (index > len(original_string) - 2 or original_string[index:index+2] != '(*'): 
                new_string += original_string[index]
            else: 
                index += 3; 
                modified = True
                bracket_level = 1
                while (bracket_level > 0 and index < len(original_string)): 
                    if (original_string[index] == '('): bracket_level += 1
                    elif (original_string[index] == ')'): bracket_level -= 1
                    if (bracket_level != 0): 
                        new_string += original_string[index]
                        index += 1; 
            index += 1; 
        if (not modified): 
            new_string = original_string
        else: 
            original_string = new_string
    return new_string
    
## finds the tree topology
def find_tree_topology(node, tree_rows, indent_level = 0): 
    if (indent_level != 0): 
        tree_rows.append([indent_level, node.value, (indent_level - 1) * '  ' + '┗━' + node.value])
        row_id = len(tree_rows) - 2 # the row id of the previous row
        ## the previous row has indentation greater than this row
        ## add the column lines, then column bars are added
        while (row_id > 0 and tree_rows[row_id][0] > indent_level): 
            tree_rows[row_id][2] = \
            tree_rows[row_id][2][0 : 2*indent_level-2] + \
            '┃ ' + tree_rows[row_id][2][2*indent_level:]
            row_id -= 1
        if (row_id != len(tree_rows) - 2): 
            tree_rows[row_id][2] = \
            tree_rows[row_id][2][0 : 2*indent_level-2] + \
            '┣━' + tree_rows[row_id][2][2*indent_level:]
            row_id -= 1
    else: ## root node
        tree_rows.append([indent_level, node.value, node.value]) 
    for children in node.children: 
        find_tree_topology(children, tree_rows, indent_level + 1)
    return tree_rows

## Repeat to examine whether starting with a state is valid
successful_parse = False
parse_attempts = 0
parse_attempts_total = grammar_string.count("\n")
all_successful_trees = []

while (parse_attempts < parse_attempts_total): 
    ## verify any unnecessary layers
    result_trees = []
    for tree in PSR_parse(Patterns_grammar, tokens):
        result_trees.append(str(tree))
    for index, tree in enumerate(result_trees): 
        lines = tree.split('\n')
        count = sum(1 for line in lines if line.startswith('  ('))
        if (count == 1 and ' ' not in lines[0]): 
            # if only one line in the second level, and the first line does not have any words
            result_trees[index] = None  # the first layer is unnecessary
        elif (count == 0): # single line tree case
            first_line = lines[0]
            brackets = [i for i in first_line if i == '(' or i == ')']
            levels = []
            for id in range (len(brackets)): 
                if (id == 0): levels.append(1)
                elif (brackets[id] == '('): levels.append(levels[-1] + 1)
                else: levels.append(levels[-1] - 1)
            if (levels.count(1) == 2): # only one second 
                result_trees[index] = None  # the first layer is unnecessary
    result_trees = [tree for tree in result_trees if tree != None]
    if (result_trees != []): 
        successful_parse = True
        result_trees_display = [translated_grammar_tree(tree, POS_key_str) for tree in result_trees]
        result_trees_raw = [translated_grammar_tree_raw(tree, POS_key_str) for tree in result_trees]
        result_trees_raw_simplified = [tree_remove_star(tree) for tree in result_trees_raw]
        all_successful_trees += result_trees_raw_simplified
        if (debug == 1): 
            print (f"result trees: {result_trees_raw} \n")
            print (f"result trees simplified: {result_trees_raw_simplified} \n")
        if (debug == 0): 
            print ('\n\n'.join(result_trees_display))
            print ()
    grammar_string = adjust_grammar_start_state(grammar_string)
    parse_attempts += 1
    while ((start_with_forbidden_state(grammar_string) and parse_attempts < parse_attempts_total)): 
        grammar_string = adjust_grammar_start_state(grammar_string)
        parse_attempts += 1

if (debug == 1): 
    if successful_parse: print("Parse was successful! \n")
    else: print("Parse was not successful :( \n")

if (debug == 0): 
    print  (f"all_successful_trees: {all_successful_trees}\n")

for tree_string in all_successful_trees: 
    root = construct_tree(tree_string)
    tree_topology = find_tree_topology(root, [])
    if (debug == 0): 
        print (f"tree_topology: {tree_topology}")
    if (debug == 1): 
        print ('\n'.join([item[2] for item in tree_topology]))
        print ('')



# 4. Capturing information






