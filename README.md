# Typing Speed Test Application

## Описание

Это приложение для тестирования скорости печати. Оно позволяет пользователям оценивать свою скорость набора текста на разных языках и сохранять результаты для последующего анализа. В приложении можно настроить количество слов, максимальную длину строки и язык теста.

## Основные функции

- **Тест скорости печати**: Пользователь может начать тест, набрав предложенный текст. По окончании теста выводятся результаты, такие как скорость печати, количество ошибок, общая точность и затраченное время.
- **История тестов**: Хранение результатов предыдущих тестов, возможность их просмотра.
- **Настройки**: Возможность изменения параметров теста, таких как количество слов, максимальная длина строки, язык теста и частотность слов.
- **Логирование**: Ведение логов для отслеживания работы приложения и отладки.

## Установка

Склонируйте репозиторий:

```sh
git clone https://github.com/a-melchikov/python-typing-speed.git
```

Установите зависимости:

```sh
pip install -r requirements.txt
```

## Использование

Запустите приложение:
```sh
python main.py
```

Интерфейс приложения будет запущен. Используйте следующие комбинации клавиш для управления:
- **Ctrl + H**: Показать историю тестов.
- **Ctrl + R**: Обновить текст для теста.
- **Ctrl + Z**: Закрыть приложение.
- **Ctrl + S**: Открыть настройки.

## Структура проекта

- **main.py**: Главный файл приложения, содержащий основной класс `TypingSpeedTest`.
- **file_utils.py**: Модуль для работы с файлами, содержащими тексты.
- **typing_test_logic.py**: Логика обработки теста скорости печати.
- **history_manager.py**: Модуль для управления историей тестов.
- **typing_test_ui.py**: Интерфейс пользователя для приложения.
- **data/**: Папка для хранения файлов настроек, логов и текстов.
Логи приложения сохраняются в файле `data/data.log`. Файл логов ограничен размером в 500 кБ.