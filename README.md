# LitRes book downloader

Скрипты для скачивания книг с litres.ru для которых нет опции скачать.

## Описание

- Заполнить свои данные в [config.py](config.py)
  - Логин
  - Пароль
  - ID книги
  - Количество страниц книги
- Запустить [get_images.py](get_images.py)
  - Ожидать пока он сохранит все страницы
- Запустить [create_pdf.py](create_pdf.py)
  - Ожидать пока он создаст PDF из изображений

В целях удобства скрипты разнесены на 2 отдельных, поскольку каждая процедура занимает около 20-30 минут

## ID книги
- Для получения ID книги открыть *Инструменты разработчика* **(Ctrl+Shift+I)** при онлайн просмотре
- Найти ссылку на изображение вида `https://www.litres.ru/pages/get_pdf_page/?file=ХХХХХХХХ`
- `XXXXXXXX` это и есть ID книги
