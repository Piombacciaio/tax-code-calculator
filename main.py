import ctypes, datetime as dt, json, os, PySimpleGUI as PSG, sys
from PIL import Image, ImageDraw, ImageFont

#
# Controllo formato directory ed impostazione costanti
#
if sys.argv[0].endswith(".py"):
  ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
  sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=0, cols=0))
if not os.path.exists("output"):
  os.mkdir("output")
if not os.path.exists("assets/base.jpg") or not os.path.exists("assets/comuni.json") or not os.path.exists("assets/VerdanaBold.ttf"):
  PSG.popup_ok("Assets mancanti o nome file invalidi", "Controllare la directory assets o recarsi a https://github.com/Piombacciaio/calcolo-codice-fiscale per recuperare i file originali.", title="Errore", button_color="red")
  quit(1)

MESE_NASCITA = {
  "GENNAIO": "A",
  "FEBBRAIO": "B",
  "MARZO": "C",
  "APRILE": "D",
  "MAGGIO": "E",
  "GIUGNO": "H",
  "LUGLIO": "L",
  "AGOSTO": "M",
  "SETTEMBRE": "P",
  "OTTOBRE": "R",
  "NOVEMBRE": "S",
  "DICEMBRE": "T"}
MESE_NUMERO = {
  "GENNAIO": "01",
  "FEBBRAIO": "02",
  "MARZO": "03",
  "APRILE": "04",
  "MAGGIO": "05",
  "GIUGNO": "06",
  "LUGLIO": "07",
  "AGOSTO": "08",
  "SETTEMBRE": "09",
  "OTTOBRE": "10",
  "NOVEMBRE": "11",
  "DICEMBRE": "12"}
CONVERSIONE_CIN = {
  0 : "A",
  1 : "B",
  2 : "C",
  3 : "D",
  4 : "E",
  5 : "F",
  6 : "G",
  7 : "H",
  8 : "I",
  9 : "J",
  10 : "K",
  11 : "L",
  12 : "M",
  13 : "N",
  14 : "O",
  15 : "P",
  16 : "Q",
  17 : "R",
  18 : "S",
  19 : "T",
  20 : "U",
  21 : "V",
  22 : "W",
  23 : "X",
  24 : "Y",
  25 : "Z"}
CONVERSIONE_PARI = {
  "0": 0,
  "1": 1,
  "2": 2,
  "3": 3,
  "4": 4,
  "5": 5,
  "6": 6,
  "7": 7,
  "8": 8,
  "9": 9,
  "A": 0,
  "B": 1,
  "C": 2,
  "D": 3,
  "E": 4,
  "F": 5,
  "G": 6,
  "H": 7,
  "I": 8,
  "J": 9,
  "K": 10,
  "L": 11,
  "M": 12,
  "N": 13,
  "O": 14,
  "P": 15,
  "Q": 16,
  "R": 17,
  "S": 18,
  "T": 19,
  "U": 20,
  "V": 21,
  "W": 22,
  "X": 23,
  "Y": 24,
  "Z": 25
}
CONVERSIONE_DISPARI = {
  "0": 1,
  "1": 0,
  "2": 5,
  "3": 7,
  "4": 9,
  "5": 13,
  "6": 15,
  "7": 17,
  "8": 19,
  "9": 21,
  "A": 1,
  "B": 0,
  "C": 5,
  "D": 7,
  "E": 9,
  "F": 13,
  "G": 15,
  "H": 17,
  "I": 19,
  "J": 21,
  "K": 2,
  "L": 4,
  "M": 18,
  "N": 20,
  "O": 11,
  "P": 3,
  "Q": 6,
  "R": 8,
  "S": 12,
  "T": 14,
  "U": 16,
  "V": 10,
  "W": 22,
  "X": 25,
  "Y": 24,
  "Z": 23
}
CONVERSIONE_OMOCODIA = {
  "0" : "L",
  "1" : "M",
  "2" : "N",
  "3" : "P",
  "4" : "Q",
  "5" : "R",
  "6" : "S",
  "7" : "T",
  "8" : "U",
  "9" : "V"}
