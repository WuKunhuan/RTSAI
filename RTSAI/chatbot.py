
import copy

def is_be_verb(word): 
    if (word.lower() in ["is", "are", "was", "were"]): 
        return word.lower()
    return None

def parse_named_entity(): 
    pass

def parse_prototype(): 
    pass

def parse_relationship(): 
    pass

def parse_what_question(tokens): 
    if (len(tokens) >= 2 and tokens[0].lower() == "what"): 
        tokens[-1] = tokens[-1].replace('?', '')
        if (is_be_verb(tokens[1])): # Example: What is HKU? 
            return (["what", tokens[2:]])
        elif (is_be_verb(tokens[-1])): # Example: What HKU is?
            return (["what", tokens[1:len(tokens)-1]])
    return None

def parse_tokens_recursive(tokens, sentence_token_structure): 
    '''
    Parse the given sentence tokens in a recursive manner. 
    '''

    knowledge_graph_updates = []
    '''
    Check whether the sub-sentence is a question
    -   What-type question
    '''
    parse_what_question_result = parse_what_question()
    if (parse_what_question_result): 

        pass

    return (sentence_token_structure, knowledge_graph_updates)



def process_info_or_query(input_content, input_type = None, mode = "PROCESS_INFO", 
                          environment_name = None, knowledge_graph_name = None, 
                          knowledge_graph_extension_allowed = False, 
                          resource = None): 
    '''
    RTSAI agent processes natural language input, or gives response to the user query. 
    '''

    '''
    Currently, we assume the input is (a combination of) english sentences. 
    In future, there might be other languages and input forms (e.g., codes)
    it can be specified by input_type so that RTSAI knows how to deal with it
    '''

    '''
    Save any ambiguities detected during the sentence parsing. For example, "HKU is [beautiful]". 
    RTSAI does not know whether [beautiful] is a prototype (noun), or a relationship (adj/adv). 
    '''

    '''
    Break up the sentences into sub-sentences
    '''
    sub_sentences = input_content.replace('?', '.').replace('!', '.').split('.')
    for sentence in sub_sentences: 

        sentence_tokens = sentence.strip().split(' ')
        sentence_parse_result = parse_tokens_recursive(sentence_tokens, resource)

        '''
        Pass all the knowledge graph updates into update.tsv under the environment
        The resulting updates should have no ambiguities. During the processing, check for any ambiguity
        '''
        sentence_tokens_structure = sentence_parse_result[0]
        knowledge_graph_updates = sentence_parse_result[1]

            

