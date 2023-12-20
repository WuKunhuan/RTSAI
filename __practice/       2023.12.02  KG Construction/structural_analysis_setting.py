
POS_id_counter = 0
def new_POS_id(): 
    global POS_id_counter; 
    POS_id_counter += 1; 
    return POS_id_counter; 
POS_key_str = dict()
POS_key_str_star_option = True

# 1. Sentence Types

# 1.1 Sentence Types

## Sentence in Full: sentence + full stop
SENTENCE_FULL = new_POS_id()
POS_key_str[f'{SENTENCE_FULL}'] = "S"

## Sentence
SENTENCE = new_POS_id()
if (POS_key_str_star_option): 
    POS_key_str[f'{SENTENCE}'] = "*"
else: 
    POS_key_str[f'{SENTENCE}'] = "S"

## Sub Sentence
SUB_SENTENCE = new_POS_id()
POS_key_str[f'{SUB_SENTENCE}'] = "S"

# 1.2 Sentence Purposes

## Declarative sentences, or declarations, convey information or make statements.
DECLARATIVE = new_POS_id()
POS_key_str[f'{DECLARATIVE}'] = "[DECLARATIVE]"

## Interrogative sentences, or questions, request information or ask questions.
INTERROGATIVE = new_POS_id()
POS_key_str[f'{INTERROGATIVE}'] = "[INTERROGATIVE]"

## Imperative sentences, or imperatives, make commands or requests.
IMPERATIVE = new_POS_id()
POS_key_str[f'{IMPERATIVE}'] = "[IMPERATIVE]"

## Exclamatory sentences, or exclamations, show emphasis.
EXCLAMATORY = new_POS_id()
POS_key_str[f'{EXCLAMATORY}'] = "[EXCLAMATORY]"

# 2. Sentence Structure

# 2.1 Nouns
## https://dictionary.cambridge.org/grammar/british-grammar/noun-phrases-dependent-words#noun-phrases-dependent-words__52

## Noun Phrase
NOUN_PHRASE = new_POS_id()
POS_key_str[f'{NOUN_PHRASE}'] = "NP"

## Noun Phrase Determiner: Noun Phrase started with determiners
NOUN_PHRASE_DET = new_POS_id()
if (POS_key_str_star_option): 
    POS_key_str[f'{NOUN_PHRASE_DET}'] = "*"
else: 
    POS_key_str[f'{NOUN_PHRASE_DET}'] = "NP_d"

## Noun Phrase Non Determiner: Noun Phrase not started with determiners
NOUN_PHRASE_NON_DET = new_POS_id()
if (POS_key_str_star_option): 
    POS_key_str[f'{NOUN_PHRASE_NON_DET}'] = "*"
else: 
    POS_key_str[f'{NOUN_PHRASE_NON_DET}'] = "NP_nd"

## Noun Phrase Non Determiner not preposition
NOUN_PHRASE_NON_DET_NON_PREPOSITION = new_POS_id()
POS_key_str[f'{NOUN_PHRASE_NON_DET_NON_PREPOSITION}'] = "NP"

## Noun Phrase Non Determiner not compound
NOUN_PHRASE_NON_DET_NON_COMPOUND = new_POS_id()
POS_key_str[f'{NOUN_PHRASE_NON_DET_NON_COMPOUND}'] = "NP"

## Noun Adjective Phrase : Noun Phrase used as Adjective Phrase
NOUN_COMPOUND = new_POS_id()
POS_key_str[f'{NOUN_COMPOUND}'] = "NC" # "NC"

## Noun, all types
NOUN = new_POS_id()
if (POS_key_str_star_option): 
    POS_key_str[f'{NOUN}'] = "*"
else: 
    POS_key_str[f'{NOUN}'] = "N0"

## Common Noun
NOUN_C = new_POS_id()
if (POS_key_str_star_option): 
    POS_key_str[f'{NOUN_C}'] = "*"
else: 
    POS_key_str[f'{NOUN_C}'] = "N_C"

## Pronoun
NOUN_P = new_POS_id()
if (POS_key_str_star_option): 
    POS_key_str[f'{NOUN_P}'] = "*"
