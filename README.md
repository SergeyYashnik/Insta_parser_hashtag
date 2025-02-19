# Instagram Parser

Этот проект предназначен для сбора данных (просмотры, лайки) с постов в Instagram с помощью Selenium.

### Создание виртуального окружения (рекомендуется)

```sh
python3 -m venv venv
```
**Для macOS/Linux:**  
```sh
source venv/bin/activate
```
**Для Windows:**  
```sh
venv\Scripts\activate
```

### Установка зависимостей

```sh
pip3 install -r requirements.txt
```

### Настройка переменных окружения

Создайте файл `.env` (можете просто скопировать `.env.example` и удалить `.example` из названия) в корневой папке проекта и укажите в нем данные:

```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### Установка драйвера Chrome

Проект использует **Google Chrome** и **ChromeDriver**. Убедитесь, что они установлены:

- **Google Chrome**: [Скачать Chrome](https://www.google.com/chrome/)
- **ChromeDriver**: [Скачать ChromeDriver](https://sites.google.com/chromium.org/driver/)

После скачивания **разместите chromedriver в папке проекта** или добавьте путь в переменную окружения.

### Запуск парсера

```sh
python3 main.py
```

## 🛠 Основные зависимости

- **Selenium** — для автоматизации браузера
- **pandas** — для обработки данных
- **python-dotenv** — для работы с переменными окружения

## 📝 Автор

[Sergey Yashnik] - [SergeyYashnik](https://github.com/SergeyYashnik)

## 📜 Лицензия

Этот проект распространяется под лицензией MIT. Используйте на свой страх и риск.

