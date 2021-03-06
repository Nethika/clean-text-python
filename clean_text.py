import re, string
from string import ascii_lowercase
import spacy
import random
from bs4 import BeautifulSoup 


# read name list from file
with open('names.txt') as f:
    names_list = f.readlines()
# remove whitespace characters like `\n` at the end of each line
names_list = [x.strip() for x in names_list] 
random.shuffle(names_list)


def cleaned_text1(text):
    # TODO: Has a problem with `,`
    punctuation = ['!', ',', '.', ':', ';', '?']
    
    # lower case
    text = text.lower()
    
    # remove non-ascii letters
    text = text.encode("ascii", errors="ignore").decode()
    
    # remove numbers
    text= re.sub(r'\d+', ' ', text)
    
    # remove punctuation other than above list.
    exclude = str(set(string.punctuation) - set(punctuation))
    print(exclude)
    regex = re.compile('[%s]' % re.escape(exclude))
    text = regex.sub(' ', text)
    
    #fix whitespaces
    text = ' '.join(text.split())

    return text

def cleaned_text2(text):
    punctuation = ['!', ',', '.', ':', ';', '?']

    # lower case
    text = text.lower()

    include = punctuation + list(ascii_lowercase) + [' ']

    uniques = ''.join(set(text))
    
    # remove any character that is not in the list:include
    for ch in uniques:
        if ch not in include:
            text = text.replace(ch, ' ')


    #fix whitespaces
    text = ' '.join(text.split())

    return text


def cleaned_text3(text):
    entity_prefixes = ['@','#']
    
    #Remove punctuation other than @ and #
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    return text

def remove_urls(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ' ')      
    return text


def replace_urls(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], 'www.example.com')  
    return text

def remove_hashtags_handles(text):
    entity_prefixes = ['@','#']

    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def replace_handles1(text):
    # Looses . , : at the end of the @word.
    # Doesn't catch '@username83'
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            print (word)
            if len(word) != 1 and word[0] == '@':
                word = '@example_com'
                print(word)
            print("")
            words.append(word)
    return ' '.join(words)

def replace_handles2(text): 
    handles_regex = re.compile('(?<=^|(?<=[^a-zA-Z0-9-_\.]))(@[A-Za-z0-9-_]+)', re.DOTALL) 
    handles = re.findall(handles_regex, text)
    print("[TWITTER HANDLES REPLACED]:",handles)
    for handle in handles:
        text = text.replace(handle, '@example_com')  
    return text

def replace_dot_handler(text):
    handles_regex = re.compile('(?<=^|(?<=[^a-zA-Z0-9-_\.]))(\.@[A-Za-z0-9-_]+)', re.DOTALL) 
    handles = re.findall(handles_regex, text)
    print("[TWITTER HANDLES REPLACED]:",handles)
    for handle in handles:
        text = text.replace(handle, '@example_com')  
    return text

def replace_reddit_user(text):
    handles_regex = re.compile('u/[A-Za-z0-9_-]+', re.DOTALL) 
    handles = re.findall(handles_regex, text)
    print("[REDDIT HANDLES REPLACED]:",handles)
    for handle in handles:
        text = text.replace(handle, '@example_com')  
    return text

def replace_subreddit(text):
    handles_regex = re.compile('r/[A-Za-z0-9_-]+', re.DOTALL) 
    handles = re.findall(handles_regex, text)
    print("[REDDIT HANDLES REPLACED]:",handles)
    for handle in handles:
        text = text.replace(handle, '@example_com')  
    return text

def replace_email(text):
    email_regex = re.compile("[\w.-]+@[\w.-]+\.\w+", re.DOTALL) 
    #email_regex = re.compile('[\w\.-]+@[\w\.-]+\.\w+', re.DOTALL) #same as above.
    emails = re.findall(email_regex, text)
    print("[EMAILS REPLACED]:",emails)
    for email in emails:
        text = text.replace(email, 'example@example_com')  
    return text


def replace_names(text):
        
    """
    # ent.label_:
    
    TYPE	    DESCRIPTION
    -------------------------------------------------------
    PERSON	    People, including fictional.
    NORP	    Nationalities or religious or political groups.
    FAC	        Buildings, airports, highways, bridges, etc.
    ORG	        Companies, agencies, institutions, etc.
    GPE	        Countries, cities, states.
    LOC	        Non-GPE locations, mountain ranges, bodies of water.
    PRODUCT	    Objects, vehicles, foods, etc. (Not services.)
    EVENT	    Named hurricanes, battles, wars, sports events, etc.
    WORK_OF_ART	Titles of books, songs, etc.
    LAW	        Named documents made into laws.
    LANGUAGE	Any named language.
    DATE	    Absolute or relative dates or periods.
    TIME	    Times smaller than a day.
    PERCENT	    Percentage, including "%".
    MONEY	    Monetary values, including unit.
    QUANTITY	Measurements, as of weight or distance.
    ORDINAL	    "first", "second", etc.
    CARDINAL	Numerals that do not fall under another type.
    """
    
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    entities = []
    ent_anonymise = ['PERSON','ORG']

    for ent in doc.ents:
        #print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_ in ent_anonymise:
            if ent.text not in entities:
                entities.append(ent.text)
        #if ent.label_ == 'PERSON':
            
    #print(entities)
    dict_entities = dict(zip(entities, names_list))
    print (dict_entities)
    for k,v in dict_entities.items():
        text = text.replace(k, v)
    #print (anonymous)
    #print("")
    return text


def remove_html_tags(html_text):  
    soup = BeautifulSoup(html_text,features="html5lib")
    raw = soup.get_text()
    return raw


def replace_digits(text):
    """
    Replace each digit with a '5'
    """
    text = re.sub('[0-9]', '5', text)
    return text

def replace_newlines_tabs(text):
    text = re.sub('[\t\n\r]', ' ', text)
    #fix whitespaces
    text = ' '.join(text.split())
    return text

if __name__ == "__main__":
        text = "### ï»¿project gutenberg's; , 7 by arthur conan doyle\n\nthis ebook is for the use of anyone anywhere at no cost and with\nalmost no restrictions whatsoever.  Hej då. hej d\xe5! TODO: fill > out + the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model def window_transform_text(text, window_size, step_size):"
        text = cleaned_text2(text)
        print("cleaned text:")
        print (text)

        html_text = '<a href="http://example.com/">\nI linked to <i>example.com</i>\n</a>'
        text = remove_html_tags(html_text)
        print("cleaned text:")
        print (text)