else: 
    POS_key_str[f'{NOUN_P}'] = "N_P"

## Noun, common, singular or mass
NOUN_CS = new_POS_id()
POS_key_str[f'{NOUN_CS}'] = "N"

## Noun, common, plural
NOUN_CP = new_POS_id()
POS_key_str[f'{NOUN_CP}'] = "N"

## Noun, proper, singular
NOUN_PS = new_POS_id()
POS_key_str[f'{NOUN_PS}'] = "PRON"

## Noun, proper, plural
NOUN_PP = new_POS_id()
POS_key_str[f'{NOUN_PP}'] = "PRON"

# 2.2 Verbs

## Verb Phrase
VERB_PHRASE = new_POS_id()
POS_key_str[f'{VERB_PHRASE}'] = "VP"

## Verb
VERB = new_POS_id()
if (POS_key_str_star_option): 
    POS_key_str[f'{VERB}'] = "*"
else: 
    POS_key_str[f'{VERB}'] = "V0"

## Verb Auxiliary
VERB_AUX = new_POS_id()
POS_key_str[f'{VERB_AUX}'] = "Aux"

## Verb Non Auxiliary
VERB_NON_AUX = new_POS_id()
POS_key_str[f'{VERB_NON_AUX}'] = "V"

## Verb Principle tense
VERB_PRINCIPLE = new_POS_id()
POS_key_str[f'{VERB_PRINCIPLE}'] = "V"

## Verb Participle tense
VERB_PARTICIPLE = new_POS_id()
POS_key_str[f'{VERB_PARTICIPLE}'] = "V"

# 2.3 Adjectives

## Adjective Phrase
ADJECTIVE_PHRASE = new_POS_id()
POS_key_str[f'{ADJECTIVE_PHRASE}'] = "AdjP"

## Adjective Phrase Non Degradable
ADJECTIVE_PHRASE_NON_DEGRADABLE = new_POS_id()
POS_key_str[f'{ADJECTIVE_PHRASE_NON_DEGRADABLE}'] = 'AdjP'

## Adjective
ADJECTIVE = new_POS_id()
POS_key_str[f'{ADJECTIVE}'] = 'A'

# 2.4 Adverbs

## Adverb Phrase
ADVERB_PHRASE = new_POS_id()
POS_key_str[f'{ADVERB_PHRASE}'] = 'AdvP'

## Degree Adverb
ADVERB_DEG = new_POS_id()
POS_key_str[f'{ADVERB_DEG}'] = 'Adv'

## Adverb
ADVERB = new_POS_id()
POS_key_str[f'{ADVERB}'] = 'Adv'

# 2.5 Articles

## Article
ARTICLE = new_POS_id()
POS_key_str[f'{ARTICLE}'] = 'Art'

# 2.6 Prepositions

## Preposition Phrase
PREPOSITION_PHRASE = new_POS_id()
POS_key_str[f'{PREPOSITION_PHRASE}'] = 'PP'

## Preposition Phrase Non Degradable
PREPOSITION_PHRASE_NON_DEGRADABLE = new_POS_id()
POS_key_str[f'{PREPOSITION_PHRASE_NON_DEGRADABLE}'] = 'PP'

## Preposition
PREPOSITION = new_POS_id()
POS_key_str[f'{PREPOSITION}'] = 'P'

# 2.7 Complements

## Complement Sentence
COMPLEMENT_SENTENCE = new_POS_id()
POS_key_str[f'{COMPLEMENT_SENTENCE}'] = 'COMP' # 'COMP_S'

## Complement Verb Phrase
COMPLEMENT_VERB_PHRASE = new_POS_id()
POS_key_str[f'{COMPLEMENT_VERB_PHRASE}'] = 'COMP' # 'COMP_VP'

## Complement Word
COMPLEMENT_WORD = new_POS_id()
POS_key_str[f'{COMPLEMENT_WORD}'] = 'COMP'

# 2.8 Others

## Conjunction Words
## for, and, nor, but, or, yet, so. 
CONJUNCTION = new_POS_id()
POS_key_str[f'{CONJUNCTION}'] = 'X'

