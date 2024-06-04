import os
import json
import time
from tkinter import *
from file_utils import FileUtils
from typing_test_logic import TypingTestLogic
from history_manager import HistoryManager
from typing_test_ui import TypingTestUI
from logging import getLogger, basicConfig, DEBUG, FileHandler, StreamHandler, ERROR, INFO

logger = getLogger()
FORMAT = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
file_handler = FileHandler('data/data.log')
file_handler.setLevel(DEBUG)
console = StreamHandler()
console.setLevel(INFO)
basicConfig(level=DEBUG, format=FORMAT, handlers=[file_handler, console])


class TypingSpeedTest:
	SETTINGS_FILE = "data/settings.json"

	def __init__(self, root, count_word: int = 10, max_len_line: int = 20, language: str = "eng"):
		self.root = root
		self.root.title("Тест скорости печати")
		self.root.geometry("800x600")

		if self.SETTINGS_FILE:
			self.load_settings()
		else:
			self.COUNT_WORD = count_word
			self.MAX_LEN_LINE = max_len_line
			self.LANGUAGE = language

		self.file = FileUtils(f"data/{self.LANGUAGE}_words.txt")
		self.text = self.file.get_text(self.COUNT_WORD, self.MAX_LEN_LINE)
		self.text_split = self.file.split_text(self.text)

		self.logic = TypingTestLogic(self.text_split)
		self.ui = TypingTestUI(self.root, self.text, self.on_key_press, self.on_key_release)
		self.history_manager = HistoryManager()

		self.root.bind("<Control-h>", self.show_history)
		self.root.bind("<Control-r>", self.update_text)
		self.root.bind("<Control-z>", self.exit_app)
		self.root.bind("<Control-s>", self.show_settings)
		logger.info(f"Параметры приложения: \nфайл с настройками - {os.path.abspath(self.SETTINGS_FILE)}\n"
					 f"файл со словами - {os.path.abspath(self.file.filename)}\n"
					 f"файл с логами - {file_handler.baseFilename}")
		logger.info("Создано окно приложения")

	def on_key_press(self, event):
		if self.logic.start_time is None:
			self.logic.start_time = time.time()
			logger.info("Начало теста, время засеклось")
		if event.keysym == "Return":
			logger.info("Enter нажимать нельзя")
			return "break"

	def on_key_release(self, event):
		if event.keysym == "Return":
			return "break"
		self.logic.process_key_release(event, self.ui, self.end_test)

	def end_test(self):
		logger.info("Завершение теста")
		elapsed_time, error_count, total_chars, accuracy, speed = self.logic.calculate_results()

		result_text = (
			f"Аккуратность: {accuracy:.2f}%\n"
			f"Ошибок: {error_count} из {total_chars} символов\n"
			f"Заняло времени: {elapsed_time:.2f} сек.\n"
			f"Скорость: {speed:.2f} символов в минуту"
		)

		self.history_manager.save_result(self.COUNT_WORD, error_count, total_chars, accuracy, elapsed_time, speed)
		self.ui.show_result(result_text)
		logger.info("Показан результат")

	def reset_ui(self):
		logger.info("Возврат в главное окно с тестом")
		for widget in self.root.winfo_children():
			widget.destroy()
		self.ui = TypingTestUI(self.root, self.text, self.on_key_press, self.on_key_release)
		logger.info("Успешно вернулись в главное окно")

	def update_text(self, event=None):
		logger.info(f"Обновление текста с параметрами кол-во слов: {self.COUNT_WORD}, "
					f"макс. длина строки: {self.MAX_LEN_LINE}, язык: {self.LANGUAGE}")
		self.text = self.file.get_text(self.COUNT_WORD, self.MAX_LEN_LINE)
		self.text_split = self.file.split_text(self.text)
		self.logic = TypingTestLogic(self.text_split)
		self.reset_ui()
		self.ui.update_display_widget(self.text)
		logger.info(f"Текст успешно обновлен на: {self.text_split}")

	def show_history(self, event=None):
		self.ui.show_history_window(self.history_manager)

	def exit_app(self, event=None):
		logger.info("Было нажато Ctrl + Z закрываем приложение...")
		self.root.quit()

	def show_settings(self, event=None):
		logger.info("Открытие окна с настройками")
		for widget in self.root.winfo_children():
			widget.destroy()

		settings_frame = Frame(self.root)
		settings_frame.pack(expand=True, fill='both')

		count_word_label = Label(settings_frame, text="Количество слов:", font=self.ui.font)
		count_word_label.pack(pady=5)
		count_word_entry = Entry(settings_frame, font=self.ui.font)
		count_word_entry.insert(0, self.COUNT_WORD)
		count_word_entry.pack(pady=5)
		logger.info(f"Показано окно с изменением количество слов, сейчас ({self.COUNT_WORD})")

		max_len_line_label = Label(settings_frame, text="Максимальное количество символов в строке:", font=self.ui.font)
		max_len_line_label.pack(pady=5)
		max_len_line_entry = Entry(settings_frame, font=self.ui.font)
		max_len_line_entry.insert(0, self.MAX_LEN_LINE)
		max_len_line_entry.pack(pady=5)
		logger.info(f"Показано окно с изменением максимального количества символов в строке, сейчас ({self.MAX_LEN_LINE})")

		language_label = Label(settings_frame, text="Язык (eng/rus):", font=self.ui.font)
		language_label.pack(pady=5)
		language_entry = Entry(settings_frame, font=self.ui.font)
		language_entry.insert(0, self.LANGUAGE)
		language_entry.pack(pady=5)
		logger.info(f"Показано окно с изменением языка, сейчас ({self.LANGUAGE})")

		save_button = Button(settings_frame, text="Сохранить",
							 command=lambda: self.save_settings(count_word_entry.get(), max_len_line_entry.get(),
																language_entry.get()), font=self.ui.font)
		save_button.pack(pady=20)
		logger.debug("Показана кнопка сохранить")

		back_button = Button(settings_frame, text="Назад", command=self.reset_ui, font=self.ui.font)
		back_button.pack(pady=5)
		logger.debug("Показана кнопка назад")

	def save_settings(self, count_word, max_len_line, language):
		logger.info("Сохранение новых настроек")
		self.COUNT_WORD = int(count_word)
		self.MAX_LEN_LINE = int(max_len_line)
		self.LANGUAGE = language
		settings = {
			"COUNT_WORD": self.COUNT_WORD,
			"MAX_LEN_LINE": self.MAX_LEN_LINE,
			"LANGUAGE": self.LANGUAGE
		}
		logger.info(f"Новые настройки: {settings}")
		with open(self.SETTINGS_FILE, "w") as file:
			json.dump(settings, file)
		logger.info(f"Настройки успешно сохранены в файл: {os.path.abspath(self.SETTINGS_FILE)}")
		self.update_text()
		logger.info("Настройки успешно сохранены")

	def load_settings(self):
		logger.info("Загрузка настроек приложения")
		if os.path.exists(self.SETTINGS_FILE):
			logger.info(f"Файл {self.SETTINGS_FILE} был успешно найден")
			with open(self.SETTINGS_FILE, "r") as file:
				logger.info(f"Файл {self.SETTINGS_FILE} был успешно открыт")
				settings = json.load(file)
				logger.info(f"Данные из файла {self.SETTINGS_FILE} были успешно получены: {settings}")
				self.COUNT_WORD = settings.get("COUNT_WORD", 10)
				self.MAX_LEN_LINE = settings.get("MAX_LEN_LINE", 20)
				self.LANGUAGE = settings.get("LANGUAGE", "eng")
		logger.info("Настройки приложения успешно загружены")


if __name__ == "__main__":
	root = Tk()
	logger.info("-------------------------Приложение успешно запустилось-------------------------")
	TypingSpeedTest(root)
	root.mainloop()
	logger.info("-------------------------Приложение было успешно закрыто-------------------------")
