
agent_kg = "/Users/abc/Desktop/RTSAI/KG_Construction/agent_kg"
agent_context = "/Users/abc/Desktop/RTSAI/KG_Construction/agent_context"

'''
Knowledge graph elements
'''
from RTSAI.counter import KG_element_ID

KG_Named_Entity_list = []
class KG_Named_Entity: 
    def __init__(self, name, prototype = "Object"): 
        self.id = KG_element_ID()
        self.name = name # can share the same name
        self.prototype = prototype
        KG_Named_Entity_list.append(self)

kg_file_lines = open(f"{agent_kg}/named_entity.tsv", 'r').readlines()
for line in kg_file_lines: 
    line = line.split('r')

'''
Handling user input
'''
def is_be_verb(word): 
    if (word.lower() in ["is", "are", "was", "were"]): 
        return word.lower()
    return None

def parse_the_phrase(tokens): 
    if (len(tokens) >= 2 and tokens[0].lower() == "the"): 
        return (tokens)
    return None

def parse_what_question(tokens): 
    if (len(tokens) >= 2 and tokens[0].lower() == "what"): 
        tokens[-1] = tokens[-1].replace('?', '')
        if (is_be_verb(tokens[1])): 
            return (["what", tokens[2:]])
        elif (is_be_verb(tokens[-1])): 
            return (["what", tokens[1:len(tokens)-1]])
    return None

def parse_of_phrase(tokens, parse_have_prototype = False): 
    if ("of" in tokens): 
        of_location = tokens.find("of")
        if (len(tokens) == of_location + 1): return None
        if (parse_the_phrase(tokens) and not parse_have_prototype): 
            return ([tokens[of_location+1:], f"have_entity:{' '.join(tokens[1:of_location])}", "<MASK>"])
        return ([tokens[of_location+1:], f"have_prototype:{' '.join(tokens[0:of_location])}", "<MASK>"])
    return None

'''
Handling knowledge graphs
'''
def check_named_entity(tokens): # ✅
    for entity in KG_Named_Entity_list: 
        if (entity.name == ''.join(tokens)): 
            return entity
    return None

'''
The agent and its action class
'''
class Agent: 

    def __init__(self): 
        self.knowledge_path = None # Retrieve knowledge graph / knowledge graphs under the specified environment

        '''
        Resources that the agent can access or modify
        '''
        self.short_term_memory = []  # remaining tokens in the user input
        self.stm_attention_start = 0
        self.stm_attention_end = 0

        '''
        Agent actions

        The default action: 
        -   "None"

        Handling the user input: 
        -   "Label Question" : Label the tokens as question (store the tokens)
        -   "Label Entity" : Label the tokens as a named entity
        -   "Label Relationship" : Label the tokens as a relationship

        Handling the context knowledge graph
        -   "Compute" : Try to resolve anything in the context knowledge graph
        -   "Focus" : Change the focus 
        -   "Check named entity" (feed with tokens) : Check whether the fed tokens are an existing named entity
        -   "Search" (feed with tokens) : Search for any satisfied contents (named entities, relationship, 

        Handling the hidden state
        -   "Discard" : Discard the specified range in the short term memory

        '''
        self.action = None  # AgentAction class instance
    
    def take_action(self): 
        if (self.action_type == "None"): 
            return
        elif (self.action_type == "Discard"): 
            self.stm_attention_start = max(0, self.stm_attention_start)
            self.stm_attention_end = min(len(self.short_term_memory), self.stm_attention_end)

class AgentAction: 
    
    def __init__(self, type): 
        self.action_type = type
        self.action_input = []
        self.action_result = []
    
    def execute(self): 
        '''
        Examples: 
        1. What is (the name of HKU)?
           -    parse: ["what", ["HKU", "have_entity:name", "<MASK>"]]
           -    type : Compute
           -    information : ["HKU", "have_entity:name", "<MASK>"]
        '''
        pass

# Task 1: Answer the sentence "What is the name of HKU? "
def answer_hku_name(input_text): 

    input_text_tokens = input_text.strip().split(' ')
    print (input_text_tokens)


    '''
    Template answering
    '''
    ############## Change the code below ##############

    # Step 1: ['what']
    short_term_memory.append(input_text_tokens.pop(0))
    action = None; token_start = 0; token_end = 0; 
    take_action(short_term_memory, action, token_start, token_end)

    # Step 2: ['what', 'is'] -- ("Label Question", 0, 2) --> []
    short_term_memory.append(input_text_tokens.pop(0))
    action = "Label Question"; token_start = 0; 
    take_action(short_term_memory, action, token_start, token_end)

    # Step 3: ['the']

    # Step 4: ['the', 'name'] -- ("Label Constraint", 0, 2) --> []

    # Step 5: ['of']

    ############## Change the code above ##############

input_text = "What is the name of HKU? "
answer_hku_name(input_text)
