import requests
import matplotlib.pyplot as plt
from collections import defaultdict
import re

# Функція Map
def map_function(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return [(word, 1) for word in words]

# Функція Shuffle
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

# Функція Reduce
def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

# MapReduce
def map_reduce(text):
    mapped_values = map_function(text)
    shuffled_values = shuffle_function(mapped_values)
    reduced_values = reduce_function(shuffled_values)
    return reduced_values

# Візуалізація топ-слів
def visualize_top_words(word_counts, top_n=10):
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    words, counts = zip(*sorted_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    try:
        # Зчитування URL з файлу
        with open('url.txt', 'r') as f:
            url = f.read().strip()

        response = requests.get(url)

        if response.status_code == 200:
            text = response.text

            # Аналіз тексту
            word_counts = map_reduce(text)

            # Візуалізація
            visualize_top_words(word_counts, top_n=10)
        else:
            print(f"Не вдалося завантажити текст. Код статусу: {response.status_code}")
    except FileNotFoundError:
        print("Файл url.txt не знайдено. Створіть файл із URL-адресою.")