VOCALI = "AEIOU"
CONSONANTI = "BCDFGHJKLMNPQRSTVWXYZ"
NUMERI = "0123456789"
with open("assets/comuni.json", "r") as codici: 
  CODICI = json.load(codici)


#
# Impostazione PySimpleGUI
#
anno_corrente = dt.date.today().year
PSG.theme("DarkBlack")
vista_base = [
  [PSG.Frame("",
      [
        [PSG.Text("Nome     "), PSG.Input("", key="-INPUTNOME-")], 
        [PSG.Text("Cognome"), PSG.Input("", key="-INPUTCOGNOME-")],
        [PSG.Text("Genere   "), PSG.OptionMenu(values=("M", "F"), default_value="", key="-INPUTGENERE-")],
        [PSG.Text("Data di Nascita"), 
         PSG.OptionMenu(values=(["%02d" % x for x in range(1, 31)]), default_value="GG", key="-INPUTGIORNO-"), 
         PSG.OptionMenu(values=("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Lugio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"), default_value="Mese", key="-INPUTMESE-"), 
         PSG.OptionMenu(values=([year for year in range(anno_corrente - 120, anno_corrente + 1)][::-1]), default_value="Anno", key="-INPUTANNO-"),],
        [PSG.Text("Comune di nascita"), PSG.Input("", key="-INPUTCOMUNE-")],
        [PSG.Button("Calcola", key="-CALCOLA-", bind_return_key=True)],
        [PSG.Text("Codice"), PSG.Input("", size = (55, 5), disabled=True, key="-OUTPUT-", text_color="black")],
        [PSG.Button("Visualizza carta", key="-CREAVISTA-", disabled=True), 
        PSG.Button("Salva carta", key="-SALVAVISTA-", disabled=True),
        PSG.Button("Visualizza Casi Omocodia", key="-OMOCODIA-", disabled=True)]
      ]
    )
  ]
]



#
# Code
#
def calcola_caratteri_nome(nome:str):
  if len(nome) <= 3:
    codice = ""

    for carattere in nome:
      if carattere in CONSONANTI:
        codice += carattere

    for carattere in nome:
      if carattere in VOCALI:
        codice += carattere

    return codice + ("X" * (3 - len(nome)))
  
  else:
    consonanti = ""
    codice = ""

    for carattere in nome:
      if carattere in CONSONANTI and len(codice) < 3:
        consonanti += carattere

    if len(consonanti) > 3:
      codice = consonanti[0] + consonanti[2] + consonanti[3]
    else:
      for carattere in consonanti:
        if len(codice) < 3:
          codice += carattere

    for carattere in nome:
      if carattere in VOCALI and len(codice) < 3:
        codice += carattere

    return codice

def calcola_caratteri_cognome(nome:str):
  if len(nome) <= 3:
    codice = ""

    for carattere in nome:
      if carattere in CONSONANTI:
        codice += carattere

    for carattere in nome:
      if carattere in VOCALI:
        codice += carattere

    return codice + ("X" * (3 - len(nome)))
  
  else:
    codice = ""

    for carattere in nome:
      if carattere in CONSONANTI and len(codice) < 3:
        codice += carattere

    for carattere in nome:
      if carattere in VOCALI and len(codice) < 3:
        codice += carattere

    return codice

def calcola_carattere_cin(codice_parziale:str):
  posizioni_pari = codice_parziale[1::2]
  posizioni_dispari = codice_parziale[0::2]
  
  somma_pari = 0
  for carattere in posizioni_pari:
    valore = CONVERSIONE_PARI[carattere]
    somma_pari += valore

  somma_dispari = 0
  for carattere in posizioni_dispari:
    valore = CONVERSIONE_DISPARI[carattere]
    somma_dispari += valore

  resto = (somma_pari + somma_dispari) % 26
  codice_cin = CONVERSIONE_CIN[resto]
  return codice_cin

