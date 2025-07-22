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
        self.root.iconbitmap(resource_path("VL.ico"))  # Используем resource_path для иконки

        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
        style.configure("TLabelframe.Label", font=("Segoe UI", 12, "bold"))

        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))

        result_frame = ttk.Frame(main_frame, relief="sunken", borderwidth=2)
        result_frame.grid(row=0, column=1, sticky="nsew")

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.entries = {}

        self.frame_screen = ttk.LabelFrame(input_frame, text="Экран")
        self.frame_module = ttk.LabelFrame(input_frame, text="Модуль")
        self.frame_receiver = ttk.LabelFrame(input_frame, text="Приёмная карта")
        self.frame_psu = ttk.LabelFrame(input_frame, text="Блоки питания")

        self.frame_screen.pack(fill="x", pady=(0,8))
        self.frame_module.pack(fill="x", pady=(0,8))
        self.frame_receiver.pack(fill="x", pady=(0,8))
        self.frame_psu.pack(fill="x", pady=(0,8))

        screen_fields = [
            ("Ширина экрана (м):", "screen_width"),
            ("Высота экрана (м):", "screen_height"),
        ]
        self._create_fields(self.frame_screen, screen_fields)

        module_fields = [
            ("Ширина модуля (мм):", "module_width"),
            ("Высота модуля (мм):", "module_height"),
            ("Шаг пикселя (мм):", "pixel_pitch"),
            ("Разрешение модуля по ширине (px):", "module_res_x"),
            ("Разрешение модуля по высоте (px):", "module_res_y"),
            ("Потребление модуля (А):", "module_current"),
        ]
        self._create_fields(self.frame_module, module_fields)

        receiver_fields = [
            ("Ширина кабинета (px):", "receiver_width_px"),
            ("Высота кабинета (px):", "receiver_height_px"),
            ("Портов на приёмной карте:", "receiver_ports"),
            ("Модулей в одной цепочке (на порт):", "modules_per_chain"),
        ]
        self._create_fields(self.frame_receiver, receiver_fields)

        psu_fields = [
            ("Напряжение блока питания (В):", "psu_voltage"),
            ("Мощность блока питания (Вт):", "psu_power"),
            ("Запас блока питания (Вт):", "psu_reserve_watts"),
        ]
        self._create_fields(self.frame_psu, psu_fields)

        btn = ttk.Button(input_frame, text="Рассчитать", command=self.calculate)
        btn.pack(fill="x", pady=10)

        self.result_box = tk.Text(result_frame, wrap="word", font=("Consolas", 11))
        self.result_box.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_box.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll = ttk.Scrollbar(result_frame, orient="horizontal", command=self.result_box.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")

        self.result_box.config(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)

    def _create_fields(self, parent, fields):
        for i, (label_text, key) in enumerate(fields):
            lbl = ttk.Label(parent, text=label_text)
            lbl.grid(row=i, column=0, sticky="w", padx=(10, 5), pady=4)
            entry = ttk.Entry(parent, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, sticky="ew", padx=(5, 10), pady=4)
            parent.columnconfigure(1, weight=1)
            self.entries[key] = entry

    def safe_float(self, value):
        return float(value.replace(",", "."))

    def calculate(self):
        try:
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
                raise ValueError("Невозможно подключить ни одного модуля к приёмной карте с заданными параметрами.")

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

            # Расчёты для общего и среднего потребления
            total_power_dc = available_power * total_psus  # Общее потребление DC
            total_power_ac = total_power_dc / 0.7  # Общее потребление AC
            average_power_ac = total_power_ac / 3  # Среднее потребление AC
            minimal_average_power_ac = average_power_ac / 3  # Среднее минимальное потребление AC

            result = (
                f"--- Расчёт модулей и экрана ---\n"
                f"Модули по ширине: {modules_x}\n"
                f"Модули по высоте: {modules_y}\n"
                f"Общее количество модулей: {total_modules}\n\n"
                f"Площадь экрана: {area_m2:.3f} м²\n"
                f"Общее разрешение: {total_px_x} × {total_px_y} пикселей\n"
                f"Плотность пикселей: {pixels_per_m2:,.3f} пикселей/м²\n\n"
                f"--- Приёмные карты ---\n"
                f"Пикселей в одном модуле: {pixels_per_module}\n"
                f"Макс. пикселей на карту (ширина x высота кабинета): {receiver_pixel_limit}\n"
                f"Макс. модулей по пикселям: {max_modules_by_pixels}\n"
                f"Макс. модулей по портам: {max_modules_by_ports} (по {modules_per_chain} мод/порт)\n"
                f"Макс. модулей на карту: {max_modules_per_card}\n"
                f"Требуется приёмных карт: {receiver_cards_needed}\n\n"
                f"--- Питание ---\n"
                f"Потребление одного модуля DC ({psu_voltage:.3f} В): {power_per_module_dc:.3f} Вт\n"
                f"Потребление одного модуля AC ({psu_voltage:.3f} В): {power_per_module_ac:.3f} Вт\n"
                f"Модулей в 1 м²: {modules_per_m2:.3f}\n"
                f"Потребление 1 м² DC: {power_per_m2_dc:.3f} Вт\n"
                f"Потребление 1 м² AC: {power_per_m2_ac:.3f} Вт\n\n"
                f"--- Блоки питания ---\n"
                f"Мощность блока питания: {psu_power:.3f} Вт\n"
                f"Запас блока питания: {psu_reserve:.3f} Вт\n"
                f"Доступная мощность: {available_power:.3f} Вт\n"
                f"Модулей на один блок питания: {modules_per_psu}\n"
                f"Остаточная мощность на блок: {reserve_power:.3f} Вт\n"
                f"Всего блоков питания: {total_psus}\n\n"
                f"--- Общее потребление ---\n"
                f"Общее потребление DC: {total_power_dc:.3f} Вт\n"
                f"Общее потребление AC: {total_power_ac:.3f} Вт\n"
                f"Среднее потребление AC: {average_power_ac:.3f} Вт\n"
                f"Среднее минимальное потребление AC: {minimal_average_power_ac:.3f} Вт\n"
            )

        except Exception as e:
            result = f"Ошибка: {e}"

        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, result)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCalcApp(root)
    root.mainloop()