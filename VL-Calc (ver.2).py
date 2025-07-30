import os
import sys
import tkinter as tk
from tkinter import ttk
import math
from tkinter import messagebox

def resource_path(relative_path):
    """Get the absolute path to a resource in .exe or when running the script"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ScreenCalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор и визуализация параметров экрана")
        self.root.geometry("1200x800")
        self.root.minsize(800, 500)
        try:
            self.root.iconbitmap(resource_path("VL.ico"))
        except tk.TclError:
            print("Ошибка загрузки иконки. Продолжаем без иконки.")

        # Configure styles
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Error.TEntry", foreground="black", fieldbackground="#ffcccc")

        # Main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Input and result frames
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)

        # Input fields dictionary
        self.entries = {}
        self.result_entries = {}
        self.viz_enabled = False  # Flag for enabling the "Show scheme" button

        # Screen type selector
        self.screen_type_var = tk.StringVar(value="folding")
        frame_type = ttk.LabelFrame(input_frame, text="Тип экрана")
        frame_type.pack(fill="x", pady=(0, 8))
        rb_folding = ttk.Radiobutton(frame_type, text="Распашной", variable=self.screen_type_var, value="folding")
        rb_cabinet = ttk.Radiobutton(frame_type, text="Кабинетный", variable=self.screen_type_var, value="cabinet")
        rb_folding.grid(row=0, column=0, padx=10, pady=4, sticky="w")
        rb_cabinet.grid(row=0, column=1, padx=10, pady=4, sticky="w")

        # Input frames
        self.frame_screen = ttk.LabelFrame(input_frame, text="Экран")
        self.frame_module = ttk.LabelFrame(input_frame, text="Модуль")
        self.frame_receiver = ttk.LabelFrame(input_frame, text="Приёмная карта")
        self.frame_psu = ttk.LabelFrame(input_frame, text="Блоки питания")

        self.frame_screen.pack(fill="x", pady=(0, 8))
        self.frame_module.pack(fill="x", pady=(0, 8))
        self.frame_receiver.pack(fill="x", pady=(0, 8))
        self.frame_psu.pack(fill="x", pady=(0, 8))

        # Dynamic field creation based on screen type
        def create_receiver_fields(screen_type):
            for widget in self.frame_receiver.winfo_children():
                widget.destroy()
            self.entries.pop("max_cab_w", None)
            self.entries.pop("max_cab_h", None)
            self.entries.pop("cabinet_width_px", None)
            self.entries.pop("cabinet_height_px", None)
            # Common fields
            lbl_ports = ttk.Label(self.frame_receiver, text="Портов на приёмной карте:")
            lbl_ports.grid(row=0, column=0, sticky="w", padx=(10, 5), pady=4)
            entry_ports = ttk.Entry(self.frame_receiver, font=("Segoe UI", 10))
            entry_ports.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=4)
            self.entries["receiver_ports"] = entry_ports

            lbl_chain = ttk.Label(self.frame_receiver, text="Модулей в одной цепочке (на порт):")
            lbl_chain.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=4)
            entry_chain = ttk.Entry(self.frame_receiver, font=("Segoe UI", 10))
            entry_chain.grid(row=1, column=1, sticky="ew", padx=(5, 10), pady=4)
            self.entries["modules_per_chain"] = entry_chain

            if screen_type == "folding":
                lbl_max_w = ttk.Label(self.frame_receiver, text="Макс. ширина кабинета (px):")
                lbl_max_w.grid(row=2, column=0, sticky="w", padx=(10, 5), pady=4)
                entry_max_w = ttk.Entry(self.frame_receiver, font=("Segoe UI", 10))
                entry_max_w.grid(row=2, column=1, sticky="ew", padx=(5, 10), pady=4)
                self.entries["max_cab_w"] = entry_max_w

                lbl_max_h = ttk.Label(self.frame_receiver, text="Макс. высота кабинета (px):")
                lbl_max_h.grid(row=3, column=0, sticky="w", padx=(10, 5), pady=4)
                entry_max_h = ttk.Entry(self.frame_receiver, font=("Segoe UI", 10))
                entry_max_h.grid(row=3, column=1, sticky="ew", padx=(5, 10), pady=4)
                self.entries["max_cab_h"] = entry_max_h
            else:
                lbl_cab_w = ttk.Label(self.frame_receiver, text="Ширина кабинета (px):")
                lbl_cab_w.grid(row=2, column=0, sticky="w", padx=(10, 5), pady=4)
                entry_cab_w = ttk.Entry(self.frame_receiver, font=("Segoe UI", 10))
                entry_cab_w.grid(row=2, column=1, sticky="ew", padx=(5, 10), pady=4)
                self.entries["cabinet_width_px"] = entry_cab_w

                lbl_cab_h = ttk.Label(self.frame_receiver, text="Высота кабинета (px):")
                lbl_cab_h.grid(row=3, column=0, sticky="w", padx=(10, 5), pady=4)
                entry_cab_h = ttk.Entry(self.frame_receiver, font=("Segoe UI", 10))
                entry_cab_h.grid(row=3, column=1, sticky="ew", padx=(5, 10), pady=4)
                self.entries["cabinet_height_px"] = entry_cab_h

        def create_psu_fields(screen_type):
            for widget in self.frame_psu.winfo_children():
                widget.destroy()
            self.entries.pop("psu_voltage", None)
            self.entries.pop("psu_power", None)
            self.entries.pop("modules_per_psu", None)
            self.entries.pop("psu_per_cabinet", None)
            lbl_voltage = ttk.Label(self.frame_psu, text="Напряжение блока питания (В):")
            lbl_voltage.grid(row=0, column=0, sticky="w", padx=(10, 5), pady=4)
            entry_voltage = ttk.Entry(self.frame_psu, font=("Segoe UI", 10))
            entry_voltage.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=4)
            self.entries["psu_voltage"] = entry_voltage

            lbl_power = ttk.Label(self.frame_psu, text="Мощность блока питания (Вт):")
            lbl_power.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=4)
            entry_power = ttk.Entry(self.frame_psu, font=("Segoe UI", 10))
            entry_power.grid(row=1, column=1, sticky="ew", padx=(5, 10), pady=4)
            self.entries["psu_power"] = entry_power

            if screen_type == "folding":
                lbl_modules = ttk.Label(self.frame_psu, text="Модулей на один блок питания:")
                lbl_modules.grid(row=2, column=0, sticky="w", padx=(10, 5), pady=4)
                entry_modules = ttk.Entry(self.frame_psu, font=("Segoe UI", 10))
                entry_modules.grid(row=2, column=1, sticky="ew", padx=(5, 10), pady=4)
                self.entries["modules_per_psu"] = entry_modules
            else:
                lbl_psu_per_cabinet = ttk.Label(self.frame_psu, text="Блоков питания на один кабинет:")
                lbl_psu_per_cabinet.grid(row=2, column=0, sticky="w", padx=(10, 5), pady=4)
                entry_psu_per_cabinet = ttk.Entry(self.frame_psu, font=("Segoe UI", 10))
                entry_psu_per_cabinet.grid(row=2, column=1, sticky="ew", padx=(5, 10), pady=4)
                self.entries["psu_per_cabinet"] = entry_psu_per_cabinet

        def update_fields():
            screen_type = self.screen_type_var.get()
            create_receiver_fields(screen_type)
            create_psu_fields(screen_type)

        self.screen_type_var.trace_add('write', lambda *args: update_fields())
        update_fields()

        # Screen input fields
        screen_fields = [
            ("Ширина экрана (м):", "screen_width"),
            ("Высота экрана (м):", "screen_height"),
        ]
        self._create_fields(self.frame_screen, screen_fields)

        # Module input fields
        module_fields = [
            ("Ширина модуля (мм):", "module_width"),
            ("Высота модуля (мм):", "module_height"),
            ("Шаг пикселя (мм):", "pixel_pitch"),
            ("Разрешение модуля по ширине (px):", "module_res_x"),
            ("Разрешение модуля по высоте (px):", "module_res_y"),
            ("Потребление модуля (А):", "module_current"),
        ]
        self._create_fields(self.frame_module, module_fields)

        # Calculate button
        btn_calc = ttk.Button(input_frame, text="Рассчитать", command=self.calculate)
        btn_calc.pack(fill="x", pady=10)
        # Show scheme button
        self.btn_viz = ttk.Button(input_frame, text="Показать схему", command=self.show_viz, state="disabled")
        self.btn_viz.pack(fill="x", pady=5)
        # Error label
        self.error_label = ttk.Label(input_frame, text="", foreground="red", font=("Segoe UI", 10))
        self.error_label.pack(fill="x", pady=(0, 8))

        # Result area with scrollbar
        self.canvas_result = tk.Canvas(result_frame, highlightthickness=0, bd=0)
        self.scrollbar_result = ttk.Scrollbar(result_frame, orient="vertical", command=self.canvas_result.yview)
        self.scrollable_frame_result = ttk.Frame(self.canvas_result)

        self.scrollable_frame_result.bind(
            "<Configure>",
            lambda e: self.canvas_result.configure(scrollregion=self.canvas_result.bbox("all"))
        )
        self.canvas_window_result = self.canvas_result.create_window((0, 0), window=self.scrollable_frame_result, anchor="nw")
        self.canvas_result.configure(yscrollcommand=self.scrollbar_result.set)
        self.canvas_result.pack(side="left", fill="both", expand=True)
        self.scrollbar_result.pack(side="right", fill="y")

        self.result_frame_inner = ttk.Frame(self.scrollable_frame_result)
        self.result_frame_inner.pack(fill="both", expand=True)
        self.result_frame_inner.bind(
            "<Configure>",
            lambda e: self.canvas_result.itemconfig(self.canvas_window_result, width=self.canvas_result.winfo_width())
        )
        self.canvas_result.bind_all("<MouseWheel>", self._on_mousewheel)

        # Initialize result fields
        row = 0
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
            ("Модулей в кабинете:", "modules_in_cabinet"),
        ]
        for label_text, key in result_fields_screen:
            self._create_result_field(self.result_frame_inner, row, label_text, key)
            row += 1

        row += 1
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

        row += 1
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

        row += 1
        lbl = ttk.Label(self.result_frame_inner, text="Блоки питания", style="Header.TLabel")
        lbl.grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=(8, 4))
        row += 1
        results_psu = [
            ("Мощность блока питания:", "psu_power"),
            ("Запас блока питания:", "psu_reserve"),
            ("Доступная мощность:", "available_power"),
            ("Максимальное количество модулей на блок:", "max_modules_per_psu"),
            ("Остаточная мощность на блок:", "reserve_power"),
            ("Всего блоков питания:", "total_psus"),
            ("Остаток модулей:", "modules_remainder"),
            ("Блоков на один кабинет:", "blocks_per_cabinet"),
            ("Кол-во кабинетов:", "total_cabinets"),
            ("Приёмных карт в одном кабинете:", "receiver_cards_per_cabinet"),
        ]
        for label_text, key in results_psu:
            self._create_result_field(self.result_frame_inner, row, label_text, key)
            row += 1

        row += 1
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
            entry.bind('<Control-v>', lambda event, e=entry: self.paste_entry_value(event, e))
            entry.bind('<Control-c>', lambda event, e=entry: self.copy_entry_value(event, e))

    def _create_result_field(self, parent, row, label_text, key):
        lbl = ttk.Label(parent, text=label_text)
        lbl.grid(row=row, column=0, sticky="w", padx=(5, 5), pady=4)
        entry = ttk.Entry(parent, font=("Segoe UI", 10), state="readonly")
        entry.grid(row=row, column=1, sticky="ew", padx=(5, 5), pady=4)
        parent.columnconfigure(1, weight=1)
        self.result_entries[key] = entry
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
        self.canvas_result.yview_scroll(int(-1 * (event.delta / 120)), "units")

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
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return f"{value:.3f}"

    def calculate(self):
        for entry in self.result_entries.values():
            entry.configure(state="normal")
            entry.delete(0, tk.END)
            entry.configure(state="readonly")

        self.error_label.config(text="")
        self.viz_enabled = False
        self.btn_viz.config(state="disabled")

        self.entries["screen_width"].config(style="TEntry")
        self.entries["screen_height"].config(style="TEntry")

        try:
            def safe_int_entry(entry, name):
                if entry is None:
                    raise ValueError(f"Поле '{name}' не найдено.")
                val = entry.get().strip()
                if not val.isdigit():
                    raise ValueError(f"Введите целое число в поле '{name}'")
                return int(val)

            def safe_float_entry(entry, name):
                if entry is None:
                    raise ValueError(f"Поле '{name}' не найдено.")
                val = entry.get().strip()
                try:
                    return float(val.replace(",", "."))
                except Exception:
                    raise ValueError(f"Введите число в поле '{name}'")

            # Required fields
            required_fields = [
                "module_width", "module_height", "pixel_pitch", "screen_width", "screen_height",
                "module_res_x", "module_res_y", "receiver_ports", "modules_per_chain",
                "module_current", "psu_voltage", "psu_power"
            ]
            if self.screen_type_var.get() == "folding":
                required_fields += ["max_cab_w", "max_cab_h", "modules_per_psu"]
            else:
                required_fields += ["cabinet_width_px", "cabinet_height_px", "psu_per_cabinet"]
            for field in required_fields:
                if field not in self.entries or self.entries[field] is None:
                    raise ValueError(f"Поле '{field}' не найдено.")

            module_w = safe_float_entry(self.entries["module_width"], "Ширина модуля (мм)")
            module_h = safe_float_entry(self.entries["module_height"], "Высота модуля (мм)")
            pixel_pitch = safe_float_entry(self.entries["pixel_pitch"], "Шаг пикселя (мм)")
            screen_w_m = safe_float_entry(self.entries["screen_width"], "Ширина экрана (м)")
            screen_h_m = safe_float_entry(self.entries["screen_height"], "Высота экрана (м)")
            module_res_x = safe_int_entry(self.entries["module_res_x"], "Разрешение модуля по ширине (px)")
            module_res_y = safe_int_entry(self.entries["module_res_y"], "Разрешение модуля по высоте (px)")
            receiver_ports = safe_int_entry(self.entries["receiver_ports"], "Портов на приёмной карте")
            modules_per_chain = safe_int_entry(self.entries["modules_per_chain"], "Модулей в одной цепочке (на порт)")
            module_current = safe_float_entry(self.entries["module_current"], "Потребление модуля (А)")
            psu_voltage = safe_float_entry(self.entries["psu_voltage"], "Напряжение блока питания (В)")
            psu_power = safe_float_entry(self.entries["psu_power"], "Мощность блока питания (Вт)")

            if self.screen_type_var.get() == "folding":
                max_cab_w = safe_float_entry(self.entries["max_cab_w"], "Макс. ширина кабинета (px)")
                max_cab_h = safe_float_entry(self.entries["max_cab_h"], "Макс. высота кабинета (px)")
                modules_per_psu = safe_int_entry(self.entries["modules_per_psu"], "Модулей на один блок питания")
                modules_in_cabinet = None
                psu_per_cabinet = None
                total_cabinets = None
                receiver_cards_per_cabinet = None
            else:
                cabinet_width_px = safe_int_entry(self.entries["cabinet_width_px"], "Ширина кабинета (px)")
                cabinet_height_px = safe_int_entry(self.entries["cabinet_height_px"], "Высота кабинета (px)")
                psu_per_cabinet = safe_int_entry(self.entries["psu_per_cabinet"], "Блоков питания на один кабинет")
                max_cab_w = cabinet_width_px
                max_cab_h = cabinet_height_px
                if cabinet_width_px % module_res_x != 0:
                    raise ValueError("Ширина кабинета должна быть кратна разрешению модуля по ширине (px)!")
                if cabinet_height_px % module_res_y != 0:
                    raise ValueError("Высота кабинета должна быть кратна разрешению модуля по высоте (px)!")
                modules_in_cabinet = (cabinet_width_px // module_res_x) * (cabinet_height_px // module_res_y)
                modules_per_psu = math.ceil(modules_in_cabinet / psu_per_cabinet) if psu_per_cabinet > 0 else 0

            if module_current == 0:
                raise ValueError("Потребление модуля не может быть 0 А.")
            if max_cab_w <= 0 or max_cab_h <= 0:
                raise ValueError("Максимальные размеры кабинета должны быть положительными.")
            if module_res_x <= 0 or module_res_y <= 0:
                raise ValueError("Разрешение модуля должно быть положительным.")

            screen_w_mm = screen_w_m * 1000
            screen_h_mm = screen_h_m * 1000

            if (screen_w_mm % module_w) != 0:
                self.entries["screen_width"].config(style="Error.TEntry")
                self.entries["screen_width"].focus_set()
                raise ValueError("Ширина экрана должна быть кратна ширине модуля!")
            if (screen_h_mm % module_h) != 0:
                self.entries["screen_height"].config(style="Error.TEntry")
                self.entries["screen_height"].focus_set()
                raise ValueError("Высота экрана должна быть кратна высоте модуля!")

            modules_x = int(math.ceil(screen_w_mm / module_w))
            modules_y = int(math.ceil(screen_h_mm / module_h))
            total_modules = modules_x * modules_y

            area_m2 = (modules_x * module_w / 1000) * (modules_y * module_h / 1000)
            total_px_x = modules_x * module_res_x
            total_px_y = modules_y * module_res_y
            total_pixels = total_px_x * total_px_y
            pixels_per_m2 = total_pixels / area_m2
            pixels_per_module = module_res_x * module_res_y

            # Receiver cards calculation
            receiver_pixel_limit = max_cab_w * max_cab_h
            max_modules_by_pixels = receiver_pixel_limit // pixels_per_module
            max_modules_by_ports = receiver_ports * modules_per_chain
            max_modules_per_card = min(max_modules_by_pixels, max_modules_by_ports)
            if max_modules_per_card < 1:
                max_modules_per_card = 1

            cabinets = []
            card_counter = [1]
            if (modules_x % modules_per_chain == 0 and modules_per_chain <= (max_cab_w // module_res_x)
                and modules_y % 2 == 0 and 2 <= (max_cab_h // module_res_y)
                and modules_per_chain * (modules_y // 2) <= max_modules_per_card):
                cab_mod_w = modules_per_chain
                cab_mod_h = modules_y // 2
                cab_cols = modules_x // cab_mod_w
                cab_rows = modules_y // cab_mod_h
                for cr in range(cab_rows):
                    for cc in range(cab_cols):
                        sx = cc * cab_mod_w
                        sy = cr * cab_mod_h
                        label = f"Card {card_counter[0]}"
                        cabinets.append((sx, sy, cab_mod_w, cab_mod_h, label))
                        card_counter[0] += 1
            elif modules_x % modules_per_chain == 0 and modules_per_chain <= (max_cab_w // module_res_x):
                cab_mod_w = modules_per_chain
                max_h = min(modules_y, max_cab_h // module_res_y, max_modules_per_card // cab_mod_w)
                cab_mod_h = int(max_h)
                cab_cols = modules_x // cab_mod_w
                cab_rows = (modules_y + cab_mod_h - 1) // cab_mod_h
                for cr in range(cab_rows):
                    for cc in range(cab_cols):
                        sx = cc * cab_mod_w
                        sy = cr * cab_mod_h
                        actual_mod_h = min(cab_mod_h, modules_y - sy)
                        label = f"Card {card_counter[0]}"
                        cabinets.append((sx, sy, cab_mod_w, actual_mod_h, label))
                        card_counter[0] += 1
            else:
                def split_area(start_x, start_y, size_x, size_y, card_counter):
                    max_w = int(min(size_x, max_cab_w // module_res_x))
                    max_h = int(min(size_y, max_cab_h // module_res_y))
                    best_w, best_h = 1, 1
                    max_area = 0
                    for test_w in range(max_w, 0, -1):
                        for test_h in range(max_h, 0, -1):
                            if test_w * test_h > max_modules_per_card:
                                continue
                            if test_w * test_h > max_area:
                                max_area = test_w * test_h
                                best_w, best_h = test_w, test_h
                    cab_mod_w = best_w
                    cab_mod_h = best_h
                    cab_cols = int(size_x // cab_mod_w)
                    cab_rows = int(size_y // cab_mod_h)
                    for cr in range(cab_rows):
                        for cc in range(cab_cols):
                            sx = start_x + cc * cab_mod_w
                            sy = start_y + cr * cab_mod_h
                            label = f"Card {card_counter[0]}"
                            cabinets.append((sx, sy, cab_mod_w, cab_mod_h, label))
                            card_counter[0] += 1
                    rest_x = size_x - cab_cols * cab_mod_w
                    if rest_x > 0:
                        for cr in range(cab_rows):
                            sx = start_x + cab_cols * cab_mod_w
                            sy = start_y + cr * cab_mod_h
                            split_area(sx, sy, rest_x, cab_mod_h, card_counter)
                    rest_y = size_y - cab_rows * cab_mod_h
                    if rest_y > 0:
                        for cc in range(cab_cols):
                            sx = start_x + cc * cab_mod_w
                            sy = start_y + cab_rows * cab_mod_h
                            split_area(sx, sy, cab_mod_w, rest_y, card_counter)
                    if rest_x > 0 and rest_y > 0:
                        sx = start_x + cab_cols * cab_mod_w
                        sy = start_y + cab_rows * cab_mod_h
                        split_area(sx, sy, rest_x, rest_y, card_counter)
                split_area(0, 0, modules_x, modules_y, card_counter)

            receiver_cards_needed = len(cabinets)

            # Power calculations
            power_per_module_dc = psu_voltage * module_current
            power_per_module_ac = power_per_module_dc / 0.7
            modules_per_m2 = (1000 * 1000) / (module_w * module_h)
            power_per_m2_dc = modules_per_m2 * power_per_module_dc
            power_per_m2_ac = power_per_m2_dc / 0.7

            if self.screen_type_var.get() == "folding":
                if modules_per_psu < 1:
                    raise ValueError("Модулей на один блок питания должно быть не меньше 1.")
                used_power = modules_per_psu * power_per_module_dc
                reserve_power = psu_power - used_power
                total_psus = math.ceil(total_modules / modules_per_psu)
                modules_remainder = total_modules % modules_per_psu
                if modules_remainder > 0 and modules_remainder <= (modules_per_psu // 2):
                    total_psus -= 1
            else:
                total_cabinets = math.ceil(total_modules / modules_in_cabinet)
                total_psus = total_cabinets * psu_per_cabinet
                modules_remainder = total_modules % modules_in_cabinet
                receiver_cards_per_cabinet = math.ceil(modules_in_cabinet / max_modules_per_card)
                used_power = modules_per_psu * power_per_module_dc
                reserve_power = psu_power - used_power

            total_power_dc = power_per_module_dc * total_modules
            total_power_ac = total_power_dc / 0.7
            average_power_ac = total_power_ac / 3
            minimal_average_power_ac = average_power_ac / 3

            results = {
                "modules_x": str(modules_x),
                "modules_y": str(modules_y),
                "total_modules": str(total_modules),
                "area_m2": f"{self.format_number(area_m2)} м²",
                "total_resolution": f"{total_px_x} × {total_px_y} пикселей",
                "total_pixels": str(total_pixels),
                "pixels_per_m2": f"{self.format_number(pixels_per_m2)} пикселей/м²",
                "pixels_per_module": str(pixels_per_module),
                "receiver_pixel_limit": str(int(receiver_pixel_limit)),
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
                "psu_reserve": f"{self.format_number(reserve_power)} Вт",
                "available_power": f"{self.format_number(psu_power)} Вт",
                "reserve_power": f"{self.format_number(reserve_power)} Вт",
                "total_psus": str(total_psus),
                "total_power_dc": f"{self.format_number(total_power_dc)} Вт",
                "total_power_ac": f"{self.format_number(total_power_ac)} Вт",
                "average_power_ac": f"{self.format_number(average_power_ac)} Вт",
                "minimal_average_power_ac": f"{self.format_number(minimal_average_power_ac)} Вт",
                "modules_remainder": str(modules_remainder),
                "max_modules_per_psu": str(modules_per_psu),
                "modules_in_cabinet": str(modules_in_cabinet) if modules_in_cabinet is not None else "",
                "blocks_per_cabinet": str(psu_per_cabinet) if psu_per_cabinet is not None else "",
                "total_cabinets": str(total_cabinets) if total_cabinets is not None else "",
                "receiver_cards_per_cabinet": str(receiver_cards_per_cabinet) if receiver_cards_per_cabinet is not None else "",
            }

            for key, value in results.items():
                if key in self.result_entries:
                    entry = self.result_entries[key]
                    entry.configure(state="normal")
                    entry.delete(0, tk.END)
                    entry.insert(0, value)
                    entry.configure(state="readonly")

            # Save data for visualization
            self.modules_x = modules_x
            self.modules_y = modules_y
            self.module_w_px = module_res_x
            self.module_h_px = module_res_y
            self.max_cab_w_px = int(max_cab_w)
            self.max_cab_h_px = int(max_cab_h)
            self.max_modules_per_card = max_modules_per_card
            self.viz_enabled = True
            self.btn_viz.config(state="normal")

            self.canvas_result.update_idletasks()
            self.canvas_result.configure(scrollregion=self.canvas_result.bbox("all"))

        except Exception as e:
            self.error_label.config(text=str(e))

    def show_viz(self):
        if not self.viz_enabled:
            messagebox.showwarning("Предупреждение", "Сначала выполните расчет!")
            return

        viz_window = tk.Toplevel(self.root)
        viz_window.title("Схема разбиения по приёмным картам")
        viz_window.geometry("800x600")
        viz_window.minsize(400, 300)
        try:
            viz_window.iconbitmap(resource_path("VL.ico"))
        except tk.TclError:
            print("Ошибка загрузки иконки для окна схемы. Продолжаем без иконки.")

        canvas_viz = tk.Canvas(viz_window, bg="white", highlightthickness=0, bd=0)
        h_scroll_viz = tk.Scrollbar(viz_window, orient=tk.HORIZONTAL, command=canvas_viz.xview)
        v_scroll_viz = tk.Scrollbar(viz_window, orient=tk.VERTICAL, command=canvas_viz.yview)
        canvas_viz.config(xscrollcommand=h_scroll_viz.set, yscrollcommand=v_scroll_viz.set)
        canvas_viz.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        h_scroll_viz.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll_viz.pack(side=tk.RIGHT, fill=tk.Y)

        try:
            modules_x = int(self.modules_x)
            modules_y = int(self.modules_y)
            module_w = int(self.module_w_px)
            module_h = int(self.module_h_px)
            max_modules_per_card = int(self.max_modules_per_card)
            max_cab_w_px = int(self.max_cab_w_px)
            max_cab_h_px = int(self.max_cab_h_px)
            modules_per_chain = int(self.entries["modules_per_chain"].get())

            cabinets = []
            card_counter = [1]
            if (modules_x % modules_per_chain == 0 and modules_per_chain <= (max_cab_w_px // module_w)
                and modules_y % 2 == 0 and 2 <= (max_cab_h_px // module_h)
                and modules_per_chain * (modules_y // 2) <= max_modules_per_card):
                cab_mod_w = modules_per_chain
                cab_mod_h = modules_y // 2
                cab_cols = modules_x // cab_mod_w
                cab_rows = modules_y // cab_mod_h
                for cr in range(cab_rows):
                    for cc in range(cab_cols):
                        sx = cc * cab_mod_w
                        sy = cr * cab_mod_h
                        label = f"Card {card_counter[0]}"
                        cabinets.append((sx, sy, cab_mod_w, cab_mod_h, label))
                        card_counter[0] += 1
            elif modules_x % modules_per_chain == 0 and modules_per_chain <= (max_cab_w_px // module_w):
                cab_mod_w = modules_per_chain
                max_h = min(modules_y, max_cab_h_px // module_h, max_modules_per_card // cab_mod_w)
                cab_mod_h = int(max_h)
                cab_cols = modules_x // cab_mod_w
                cab_rows = (modules_y + cab_mod_h - 1) // cab_mod_h
                for cr in range(cab_rows):
                    for cc in range(cab_cols):
                        sx = cc * cab_mod_w
                        sy = cr * cab_mod_h
                        actual_mod_h = min(cab_mod_h, modules_y - sy)
                        label = f"Card {card_counter[0]}"
                        cabinets.append((sx, sy, cab_mod_w, actual_mod_h, label))
                        card_counter[0] += 1
            else:
                def split_area(start_x, start_y, size_x, size_y, card_counter):
                    max_w = min(size_x, max_cab_w_px // module_w)
                    max_h = min(size_y, max_cab_h_px // module_h)
                    best_w, best_h = 1, 1
                    max_area = 0
                    for test_w in range(int(max_w), 0, -1):
                        for test_h in range(int(max_h), 0, -1):
                            if test_w * test_h > max_modules_per_card:
                                continue
                            if test_w * test_h > max_area:
                                max_area = test_w * test_h
                                best_w, best_h = test_w, test_h
                    cab_mod_w = best_w
                    cab_mod_h = best_h
                    cab_cols = int(size_x // cab_mod_w)
                    cab_rows = int(size_y // cab_mod_h)
                    for cr in range(cab_rows):
                        for cc in range(cab_cols):
                            sx = start_x + cc * cab_mod_w
                            sy = start_y + cr * cab_mod_h
                            label = f"Card {card_counter[0]}"
                            cabinets.append((sx, sy, cab_mod_w, cab_mod_h, label))
                            card_counter[0] += 1
                    rest_x = size_x - cab_cols * cab_mod_w
                    if rest_x > 0:
                        for cr in range(cab_rows):
                            sx = start_x + cab_cols * cab_mod_w
                            sy = start_y + cr * cab_mod_h
                            split_area(sx, sy, rest_x, cab_mod_h, card_counter)
                    rest_y = size_y - cab_rows * cab_mod_h
                    if rest_y > 0:
                        for cc in range(cab_cols):
                            sx = start_x + cc * cab_mod_w
                            sy = start_y + cab_rows * cab_mod_h
                            split_area(sx, sy, cab_mod_w, rest_y, card_counter)
                    if rest_x > 0 and rest_y > 0:
                        sx = start_x + cab_cols * cab_mod_w
                        sy = start_y + cab_rows * cab_mod_h
                        split_area(sx, sy, rest_x, rest_y, card_counter)
                split_area(0, 0, modules_x, modules_y, card_counter)

            scale = min(700 / (modules_x * module_w), 700 / (modules_y * module_h)) if (modules_x * module_w) > 700 or (modules_y * module_h) > 700 else 1
            offset_x = 50
            offset_y = 50
            canvas_width = offset_x + (modules_x * module_w) * scale + 50
            canvas_height = offset_y + (modules_y * module_h) * scale + 50
            canvas_viz.config(scrollregion=(0, 0, canvas_width, canvas_height))

            # Draw modules
            for row in range(modules_y):
                for col in range(modules_x):
                    x0 = offset_x + col * module_w * scale
                    y0 = offset_y + row * module_h * scale
                    x1 = x0 + module_w * scale
                    y1 = y0 + module_h * scale
                    canvas_viz.create_rectangle(x0, y0, x1, y1, outline="gray", width=1)

            # Draw cabinets
            for sx, sy, size_x, size_y, label in cabinets:
                x0 = offset_x + sx * module_w * scale
                y0 = offset_y + sy * module_h * scale
                x1 = x0 + size_x * module_w * scale
                y1 = y0 + size_y * module_h * scale
                canvas_viz.create_rectangle(x0, y0, x1, y1, outline="purple", width=2)
                canvas_viz.create_text((x0 + x1) / 2, (y0 + y1) / 2,
                                      text=label,
                                      font=("Arial", 10, "bold"))
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCalcApp(root)
    root.mainloop()