## Conjunction Words : Connecting NPs
## Only and, or, nor can be used to connect noun phrases
CONJUNCTION_NOUN = new_POS_id()
POS_key_str[f'{CONJUNCTION_NOUN}'] = 'X'

## Possession
POSSESSION = new_POS_id()
POS_key_str[f'{POSSESSION}'] = 'Poss'

## Possessive Ending
POSSESSIVE_ENDING = new_POS_id()
POS_key_str[f'{POSSESSIVE_ENDING}'] = 'PossEnd'

EXCLAMATION = new_POS_id()
POS_key_str[f'{EXCLAMATION}'] = 'Excl'

## Particle
PARTICLE = new_POS_id()
POS_key_str[f'{PARTICLE}'] = 'Par'

## Determiner
DETERMINER = new_POS_id()
POS_key_str[f'{DETERMINER}'] = 'Det'

# 2.8 Others : punctuation

## Punctuation
PUNCTUATION = new_POS_id()
POS_key_str[f'{PUNCTUATION}'] = '*'

## Punctuation, single
PUNCTUATION_SINGLE = new_POS_id()
POS_key_str[f'{PUNCTUATION_SINGLE}'] = '*' # 'Punc'

## Open parentheses
PAREN_OPEN = new_POS_id()
POS_key_str[f'{PAREN_OPEN}'] = 'PAREN_OPEN'

## Close parentheses
PAREN_CLOSE = new_POS_id()
POS_key_str[f'{PAREN_CLOSE}'] = 'PAREN_CLOSE'

## Open Quote
QUOTE_OPEN = new_POS_id()
POS_key_str[f'{QUOTE_OPEN}'] = 'QUOTE_OPEN'

## Close Quote
QUOTE_CLOSE = new_POS_id()
POS_key_str[f'{QUOTE_CLOSE}'] = 'QUOTE_CLOSE'

## Comma
COMMA = new_POS_id()
POS_key_str[f'{COMMA}'] = 'COMMA'

## Full Stop
FULL_STOP = new_POS_id()
POS_key_str[f'{FULL_STOP}'] = 'FULL_STOP'

## Dash
DASH = new_POS_id()
POS_key_str[f'{DASH}'] = 'DASH'

## Colon
COLON = new_POS_id()
POS_key_str[f'{COLON}'] = 'COLON'

## Dollar
DOLLAR = new_POS_id()
POS_key_str[f'{DOLLAR}'] = 'DOLLAR'

# 3. Patterns Grammar Tree

