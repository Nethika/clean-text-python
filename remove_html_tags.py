from bs4 import BeautifulSoup 


def remove_html_tags(html_text):  
    soup = BeautifulSoup(html_text,features="html5lib")
    raw = soup.get_text()
    return raw

if __name__ == "__main__":
        html_text = '<a href="http://example.com/">\nI linked to <i>example.com</i>\n</a>'
        text = remove_html_tags(html_text)
        print("cleaned text:")
        print (text)