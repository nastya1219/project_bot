Телеграм-бот
Предназначен для теста на знание русской литературы. Есть тексты двух произведений:
Преступления и наказания и Обломова, с помощью рандома мы выбираем любое из произведений, после этого генерируем на основе него текст путем создания марковской цепи.
Далее проводится текст, где пользователь видит сгенерированное предложение, выбирает одно из произведений, далее система говорит, прав пользователь или нет (откуда взято предложение).
Также бот может показать облака частотных слов из этих произведений.

Использование:
1. Для начала работы с ботом нужно написать /start
2. Для просмотра информации о боте нужно написать /help
3. Для генерации предложения нужно нажать /generate

Файлы в репозитории:
bot_telegram.py - основной файл, где происходит работа с моделью и ботом
clouds_pin.py - файл, в котором создается облако слов на основе текста Преступления и наказания
clouds_oblomov.py - файл, в котором создается облако слов на основе текста Обломова
oblomov.txt, PiN.txt - тексты нужных произведений
winner.jpg, lost.jpg - картинки, которые используются в боте
word_cloud_pin, word_cloud_oblomov - созданные облака слов

Автор: Анастасия Кленова (@stasik1219)