# 3.1 English Version
Grammar_Patterns_ENGLISH = {

    ## 3.1.1 Sentence and Sub Sentence
    f'{SENTENCE_FULL}': [
        f'{SENTENCE} {FULL_STOP}', 
    ], 

    f'{SENTENCE}': [
        f'{SUB_SENTENCE}', 
        f'{SUB_SENTENCE} {CONJUNCTION} {SENTENCE}', 
    ], 
    
    f'{SUB_SENTENCE}': [
        f'{DECLARATIVE}', 
        f'{INTERROGATIVE}', 
        f'{IMPERATIVE}', 
        f'{EXCLAMATORY}', 
        f'{NOUN_PHRASE} {VERB_PHRASE}', 
    ], 

    ## 3.1.2 Sentence Purpose
    f'{DECLARATIVE}': [
        f'{NOUN_PHRASE} {VERB} {NOUN_PHRASE}', 
    ], 
    f'{INTERROGATIVE}': [

    ], 
    f'{IMPERATIVE}': [

    ], 
    f'{EXCLAMATORY}': [
        f'{EXCLAMATION}', 
    ], 

    ## 3.2.1 Nouns

    f'{NOUN_PHRASE}': [

        f'{NOUN_PHRASE_DET}', 

        f'{NOUN_PHRASE_NON_DET}', 

    ], 

    f'{NOUN_COMPOUND}': [

        # ✅ <knowledge> graph
        # ❌ 
        f'{NOUN}', 

        # ✅ <big, beautiful> graph
        # ❌ 
        f'{NOUN_COMPOUND} {COMMA} {NOUN}', 

        # ✅ 
        # ❌ 
        f'{NOUN_COMPOUND} {NOUN}', 

    ], 

    f'{NOUN_PHRASE_DET}': [

        # ✅ 
        # ❌ 
        f'{DETERMINER} {NOUN_PHRASE_NON_DET}', 

        # ✅ 
        # ❌ 
        f'{NOUN_PHRASE_DET} {CONJUNCTION_NOUN} {NOUN_PHRASE_DET}', 

    ], 

    f'{NOUN_PHRASE_NON_DET}': [

        f'{NOUN}', 
                 
        ## Pre-modifier : possession modifier
        ## cannot add preposition phrase? 
        ## e.g. my <reaction to it> is invalid
        # ✅ <your> <happiness> : pre-modifier
        # ❌ 
        f'{POSSESSION} {NOUN_PHRASE_NON_DET_NON_PREPOSITION}', 

        ## Pre-modifier
        ## cannot add preposition phrase? 
        ## e.g. correct <reaction to it> is invalid
        # ✅ <good> <student> : pre-modifier
        # ❌ 
        f'{ADJECTIVE_PHRASE} {NOUN_PHRASE_NON_DET_NON_PREPOSITION}', 

        ## Pre-modifier
        # ✅ <thrilling> <story> : pre-modifier
        # ❌ 
        f'{VERB_PARTICIPLE} {NOUN_PHRASE_NON_DET}', 

        ## Post-modifier
        # ✅ <man> <with grey hair>
        # ❌ 
        f'{NOUN_PHRASE_NON_DET} {PREPOSITION_PHRASE_NON_DEGRADABLE}', 

        ## Post-modifier : related clause modifier
        # ✅ <thing> <the student> <wrote>
        # ❌ 
        f'{NOUN_PHRASE_NON_DET} {NOUN_PHRASE} {VERB_PHRASE}', 

        ## Compound (noun as pre-modifier)
        ## noun compound cannot add pronouns
        # ✅ <colorless green> <ideas>
        # ❌ 
        f'{NOUN_COMPOUND} {NOUN_C}', 

        # ✅ 
        # ❌ 
        f'{NOUN_PHRASE_NON_DET} {CONJUNCTION_NOUN} {NOUN_PHRASE_NON_DET}', 

    ], 

    f'{NOUN}': [

        f'{NOUN_C}', 

        f'{NOUN_P}', 

    ], 

    f'{NOUN_C}': [

        f'{NOUN_CS}', 

        f'{NOUN_CP}', 

    ], 


    f'{NOUN_P}': [

        f'{NOUN_PS}', 

        f'{NOUN_PP}', 

    ], 

    ## 3.2.2 Verbs
    f'{VERB_PHRASE}': [

        f'{VERB}', 

        f'{VERB} {NOUN_PHRASE}', 

        f'{VERB} {NOUN_PHRASE} {PREPOSITION_PHRASE}', 

        f'{VERB} {NOUN_PHRASE} {ADVERB_PHRASE}', 

        f'{VERB} {NOUN_PHRASE} {PREPOSITION_PHRASE} {ADVERB_PHRASE}', 

        # f'{VERB} {NOUN_PHRASE_NON_DET} {NOUN_PHRASE_NON_DET}', 

        # f'{VERB} {NOUN_PHRASE_NON_DET} {NOUN_PHRASE_NON_DET} {PREPOSITION_PHRASE}', 

        # f'{VERB} {NOUN_PHRASE_NON_DET} {NOUN_PHRASE_NON_DET} {ADVERB_PHRASE}', 

        # f'{VERB} {NOUN_PHRASE_NON_DET} {NOUN_PHRASE_NON_DET} {PREPOSITION_PHRASE} {ADVERB_PHRASE}', 

        f'{VERB} {PREPOSITION_PHRASE}', 

        f'{VERB} {PREPOSITION_PHRASE} {ADVERB_PHRASE}', 

        # ✅ HKU is <very good>
        # ❌ 
        f'{VERB} {ADJECTIVE_PHRASE}', 

        f'{VERB} {ADVERB_PHRASE}', 

        f'{VERB} {COMPLEMENT_SENTENCE}', 

        f'{VERB} {COMPLEMENT_VERB_PHRASE}', 

        f'{VERB} {PARTICLE}', 

        f'{VERB} {PARTICLE} {NOUN_PHRASE}', 

        f'{VERB_PHRASE} {CONJUNCTION} {VERB_PHRASE}', 

        f'{VERB_PHRASE} {COMPLEMENT_WORD} {VERB_PHRASE}', 

        # ✅ We <enjoy singing>
        # ❌ 
        f'{VERB_NON_AUX} {VERB_PARTICIPLE}', 

    ], 

    f'{VERB}': [
        
        f'{VERB_AUX} {VERB_NON_AUX}', 
        
        # ✅ The book first <came out> in 1997
        # ❌ 
        f'{VERB} {PARTICLE}', 

        f'{VERB_NON_AUX}', 
    
    ], 

    ## 3.2.3 Adjectives
    f'{ADJECTIVE_PHRASE}': [

        # ✅ 
        # ❌ 
        f'{ADJECTIVE}', 

        # ✅ 
        # ❌ 
        f'{ADJECTIVE} {PREPOSITION_PHRASE}', 

        # ✅ 
        # ❌ 
        f'{ADJECTIVE} {PARTICLE}', 

        # ✅ <very> <very good>
        # ❌ 
        f'{ADVERB_PHRASE} {ADJECTIVE_PHRASE}', 
    ], 

    ## 3.2.4 Adverbs
    f'{ADVERB_PHRASE}': [

        # ✅ 
        # ❌ 
        f'{ADVERB}', 

        # ✅ 
        # ❌ 
        f'{ADVERB} {PARTICLE}', 

        # ✅ 
        # ❌ 
        f'{ADVERB_DEG}', 

        # ✅ 
        # ❌ 
        f'{ADVERB_DEG} {ADVERB}', 

        # ✅ 
        # ❌ 
    ], 

    ## 3.2.5 Articles
    f'{ARTICLE}': [
        f'{NOUN_PHRASE} {POSSESSIVE_ENDING}', 
    ], 

    ## 3.2.6 Prepositions
    ## https://dictionary.cambridge.org/grammar/british-grammar/prepositional-phrases
    f'{PREPOSITION_PHRASE}': [

        # ✅ 
        # ❌ 
        f'{PREPOSITION}', 

        # ✅ If you can wait <until after my meeting with Jack>
        # ❌ 
        f'{PREPOSITION} {PREPOSITION_PHRASE}', 

        # ✅ They first met <at a party>
        # ❌ 
        f'{PREPOSITION} {NOUN_PHRASE}', # complement usage

        # ✅ <Until quite recently>, no one knew ...
        # ❌ 
        f'{PREPOSITION} {ADVERB_PHRASE}', 

    ], 

    ## 3.2.7 Complements

    f'{COMPLEMENT_SENTENCE}': [

        # ✅ 
        # ❌ 
        f'{COMPLEMENT_WORD} {SUB_SENTENCE}', 

        # ✅ 
        # ❌ 
        f'{SUB_SENTENCE}', 

    ], 

    f'{COMPLEMENT_VERB_PHRASE}': [

        # ✅ I am practising <playing the piano>
        # ❌ 
        f'{VERB_PHRASE}', 

        # ✅ 
        # ❌ 
        f'{COMPLEMENT_WORD} {VERB_PHRASE}', 
        
        # ✅ to <work or rest>
        # ❌ 
        f'{COMPLEMENT_VERB_PHRASE} {CONJUNCTION} {COMPLEMENT_VERB_PHRASE}', 

    ], 

    # 3.2.8 Others
    f'{PUNCTUATION}': [
        f'{PUNCTUATION_SINGLE}', 
        f'{PUNCTUATION_SINGLE} {PUNCTUATION}', 
    ], 

    f'{PUNCTUATION_SINGLE}': [
        f'{PAREN_OPEN}', 
        f'{PAREN_CLOSE}', 
        f'{QUOTE_OPEN}', 
        f'{QUOTE_CLOSE}', 
        f'{COMMA}', 
        f'{FULL_STOP}', 
        f'{DASH}', 
        f'{COLON}', 
        f'{DOLLAR}', 
    ], 


}

