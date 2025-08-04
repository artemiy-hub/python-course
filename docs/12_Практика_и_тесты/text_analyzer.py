# Анализатор текста - практическое задание
def analyze_text(text):
    words = text.split()
    unique_words = set(word.lower().strip('.,!?;:') for word in words)
    longest_word = max(words, key=len) if words else ""
    
    return {
        'total_chars': len(text),
        'total_words': len(words),
        'unique_words': len(unique_words),
        'longest_word': longest_word,
        'word_list': list(unique_words)
    }

def main():
    text = input("Введите текст для анализа: ")
    result = analyze_text(text)
    
    print(f"\nАнализ текста:")
    print(f"Количество символов: {result['total_chars']}")
    print(f"Количество слов: {result['total_words']}")
    print(f"Уникальных слов: {result['unique_words']}")
    print(f"Самое длинное слово: {result['longest_word']}")
    print(f"Список уникальных слов: {', '.join(result['word_list'])}")

if __name__ == "__main__":
    main() 