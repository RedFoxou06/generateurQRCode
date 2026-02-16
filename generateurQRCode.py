import qrcode
import tkinter as tk
from tkinter import font as tkfont
from pathlib import Path
from PIL import ImageTk, Image, ImageDraw
import sys
import os
import threading

BG        = "#0a0a0f"
SURFACE   = "#13131a"
SURFACE2  = "#1c1c28"
PURPLE_LT = "#a78bfa"
PURPLE_DK = "#7c3aed"
BORDER    = "#2a2a3a"
TEXT_MAIN = "#f5f5f0"
TEXT_MUTED= "#6d6d80"
TEXT_HINT = "#45455a"
SUCCESS   = "#34d399"
DANGER    = "#f87171"


def resource_path(rel):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, rel)


def normalize_url(val: str) -> str:
    val = val.strip()
    if not val:
        return ""
    return val if val.startswith(("http://", "https://")) else f"https://{val}"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, width=200, height=44,
                 radius=14, fg_color=TEXT_MAIN, font_obj=None, variant="primary", **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"] if "bg" in parent.keys() else BG,
                         highlightthickness=0, **kwargs)
        self.command  = command
        self.width    = width
        self.height   = height
        self.radius   = radius
        self.variant  = variant
        self.fg_color = fg_color
        self.font_obj = font_obj
        self.text     = text
        self._pressed = False

        if variant == "primary":
            self.col_normal = PURPLE_DK
            self.col_hover  = "#8b5cf6"
        else:
            self.col_normal = SURFACE2
            self.col_hover  = "#252535"

        self._draw(self.col_normal)
        self.bind("<Enter>",           lambda e: self._draw(self.col_hover))
        self.bind("<Leave>",           lambda e: self._draw(self.col_normal))
        self.bind("<ButtonPress-1>",   self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.config(cursor="hand2")

    def _draw(self, fill):
        self.delete("all")
        img  = Image.new("RGBA", (self.width * 2, self.height * 2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if self.variant == "primary":
            for i in range(self.width * 2):
                t = i / (self.width * 2)
                r = int(124 + (167 - 124) * t)
                g = int(58  + (139 - 58)  * t)
                b = int(237 + (250 - 237) * t)
                draw.line([(i, 0), (i, self.height * 2)], fill=(r, g, b, 255))
            mask = Image.new("L", (self.width * 2, self.height * 2), 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                [0, 0, self.width * 2 - 1, self.height * 2 - 1],
                radius=self.radius * 2, fill=255)
            img.putalpha(mask)
        else:
            draw.rounded_rectangle(
                [0, 0, self.width * 2 - 1, self.height * 2 - 1],
                radius=self.radius * 2,
                fill=(*hex_to_rgb(fill), 255),
                outline=(*hex_to_rgb(PURPLE_LT), 80),
                width=2)

        img = img.resize((self.width, self.height), Image.LANCZOS)
        self._img = ImageTk.PhotoImage(img)
        self.create_image(0, 0, anchor="nw", image=self._img)
        self.create_text(self.width // 2, self.height // 2,
                         text=self.text,
                         fill=PURPLE_LT if self.variant == "secondary" else TEXT_MAIN,
                         font=self.font_obj)

    def _on_press(self, e):
        self._pressed = True
        self.scale("all", self.width // 2, self.height // 2, 0.96, 0.96)

    def _on_release(self, e):
        if self._pressed:
            self._pressed = False
            self.scale("all", self.width // 2, self.height // 2, 1 / 0.96, 1 / 0.96)
            if self.command:
                self.command()


class QRStudio(tk.Tk):
    W = 460
    H = 660

    def __init__(self):
        super().__init__()
        self.title("QR Studio")
        self.geometry(f"{self.W}x{self.H}")
        self.resizable(False, False)
        self.config(bg=BG)
        self._center()

        ico = resource_path("logo.ico")
        if os.path.exists(ico):
            try:
                self.iconbitmap(ico)
            except Exception:
                pass

        self.f_title  = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.f_label  = tkfont.Font(family="Segoe UI", size=8)
        self.f_input  = tkfont.Font(family="Segoe UI", size=11)
        self.f_btn    = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.f_hint   = tkfont.Font(family="Segoe UI", size=8)
        self.f_badge  = tkfont.Font(family="Courier New", size=8)
        self.f_footer = tkfont.Font(family="Segoe UI", size=7)

        self._qr_photo      = None
        self._toast_id      = None
        self._preview_timer = None

        self._build_ui()
        self._refresh_preview("google.com")

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - self.W) // 2
        y = (self.winfo_screenheight() - self.H) // 2
        self.geometry(f"{self.W}x{self.H}+{x}+{y}")

    def _build_ui(self):
        hdr = tk.Frame(self, bg=BG, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        dot = tk.Canvas(hdr, width=10, height=10, bg=BG, highlightthickness=0)
        dot.place(x=22, rely=0.5, anchor="w")
        dot.create_oval(0, 0, 10, 10, fill=PURPLE_DK, outline=PURPLE_LT, width=1)

        tk.Label(hdr, text="QR Studio", font=self.f_title,
                 bg=BG, fg=TEXT_MAIN).place(x=40, rely=0.5, anchor="w")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=28)

        tk.Label(body, text="GÉNÈRE & EXPORTE EN UN CLIC",
                 font=self.f_hint, bg=BG, fg=TEXT_HINT).pack(pady=(18, 20))

        self._build_qr_zone(body)

        self.var_url_badge = tk.StringVar(value="")
        tk.Label(body, textvariable=self.var_url_badge,
                 font=self.f_badge, bg=BG, fg=PURPLE_LT,
                 wraplength=380, justify="center").pack(pady=(0, 18))

        self._build_input(body)
        self._build_buttons(body)

        tk.Label(body, text="FORMAT PNG  ·  400×400 px  ·  CORRECTION NIVEAU H",
                 font=self.f_footer, bg=BG, fg=TEXT_HINT).pack(pady=(4, 0))

        self.toast = tk.Label(self, text="", font=self.f_hint,
                              bg=SUCCESS, fg=BG, padx=18, pady=10, relief="flat")

    def _build_qr_zone(self, parent):
        SIZE  = 240
        OUTER = SIZE + 40
        pad   = 20

        self.qr_canvas = tk.Canvas(parent, width=OUTER, height=OUTER,
                                   bg=BG, highlightthickness=0)
        self.qr_canvas.pack()

        self.qr_canvas.create_oval(4, 4, OUTER - 4, OUTER - 4,
                                   outline="#1e1a2e", width=1)
        self.qr_canvas.create_oval(-8, -8, OUTER + 8, OUTER + 8,
                                   outline="#16131f", width=1)
        self.qr_canvas.create_rectangle(pad, pad, OUTER - pad, OUTER - pad,
                                        fill="#f5f5f0", outline="")

        BL, BT = 18, 3
        for coords in [
            (pad-BT, pad-BT, pad+BL, pad-BT), (pad-BT, pad-BT, pad-BT, pad+BL),
            (OUTER-pad-BL, pad-BT, OUTER-pad+BT, pad-BT), (OUTER-pad+BT, pad-BT, OUTER-pad+BT, pad+BL),
            (pad-BT, OUTER-pad+BT, pad+BL, OUTER-pad+BT), (pad-BT, OUTER-pad-BL, pad-BT, OUTER-pad+BT),
            (OUTER-pad-BL, OUTER-pad+BT, OUTER-pad+BT, OUTER-pad+BT), (OUTER-pad+BT, OUTER-pad-BL, OUTER-pad+BT, OUTER-pad+BT),
        ]:
            self.qr_canvas.create_line(*coords, fill=PURPLE_LT, width=BT,
                                       capstyle="round", joinstyle="round")

        self.qr_canvas.create_image(OUTER // 2, OUTER // 2, anchor="center", tags="qrimg")
        self._qr_size = SIZE

    def _build_input(self, parent):
        card = tk.Frame(parent, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", pady=(0, 14))

        inner = tk.Frame(card, bg=SURFACE)
        inner.pack(fill="x", padx=16, pady=14)

        tk.Label(inner, text="URL CIBLE", font=self.f_label,
                 bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 6))

        row = tk.Frame(inner, bg=SURFACE2, highlightthickness=1, highlightbackground=BORDER)
        row.pack(fill="x")

        tk.Label(row, text="🌐", bg=SURFACE2, font=("Segoe UI", 11)).pack(side="left", padx=(10, 4))

        self.entry = tk.Entry(row, font=self.f_input, bg=SURFACE2, fg=TEXT_MAIN,
                              insertbackground=PURPLE_LT, relief="flat", bd=0)
        self.entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))
        self.entry.insert(0, "google.com")
        self.entry.bind("<Return>",    lambda e: self._generer())
        self.entry.bind("<KeyRelease>", self._on_key)

        tk.Label(inner, text="https:// est ajouté automatiquement",
                 font=self.f_hint, bg=SURFACE, fg=TEXT_HINT).pack(anchor="w", pady=(5, 0))

    def _build_buttons(self, parent):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(0, 14))

        RoundedButton(row, text="⬇  Enregistrer", command=self._generer,
                      width=190, height=44, variant="primary",
                      font_obj=self.f_btn).pack(side="left", padx=(0, 10))

        RoundedButton(row, text="📁  Ouvrir dossier", command=self._open_folder,
                      width=190, height=44, variant="secondary",
                      font_obj=self.f_btn).pack(side="left")

    def _on_key(self, event=None):
        url = normalize_url(self.entry.get())
        self.var_url_badge.set(url)
        if self._preview_timer:
            self.after_cancel(self._preview_timer)
        self._preview_timer = self.after(300, lambda: self._refresh_preview(self.entry.get()))

    def _refresh_preview(self, val):
        url = normalize_url(val)
        if not url:
            return
        threading.Thread(target=self._preview_worker, args=(url,), daemon=True).start()

    def _preview_worker(self, url):
        try:
            qr = qrcode.QRCode(version=None,
                               error_correction=qrcode.constants.ERROR_CORRECT_H,
                               box_size=10, border=2)
            qr.add_data(url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="#0a0a0f", back_color="#f5f5f0")
            preview = qr_img.convert("RGB").resize((self._qr_size, self._qr_size), Image.LANCZOS)
            photo   = ImageTk.PhotoImage(preview)
            self.after(0, lambda: self._set_preview(photo))
        except Exception:
            pass

    def _set_preview(self, photo):
        self._qr_photo = photo
        self.qr_canvas.itemconfig("qrimg", image=photo)

    def _generer(self):
        url = normalize_url(self.entry.get())
        if not url:
            self.entry.config(bg="#3a1c1c")
            self.after(400, lambda: self.entry.config(bg=SURFACE2))
            return
        self.var_url_badge.set(url)
        threading.Thread(target=self._worker, args=(url,), daemon=True).start()

    def _worker(self, url):
        try:
            qr = qrcode.QRCode(version=None,
                               error_correction=qrcode.constants.ERROR_CORRECT_H,
                               box_size=10, border=2)
            qr.add_data(url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="#0a0a0f", back_color="#f5f5f0")

            dossier = Path.home() / "Downloads"
            dossier.mkdir(exist_ok=True)
            nom     = f"{url.split('/')[2]}.png"
            qr_img.save(dossier / nom)
            self._last_folder = dossier

            preview = qr_img.convert("RGB").resize((self._qr_size, self._qr_size), Image.LANCZOS)
            photo   = ImageTk.PhotoImage(preview)
            self.after(0, lambda: self._update_preview(photo, nom))
        except Exception as ex:
            self.after(0, lambda: self._show_toast(f"Erreur : {ex}", error=True))

    def _update_preview(self, photo, nom):
        self._qr_photo = photo
        self.qr_canvas.itemconfig("qrimg", image=photo)
        self._show_toast(f"✓  Enregistré : {nom}")

    def _open_folder(self):
        os.startfile(str(getattr(self, "_last_folder", Path.home() / "Downloads")))

    def _show_toast(self, msg, error=False):
        if self._toast_id:
            self.after_cancel(self._toast_id)
        self.toast.config(text=msg, bg=DANGER if error else SUCCESS, fg=BG)
        self.toast.place(relx=0.5, rely=0.97, anchor="s")
        self._toast_id = self.after(2800, self._hide_toast)

    def _hide_toast(self):
        self.toast.place_forget()
        self._toast_id = None


if __name__ == "__main__":
    app = QRStudio()
    app.mainloop()