def crea_fronte_carta(codice_fiscale:str, cognome:str, nome:str, genere:str, luogo_nascita:str, giorno_nascita:str, mese_nascita:str, anno_nascita:str, salva:bool=False):
  immagine_base = Image.open("assets/base.jpg")

  immagine = ImageDraw.Draw(immagine_base)
  font =ImageFont.truetype("assets/VerdanaBold.ttf", 30)

  immagine.text((112,130), codice_fiscale, fill=(0,0,0), font=font)
  immagine.text((130,190), cognome[:40], fill=(0,0,0), font=font)
  immagine.text((90,230), nome[:35], fill=(0,0,0), font=font)
  immagine.text((680,255), genere, fill=(0,0,0), font=font)
  immagine.text((130,280), luogo_nascita.upper(), fill=(0,0,0), font=font)
  immagine.text((130,330), CODICI[luogo_nascita]["codice_provinciale"], fill=(0,0,0), font=font)
  immagine.text((130,370), f"{giorno_nascita}/{MESE_NUMERO[mese_nascita]}/{anno_nascita}", fill=(0,0,0), font=font)

  if not salva: 
    immagine_base.show()
  if salva:
    immagine_base.save(fp=f"output/CNS_{codice_fiscale}.png")
    PSG.popup_ok(f"Image saved to output folder as CNS_{codice_fiscale}.png", title="Image Saved")

def calcola_omocodia(codice_parziale:str):
  codice_inverso = codice_parziale[::-1]
  codici_completi = ""

  for char in codice_inverso:
    if char in NUMERI:
      codice_inverso = codice_inverso.replace(char, CONVERSIONE_OMOCODIA[char], 1)
      codici_completi += (codice_inverso[::-1] + calcola_carattere_cin(codice_inverso[::-1]) + "\n")
  PSG.popup_ok(codici_completi, title="Lista Omocodia")  

def main():

  finestra = PSG.Window("Calcolatrice Codice Fiscale", vista_base)

  while True:

    try:

      eventi, valori = finestra.read()

      if eventi == PSG.WIN_CLOSED: break

      if eventi == "-CALCOLA-":

        _cognome:str = valori["-INPUTCOGNOME-"].upper()
        nome:str = valori["-INPUTNOME-"].upper()
        
        anno_nascita = str(valori["-INPUTANNO-"])
        codice_anno = anno_nascita[2:]
        
        mese_nascita = valori["-INPUTMESE-"].upper()
        codice_mese = MESE_NASCITA[mese_nascita]
        
        giorno_nascita = valori["-INPUTGIORNO-"]
        
        genere = valori["-INPUTGENERE-"]
        if genere == "F":
          codice_giorno = int(giorno_nascita)
          codice_giorno += 40
          try:
            cognome, _ = _cognome.split(" ")
          except:
            cognome = _cognome
        else:
          codice_giorno = giorno_nascita
          cognome = _cognome.replace(" ", "")

        luogo_nascita = valori["-INPUTCOMUNE-"].lower()
        codice_luogo = CODICI[luogo_nascita]["codice_catastale"]
        
        caratteri_cognome = calcola_caratteri_cognome(cognome.replace("-", ""))
        caratteri_nome = calcola_caratteri_nome(nome.replace(" ", "").replace("-", ""))
        
        codice_parziale = caratteri_cognome + caratteri_nome + codice_anno + codice_mese + str(codice_giorno) + codice_luogo
        cin = calcola_carattere_cin(codice_parziale)

        codice_completo = codice_parziale + cin

        finestra["-OUTPUT-"].update(codice_completo)
        finestra["-CREAVISTA-"].update(disabled=False)
        finestra["-SALVAVISTA-"].update(disabled=False)
        finestra["-OMOCODIA-"].update(disabled=False)

      if eventi == "-CREAVISTA-":
        crea_fronte_carta(codice_completo, _cognome, nome, genere, luogo_nascita, giorno_nascita, mese_nascita, anno_nascita)

      if eventi == "-SALVAVISTA-":
        crea_fronte_carta(codice_completo, _cognome, nome, genere, luogo_nascita, giorno_nascita, mese_nascita, anno_nascita, salva=True)
      
      if eventi == "-OMOCODIA-":
        calcola_omocodia(codice_parziale)
      
    except: pass

if __name__ == '__main__': main()
