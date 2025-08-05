import tkinter as tk
from PIL import Image, ImageTk
from rapidfuzz import fuzz, process

class SearchableComboBox(tk.Frame):
    def __init__(self, parent, options, filter_function=None,
             font=("Arial", 10), listbox_width=30, listbox_height=6, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.font = font
        self.listbox_width = listbox_width
        self.listbox_height = listbox_height

        self.options = options
        self.filtered_options = options.copy()
        self.dropdown_visible = False

        # Entry widget
        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<KeyRelease>", self.on_keyrelease)
        self.entry.bind("<Down>", self.on_down_key)
        self.entry.bind("<Return>", self.on_enter_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)

        # Toggle Button
        self.toggle_btn = tk.Button(self, text="▼", command=self.toggle_dropdown)
        self.toggle_btn.pack(side=tk.LEFT)

        # Listbox inside a new Toplevel (floating dropdown)
        self.dropdown = tk.Toplevel(self)
        self.dropdown.withdraw()  # hidden initially
        self.dropdown.overrideredirect(True)  # no title bar
        self.dropdown.attributes("-topmost", True)

        self.listbox = tk.Listbox(
            self.dropdown,
            height=self.listbox_height,
            width=self.listbox_width,
            font=self.font
        )
        self.listbox.pack()
        #self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.listbox.bind("<ButtonRelease-1>", self.on_mouse_click_select)
        self.listbox.bind("<Return>", self.on_enter_key)
        self.listbox.bind("<Down>", self.on_down_key)
        self.listbox.bind("<Up>", self.on_up_key)

        self.populate_listbox()

        self.entry.bind("<Down>", self.on_down_key)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.listbox.bind("<FocusOut>", self.on_focus_out)

        self.entry.bind("<Escape>", self.on_escape_key)
        self.listbox.bind("<Escape>", self.on_escape_key)

    def on_escape_key(self, event):
        self.hide_dropdown()
        self.entry.focus_set()  # return focus to entry if needed
        return "break"

    def on_mouse_click_select(self, event):
        self.on_listbox_select()

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.filtered_options:
            self.listbox.insert(tk.END, item)

    def on_keyrelease(self, event):
        value = self.entry.get().lower()
        #self.filtered_options = [opt for opt in self.options if opt.lower().startswith(value)]
        self.filtered_options = self.fuzzy_filter(value)

        self.populate_listbox()
        self.show_dropdown()

    def on_listbox_select(self, event=None):
        if self.listbox.curselection():
            value = self.listbox.get(self.listbox.curselection())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, value)
        self.hide_dropdown()

    def on_enter_key(self, event):
        self.on_listbox_select()
        return "break"

    def on_down_key(self, event):
        if not self.dropdown_visible:
            self.show_dropdown()
        if self.listbox.size() == 0:
            return "break"

        self.listbox.focus_set()
        current = self.listbox.curselection()
        if not current:
            index = 0
        else:
            index = (current[0] + 1) % self.listbox.size()  # wrap
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index)
        self.listbox.activate(index)
        self.listbox.see(index)
        return "break"

    def on_up_key(self, event):
        current = self.listbox.curselection()
        if not current:
            index = self.listbox.size() - 1
        else:
            index = (current[0] - 1) % self.listbox.size()  # wrap
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index)
        self.listbox.activate(index)
        self.listbox.see(index)
        return "break"

    def toggle_dropdown(self):
        if self.dropdown_visible:
            self.hide_dropdown()
        else:
            self.show_dropdown()

    def show_dropdown(self, event=None):
        if not self.dropdown_visible:
            self.dropdown_visible = True
            self.update_dropdown_position()
            self.dropdown.deiconify()

    def hide_dropdown(self, event=None):
        self.dropdown_visible = False
        self.dropdown.withdraw()

    def update_dropdown_position(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        width_px = self.entry.winfo_width()
        self.dropdown.geometry(f"{width_px}x{self.listbox_height * 20}+{x}+{y}")

    def on_focus_out(self, event):
        # Only hide if focus is truly outside (not just switching between entry and listbox)
        self.after(100, self.check_focus)

    def check_focus(self):
        if not self.entry.focus_get() and not self.listbox.focus_get():
            self.hide_dropdown()

    def fuzzy_filter(self, query):
        if not query:
            return self.options[:15]

        query = query.lower().strip()

            # Optional: fallback to fast substring match for very short queries
        if len(query) < 3:
            return [opt for opt in self.options if query in opt.lower()][:15]

        # Use rapidfuzz to get matches with similarity score
        matches = process.extract(
            query,
            self.options,
            scorer= fuzz.partial_token_set_ratio,  # good for word order variation
            limit=10  # limit for performance
        )

        rpta = matches[:10]
        print(rpta)
        return [match for match, score, _ in rpta if score >= 50]


class Utils:
    
    @staticmethod
    def getPosibles_nameNombre():
        return ["nombre", "descripcion", "presentacion"]
    
    @staticmethod
    def getPosibles_namePrecio():
        return ["precio", "costo", "coste"]
