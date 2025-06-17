#!/usr/bin/env python3
"""
OrtoIoT Preset Creator - Simplified Version
A standalone application for creating cultivation presets.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
import uuid

# Try to import customtkinter for modern UI
try:
    import customtkinter as ctk
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    MODERN_UI = True
    print("✅ Using CustomTkinter for modern UI")
except ImportError:
    MODERN_UI = False
    print("ℹ️ Using standard Tkinter")


class PresetCreatorApp:
    def __init__(self):
        # Initialize main window
        if MODERN_UI:
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()

        self.root.title("OrtoIoT Preset Creator v1.0")
        self.root.geometry("1800x1200")  # Finestra più grande per font enormi
        self.root.minsize(1600, 1000)    # Minimo più grande
        
        # Configure DPI awareness and force large fonts
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
            
        # Force large fonts for all ttk widgets
        style = ttk.Style()
        
        # Force large fonts for all ttk widgets - MASSIVE FONTS
        style = ttk.Style()
        
        # Configure all ttk widget fonts to be HUGE
        style.configure('TLabel', font=('Arial', 24, 'bold'))
        style.configure('TButton', font=('Arial', 20, 'bold'))
        style.configure('TEntry', font=('Arial', 20))
        style.configure('TCombobox', font=('Arial', 20))
        style.configure('TCheckbutton', font=('Arial', 20))
        style.configure('TRadiobutton', font=('Arial', 20))
        style.configure('TLabelFrame.Label', font=('Arial', 20, 'bold'))
        style.configure('TNotebook.Tab', font=('Arial', 18, 'bold'))
        style.configure('TSpinbox', font=('Arial', 20))
        
        # Configure root font as fallback - GIGANTIC fonts
        self.root.option_add('*Font', 'Arial 24 bold')
        self.root.option_add('*Label*Font', 'Arial 24 bold')
        self.root.option_add('*Button*Font', 'Arial 20 bold')
        self.root.option_add('*Entry*Font', 'Arial 20')
        self.root.option_add('*Text*Font', 'Arial 20')
        self.root.option_add('*Listbox*Font', 'Arial 24 bold')

        # Data storage
        self.presets = {}
        self.current_preset = None
        self.preset_file = "presets_library.json"
        self.categories_file = "custom_categories.json"

        # Categories (can be customized)
        self.default_categories = {
            "cannabis": {
                "name": "Cannabis",
                "subcategories": ["indica", "sativa", "hybrid", "ruderalis"]
            },
            "vegetables": {
                "name": "Vegetables",
                "subcategories": ["leafy_greens", "fruiting_plants", "herbs"]
            },
            "flowers": {
                "name": "Flowers",
                "subcategories": ["annuals", "perennials"]
            },
            "specialty": {
                "name": "Specialty",
                "subcategories": ["mushrooms", "microgreens"]
            }
        }
        
        # Load custom categories or use defaults
        self.categories = self.load_categories()

        # Automation settings structure
        self.automation_defaults = {
            "temperature": {"enabled": False, "value": 22.0},
            "humidity": {"enabled": False, "value": 60.0},
            "co2": {"enabled": False, "value": 800},
            "ec": {"enabled": False, "value": 1.2},
            "irrigation": {"enabled": False, "duration": 5, "interval": 12},
            "light": {"enabled": False, "duration": 18, "startTime": "06:00"},
            "lamp": {"enabled": False, "distance": 30},
            "ventilation": {"enabled": False, "duration": 15, "interval": 3},
            "foliar_feeding": {"enabled": False, "frequency": 3, "duration": 2}
        }

        # Initialize phases data
        self.phases = []
        self.current_phase_index = -1

        self.setup_ui()
        self.load_presets()

    def setup_ui(self):
        """Setup the user interface"""
        # Create menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Preset", command=self.new_preset)
        file_menu.add_command(label="Save Library", command=self.save_library)
        file_menu.add_command(label="Load Library", command=self.load_library)
        file_menu.add_separator()
        file_menu.add_command(label="Import Preset", command=self.import_preset)
        file_menu.add_command(label="Export for OrtoIoT", command=self.export_for_ortoiot)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="🏷️ Category Editor", command=self.open_category_editor)
        tools_menu.add_command(label="📊 Preset Statistics", command=self.show_preset_stats)

        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create paned window
        self.paned = ttk.PanedWindow(main_frame, orient="horizontal")
        self.paned.pack(fill="both", expand=True)

        # Left panel - Preset list
        self.create_preset_list()

        # Right panel - Editor
        self.create_editor()

        # Status bar
        self.status_var = tk.StringVar(value="Ready - OrtoIoT Preset Creator v1.0")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief="sunken")
        status_bar.pack(fill="x", side="bottom", pady=(5, 0))

    def create_preset_list(self):
        """Create preset list panel"""
        list_frame = ttk.Frame(self.paned)
        self.paned.add(list_frame)

        # Title
        title_label = ttk.Label(list_frame, text="📚 Preset Library")
        title_label.pack(pady=10)

        # Buttons
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        btn_style = {"width": 8}  # Removed font from ttk.Button (not supported)
        ttk.Button(btn_frame, text="🆕 New", command=self.new_preset, **btn_style).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="💾 Save", command=self.save_current_preset, **btn_style).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_preset, **btn_style).pack(side="left")

        # Search
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="🔍 Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_changed)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Preset listbox (NOT ttk - needs explicit font)
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.preset_listbox = tk.Listbox(listbox_frame, font=("Arial", 18, "bold"), height=15)
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.preset_listbox.yview)
        self.preset_listbox.configure(yscrollcommand=scrollbar.set)

        self.preset_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.preset_listbox.bind("<<ListboxSelect>>", self.on_preset_selected)
        self.preset_listbox.bind("<Double-Button-1>", self.on_preset_double_click)

    def create_editor(self):
        """Create preset editor panel"""
        editor_frame = ttk.Frame(self.paned)
        self.paned.add(editor_frame)
        
        # Configure paned window proportions - MUCH WIDER left panel (preset list)
        self.root.after(1, lambda: self.paned.sashpos(0, 800))

        # Notebook for tabs
        self.notebook = ttk.Notebook(editor_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Basic Info tab
        self.create_basic_info_tab()

        # Automation Settings tab
        self.create_automation_tab()

        # Phases tab (for progressive presets)
        self.create_phases_tab()

        # Preview tab
        self.create_preview_tab()

    def create_basic_info_tab(self):
        """Create basic information tab"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="📝 Basic Info")

        # Main container with scrollbar
        canvas = tk.Canvas(basic_frame)
        scrollbar = ttk.Scrollbar(basic_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Form fields
        row = 0

        # Name
        ttk.Label(scrollable_frame, text="Name *:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=10, pady=8)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(scrollable_frame, textvariable=self.name_var, width=40, font=("Arial", 11))
        name_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
        row += 1

        # Description
        ttk.Label(scrollable_frame, text="Description *:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="nw", padx=10, pady=8)
        self.description_text = tk.Text(scrollable_frame, height=5, width=40, font=("Arial", 11))
        self.description_text.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
        row += 1

        # Icon
        ttk.Label(scrollable_frame, text="Icon:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=10, pady=8)
        icon_frame = ttk.Frame(scrollable_frame)
        icon_frame.grid(row=row, column=1, sticky="ew", padx=10, pady=8)

        self.icon_var = tk.StringVar(value="🌱")
        icon_entry = ttk.Entry(icon_frame, textvariable=self.icon_var, width=8, font=("Arial", 14))
        icon_entry.pack(side="left", padx=(0, 10))

        # Common icons
        common_icons = ["🌱", "🌿", "🌾", "🌸", "🥬", "🍃", "🌳", "🌺"]
        for icon in common_icons:
            icon_btn = ttk.Button(icon_frame, text=icon, width=4,
                                  command=lambda i=icon: self.icon_var.set(i))
            icon_btn.pack(side="left", padx=2)
        row += 1

        # Category
        ttk.Label(scrollable_frame, text="Category *:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=10, pady=8)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(scrollable_frame, textvariable=self.category_var,
                                      values=list(self.categories.keys()), width=37, font=("Arial", 11))
        category_combo.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
        category_combo.bind("<<ComboboxSelected>>", self.on_category_changed)
        row += 1

        # Subcategory
        ttk.Label(scrollable_frame, text="Subcategory:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=10, pady=8)
        self.subcategory_var = tk.StringVar()
        self.subcategory_combo = ttk.Combobox(scrollable_frame, textvariable=self.subcategory_var, width=37, font=("Arial", 11))
        self.subcategory_combo.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
        row += 1

        # Tags
        ttk.Label(scrollable_frame, text="Tags:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=10, pady=8)
        self.tags_var = tk.StringVar()
        tags_entry = ttk.Entry(scrollable_frame, textvariable=self.tags_var, width=40, font=("Arial", 11))
        tags_entry.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
        ttk.Label(scrollable_frame, text="(comma separated)", font=("Arial", 10)).grid(row=row, column=2, sticky="w", padx=5)
        row += 1

        # Preset Type
        ttk.Label(scrollable_frame, text="Preset Type *:", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=10, pady=8)
        type_frame = ttk.Frame(scrollable_frame)
        type_frame.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
        
        self.preset_type_var = tk.StringVar(value="static")
        
        # Create style for larger radio buttons (ttk doesn't support font directly)
        style = ttk.Style()
        style.configure("Large.TRadiobutton", font=("Arial", 14))
        
        static_radio = ttk.Radiobutton(type_frame, text="🔒 Static (Fixed settings)", 
                                       variable=self.preset_type_var, value="static",
                                       command=self.on_preset_type_changed, style="Large.TRadiobutton")
        static_radio.pack(anchor="w", pady=2)
        
        progressive_radio = ttk.Radiobutton(type_frame, text="🔄 Progressive (Multi-phase)", 
                                           variable=self.preset_type_var, value="progressive",
                                           command=self.on_preset_type_changed, style="Large.TRadiobutton")
        progressive_radio.pack(anchor="w", pady=2)
        
        # Type description
        self.type_desc_label = ttk.Label(type_frame, 
                                        text="Static presets use the same settings throughout the entire growth cycle.",
                                        font=("Arial", 10), foreground="gray")
        self.type_desc_label.pack(anchor="w", pady=(5, 0))

        # Configure grid weights
        scrollable_frame.columnconfigure(1, weight=1)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_phases_tab(self):
        """Create phases tab for progressive presets"""
        phases_frame = ttk.Frame(self.notebook)
        self.notebook.add(phases_frame, text="🔄 Phases")

        # Header
        header_frame = ttk.Frame(phases_frame)
        header_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(header_frame, text="🔄 Progressive Preset Phases").pack(side="left")

        # Phase management buttons
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side="right")

        btn_style = {}  # Removed font from ttk.Button (not supported)
        ttk.Button(btn_frame, text="➕ Add Phase", command=self.add_phase, **btn_style).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="🗑️ Delete Phase", command=self.delete_phase, **btn_style).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="⬆️ Move Up", command=self.move_phase_up, **btn_style).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="⬇️ Move Down", command=self.move_phase_down, **btn_style).pack(side="left", padx=2)

        # Main phases area
        main_frame = ttk.Frame(phases_frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left: Phase list
        list_frame = ttk.LabelFrame(main_frame, text="📋 Phases List")
        list_frame.pack(side="left", fill="y", padx=(0, 10))

        # Phases listbox (NOT ttk - needs explicit font) - HUGE FONT
        self.phases_listbox = tk.Listbox(list_frame, width=15, font=("Arial", 24, "bold"))
        self.phases_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.phases_listbox.bind("<<ListboxSelect>>", self.on_phase_selected)

        # Right: Phase editor
        self.phase_editor_frame = ttk.LabelFrame(main_frame, text="✏️ Phase Editor")
        self.phase_editor_frame.pack(side="right", fill="both", expand=True)

        # Phase editor content (initially empty)
        self.create_phase_editor()

    def create_automation_tab(self):
        """Create automation settings tab"""
        auto_frame = ttk.Frame(self.notebook)
        self.notebook.add(auto_frame, text="⚙️ Automations")

        # Canvas for scrolling
        canvas = tk.Canvas(auto_frame)
        scrollbar = ttk.Scrollbar(auto_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Automation widgets
        self.automation_widgets = {}

        # Temperature
        temp_frame = ttk.LabelFrame(scrollable_frame, text="🌡️ Temperature Control")
        temp_frame.pack(fill="x", padx=10, pady=5)

        temp_enabled = tk.BooleanVar()
        ttk.Checkbutton(temp_frame, text="Enable Temperature Control",
                        variable=temp_enabled).pack(anchor="w", padx=5, pady=2)

        temp_value_frame = ttk.Frame(temp_frame)
        temp_value_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(temp_value_frame, text="Target Temperature (°C):").pack(side="left")
        temp_value = tk.DoubleVar(value=22.0)
        temp_scale = ttk.Scale(temp_value_frame, from_=15, to=35, variable=temp_value, orient="horizontal")
        temp_scale.pack(side="left", fill="x", expand=True, padx=5)
        temp_label = ttk.Label(temp_value_frame, text="22.0°C")
        temp_label.pack(side="right")

        def update_temp_label(*args):
            temp_label.config(text=f"{temp_value.get():.1f}°C")
        temp_value.trace("w", update_temp_label)

        self.automation_widgets["temperature"] = {"enabled": temp_enabled, "value": temp_value}

        # Humidity
        hum_frame = ttk.LabelFrame(scrollable_frame, text="💧 Humidity Control")
        hum_frame.pack(fill="x", padx=10, pady=5)

        hum_enabled = tk.BooleanVar()
        ttk.Checkbutton(hum_frame, text="Enable Humidity Control",
                        variable=hum_enabled).pack(anchor="w", padx=5, pady=2)

        hum_value_frame = ttk.Frame(hum_frame)
        hum_value_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(hum_value_frame, text="Target Humidity (%):").pack(side="left")
        hum_value = tk.DoubleVar(value=60.0)
        hum_scale = ttk.Scale(hum_value_frame, from_=30, to=90, variable=hum_value, orient="horizontal")
        hum_scale.pack(side="left", fill="x", expand=True, padx=5)
        hum_label = ttk.Label(hum_value_frame, text="60.0%")
        hum_label.pack(side="right")

        def update_hum_label(*args):
            hum_label.config(text=f"{hum_value.get():.1f}%")
        hum_value.trace("w", update_hum_label)

        self.automation_widgets["humidity"] = {"enabled": hum_enabled, "value": hum_value}

        # CO2
        co2_frame = ttk.LabelFrame(scrollable_frame, text="💨 CO2 Control")
        co2_frame.pack(fill="x", padx=10, pady=5)

        co2_enabled = tk.BooleanVar()
        ttk.Checkbutton(co2_frame, text="Enable CO2 Control",
                        variable=co2_enabled).pack(anchor="w", padx=5, pady=2)

        co2_value_frame = ttk.Frame(co2_frame)
        co2_value_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(co2_value_frame, text="Target CO2 (ppm):").pack(side="left")
        co2_value = tk.IntVar(value=800)
        co2_scale = ttk.Scale(co2_value_frame, from_=400, to=1500, variable=co2_value, orient="horizontal")
        co2_scale.pack(side="left", fill="x", expand=True, padx=5)
        co2_label = ttk.Label(co2_value_frame, text="800 ppm")
        co2_label.pack(side="right")

        def update_co2_label(*args):
            co2_label.config(text=f"{co2_value.get()} ppm")
        co2_value.trace("w", update_co2_label)

        self.automation_widgets["co2"] = {"enabled": co2_enabled, "value": co2_value}

        # EC
        ec_frame = ttk.LabelFrame(scrollable_frame, text="⚡ EC/Fertilizer Control")
        ec_frame.pack(fill="x", padx=10, pady=5)

        ec_enabled = tk.BooleanVar()
        ttk.Checkbutton(ec_frame, text="Enable EC Control",
                        variable=ec_enabled).pack(anchor="w", padx=5, pady=2)

        ec_value_frame = ttk.Frame(ec_frame)
        ec_value_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(ec_value_frame, text="Target EC (mS/cm):").pack(side="left")
        ec_value = tk.DoubleVar(value=1.2)
        ec_scale = ttk.Scale(ec_value_frame, from_=0.5, to=3.0, variable=ec_value, orient="horizontal")
        ec_scale.pack(side="left", fill="x", expand=True, padx=5)
        ec_label = ttk.Label(ec_value_frame, text="1.2 mS/cm")
        ec_label.pack(side="right")

        def update_ec_label(*args):
            ec_label.config(text=f"{ec_value.get():.1f} mS/cm")
        ec_value.trace("w", update_ec_label)

        self.automation_widgets["ec"] = {"enabled": ec_enabled, "value": ec_value}

        # Irrigation
        irr_frame = ttk.LabelFrame(scrollable_frame, text="🚿 Irrigation")
        irr_frame.pack(fill="x", padx=10, pady=5)

        irr_enabled = tk.BooleanVar()
        ttk.Checkbutton(irr_frame, text="Enable Irrigation",
                        variable=irr_enabled).pack(anchor="w", padx=5, pady=2)

        irr_settings = ttk.Frame(irr_frame)
        irr_settings.pack(fill="x", padx=5, pady=2)

        ttk.Label(irr_settings, text="Duration (min):").grid(row=0, column=0, sticky="w", padx=5)
        irr_duration = tk.IntVar(value=5)
        ttk.Spinbox(irr_settings, from_=1, to=60, textvariable=irr_duration,
                    width=10).grid(row=0, column=1, padx=5)

        ttk.Label(irr_settings, text="Interval (hours):").grid(row=0, column=2, sticky="w", padx=5)
        irr_interval = tk.IntVar(value=12)
        ttk.Spinbox(irr_settings, from_=1, to=72, textvariable=irr_interval,
                    width=10).grid(row=0, column=3, padx=5)

        self.automation_widgets["irrigation"] = {
            "enabled": irr_enabled, "duration": irr_duration, "interval": irr_interval}

        # Light
        light_frame = ttk.LabelFrame(scrollable_frame, text="💡 Lighting")
        light_frame.pack(fill="x", padx=10, pady=5)

        light_enabled = tk.BooleanVar()
        ttk.Checkbutton(light_frame, text="Enable Lighting",
                        variable=light_enabled).pack(anchor="w", padx=5, pady=2)

        light_settings = ttk.Frame(light_frame)
        light_settings.pack(fill="x", padx=5, pady=2)

        ttk.Label(light_settings, text="Start Time:").grid(row=0, column=0, sticky="w", padx=5)
        light_start = tk.StringVar(value="06:00")
        ttk.Entry(light_settings, textvariable=light_start,
                  width=10).grid(row=0, column=1, padx=5)

        ttk.Label(light_settings, text="Duration (hours):").grid(row=0, column=2, sticky="w", padx=5)
        light_duration = tk.IntVar(value=18)
        ttk.Spinbox(light_settings, from_=6, to=24,
                    textvariable=light_duration, width=10).grid(row=0, column=3, padx=5)

        self.automation_widgets["light"] = {
            "enabled": light_enabled, "startTime": light_start, "duration": light_duration}

        # Lamp Height
        lamp_frame = ttk.LabelFrame(scrollable_frame, text="🔆 Lamp Height")
        lamp_frame.pack(fill="x", padx=10, pady=5)

        lamp_enabled = tk.BooleanVar()
        ttk.Checkbutton(lamp_frame, text="Enable Lamp Control",
                        variable=lamp_enabled).pack(anchor="w", padx=5, pady=2)

        lamp_value_frame = ttk.Frame(lamp_frame)
        lamp_value_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(lamp_value_frame, text="Distance (cm):").pack(side="left")
        lamp_distance = tk.IntVar(value=30)
        lamp_scale = ttk.Scale(lamp_value_frame, from_=10, to=100, variable=lamp_distance, orient="horizontal")
        lamp_scale.pack(side="left", fill="x", expand=True, padx=5)
        lamp_label = ttk.Label(lamp_value_frame, text="30 cm")
        lamp_label.pack(side="right")

        def update_lamp_label(*args):
            lamp_label.config(text=f"{lamp_distance.get()} cm")
        lamp_distance.trace("w", update_lamp_label)

        self.automation_widgets["lamp"] = {"enabled": lamp_enabled, "distance": lamp_distance}

        # Ventilation
        vent_frame = ttk.LabelFrame(scrollable_frame, text="🌪️ Ventilation")
        vent_frame.pack(fill="x", padx=10, pady=5)

        vent_enabled = tk.BooleanVar()
        ttk.Checkbutton(vent_frame, text="Enable Ventilation",
                        variable=vent_enabled).pack(anchor="w", padx=5, pady=2)

        vent_settings = ttk.Frame(vent_frame)
        vent_settings.pack(fill="x", padx=5, pady=2)

        ttk.Label(vent_settings, text="Duration (min):").grid(row=0, column=0, sticky="w", padx=5)
        vent_duration = tk.IntVar(value=15)
        ttk.Spinbox(vent_settings, from_=5, to=60, textvariable=vent_duration,
                    width=10).grid(row=0, column=1, padx=5)

        ttk.Label(vent_settings, text="Interval (hours):").grid(row=0, column=2, sticky="w", padx=5)
        vent_interval = tk.IntVar(value=3)
        ttk.Spinbox(vent_settings, from_=1, to=12, textvariable=vent_interval,
                    width=10).grid(row=0, column=3, padx=5)

        self.automation_widgets["ventilation"] = {
            "enabled": vent_enabled, "duration": vent_duration, "interval": vent_interval}

        # Foliar Feeding
        foliar_frame = ttk.LabelFrame(scrollable_frame, text="🌿 Foliar Feeding")
        foliar_frame.pack(fill="x", padx=10, pady=5)

        foliar_enabled = tk.BooleanVar()
        ttk.Checkbutton(foliar_frame, text="Enable Foliar Feeding",
                        variable=foliar_enabled).pack(anchor="w", padx=5, pady=2)

        foliar_settings = ttk.Frame(foliar_frame)
        foliar_settings.pack(fill="x", padx=5, pady=2)

        ttk.Label(foliar_settings, text="Frequency (days):").grid(row=0, column=0, sticky="w", padx=5)
        foliar_freq = tk.IntVar(value=3)
        ttk.Spinbox(foliar_settings, from_=1, to=14,
                    textvariable=foliar_freq, width=10).grid(row=0, column=1, padx=5)

        ttk.Label(foliar_settings, text="Duration (min):").grid(row=0, column=2, sticky="w", padx=5)
        foliar_duration = tk.IntVar(value=2)
        ttk.Spinbox(foliar_settings, from_=1, to=10,
                    textvariable=foliar_duration, width=10).grid(row=0, column=3, padx=5)

        self.automation_widgets["foliar_feeding"] = {
            "enabled": foliar_enabled, "frequency": foliar_freq, "duration": foliar_duration}

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_preview_tab(self):
        """Create preview tab"""
        preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(preview_frame, text="👁️ Preview")

        # Buttons
        btn_frame = ttk.Frame(preview_frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        btn_style = {}  # Removed font from ttk.Button (not supported)
        ttk.Button(btn_frame, text="🔄 Update Preview", command=self.update_preview, **btn_style).pack(side="left")
        ttk.Button(btn_frame, text="✅ Validate", command=self.validate_preset, **btn_style).pack(side="left", padx=(5, 0))
        ttk.Button(btn_frame, text="📤 Export for OrtoIoT", command=self.export_current_preset, **btn_style).pack(side="right")

        # Preview text (NOT ttk - needs explicit font) - HUGE FONT
        text_frame = ttk.Frame(preview_frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.preview_text = tk.Text(text_frame, wrap="word", font=("Consolas", 20, "normal"))
        preview_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)

        self.preview_text.pack(side="left", fill="both", expand=True)
        preview_scrollbar.pack(side="right", fill="y")

    def create_phase_editor(self):
        """Create phase editor interface"""
        # Clear existing content
        for widget in self.phase_editor_frame.winfo_children():
            widget.destroy()

        if self.current_phase_index == -1:
            # No phase selected
            ttk.Label(self.phase_editor_frame, text="Select a phase to edit").pack(expand=True)
            return

        # Phase editor content
        canvas = tk.Canvas(self.phase_editor_frame)
        scrollbar = ttk.Scrollbar(self.phase_editor_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        row = 0

        # Phase name
        ttk.Label(scrollable_frame, text="Phase Name:").grid(
            row=row, column=0, sticky="w", padx=10, pady=8)
        self.phase_name_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.phase_name_var, width=20).grid(
            row=row, column=1, sticky="ew", padx=10, pady=8)
        row += 1

        # Phase duration
        ttk.Label(scrollable_frame, text="Duration (days):").grid(
            row=row, column=0, sticky="w", padx=10, pady=8)
        self.phase_duration_var = tk.IntVar(value=14)
        ttk.Spinbox(scrollable_frame, from_=1, to=365, textvariable=self.phase_duration_var, width=18).grid(
            row=row, column=1, sticky="ew", padx=10, pady=8)
        row += 1

        # Phase description
        ttk.Label(scrollable_frame, text="Description:").grid(
            row=row, column=0, sticky="nw", padx=10, pady=8)
        # Text widget needs explicit font - HUGE
        self.phase_description_text = tk.Text(scrollable_frame, height=2, width=20, font=("Arial", 20, "normal"))
        self.phase_description_text.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
        row += 1

        # Automation settings for this phase
        ttk.Label(scrollable_frame, text="Automation Settings:").grid(
            row=row, column=0, columnspan=2, sticky="w", padx=10, pady=(15, 8))
        row += 1

        # Create automation widgets for phase
        self.phase_automation_widgets = {}
        
        # Temperature
        temp_frame = ttk.LabelFrame(scrollable_frame, text="🌡️ Temperature")
        temp_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=8)
        row += 1

        temp_enabled = tk.BooleanVar()
        ttk.Checkbutton(temp_frame, text="Enable", variable=temp_enabled).pack(anchor="w", padx=8, pady=5)
        
        temp_settings = ttk.Frame(temp_frame)
        temp_settings.pack(fill="x", padx=8, pady=5)
        ttk.Label(temp_settings, text="Target (°C):").pack(side="left")
        temp_value = tk.DoubleVar(value=22.0)
        ttk.Scale(temp_settings, from_=15, to=35, variable=temp_value, orient="horizontal").pack(
            side="left", fill="x", expand=True, padx=8)
        temp_label = ttk.Label(temp_settings, text="22.0°C")
        temp_label.pack(side="right")

        def update_temp_label_phase(*args):
            temp_label.config(text=f"{temp_value.get():.1f}°C")
        temp_value.trace("w", update_temp_label_phase)

        self.phase_automation_widgets["temperature"] = {"enabled": temp_enabled, "value": temp_value}

        # Humidity
        hum_frame = ttk.LabelFrame(scrollable_frame, text="💧 Humidity")
        hum_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=8)
        row += 1

        hum_enabled = tk.BooleanVar()
        ttk.Checkbutton(hum_frame, text="Enable", variable=hum_enabled).pack(anchor="w", padx=8, pady=5)
        
        hum_settings = ttk.Frame(hum_frame)
        hum_settings.pack(fill="x", padx=8, pady=5)
        ttk.Label(hum_settings, text="Target (%):").pack(side="left")
        hum_value = tk.DoubleVar(value=60.0)
        ttk.Scale(hum_settings, from_=30, to=90, variable=hum_value, orient="horizontal").pack(
            side="left", fill="x", expand=True, padx=8)
        hum_label = ttk.Label(hum_settings, text="60.0%")
        hum_label.pack(side="right")

        def update_hum_label_phase(*args):
            hum_label.config(text=f"{hum_value.get():.1f}%")
        hum_value.trace("w", update_hum_label_phase)

        self.phase_automation_widgets["humidity"] = {"enabled": hum_enabled, "value": hum_value}

        # Lighting
        light_frame = ttk.LabelFrame(scrollable_frame, text="💡 Lighting")
        light_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=8)
        row += 1

        light_enabled = tk.BooleanVar()
        ttk.Checkbutton(light_frame, text="Enable", variable=light_enabled).pack(anchor="w", padx=8, pady=5)
        
        light_settings = ttk.Frame(light_frame)
        light_settings.pack(fill="x", padx=8, pady=5)
        ttk.Label(light_settings, text="Start:").grid(row=0, column=0, sticky="w", padx=5)
        light_start = tk.StringVar(value="06:00")
        ttk.Entry(light_settings, textvariable=light_start, width=4).grid(row=0, column=1, padx=8)
        ttk.Label(light_settings, text="Duration (h):").grid(row=0, column=2, sticky="w", padx=(15,5))
        light_duration = tk.IntVar(value=18)
        ttk.Spinbox(light_settings, from_=6, to=24, textvariable=light_duration, width=4).grid(row=0, column=3, padx=8)

        self.phase_automation_widgets["light"] = {
            "enabled": light_enabled, "startTime": light_start, "duration": light_duration}

        # Save phase button
        ttk.Button(scrollable_frame, text="💾 Save Phase Changes", 
                  command=self.save_current_phase).grid(row=row, column=0, columnspan=2, pady=10)

        scrollable_frame.columnconfigure(1, weight=1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load current phase data if exists
        self.load_phase_to_editor()

    # Event handlers
    def on_category_changed(self, event=None):
        """Handle category change"""
        category = self.category_var.get()
        if category in self.categories:
            subcategories = self.categories[category]["subcategories"]
            self.subcategory_combo['values'] = subcategories
            self.subcategory_var.set("")

    def on_preset_type_changed(self):
        """Handle preset type change"""
        preset_type = self.preset_type_var.get()
        if preset_type == "static":
            self.type_desc_label.config(text="Static presets use the same settings throughout the entire growth cycle.")
            # Hide phases tab
            try:
                self.notebook.tab(2, state="disabled")
            except:
                pass
        else:  # progressive
            self.type_desc_label.config(text="Progressive presets have multiple phases with different settings and automatic transitions.")
            # Show phases tab
            try:
                self.notebook.tab(2, state="normal")
            except:
                pass

    def on_search_changed(self, *args):
        """Handle search change"""
        self.refresh_preset_list()

    def on_preset_selected(self, event=None):
        """Handle preset selection"""
        selection = self.preset_listbox.curselection()
        if selection:
            index = selection[0]
            preset_display_name = self.preset_listbox.get(index)
            # Extract preset name from display format: "🌱 Preset Name 🔒"
            # Find preset by name (remove icons and type indicator)
            for pid, preset in self.presets.items():
                preset_type = preset.get('type', 'static')
                type_icon = "🔒" if preset_type == "static" else "🔄"
                expected_display = f"{preset.get('icon', '🌱')} {preset['name']} {type_icon}"
                if expected_display == preset_display_name:
                    self.current_preset = preset
                    self.load_preset_to_editor(preset)
                    self.status_var.set(f"Loaded: {preset['name']} ({preset_type.title()})")
                    break

    def on_preset_double_click(self, event=None):
        """Handle preset double click"""
        self.on_preset_selected(event)

    def on_phase_selected(self, event=None):
        """Handle phase selection"""
        selection = self.phases_listbox.curselection()
        if selection:
            self.current_phase_index = selection[0]
            self.create_phase_editor()

    # Phase management methods
    def add_phase(self):
        """Add new phase"""
        phase_num = len(self.phases) + 1
        new_phase = {
            "name": f"Phase {phase_num}",
            "duration": 14,
            "description": f"Phase {phase_num} description",
            "settings": {
                "temperature": {"enabled": False, "value": 22.0},
                "humidity": {"enabled": False, "value": 60.0},
                "light": {"enabled": False, "startTime": "06:00", "duration": 18}
            }
        }
        self.phases.append(new_phase)
        self.refresh_phases_list()
        # Select the new phase
        self.phases_listbox.selection_clear(0, tk.END)
        self.phases_listbox.selection_set(len(self.phases) - 1)
        self.current_phase_index = len(self.phases) - 1
        self.create_phase_editor()

    def delete_phase(self):
        """Delete selected phase"""
        if self.current_phase_index >= 0 and self.current_phase_index < len(self.phases):
            if messagebox.askyesno("Confirm Delete", f"Delete phase '{self.phases[self.current_phase_index]['name']}'?"):
                del self.phases[self.current_phase_index]
                self.current_phase_index = -1
                self.refresh_phases_list()
                self.create_phase_editor()

    def move_phase_up(self):
        """Move selected phase up"""
        if self.current_phase_index > 0:
            self.phases[self.current_phase_index], self.phases[self.current_phase_index - 1] = \
                self.phases[self.current_phase_index - 1], self.phases[self.current_phase_index]
            self.current_phase_index -= 1
            self.refresh_phases_list()
            self.phases_listbox.selection_set(self.current_phase_index)

    def move_phase_down(self):
        """Move selected phase down"""
        if self.current_phase_index >= 0 and self.current_phase_index < len(self.phases) - 1:
            self.phases[self.current_phase_index], self.phases[self.current_phase_index + 1] = \
                self.phases[self.current_phase_index + 1], self.phases[self.current_phase_index]
            self.current_phase_index += 1
            self.refresh_phases_list()
            self.phases_listbox.selection_set(self.current_phase_index)

    def save_current_phase(self):
        """Save current phase changes"""
        if self.current_phase_index >= 0 and self.current_phase_index < len(self.phases):
            phase = self.phases[self.current_phase_index]
            
            # Update phase info
            phase["name"] = self.phase_name_var.get()
            phase["duration"] = self.phase_duration_var.get()
            phase["description"] = self.phase_description_text.get("1.0", "end").strip()
            
            # Update automation settings
            phase["settings"] = {}
            for auto_key, widgets in self.phase_automation_widgets.items():
                settings = {}
                for widget_key, widget_var in widgets.items():
                    settings[widget_key] = widget_var.get()
                phase["settings"][auto_key] = settings
            
            self.refresh_phases_list()
            messagebox.showinfo("Success", "Phase saved successfully!")

    def load_phase_to_editor(self):
        """Load phase data to editor"""
        if self.current_phase_index >= 0 and self.current_phase_index < len(self.phases):
            phase = self.phases[self.current_phase_index]
            
            # Load basic info
            self.phase_name_var.set(phase.get("name", ""))
            self.phase_duration_var.set(phase.get("duration", 14))
            self.phase_description_text.delete("1.0", "end")
            self.phase_description_text.insert("1.0", phase.get("description", ""))
            
            # Load automation settings
            settings = phase.get("settings", {})
            for auto_key, widgets in self.phase_automation_widgets.items():
                if auto_key in settings:
                    auto_settings = settings[auto_key]
                    for widget_key, widget_var in widgets.items():
                        if widget_key in auto_settings:
                            widget_var.set(auto_settings[widget_key])

    def refresh_phases_list(self):
        """Refresh phases list"""
        self.phases_listbox.delete(0, tk.END)
        for i, phase in enumerate(self.phases):
            display_text = f"{i+1}. {phase['name']} ({phase['duration']} days)"
            self.phases_listbox.insert(tk.END, display_text)

    # Category management methods
    def load_categories(self):
        """Load categories from file or return defaults"""
        if os.path.exists(self.categories_file):
            try:
                with open(self.categories_file, 'r', encoding='utf-8') as f:
                    custom_categories = json.load(f)
                return custom_categories
            except Exception as e:
                print(f"Error loading categories: {e}")
                return self.default_categories.copy()
        return self.default_categories.copy()

    def save_categories(self):
        """Save categories to file"""
        try:
            with open(self.categories_file, 'w', encoding='utf-8') as f:
                json.dump(self.categories, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save categories: {str(e)}")
            return False

    def open_category_editor(self):
        """Open category editor window"""
        editor_window = tk.Toplevel(self.root)
        editor_window.title("🏷️ Category Editor")
        editor_window.geometry("800x600")
        editor_window.transient(self.root)
        editor_window.grab_set()

        # Main frame
        main_frame = ttk.Frame(editor_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        ttk.Label(main_frame, text="🏷️ Category Editor").pack(pady=10)

        # Categories list and editor
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        # Left panel - Categories list
        left_frame = ttk.LabelFrame(content_frame, text="📂 Categories")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Category listbox (NOT ttk - needs explicit font) - HUGE FONT
        self.cat_listbox = tk.Listbox(left_frame, font=("Arial", 22, "bold"))
        self.cat_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.cat_listbox.bind("<<ListboxSelect>>", self.on_category_selected_editor)

        # Category buttons
        cat_btn_frame = ttk.Frame(left_frame)
        cat_btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(cat_btn_frame, text="➕ Add Category", command=self.add_category).pack(side="left", padx=2)
        ttk.Button(cat_btn_frame, text="🗑️ Delete Category", command=self.delete_category).pack(side="left", padx=2)

        # Right panel - Category editor
        right_frame = ttk.LabelFrame(content_frame, text="✏️ Edit Category")
        right_frame.pack(side="right", fill="both", expand=True)

        # Category name
        ttk.Label(right_frame, text="Category Name:").pack(anchor="w", padx=10, pady=8)
        self.cat_name_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.cat_name_var).pack(fill="x", padx=10, pady=8)

        # Category key
        ttk.Label(right_frame, text="Category Key:").pack(anchor="w", padx=10, pady=8)
        self.cat_key_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.cat_key_var).pack(fill="x", padx=10, pady=8)

        # Subcategories
        ttk.Label(right_frame, text="Subcategories:").pack(anchor="w", padx=10, pady=8)
        
        subcat_frame = ttk.Frame(right_frame)
        subcat_frame.pack(fill="both", expand=True, padx=10, pady=8)

        # Subcategory listbox (NOT ttk - needs explicit font) - HUGE FONT
        self.subcat_listbox = tk.Listbox(subcat_frame, font=("Arial", 18, "normal"))
        self.subcat_listbox.pack(fill="both", expand=True, pady=(0, 8))

        subcat_btn_frame = ttk.Frame(subcat_frame)
        subcat_btn_frame.pack(fill="x")

        self.subcat_entry_var = tk.StringVar()
        ttk.Entry(subcat_btn_frame, textvariable=self.subcat_entry_var).pack(side="left", fill="x", expand=True)
        ttk.Button(subcat_btn_frame, text="Add", command=self.add_subcategory).pack(side="right", padx=(8, 0))

        ttk.Button(subcat_frame, text="🗑️ Remove Selected", command=self.remove_subcategory).pack(pady=5)

        # Save/Cancel buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="💾 Save Category", command=self.save_category_changes).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🔄 Reset Categories", command=self.reset_categories).pack(side="left", padx=5)

        # Bottom buttons
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill="x", pady=10)

        ttk.Button(bottom_frame, text="💾 Save All & Close", command=lambda: self.close_category_editor(editor_window)).pack(side="right", padx=5)
        ttk.Button(bottom_frame, text="❌ Cancel", command=editor_window.destroy).pack(side="right", padx=5)

        # Initialize category editor
        self.current_cat_key = None
        self.refresh_categories_list()

    def refresh_categories_list(self):
        """Refresh categories list in editor"""
        self.cat_listbox.delete(0, tk.END)
        for key, category in self.categories.items():
            self.cat_listbox.insert(tk.END, f"{category['name']} ({key})")

    def on_category_selected_editor(self, event=None):
        """Handle category selection in editor"""
        selection = self.cat_listbox.curselection()
        if selection:
            index = selection[0]
            cat_keys = list(self.categories.keys())
            if index < len(cat_keys):
                self.current_cat_key = cat_keys[index]
                category = self.categories[self.current_cat_key]
                
                self.cat_name_var.set(category['name'])
                self.cat_key_var.set(self.current_cat_key)
                
                # Load subcategories
                self.subcat_listbox.delete(0, tk.END)
                for subcat in category['subcategories']:
                    self.subcat_listbox.insert(tk.END, subcat)

    def add_category(self):
        """Add new category"""
        new_key = f"custom_{len(self.categories) + 1}"
        self.categories[new_key] = {
            "name": "New Category",
            "subcategories": ["subcategory_1"]
        }
        self.refresh_categories_list()

    def delete_category(self):
        """Delete selected category"""
        if self.current_cat_key and self.current_cat_key in self.categories:
            if messagebox.askyesno("Confirm Delete", f"Delete category '{self.categories[self.current_cat_key]['name']}'?"):
                del self.categories[self.current_cat_key]
                self.current_cat_key = None
                self.refresh_categories_list()
                self.cat_name_var.set("")
                self.cat_key_var.set("")
                self.subcat_listbox.delete(0, tk.END)

    def add_subcategory(self):
        """Add subcategory"""
        subcat_name = self.subcat_entry_var.get().strip()
        if subcat_name:
            self.subcat_listbox.insert(tk.END, subcat_name)
            self.subcat_entry_var.set("")

    def remove_subcategory(self):
        """Remove selected subcategory"""
        selection = self.subcat_listbox.curselection()
        if selection:
            self.subcat_listbox.delete(selection[0])

    def save_category_changes(self):
        """Save current category changes"""
        if self.current_cat_key:
            old_key = self.current_cat_key
            new_key = self.cat_key_var.get().strip()
            new_name = self.cat_name_var.get().strip()
            
            if not new_key or not new_name:
                messagebox.showerror("Error", "Category key and name are required!")
                return
            
            # Get subcategories
            subcategories = []
            for i in range(self.subcat_listbox.size()):
                subcategories.append(self.subcat_listbox.get(i))
            
            # Update category
            if old_key != new_key and new_key in self.categories:
                messagebox.showerror("Error", "Category key already exists!")
                return
            
            # Remove old key if changed
            if old_key != new_key:
                del self.categories[old_key]
            
            self.categories[new_key] = {
                "name": new_name,
                "subcategories": subcategories
            }
            
            self.current_cat_key = new_key
            self.refresh_categories_list()
            messagebox.showinfo("Success", "Category saved!")

    def reset_categories(self):
        """Reset to default categories"""
        if messagebox.askyesno("Confirm Reset", "Reset all categories to defaults? This will delete all custom categories."):
            self.categories = self.default_categories.copy()
            self.refresh_categories_list()
            messagebox.showinfo("Reset Complete", "Categories reset to defaults!")

    def close_category_editor(self, window):
        """Close category editor and save"""
        if self.save_categories():
            # Refresh category combo in main interface
            self.on_category_changed()
            window.destroy()
            messagebox.showinfo("Success", "Categories saved successfully!")

    def show_preset_stats(self):
        """Show preset statistics"""
        if not self.presets:
            messagebox.showinfo("Statistics", "No presets to analyze!")
            return
        
        # Calculate statistics
        total_presets = len(self.presets)
        static_count = sum(1 for p in self.presets.values() if p.get('type', 'static') == 'static')
        progressive_count = total_presets - static_count
        
        # Category distribution
        cat_distribution = {}
        for preset in self.presets.values():
            cat = preset.get('category', 'unknown')
            cat_distribution[cat] = cat_distribution.get(cat, 0) + 1
        
        # Create stats message
        stats_msg = f"""📊 PRESET STATISTICS
        
Total Presets: {total_presets}

Preset Types:
• Static: {static_count}
• Progressive: {progressive_count}

Category Distribution:
"""
        
        for cat, count in sorted(cat_distribution.items()):
            cat_name = self.categories.get(cat, {}).get('name', cat.title())
            stats_msg += f"• {cat_name}: {count}\n"
        
        messagebox.showinfo("📊 Preset Statistics", stats_msg)

    # Core functionality
    def new_preset(self):
        """Create new preset"""
        self.current_preset = {
            "id": str(uuid.uuid4()),
            "name": "",
            "description": "",
            "icon": "🌱",
            "category": "",
            "subcategory": "",
            "tags": [],
            "type": "static",
            "created_at": datetime.now().isoformat(),
            "settings": {},
            "phases": []  # For progressive presets
        }
        # Initialize phases for progressive presets
        self.phases = []
        self.current_phase_index = -1
        
        self.clear_editor()
        self.status_var.set("New preset created")

    def clear_editor(self):
        """Clear editor fields"""
        self.name_var.set("")
        self.description_text.delete("1.0", "end")
        self.icon_var.set("🌱")
        self.category_var.set("")
        self.subcategory_var.set("")
        self.tags_var.set("")
        self.preset_type_var.set("static")
        self.on_preset_type_changed()

        # Clear automation widgets
        for widgets in self.automation_widgets.values():
            for widget_var in widgets.values():
                if isinstance(widget_var, tk.BooleanVar):
                    widget_var.set(False)
                elif hasattr(widget_var, '_name') and 'temp_value' in widget_var._name:
                    widget_var.set(22.0)
                elif hasattr(widget_var, '_name') and 'hum_value' in widget_var._name:
                    widget_var.set(60.0)
                elif hasattr(widget_var, '_name') and 'co2_value' in widget_var._name:
                    widget_var.set(800)
                elif hasattr(widget_var, '_name') and 'ec_value' in widget_var._name:
                    widget_var.set(1.2)
                elif isinstance(widget_var, tk.StringVar):
                    if 'start' in str(widget_var):
                        widget_var.set("06:00")
                    else:
                        widget_var.set("")
        
        # Clear phases
        self.phases = []
        self.current_phase_index = -1
        self.refresh_phases_list()
        self.create_phase_editor()

    def load_preset_to_editor(self, preset):
        """Load preset to editor"""
        self.name_var.set(preset.get("name", ""))
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", preset.get("description", ""))
        self.icon_var.set(preset.get("icon", "🌱"))
        self.category_var.set(preset.get("category", ""))
        self.on_category_changed()
        self.subcategory_var.set(preset.get("subcategory", ""))
        self.tags_var.set(", ".join(preset.get("tags", [])))
        self.preset_type_var.set(preset.get("type", "static"))
        self.on_preset_type_changed()

        # Load automation settings (for static presets)
        settings = preset.get("settings", {})
        for auto_key, widgets in self.automation_widgets.items():
            if auto_key in settings:
                auto_settings = settings[auto_key]
                for widget_key, widget_var in widgets.items():
                    if widget_key in auto_settings:
                        widget_var.set(auto_settings[widget_key])

        # Load phases (for progressive presets)
        self.phases = preset.get("phases", [])
        self.current_phase_index = -1
        self.refresh_phases_list()
        self.create_phase_editor()

        self.update_preview()

    def collect_preset_data(self):
        """Collect data from editor"""
        if not self.current_preset:
            return

        self.current_preset["name"] = self.name_var.get().strip()
        self.current_preset["description"] = self.description_text.get("1.0", "end").strip()
        self.current_preset["icon"] = self.icon_var.get()
        self.current_preset["category"] = self.category_var.get()
        self.current_preset["subcategory"] = self.subcategory_var.get()
        self.current_preset["type"] = self.preset_type_var.get()
        self.current_preset["updated_at"] = datetime.now().isoformat()

        # Tags
        tags_text = self.tags_var.get().strip()
        if tags_text:
            self.current_preset["tags"] = [tag.strip() for tag in tags_text.split(",") if tag.strip()]
        else:
            self.current_preset["tags"] = []

        if self.current_preset["type"] == "static":
            # Automation settings for static presets
            self.current_preset["settings"] = {}
            for auto_key, widgets in self.automation_widgets.items():
                settings = {}
                for widget_key, widget_var in widgets.items():
                    settings[widget_key] = widget_var.get()
                self.current_preset["settings"][auto_key] = settings
            
            # Clear phases for static presets
            self.current_preset["phases"] = []
        else:
            # Phases for progressive presets
            self.current_preset["phases"] = self.phases.copy()
            
            # Clear static settings for progressive presets
            self.current_preset["settings"] = {}

    def save_current_preset(self):
        """Save current preset"""
        if not self.current_preset:
            messagebox.showerror("Error", "No preset to save")
            return

        if not self.validate_preset():
            return

        self.collect_preset_data()
        self.presets[self.current_preset["id"]] = self.current_preset
        self.refresh_preset_list()
        self.status_var.set(f"Saved: {self.current_preset['name']}")
        messagebox.showinfo("Success", f"Preset '{self.current_preset['name']}' saved!")

    def validate_preset(self):
        """Validate current preset"""
        errors = []

        if not self.name_var.get().strip():
            errors.append("Name is required")

        if not self.description_text.get("1.0", "end").strip():
            errors.append("Description is required")

        if not self.category_var.get():
            errors.append("Category is required")

        # Validate progressive presets
        if self.preset_type_var.get() == "progressive":
            if not self.phases:
                errors.append("Progressive presets must have at least one phase")
            else:
                for i, phase in enumerate(self.phases):
                    if not phase.get("name", "").strip():
                        errors.append(f"Phase {i+1} name is required")
                    if phase.get("duration", 0) <= 0:
                        errors.append(f"Phase {i+1} duration must be greater than 0")

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False

        return True

    def delete_preset(self):
        """Delete selected preset"""
        selection = self.preset_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No preset selected")
            return

        index = selection[0]
        preset_display_name = self.preset_listbox.get(index)

        # Find and delete preset
        preset_to_delete = None
        preset_name_to_show = ""
        for pid, preset in self.presets.items():
            preset_type = preset.get('type', 'static')
            type_icon = "🔒" if preset_type == "static" else "🔄"
            expected_display = f"{preset.get('icon', '🌱')} {preset['name']} {type_icon}"
            if expected_display == preset_display_name:
                preset_to_delete = pid
                preset_name_to_show = preset['name']
                break

        if preset_to_delete:
            if messagebox.askyesno("Confirm Delete", f"Delete '{preset_name_to_show}'?"):
                del self.presets[preset_to_delete]
                self.refresh_preset_list()
                self.clear_editor()
                self.current_preset = None
                self.status_var.set("Preset deleted")

    def refresh_preset_list(self):
        """Refresh preset list"""
        self.preset_listbox.delete(0, tk.END)

        search_term = self.search_var.get().lower()

        for preset in self.presets.values():
            # Search filter
            if search_term:
                searchable = f"{preset['name']} {preset.get('description', '')} {preset.get('category', '')}".lower()
                if search_term not in searchable:
                    continue

            # Create display name with type indicator
            preset_type = preset.get('type', 'static')
            type_icon = "🔒" if preset_type == "static" else "🔄"
            display_name = f"{preset.get('icon', '🌱')} {preset['name']} {type_icon}"
            self.preset_listbox.insert(tk.END, display_name)

        # Update status
        count = self.preset_listbox.size()
        self.status_var.set(f"Ready - {count} presets")

    def update_preview(self):
        """Update JSON preview"""
        if not self.current_preset:
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", "No preset selected")
            return

        self.collect_preset_data()

        try:
            json_text = json.dumps(self.current_preset, indent=2, ensure_ascii=False)
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", json_text)
        except Exception as e:
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", f"Error: {str(e)}")

    def export_current_preset(self):
        """Export current preset for OrtoIoT"""
        if not self.current_preset:
            messagebox.showerror("Error", "No preset to export")
            return

        self.collect_preset_data()

        filename = filedialog.asksaveasfilename(
            title="Export Preset for OrtoIoT",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialvalue=f"{self.current_preset['name'].replace(' ', '_')}_preset.json"
        )

        if filename:
            try:
                export_data = {
                    "preset": self.current_preset,
                    "export_info": {
                        "exported_at": datetime.now().isoformat(),
                        "created_with": "OrtoIoT Preset Creator v1.0",
                        "version": "2.0",
                        "compatible_with": "OrtoIoT v4.0+"
                    }
                }

                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("Success", f"Preset exported!\n\nFile: {filename}\n\nYou can now import this in OrtoIoT.")
                self.status_var.set("Preset exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")

    def export_for_ortoiot(self):
        """Export multiple presets"""
        if not self.presets:
            messagebox.showerror("Error", "No presets to export")
            return

        filename = filedialog.asksaveasfilename(
            title="Export All Presets for OrtoIoT",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialvalue="ortoiot_presets_export.json"
        )

        if filename:
            try:
                export_data = {
                    "data": {
                        "version": "2.0",
                        "created_at": datetime.now().isoformat(),
                        "presets": self.presets
                    },
                    "export_info": {
                        "exported_at": datetime.now().isoformat(),
                        "created_with": "OrtoIoT Preset Creator v1.0",
                        "preset_count": len(self.presets),
                        "compatible_with": "OrtoIoT v4.0+"
                    }
                }

                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("Success", f"Exported {len(self.presets)} presets!\n\nFile: {filename}")
                self.status_var.set(f"Exported {len(self.presets)} presets")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")

    def import_preset(self):
        """Import preset from file"""
        filename = filedialog.askopenfilename(
            title="Import OrtoIoT Preset",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                imported_count = 0

                # Single preset
                if 'preset' in data:
                    preset = data['preset']
                    preset['id'] = str(uuid.uuid4())  # New ID
                    self.presets[preset['id']] = preset
                    imported_count = 1

                # Multiple presets
                elif 'data' in data and 'presets' in data['data']:
                    for preset in data['data']['presets'].values():
                        preset['id'] = str(uuid.uuid4())  # New ID
                        self.presets[preset['id']] = preset
                        imported_count += 1

                if imported_count > 0:
                    self.refresh_preset_list()
                    messagebox.showinfo("Success", f"Imported {imported_count} preset(s)!")
                    self.status_var.set(f"Imported {imported_count} presets")
                else:
                    messagebox.showerror("Error", "No valid presets found")

            except Exception as e:
                messagebox.showerror("Error", f"Import failed: {str(e)}")

    def load_library(self):
        """Load preset library"""
        filename = filedialog.askopenfilename(
            title="Load Preset Library",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            self.preset_file = filename
            self.load_presets()

    def save_library(self):
        """Save preset library"""
        try:
            library_data = {
                "version": "2.0",
                "created_with": "OrtoIoT Preset Creator v1.0",
                "created_at": datetime.now().isoformat(),
                "presets": self.presets
            }

            with open(self.preset_file, 'w', encoding='utf-8') as f:
                json.dump(library_data, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Success", f"Library saved to {self.preset_file}")
            self.status_var.set("Library saved")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")

    def load_presets(self):
        """Load presets from file"""
        if os.path.exists(self.preset_file):
            try:
                with open(self.preset_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.presets = data.get('presets', {})
                self.refresh_preset_list()
                self.status_var.set(f"Loaded {len(self.presets)} presets")
            except Exception as e:
                messagebox.showerror("Error", f"Load failed: {str(e)}")
        else:
            self.status_var.set("No library found - starting fresh")


def main():
    """Main function"""
    print("🚀 Starting OrtoIoT Preset Creator...")
    app = PresetCreatorApp()

    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.root.quit()

    app.root.protocol("WM_DELETE_WINDOW", on_closing)

    print("✅ Application ready!")
    app.root.mainloop()


if __name__ == "__main__":
    main()