# 3.2 Next Language (COMING SOON)

# 3.2.9 Others - dependent

## 
def start_with(text, key): 
    if (len(text) >= len(key) and text[0:len(key)] == key): 
        return True
    return False

## 
def start_replace(text, key, key_new): 
    if (len(text) >= len(key) and text[0:len(key)] == key): 
        return (key_new + text[len(key):])
    return text

## Noun Phrase Non Det Non Preposition : cannot be simplified to noun prepositions
Grammar_Patterns_ENGLISH[f'{NOUN_PHRASE_NON_DET_NON_PREPOSITION}'] = [
    item for item in Grammar_Patterns_ENGLISH[f'{NOUN_PHRASE_NON_DET}'] if item != f'{NOUN_PHRASE_NON_DET} {PREPOSITION_PHRASE_NON_DEGRADABLE}'
]

## Noun Phrase Non Det Non Compound : cannot be simplified to noun compounds
Grammar_Patterns_ENGLISH[f'{NOUN_PHRASE_NON_DET_NON_COMPOUND}'] = [
    item for item in Grammar_Patterns_ENGLISH[f'{NOUN_PHRASE_NON_DET}'] if not start_with (item, f'{NOUN_COMPOUND}')
]

## Adjective Phrase Non Degradable : cannot be simplified to adjectives
Grammar_Patterns_ENGLISH[f'{ADJECTIVE_PHRASE_NON_DEGRADABLE}'] = [
    item for item in Grammar_Patterns_ENGLISH[f'{ADJECTIVE_PHRASE}'] if item != f'{ADJECTIVE}'
]

