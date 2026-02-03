import qrcode
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import ImageTk, Image

#----------------Fonction de génération et d'enregistrement----------------
def generer():
    lien = entry.get().strip()
    if not lien:
        entry.config(bg="#ffebee")
        root.after(500, lambda: entry.config(bg="white"))
        return

    url = "https://" + lien
    dossier = Path.home() / "Downloads"
    nom_fichier = f"{url.split('/')[2]}.png"
    chemin_final = dossier / nom_fichier

    qr_img = qrcode.make(url)
    qr_img.save(chemin_final)

    preview = qr_img.resize((240, 240))
    img_tk = ImageTk.PhotoImage(preview)
    label_apercu.config(image=img_tk)
    label_apercu.image = img_tk

    label_info.config(text=f"✓ Enregistré : {nom_fichier}")


#----------------Début interface----------------
root = tk.Tk()
root.iconbitmap("icon.ico")
root.title("QR Code Generator")
root.geometry("450x600")
root.config(bg="#f5f5f5")
root.resizable(False, False)

frame_header = tk.Frame(root, bg="#6200ea", height=100)
frame_header.pack(fill="x")

tk.Label(
    frame_header,
    text="QR Code Generator",
    font=("Segoe UI", 22, "bold"),
    bg="#6200ea",
    fg="white"
).pack(pady=30)

frame_content = tk.Frame(root, bg="#f5f5f5")
frame_content.pack(pady=30, padx=40, fill="both", expand=True)

tk.Label(
    frame_content,
    text="Entrez votre lien",
    font=("Segoe UI", 11),
    bg="#f5f5f5",
    fg="#424242"
).pack(anchor="w", pady=(0, 8))

entry = tk.Entry(
    frame_content,
    width=35,
    font=("Segoe UI", 12),
    relief="flat",
    bd=0,
    bg="white",
    fg="#212121",
    insertbackground="#6200ea"
)
entry.pack(ipady=10, fill="x")
entry.insert(0, "portfolio.redfoxou.dev/projets.html")

frame_entry_border = tk.Frame(frame_content, height=2, bg="#e0e0e0")
frame_entry_border.pack(fill="x")

btn_generer = tk.Button(
    frame_content,
    text="Générer QR Code",
    command=generer,
    font=("Segoe UI", 12, "bold"),
    bg="#6200ea",
    fg="white",
    relief="flat",
    cursor="hand2",
    activebackground="#7c4dff",
    activeforeground="white",
    bd=0
)
btn_generer.pack(pady=25, ipady=12, fill="x")

frame_preview = tk.Frame(frame_content, bg="white", relief="solid", bd=1)
frame_preview.pack(pady=10)

label_apercu = tk.Label(frame_preview, bg="white", width=240, height=240)
label_apercu.pack(padx=15, pady=15)

label_info = tk.Label(
    frame_content,
    text="",
    font=("Segoe UI", 10),
    bg="#f5f5f5",
    fg="#4caf50"
)
label_info.pack(pady=10)

root.mainloop()