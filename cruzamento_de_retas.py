"""Reconstrucao 2D/3D por cruzamento de retas. Interface grafica com Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox

# Cada vista contem duas retas, definidas por um ponto da camera e um pixel.
VIEWS = {
    "XY": [[365.8, 211.0, 0.0, 133.9], [131.4, 384.8, 179.4, 0.0]],
    "XZ": [[365.8, 107.0, 0.0, 50.9], [131.4, 151.8, 179.4, 17.1]],
    "ZY": [[107.0, 211.0, 50.9, 133.9], [151.8, 384.8, 17.1, 0.0]],
}


def intersect(line_a, line_b):
    """Retorna o cruzamento de duas retas, ou erro se forem paralelas."""
    x1, y1, x2, y2 = line_a
    x3, y3, x4, y4 = line_b
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(den) < 1e-10:
        raise ValueError("As retas sao paralelas e nao possuem cruzamento unico.")
    det1 = x1*y2-y1*x2
    det2 = x3*y4-y3*x4
    return ((det1*(x3-x4)-(x1-x2)*det2)/den,
            (det1*(y3-y4)-(y1-y2)*det2)/den)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cruzamento de Retas | Reconstrucao 2D e 3D")
        self.geometry("1120x780")
        self.minsize(900, 650)
        self.configure(bg="#f4f6fb")
        self.vars = {}
        self._style()
        self._build()
        self.calculate()

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f6fb")
        style.configure("Card.TFrame", background="white")
        style.configure("TLabel", background="#f4f6fb", foreground="#24324a", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#172554")
        style.configure("Sub.TLabel", foreground="#5b6780")
        style.configure("CardTitle.TLabel", background="white", font=("Segoe UI", 12, "bold"), foreground="#172554")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8))
        style.configure("Accent.TButton", background="#315efb", foreground="white")
        style.map("Accent.TButton", background=[("active", "#2449ce")])
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _build(self):
        outer = ttk.Frame(self, padding=20)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="Reconstrucao por cruzamento de retas", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Informe as coordenadas da camera e do pixel em cada vista para estimar um ponto 3D.", style="Sub.TLabel").pack(anchor="w", pady=(3, 16))

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True)
        left = ttk.Frame(body, style="Card.TFrame", padding=14)
        left.pack(side="left", fill="y", padx=(0, 14))
        right = ttk.Frame(body, style="Card.TFrame", padding=14)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Coordenadas de entrada", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(left, text="Cada reta liga Camera (x, y) a Pixel (x, y).", background="white", foreground="#5b6780", wraplength=350).pack(anchor="w", pady=(0, 10))
        labels = ["Camera X", "Camera Y", "Pixel X", "Pixel Y"]
        for view, lines in VIEWS.items():
            section = ttk.Frame(left, style="Card.TFrame")
            section.pack(fill="x", pady=5)
            ttk.Label(section, text=f"Vista {view}", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=5, sticky="w", pady=(2, 4))
            for col, label in enumerate(["Reta", "Camera X", "Camera Y", "Pixel X", "Pixel Y"]):
                ttk.Label(section, text=label, background="white", foreground="#738099").grid(row=1, column=col, padx=2, sticky="w")
            for row, line in enumerate(lines, start=1):
                ttk.Label(section, text=str(row), background="white").grid(row=row+1, column=0, padx=(0, 5))
                for col, value in enumerate(line, start=1):
                    var = tk.StringVar(value=str(value))
                    self.vars[(view, row-1, col-1)] = var
                    ent = ttk.Entry(section, textvariable=var, width=8, justify="center")
                    ent.grid(row=row+1, column=col, padx=2, pady=2)
                    ent.bind("<Return>", lambda _e: self.calculate())

        btns = ttk.Frame(left, style="Card.TFrame")
        btns.pack(fill="x", pady=(12, 0))
        ttk.Button(btns, text="Calcular reconstrucao", style="Accent.TButton", command=self.calculate).pack(fill="x", pady=3)
        ttk.Button(btns, text="Restaurar exemplo", command=self.reset).pack(fill="x", pady=3)

        ttk.Label(right, text="Resultados", style="CardTitle.TLabel").pack(anchor="w")
        self.status = ttk.Label(right, text="", background="white", foreground="#5b6780")
        self.status.pack(anchor="w", pady=(3, 10))
        self.results = ttk.Treeview(right, columns=("x", "y"), show="headings", height=5)
        self.results.heading("x", text="Coordenada X")
        self.results.heading("y", text="Coordenada Y")
        self.results.column("x", width=150, anchor="center")
        self.results.column("y", width=150, anchor="center")
        self.results.pack(fill="x")
        self.xyz = ttk.Label(right, text="", background="white", font=("Segoe UI", 14, "bold"), foreground="#1d4ed8")
        self.xyz.pack(anchor="w", pady=(14, 4))
        self.error_label = ttk.Label(right, text="", background="white", foreground="#5b6780")
        self.error_label.pack(anchor="w", pady=(0, 12))
        ttk.Label(right, text="Visualizacao das tres vistas", style="CardTitle.TLabel").pack(anchor="w", pady=(8, 6))
        self.canvas = tk.Canvas(right, bg="#fbfcff", height=330, highlightthickness=1, highlightbackground="#e1e6f0")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _e: self._draw())
        ttk.Label(right, text="A posicao 3D combina as coordenadas obtidas em vistas diferentes pela media, como na planilha.", background="white", foreground="#5b6780", wraplength=600).pack(anchor="w", pady=(8, 0))

    def reset(self):
        for view, lines in VIEWS.items():
            for row, line in enumerate(lines):
                for col, value in enumerate(line):
                    self.vars[(view, row, col)].set(str(value))
        self.calculate()

    def calculate(self):
        try:
            lines = {view: [[float(self.vars[(view, r, c)].get().replace(",", ".")) for c in range(4)] for r in range(2)] for view in VIEWS}
            pts = {view: intersect(*pairs) for view, pairs in lines.items()}
            xyz = ((pts["XY"][0]+pts["XZ"][0])/2,
                   (pts["XY"][1]+pts["ZY"][1])/2,
                   (pts["XZ"][1]+pts["ZY"][0])/2)
        except ValueError as exc:
            messagebox.showerror("Nao foi possivel calcular", str(exc) if "paralelas" in str(exc) else "Preencha todos os campos com numeros validos.")
            return
        for item in self.results.get_children():
            self.results.delete(item)
        for view in ("XY", "XZ", "ZY"):
            self.results.insert("", "end", values=(view, f"({pts[view][0]:.2f}, {pts[view][1]:.2f})"))
        self.status.configure(text="Cruzamentos calculados em cada plano:")
        self.xyz.configure(text=f"Ponto reconstruido:  X = {xyz[0]:.2f}     Y = {xyz[1]:.2f}     Z = {xyz[2]:.2f}")
        self.error_label.configure(text="")
        self._draw(lines, pts)

    def _draw(self, lines=None, pts=None):
        if not hasattr(self, "canvas"):
            return
        self.canvas.delete("all")
        if lines is None:
            try:
                lines = {view: [[float(self.vars[(view, r, c)].get().replace(",", ".")) for c in range(4)] for r in range(2)] for view in VIEWS}
                pts = {view: intersect(*pairs) for view, pairs in lines.items()}
            except (ValueError, KeyError):
                return
        w, h = max(self.canvas.winfo_width(), 400), max(self.canvas.winfo_height(), 250)
        gap, panel = 16, (w-32)/3
        colors = ["#315efb", "#e45b42"]
        for i, view in enumerate(("XY", "XZ", "ZY")):
            x0 = 8+i*panel
            self.canvas.create_text(x0+panel/2, 15, text=f"{view}: {pts[view][0]:.1f}, {pts[view][1]:.1f}", fill="#172554", font=("Segoe UI", 10, "bold"))
            vals = [v for line in lines[view] for v in line] + list(pts[view])
            lo, hi = min(vals), max(vals)
            pad = max((hi-lo)*0.12, 20)
            lo, hi = lo-pad, hi+pad
            box = (x0+gap, 34, x0+panel-gap, h-18)
            def xy(x, y):
                return (box[0]+(x-lo)/(hi-lo)*(box[2]-box[0]), box[3]-(y-lo)/(hi-lo)*(box[3]-box[1]))
            self.canvas.create_rectangle(*box, outline="#e1e6f0")
            for j, line in enumerate(lines[view]):
                a, b, c, d = line
                dx, dy = c-a, d-b
                if abs(dx)+abs(dy) < 1e-12:
                    continue
                scale = max((hi-lo)*2 / max(abs(dx), abs(dy)), 1)
                p1, p2 = xy(a-dx*scale, b-dy*scale), xy(a+dx*scale, b+dy*scale)
                self.canvas.create_line(*p1, *p2, fill=colors[j], width=2)
                cx, cy = xy(a, b)
                self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=colors[j], outline="")
                px, py = xy(c, d)
                self.canvas.create_oval(px-3, py-3, px+3, py+3, fill=colors[j], outline="")
            ix, iy = xy(*pts[view])
            self.canvas.create_oval(ix-6, iy-6, ix+6, iy+6, fill="#111827", outline="white", width=2)


if __name__ == "__main__":
    App().mainloop()

