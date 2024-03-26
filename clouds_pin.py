import nltk
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from pymystem3 import Mystem

nltk.download('punkt')
nltk.download('stopwords')

with open('PiN.txt', 'r', encoding='windows-1251') as file:
    text = file.read()

m = Mystem()
all_text = m.lemmatize(text)  # лемматизируем текст
all_text = [w for w in all_text if w.strip()]


# Загрузка стоп-слов на русском языке
stop_words = set(stopwords.words('russian') + ['это', 'то', 'все', 'всё'])

# Список слов
words = all_text

# Удаление стоп-слов из списка слов
filtered_words = [word for word in words if word.lower() not in stop_words]

# Объединение слов в строку
text = ' '.join(filtered_words)

# Создание облака слов
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
wordcloud.to_file("wordcloud_pin.png")

# Отображение облака слов
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
