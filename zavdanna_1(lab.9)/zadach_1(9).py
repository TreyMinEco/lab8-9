import matplotlib.pyplot as plt
import nltk
from nltk.corpus import gutenberg, stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def load_text(filename):
    try:
        if filename in gutenberg.fileids():
            raw_text = gutenberg.raw(filename)
            print("File yspishno vidcrito")
            return raw_text
        else:
            print("Error, file ne znaydeno!")
            return None
    except Exception as e:
        print("Error:", e)
        return None

def analyze_words(raw_text):
    if raw_text is None:
        print("Error, dani ne proanalizovano!")
        return None

    tokens = word_tokenize(raw_text)
    words = [w.lower() for w in tokens if w.isalpha()]

    total_words = len(words)
    total_unique = len(set(words))

    print("\nPochatkovi dani:")
    print(f"Total words: {total_words}")
    print(f"Unique words: {total_unique}")
    return words

def draw_plot(top_data, title_text):
    w_list, f_list = zip(*top_data)
    plt.bar(w_list, f_list)
    plt.title(title_text)
    plt.xlabel("Words")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

def top_ten_raw(words):
    if words is None:
        print("Error ne mae danih!")
        return

    fdist = FreqDist(words)
    top_ten = fdist.most_common(10)

    print("\nTop 10 raw words:")
    for word, freq in top_ten:
        print(f"{word}: {freq}")

    draw_plot(top_ten, "Top 10 Raw Words")

def clean_and_filter(words):
    if words is None:
        print("Error ne mae danih dlya ochishenya!")
        return None

    stop_words = set(stopwords.words("english"))
    cleaned_words = [w for w in words if w not in stop_words]

    fdist = FreqDist(cleaned_words)
    top_ten_clean = fdist.most_common(10)

    print("\nTop 10 clean words:")
    for word, freq in top_ten_clean:
        print(f"  - '{word}': {freq}")

    draw_plot(top_ten_clean, "Top 10 Clean Words")
    return cleaned_words

def apply_stemming(cleaned_words):
    if cleaned_words is None:
        print("Error ne mae danih dlya stemming!")
        return

    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(w) for w in cleaned_words]

    fdist = FreqDist(stemmed_words)
    top_ten_stemmed = fdist.most_common(10)

    print("\nTop 10 stemmed words:")
    for word, freq in top_ten_stemmed:
        print(f"  - '{word}': {freq}")

    draw_plot(top_ten_stemmed, "Top 10 Stemmed Words")

def main():
    filename = "whitman-leaves.txt"
    raw_text = load_text(filename)
    if raw_text is None:
        print("Program finish!")
        return

    words = analyze_words(raw_text)
    top_ten_raw(words)
    cleaned_words = clean_and_filter(words)
    apply_stemming(cleaned_words)

main()