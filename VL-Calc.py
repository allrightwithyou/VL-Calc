import os
import sys
import tkinter as tk
from tkinter import ttk
import math

def resource_path(relative_path):
    """Получить абсолютный путь к ресурсу в .exe или при запуске скрипта"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ScreenCalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор параметров экрана")
        self.root.geometry("1000x700")
        self.root.minsize(800, 500)
        try:
            self.root.iconbitmap(resource_path("VL.ico"))  # Используем resource_path для иконки
        except tk.TclError:
            print("Ошибка загрузки иконки. Продолжаем без иконки.")

        # Настройка стилей
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))

        # Основной фрейм
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Фреймы для ввода и результатов
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Поля ввода
        self.entries = {}
        self.result_entries = {}

        # Создание фреймов для категорий ввода
        self.frame_screen = ttk.LabelFrame(input_frame, text="Экран")
        self.frame_module = ttk.LabelFrame(input_frame, text="Модуль")
        self.frame_receiver = ttk.LabelFrame(input_frame, text="Приёмная карта")
        self.frame_psu = ttk.LabelFrame(input_frame, text="Блоки питания")

        self.frame_screen.pack(fill="x", pady=(0, 8))
        self.frame_module.pack(fill="x", pady=(0, 8))
        self.frame_receiver.pack(fill="x", pady=(0, 8))
        self.frame_psu.pack(fill="x", pady=(0, 8))

        # Поля ввода для экрана
        screen_fields = [
            ("Ширина экрана (м):", "screen_width"),
            ("Высота экрана (м):", "screen_height"),
        ]
        self._create_fields(self.frame_screen, screen_fields)

        # Поля ввода для модуля
        module_fields = [
            ("Ширина модуля (мм):", "module_width"),
            ("Высота модуля (мм):", "module_height"),
            ("Шаг пикселя (мм):", "pixel_pitch"),
            ("Разрешение модуля по ширине (px):", "module_res_x"),
            ("Разрешение модуля по высоте (px):", "module_res_y"),
            ("Потребление модуля (А):", "module_current"),
        ]
        self._create_fields(self.frame_module, module_fields)

        # Поля ввода для приёмной карты
        receiver_fields = [
            ("Ширина кабинета (px):", "receiver_width_px"),
            ("Высота кабинета (px):", "receiver_height_px"),
            ("Портов на приёмной карте:", "receiver_ports"),
            ("Модулей в одной цепочке (на порт):", "modules_per_chain"),
        ]
        self._create_fields(self.frame_receiver, receiver_fields)

        # Поля ввода для блоков питания
        psu_fields = [
            ("Напряжение блока питания (В):", "psu_voltage"),
            ("Мощность блока питания (Вт):", "psu_power"),
            ("Запас блока питания (Вт):", "psu_reserve_watts"),
        ]
        self._create_fields(self.frame_psu, psu_fields)

        # Кнопка "Рассчитать"
        btn = ttk.Button(input_frame, text="Рассчитать", command=self.calculate)
        btn.pack(fill="x", pady=10)

        # Создание области результатов с прокруткой
        self.canvas = tk.Canvas(result_frame, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Привязка события Configure для обновления области прокрутки
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Создание окна в Canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Упаковка Canvas и Scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Внутренний фрейм для результатов
        self.result_frame_inner = ttk.Frame(self.scrollable_frame)
        self.result_frame_inner.pack(fill="both", expand=True)

        # Синхронизация ширины окна Canvas
        self.result_frame_inner.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())
        )

        # Привязка прокрутки колесом мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Создание полей результатов
        row = 0
        # Категория: Расчёт модулей и экрана
        lbl = ttk.Label(self.result_frame_inner, text="Расчёт модулей и экрана", style="Header.TLabel")
        lbl.grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=(8, 4))
        row += 1
        result_fields_screen = [
            ("Модули по ширине:", "modules_x"),
            ("Модули по высоте:", "modules_y"),
            ("Общее количество модулей:", "total_modules"),
            ("Площадь экрана:", "area_m2"),
            ("Общее разрешение:", "total_resolution"),
            ("Общее число пикселей:", "total_pixels"),
            ("Плотность пикселей:", "pixels_per_m2"),
        ]
        for label_text, key in result_fields_screen:
            self._create_result_field(self.result_frame_inner, row, label_text, key)
            row += 1

        # Пустая строка
        row += 1

        # Категория: Приёмные карты
        lbl = ttk.Label(self.result_frame_inner, text="Приёмные карты", style="Header.TLabel")
        lbl.grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=(8, 4))
        row += 1
        result_fields_receiver = [
            ("Пикселей в одном модуле:", "pixels_per_module"),
            ("Макс. пикселей на карту:", "receiver_pixel_limit"),
            ("Макс. модулей по пикселям:", "max_modules_by_pixels"),
            ("Макс. модулей по портам:", "max_modules_by_ports"),
            ("Макс. модулей на карту:", "max_modules_per_card"),
            ("Требуется приёмных карт:", "receiver_cards_needed"),
        ]
        for label_text, key in result_fields_receiver:
            self._create_result_field(self.result_frame_inner, row, label_text, key)
            row += 1

        # Пустая строка
        row += 1

        # Категория: Питание
        lbl = ttk.Label(self.result_frame_inner, text="Питание", style="Header.TLabel")
        lbl.grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=(8, 4))
        row += 1
        result_fields_power = [
            ("Потребление одного модуля DC:", "power_per_module_dc"),
            ("Потребление одного модуля AC:", "power_per_module_ac"),
            ("Модулей в 1 м²:", "modules_per_m2"),
            ("Потребление 1 м² DC:", "power_per_m2_dc"),
            ("Потребление 1 м² AC:", "power_per_m2_ac"),
        ]
        for label_text, key in result_fields_power:
            self._create_result_field(self.result_frame_inner, row, label_text, key)
            row += 1

        # Пустая строка
        row += 1

        # Категория: Блоки питания
        lbl = ttk.Label(self.result_frame_inner, text="Блоки питания", style="Header.TLabel")
        lbl.grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=(8, 4))
        row += 1
        result_fields_psu = [
            ("Мощность блока питания:", "psu_power"),
            ("Запас блока питания:", "psu_reserve"),
            ("Доступная мощность:", "available_power"),
            ("Модулей на один блок питания:", "modules_per_psu"),
            ("Остаточная мощность на блок:", "reserve_power"),
            ("Всего блоков питания:", "total_psus"),
        ]
        for label_text, key in result_fields_psu:
            self._create_result_field(self.result_frame_inner, row, label_text, key)
            row += 1

        # Пустая строка
        row += 1

        # Категория: Общее потребление
        lbl = ttk.Label(self.result_frame_inner, text="Общее потребление", style="Header.TLabel")
        lbl.grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=(8, 4))
        row += 1
        result_fields_total_power = [
            ("Общее потребление DC:", "total_power_dc"),
            ("Общее потребление AC:", "total_power_ac"),
            ("Среднее потребление AC:", "average_power_ac"),
            ("Среднее минимальное потребление AC:", "minimal_average_power_ac"),
        ]
        for label_text, key in result_fields_total_power:
            self._create_result_field(self.result_frame_inner, row, label_text, key)
            row += 1

    def _create_fields(self, parent, fields):
        for i, (label_text, key) in enumerate(fields):
            lbl = ttk.Label(parent, text=label_text)
            lbl.grid(row=i, column=0, sticky="w", padx=(10, 5), pady=4)
            entry = ttk.Entry(parent, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, sticky="ew", padx=(5, 10), pady=4)
            parent.columnconfigure(1, weight=1)
            self.entries[key] = entry
            # Привязка Ctrl+V к вставке значения
            entry.bind('<Control-v>', lambda event, e=entry: self.paste_entry_value(event, e))

    def _create_result_field(self, parent, row, label_text, key):
        lbl = ttk.Label(parent, text=label_text)
        lbl.grid(row=row, column=0, sticky="w", padx=(5, 5), pady=4)
        entry = ttk.Entry(parent, font=("Segoe UI", 10), state="readonly")
        entry.grid(row=row, column=1, sticky="ew", padx=(5, 5), pady=4)
        parent.columnconfigure(1, weight=1)
        self.result_entries[key] = entry
        # Привязка Ctrl+C к копированию значения
        entry.bind('<Control-c>', lambda event, e=entry: self.copy_entry_value(event, e))

    def copy_entry_value(self, event, entry):
        value = entry.get()
        if value:
            self.root.clipboard_clear()
            self.root.clipboard_append(value)
        return "break"

    def paste_entry_value(self, event, entry):
        try:
            value = self.root.clipboard_get()
            entry.delete(0, tk.END)
            entry.insert(0, value)
        except Exception:
            pass
        return "break"

    def _on_mousewheel(self, event):
        # Прокрутка колесом мыши для Windows
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def copy_selection(self, event):
        focused_widget = self.root.focus_get()
        if isinstance(focused_widget, ttk.Entry) and focused_widget in self.result_entries.values():
            selected_text = focused_widget.get()
            if selected_text:
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
        return "break"

    def safe_float(self, value):
        try:
            return float(value.replace(",", "."))
        except ValueError:
            raise ValueError(f"Некорректное значение: {value}")

    def format_number(self, value):
        """Форматирование числа: целое без дробной части, дробное с 3 знаками"""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return f"{value:.3f}"

    def calculate(self):
        # Очистка предыдущих результатов
        for entry in self.result_entries.values():
            entry.configure(state="normal")
            entry.delete(0, tk.END)
            entry.configure(state="readonly")

        try:
            # Получение входных данных
            module_w = self.safe_float(self.entries["module_width"].get())
            module_h = self.safe_float(self.entries["module_height"].get())
            pixel_pitch = self.safe_float(self.entries["pixel_pitch"].get())
            screen_w_m = self.safe_float(self.entries["screen_width"].get())
            screen_h_m = self.safe_float(self.entries["screen_height"].get())
            module_res_x = int(self.entries["module_res_x"].get())
            module_res_y = int(self.entries["module_res_y"].get())
            receiver_ports = int(self.entries["receiver_ports"].get())
            receiver_width_px = int(self.entries["receiver_width_px"].get())
            receiver_height_px = int(self.entries["receiver_height_px"].get())
            modules_per_chain = int(self.entries["modules_per_chain"].get())
            module_current = self.safe_float(self.entries["module_current"].get())
            psu_voltage = self.safe_float(self.entries["psu_voltage"].get())
            psu_power = self.safe_float(self.entries["psu_power"].get())
            psu_reserve = self.safe_float(self.entries["psu_reserve_watts"].get())

            if module_current == 0:
                raise ValueError("Потребление модуля не может быть 0 А.")

            # Расчёты
            screen_w_mm = screen_w_m * 1000
            screen_h_mm = screen_h_m * 1000

            modules_x = math.ceil(screen_w_mm / module_w)
            modules_y = math.ceil(screen_h_mm / module_h)
            total_modules = modules_x * modules_y

            area_m2 = (modules_x * module_w / 1000) * (modules_y * module_h / 1000)

            total_px_x = modules_x * module_res_x
            total_px_y = modules_y * module_res_y
            total_pixels = total_px_x * total_px_y
            pixels_per_m2 = total_pixels / area_m2
            pixels_per_module = module_res_x * module_res_y

            receiver_pixel_limit = receiver_width_px * receiver_height_px

            max_modules_by_pixels = receiver_pixel_limit // pixels_per_module
            max_modules_by_ports = receiver_ports * modules_per_chain
            max_modules_per_card = min(max_modules_by_pixels, max_modules_by_ports)

            if max_modules_per_card == 0:
                raise ValueError("Невозможно подключить ни одного модуля к приёмной карте.")

            receiver_cards_needed = math.ceil(total_modules / max_modules_per_card)

            power_per_module_dc = psu_voltage * module_current
            power_per_module_ac = power_per_module_dc / 0.7

            modules_per_m2 = (1000 * 1000) / (module_w * module_h)
            power_per_m2_dc = modules_per_m2 * power_per_module_dc
            power_per_m2_ac = power_per_m2_dc / 0.7

            available_power = psu_power - psu_reserve
            if available_power <= 0:
                raise ValueError("Запас превышает или равен общей мощности блока питания.")

            modules_per_psu = int(available_power // power_per_module_dc)
            used_power = modules_per_psu * power_per_module_dc
            reserve_power = psu_power - used_power

            if modules_per_psu < 1:
                modules_per_psu = 1
                reserve_power = psu_power - power_per_module_dc

            total_psus = math.ceil(total_modules / modules_per_psu)

            total_power_dc = available_power * total_psus
            total_power_ac = total_power_dc / 0.7
            average_power_ac = total_power_ac / 3
            minimal_average_power_ac = average_power_ac / 3

            # Заполнение полей результатов
            results = {
                "modules_x": str(modules_x),
                "modules_y": str(modules_y),
                "total_modules": str(total_modules),
                "area_m2": f"{self.format_number(area_m2)} м²",
                "total_resolution": f"{total_px_x} × {total_px_y} пикселей",
                "total_pixels": str(total_pixels),  # Без запятых
                "pixels_per_m2": f"{self.format_number(pixels_per_m2)} пикселей/м²",  # Без запятых и дробной части для целых
                "pixels_per_module": str(pixels_per_module),
                "receiver_pixel_limit": str(receiver_pixel_limit),
                "max_modules_by_pixels": str(max_modules_by_pixels),
                "max_modules_by_ports": f"{max_modules_by_ports} (по {modules_per_chain} мод/порт)",
                "max_modules_per_card": str(max_modules_per_card),
                "receiver_cards_needed": str(receiver_cards_needed),
                "power_per_module_dc": f"{self.format_number(power_per_module_dc)} Вт ({self.format_number(psu_voltage)} В)",
                "power_per_module_ac": f"{self.format_number(power_per_module_ac)} Вт ({self.format_number(psu_voltage)} В)",
                "modules_per_m2": f"{self.format_number(modules_per_m2)}",
                "power_per_m2_dc": f"{self.format_number(power_per_m2_dc)} Вт",
                "power_per_m2_ac": f"{self.format_number(power_per_m2_ac)} Вт",
                "psu_power": f"{self.format_number(psu_power)} Вт",
                "psu_reserve": f"{self.format_number(psu_reserve)} Вт",
                "available_power": f"{self.format_number(available_power)} Вт",
                "modules_per_psu": str(modules_per_psu),
                "reserve_power": f"{self.format_number(reserve_power)} Вт",
                "total_psus": str(total_psus),
                "total_power_dc": f"{self.format_number(total_power_dc)} Вт",
                "total_power_ac": f"{self.format_number(total_power_ac)} Вт",
                "average_power_ac": f"{self.format_number(average_power_ac)} Вт",
                "minimal_average_power_ac": f"{self.format_number(minimal_average_power_ac)} Вт",
            }

            for key, value in results.items():
                entry = self.result_entries[key]
                entry.configure(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, value)
                entry.configure(state="readonly")

            # Обновление области прокрутки после заполнения результатов
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        except Exception as e:
            self.result_entries["modules_x"].configure(state="normal")
            self.result_entries["modules_x"].delete(0, tk.END)
            self.result_entries["modules_x"].insert(0, f"Ошибка: {str(e)}")
            self.result_entries["modules_x"].configure(state="readonly")
            for key in self.result_entries:
                if key != "modules_x":
                    entry = self.result_entries[key]
                    entry.configure(state="normal")
                    entry.delete(0, tk.END)
                    entry.configure(state="readonly")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCalcApp(root)
    root.mainloop()