import re, string

def cleaned_text(text):
    
    punctuation = ['!', ',', '.', ':', ';', '?']
    

    # lower case
    text = text.lower()
    
    # remove non-ascii letters
    text = text.encode("ascii", errors="ignore").decode()
    
    # remove numbers
    text= re.sub(r'\d+', ' ', text)
    
    # remove punctuation other than above list.
    exclude = str(set(string.punctuation) - set(punctuation))
    regex = re.compile('[%s]' % re.escape(exclude))
    text = regex.sub(' ', text)
    
    #fix whitespaces
    text = ' '.join(text.split())

    return text

if __name__ == "__main__":
        text = "### ï»¿project gutenberg's; , 7 by arthur conan doyle\n\nthis ebook is for the use of anyone anywhere at no cost and with\nalmost no restrictions whatsoever.  Hej då. hej d\xe5! TODO: fill > out + the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model def window_transform_text(text, window_size, step_size):"
        text = cleaned_text(text)
        print("cleaned text:")
        print (text)
