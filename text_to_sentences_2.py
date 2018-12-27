from nltk import tokenize


if __name__ == "__main__":
    with open("original_text.txt",encoding='utf-8') as txt:
        text = txt.read()
    sntns = tokenize.sent_tokenize(text)
    
    for s in sntns:
        print (s)
        print ("________")
