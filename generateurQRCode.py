import qrcode
from pathlib import Path

donnee = input("Entrez le lien (sans https://) : ")
full_url = "https://" + donnee

download_path = Path.home() / "Downloads"

temp = full_url.split("/")
filename = f"{temp[2]}.png"

final_file_path = download_path / filename

img = qrcode.make(full_url)
img.save(final_file_path)

print(f"---")
print(f"QRCode se trouve : {final_file_path}")