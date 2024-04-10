
kg = "/Users/abc/Desktop/RTSAI/KG_Construction/kg"

def parse_be_verb(word): 
    if (word.lower() in ["is", "are", "was", "were"]): 
        return word.lower()
    return None

def is_what_question(tokens): 
    if (len(tokens) >= 2): 
        if (tokens[0].lower() == "what" and parse_be_verb(tokens[1])): 
            tokens[-1] = tokens[-1].replace('?', '')
            return (["what", tokens[2:]])
    return None

input_text = "What is the name of HKU? "

def is_named_entity(tokens): 
    kg_file_lines = open(f"{kg}/named_entity.tsv", 'r').readlines()
    print (kg_file_lines)
    pass

def answer(input_text): 
    input_text_tokens = input_text.strip().split(' ')
    if (is_what_question(input_text_tokens)): 
        parsed_question = is_what_question(input_text_tokens)
        print (parsed_question)
        is_named_entity(parsed_question[1])


answer(input_text)