## Preposition Phrase Non Degradable : cannot be simplified to prepositions
Grammar_Patterns_ENGLISH[f'{PREPOSITION_PHRASE_NON_DEGRADABLE}'] = [
    item for item in Grammar_Patterns_ENGLISH[f'{PREPOSITION_PHRASE}'] if item != f'{PREPOSITION}'
]

# 4. The overall POS tags to Patterns rules

# 4.1 English Version
## pos tags to patterns
pos_tags_to_Patterns_ENGLISH = {

    "$": [ # dollar

        # ✅ 
        # ❌ 
        f'{DOLLAR}', 
    ], 

    # special management for the closing quotation mark
    '"': [ # closing quotation mark

        # ✅ 
        # ❌ 
        f'{QUOTE_CLOSE}', 

    ], 

    "(": [ # opening parenthesis

        # ✅ 
        # ❌ 
        f'{PAREN_OPEN}', 
    ],  

    ")": [ # closing parenthesis

        # ✅ 
        # ❌ 
        f'{PAREN_CLOSE}', 
    ], 

    ",": [ # comma

        # ✅ 
        # ❌ 
        f'{COMMA}', 
    ],  

    "--": [ # dash

        # ✅ 
        # ❌ 
        f'{DASH}', 
    ],  

    ".": [ # sentence terminator

        # ✅ 
        # ❌ 
        f'{FULL_STOP}', 
    ],  

    ":": [ # colon or ellipsis

        # ✅ 
        # ❌ 
        f'{COLON}', 
    ], 

    "CC": [ # conjunction, coordinating

        # ✅ 
        # ❌ 
        f'{CONJUNCTION}', 

        # ✅ 
        # ❌ 
        f'{CONJUNCTION_NOUN}', 
    ],  

    "CD": [ # numeral, cardinal

        # ✅ 
        # ❌ 
        f'{ADJECTIVE}', 

        # ✅ 
        # ❌ 
        f'{NOUN}', 
    ], 

    "DT": [ # determiner

        # ✅ 
        # ❌ 
        f'{DETERMINER}', 
    ], 

    "EX": [ # existential there

    ], 

    "FW": [ # foreign word

    ], 

    "IN": [ # preposition or conjunction, subordinating

        # ✅ 
        # ❌ 
        f'{PREPOSITION}', 

        # ✅ 
        # ❌ 
        f'{COMPLEMENT_WORD}', 
    ], 

    "JJ": [ # adjective or numeral, ordinal
        f'{ADJECTIVE}', 
    ], 

    "JJR": [ # adjective, comparative

    ], 

    "JJS": [ # adjective, superlative

    ], 

    "LS": [ # list item marker

    ], 

    "MD": [ # modal auxiliary

        # ✅ 
        # ❌ 
        f'{VERB_AUX}', 

    ], 

    "NN": [ # noun, common, singular or mass

        # ✅ <knowledge> graph, knowledge <graph>
        # ❌ 
        f'{NOUN_CS}', 

    ], 

    "NNP": [ # noun, proper, singular

        # ✅ 
        # ❌ 
        f'{NOUN_PS}', 
    ], 

    "NNPS": [ # noun, proper, plural
        # ✅ 
        # ❌ 
        f'{NOUN_PP}', 
    ], 

    "NNS": [ # noun, common, plural

        # ✅  <data> model, data <model>
        # ❌ 
        f'{NOUN_CP}', 
    ], 

    "PDT": [ # pre-determiner

    ], 

    "POS": [ # genitive marker

        # ✅ 
        # ❌ 
        f'{POSSESSIVE_ENDING}', 

    ], 

    "PRP": [ # pronoun, personal

        # ✅ 
        # ❌ the thing <they>
        f'{NOUN_P}', 
    ],  

    "PRP$": [ # pronoun, possessive

        # ✅ <Her> hat is beautiful
        # ❌ 
        f'{POSSESSION}', 
    ],  

    "RB": [ # adverb

        # ✅ 
        # ❌ 
        f'{ADVERB_DEG}', 

    ], 

    "RBR": [ # adverb, comparative

    ], 

    "RBS": [ # adverb, superlative

    ], 

    "RP": [ # particle

        # ✅ 
        # ❌ 
        f'{PARTICLE}', 
    ], 

    "SYM": [ # symbol

    ], 

    "TO": [ # "to" as preposition or infinitive marker

        # ✅ 
        # ❌ 
        f'{PREPOSITION}', 

        # ✅ 
        # ❌ 
        f'{COMPLEMENT_WORD}', 
    ], 

    "UH": [ # interjection

        # ✅ 
        # ❌ 
        f'{EXCLAMATION}', 

    ], 

    "VB": [ # verb, base form

        # ✅ 
        # ❌ 
        f'{VERB_NON_AUX}', 

        # ✅ 
        # ❌ 
        f'{VERB_PRINCIPLE}', 
    ], 

    "VBD": [ # verb, past tense

        # ✅ 
        # ❌ 
        f'{VERB_NON_AUX}', 

        # ✅ 
        # ❌ 
        f'{VERB_PRINCIPLE}', 
    ],  

    "VBG": [ # verb, present participle or gerund

        # ✅ 
        # ❌ 
        f'{VERB_NON_AUX}', 

        # ✅ 
        # ❌ 
        f'{VERB_PARTICIPLE}', 
    ],  

    "VBN": [ # verb, past participle

        # ✅ 
        # ❌ 
        f'{VERB_NON_AUX}', 

        # ✅ 
        # ❌ 
        f'{VERB_PARTICIPLE}', 

    ],  

    "VBP": [ # verb, present tense, not 3rd person singular

        # ✅ 
        # ❌ 
        f'{VERB_NON_AUX}', 
    ],  

    "VBZ": [ # verb, present tense, 3rd person singular

        # ✅ 
        # ❌ 
        f'{VERB_NON_AUX}', 
    ], 

    "WDT": [ # WH-determiner

        # ✅ 
        # ❌ 
        f'{ARTICLE}', 

        # ✅ a knowledge base <that> uses a graph-structured data model
        # ❌ 
        f'{COMPLEMENT_WORD}', 
    ], 

    "WP": [ # WH-pronoun

        # ✅ 
        # ❌ 

    ], 

    "WP$": [ # WH-pronoun, possessive
        
        # ✅ 
        # ❌ 
        f'{POSSESSION}', 

    ], 

    "WRB": [ # Wh-adverb

    ], 

    "``": [ # opening quotation mark

        # ✅ 
        # ❌ 
        f'{QUOTE_OPEN}', 
    ], 
}

# 4.2 Next Language (COMING SOON)

# 5. Other Settings

language_supported = ['ENGLISH']






















