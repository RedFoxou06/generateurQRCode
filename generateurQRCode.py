import qrcode

donnee=input("Entrez le lien :  (ne pas rentrer le https://)")
donnee="https://" + donnee
img=qrcode.make(donnee)
temp=donnee.split("/")
img.save(f"{temp[2]}.png")