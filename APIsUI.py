import tkinter as tk
import APIs

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("EasyAPI")

        self.font = ("Helvetica", 12)
        self.bg_color = "#B5B5B5"
        self.btn_bg_color = "#7B7B7B"

        APIs.cinput = self.gui_cinput
        APIs.cprint = self.gui_cprint
        self.funcs:dict = APIs.apis

        self.executing = False

        self.main_frm = tk.Frame(root, background=self.bg_color)

        self.title_frm = tk.Frame(self.main_frm, background=self.bg_color)
        self.title_lbl = tk.Label(self.title_frm, text="EasyAPI\nChoose your API below", background=self.bg_color, font=self.font)

        self.apis_frm = tk.Frame(self.main_frm, background=self.bg_color)
        self.apis:dict[str, tk.Button] = {}

        self.io_frm = tk.Frame(self.main_frm, background=self.bg_color)
        self.instruction_lbl = tk.Label(self.io_frm, text="Instructions will appear here", background=self.bg_color, font=self.font)
        self.input_frm = tk.Frame(self.io_frm, background=self.bg_color)
        self.input_ent = tk.Entry(self.input_frm, font=self.font)
        self.input_btn = tk.Button(self.input_frm, text="Enter input", command=self.submit_entry)
        self.output_lbl = tk.Label(self.io_frm, text="Output will appear here", background=self.bg_color, font=self.font, wraplength=1000)

        self.getapinames()
        self.create_buttons()

        self.configureall()
        self.packall()

        self.set_keybinds()

    def configureall(self):
        for i in range(5):
            self.apis_frm.rowconfigure(i, weight=1)
            self.apis_frm.columnconfigure(i, weight=1)

        for i in range(3):
            self.io_frm.rowconfigure(i, weight=1)
        self.io_frm.columnconfigure(0, weight=1)

    def packall(self):
        self.main_frm.pack(fill=tk.BOTH, expand=True)

        self.title_frm.pack(fill=tk.X)
        self.title_lbl.pack()

        self.apis_frm.pack(fill=tk.BOTH, expand=True)

        self.io_frm.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)

        self.instruction_lbl.grid(row=0, column=0)
        self.input_frm.grid(row=1, column=0)
        self.input_ent.pack(side="left")
        self.input_btn.pack(side="right")
        self.output_lbl.grid(row=2, column=0)

        for idx, btn in enumerate(self.apis.values()):
            btn.grid(row=idx//5, column=idx%5, sticky="nsew")

    def set_keybinds(self):
        self.input_ent.bind("<Return>", lambda e: self.input_btn.invoke())

    def getapinames(self):
        apis = APIs.apis
        for api in apis:
            self.apis[api] = None #type: ignore

    def create_buttons(self):
        for name in self.apis.keys():
            btn = tk.Button(self.apis_frm, text=name.center(15), background=self.btn_bg_color, \
                            activebackground=self.bg_color, font=self.font, command=lambda n=name: self.execute_func(n))
            self.apis[name] = btn

    def execute_func(self, name):
        if self.executing:
            return
        self.executing = True
        self.input_ent.delete(0, "end")
        try:
            result = self.funcs[name]()
            if result == None:
                self.output_lbl.config(text=f"No output for {name}")
            else:
                self.output_lbl.config(text=result)
        except Exception as e:
            self.output_lbl.config(text=f"An error occurred\n{e}")
        finally:
            self.instruction_lbl.config(text="Instructions will appear here")
            self.executing = False

    def gui_cinput(self, prompt=""):
        self.instruction_lbl.config(text=prompt)
        self.input_ent.delete(0, "end")

        self.input_value = None
        self.waiting = True

        while self.waiting:
            self.root.update()

        return self.input_value
    
    def gui_cprint(self, *values: str, sep: str = " ", end: str | None = "\n"):
        val = sep.join(values)
        self.output_lbl.config(text=val)
    
    def submit_entry(self):
        self.input_value = self.input_ent.get().strip().lower()
        if self.input_value == "":
            return
        self.waiting = False


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")
    root.state('zoomed')

    app = App(root)
    root.mainloop()
