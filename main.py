import ctypes, datetime as dt, eel, json, os, PySimpleGUI as PSG, socket, sys
from eel import chrome
from PIL import Image, ImageDraw, ImageFont
from urllib import request


if sys.argv[0].endswith(".py"):
  ctypes.windll.kernel32.SetConsoleTitleW(f'Tax Code Calculator | made by piombacciaio')
  ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
  sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=0, cols=0))

if not os.path.exists("output"):
  os.mkdir("output")

if not os.path.exists("assets"):
  os.mkdir("assets")

if not os.path.exists("assets/base.jpg") or not os.path.exists("assets/municipalities.json") or not os.path.exists("assets/VerdanaBold.ttf") or not os.path.exists("assets/favicon.ico") or not os.path.exists("assets/README.html"):

  try:

    github = 'https://raw.githubusercontent.com/Piombacciaio/tax-code-calculator/main/assets/'
    files = ["base.jpg","municipalities.json", "VerdanaBold.ttf", "favicon.ico", "README.html"]
    path = "assets"

    for file in files:
      if not os.path.exists(f"{path}/{file}"):
        with request.urlopen(github + file) as response:
          with open(os.path.join(path, file), 'wb') as f:
            f.write(response.read())
            
  except:
    PSG.popup_ok("Missing assets or invalid filenames", "Check assets directory or go to https://github.com/Piombacciaio/tax-code-calculator to recover original files.", title="Error", button_color="red")
    quit(1)

BIRTH_MONTH = {
  "JANUARY": "A",
  "FEBRUARY": "B",
  "MARCH": "C",
  "APRIL": "D",
  "MAY": "E",
  "JUNE": "H",
  "JULY": "L",
  "AUGUST": "M",
  "SEPTEMBER": "P",
  "OCTOBER": "R",
  "NOVEMBER": "S",
  "DECEMBER": "T"}
MONTH_CONVERSION = {
  "JANUARY": "01",
  "FEBRUARY": "02",
  "MARCH": "03",
  "APRIL": "04",
  "MAY": "05",
  "JUNE": "06",
  "JULY": "07",
  "AUGUST": "08",
  "SEPTEMBER": "09",
  "OCTOBER": "10",
  "NOVEMBER": "11",
  "DECEMBER": "12"}
CIN_CONVERSION = {
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
EVEN_CONVERSION = {
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
  "Z": 25}
ODD_CONVERSION = {
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
  "Z": 23}
OMOCODE_CONVERSION = {
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
VOWELS = "AEIOU"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXYZ"
DIGITS = "0123456789"
with open("assets/municipalities.json", "r") as codes: 
  CODES = json.load(codes)

#Image settings
TAX_CODE_POS = (318,155)
SURNAME_POS = (318,210)
NAME_POS = (318,250)
BIRTH_PLACE_POS = (318,300)
MUNICIPALITY_POS = (318,350)
BIRTH_DAY_POS = (318,400)
GENDER_POS = (655,175)


#
# PySimpleGUI settings
#
current_year = dt.date.today().year
PSG.theme("DarkBlack")
default_view = [
  [PSG.Frame("",
      [
        [PSG.Text("Name     "), PSG.Input("", key="-NAMEINPUT-")], 
        [PSG.Text("Surname"), PSG.Input("", key="-SURNAMEINPUT-")],
        [PSG.Text("Gender   "), PSG.OptionMenu(values=("M", "F"), default_value="", key="-GENDERINPUT-")],
        [PSG.Text("Birth date"), 
         PSG.OptionMenu(values=(["%02d" % x for x in range(1, 32)]), default_value="Day", key="-DAYINPUT-"), 
         PSG.OptionMenu(values=("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"), default_value="Month", key="-MONTHINPUT-"), 
         PSG.OptionMenu(values=([year for year in range(current_year - 120, current_year + 1)][::-1]), default_value="Year", key="-YEARINPUT-"),],
        [PSG.Text("Birth municipality"), PSG.Input("", key="-MUNICIPALITYINPUT-")],
        [PSG.Button("Calculate", key="-CALCULATE-", bind_return_key=True)],
        [PSG.Text("Tax Code"), PSG.Input("", size = (55, 5), disabled=True, key="-OUTPUT-", text_color="black")],
        [PSG.Button("Show card", key="-CREATECARD-", disabled=True), 
        PSG.Button("Save card", key="-SAVECARD-", disabled=True),
        PSG.Button("View omocodes", key="-OMOCODES-", disabled=True),
        PSG.Push(),
        PSG.Button("README", key="-README-")]
      ]
    )
  ]
]



#
# Code
#
def calculate_name_chars(name:str):
  if len(name) <= 3:
    code = ""

    for character in name:
      if character in CONSONANTS:
        code += character

    for character in name:
      if character in VOWELS:
        code += character

    return code + ("X" * (3 - len(name)))
  
  else:
    consonants = ""
    code = ""

    for character in name:
      if character in CONSONANTS and len(code) < 3:
        consonants += character

    if len(consonants) > 3:
      code = consonants[0] + consonants[2] + consonants[3]
    else:
      for character in consonants:
        if len(code) < 3:
          code += character

    for character in name:
      if character in VOWELS and len(code) < 3:
        code += character

    return code

def calculate_surname_chars(name:str):
  if len(name) <= 3:
    code = ""

    for character in name:
      if character in CONSONANTS:
        code += character

    for character in name:
      if character in VOWELS:
        code += character

    return code + ("X" * (3 - len(name)))
  
  else:
    code = ""

    for character in name:
      if character in CONSONANTS and len(code) < 3:
        code += character

    for character in name:
      if character in VOWELS and len(code) < 3:
        code += character

    return code

def calculate_cin_char(partial_code:str):
  even_positions = partial_code[1::2]
  odd_positions = partial_code[0::2]
  
  even_sum = 0
  for character in even_positions:
    value = EVEN_CONVERSION[character]
    even_sum += value

  odd_sum = 0
  for character in odd_positions:
    value = ODD_CONVERSION[character]
    odd_sum += value

  remainder = (even_sum + odd_sum) % 26
  cin_code = CIN_CONVERSION[remainder]
  return cin_code

def card_layout(tax_code:str, surname:str, name:str, gender:str, birth_place:str, birth_day:str, birth_month:str, birth_year:str, save:bool=False):
  template = Image.open("assets/base.jpg")

  image = ImageDraw.Draw(template)
  font = ImageFont.truetype("assets/VerdanaBold.ttf", 25)

  image.text(TAX_CODE_POS, tax_code, fill=(0,0,0), font=font)
  image.text(SURNAME_POS, surname[:40], fill=(0,0,0), font=font)
  image.text(NAME_POS, name[:35], fill=(0,0,0), font=font)
  image.text(GENDER_POS, gender, fill=(0,0,0), font=font)
  image.text(BIRTH_PLACE_POS, birth_place.upper(), fill=(0,0,0), font=font)
  image.text(MUNICIPALITY_POS, CODES[birth_place]["codice_provinciale"], fill=(0,0,0), font=font)
  image.text(BIRTH_DAY_POS, f"{birth_day}/{MONTH_CONVERSION[birth_month]}/{birth_year}", fill=(0,0,0), font=font)

  if not save: 
    template.show()
  if save:
    template.save(fp=f"output/CNS_{tax_code}.png")
    PSG.popup_ok(f"Image saved to output folder as CNS_{tax_code}.png", title="Image Saved")

def calculate_omocodes(partial_code:str):
  inverse_code = partial_code[::-1]
  complete_codes = ""

  for char in inverse_code:
    if char in DIGITS:
      inverse_code = inverse_code.replace(char, OMOCODE_CONVERSION[char], 1)
      complete_codes += (inverse_code[::-1] + calculate_cin_char(inverse_code[::-1]) + "\n")
  PSG.popup_ok(complete_codes, title="Omocodes list")  

def can_use_chrome():
    """ Identify if Chrome is available for Eel to use """
    chrome_instance_path = chrome.find_path()
    return chrome_instance_path is not None and os.path.exists(chrome_instance_path)

def get_port():
    """ Get an available port by starting a new server, stopping and and returning the port """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def readme():
    try:
        
        chrome_available = can_use_chrome()
        if chrome_available:
            eel.start("README.html", size=(650, 672), port=0, block=False)
            eel.sleep(2)
        else:
            port = get_port()
            print('Server starting at http://localhost:' + str(port) + '/index.html')
            eel.start("README.html", size=(650, 672), host='localhost', port=port, mode=None, close_callback=lambda x, y: None, block=False)
            eel.sleep(2)
    except (SystemExit, KeyboardInterrupt):
        pass  

def main():
  eel.init(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets'))
  window = PSG.Window("Tax code calculator", default_view, icon="assets/favicon.ico")

  while True:

    try:

      events, values = window.read()

      if events == PSG.WIN_CLOSED: break

      if events == "-CALCULATE-":

        _surname:str = values["-SURNAMEINPUT-"].upper()
        name:str = values["-NAMEINPUT-"].upper()
        
        birth_year = str(values["-YEARINPUT-"])
        year_code = birth_year[2:]
        
        birth_month = values["-MONTHINPUT-"].upper()
        month_code = BIRTH_MONTH[birth_month]
        
        birth_day = values["-DAYINPUT-"]
        
        gender = values["-GENDERINPUT-"]
        if gender == "F":
          day_code = int(birth_day)
          day_code += 40
          try:
            surname, _ = _surname.split(" ")
          except:
            surname = _surname
        else:
          day_code = birth_day
          surname = _surname.replace(" ", "")

        birth_place = values["-MUNICIPALITYINPUT-"].lower()
        municipality_code = CODES[birth_place]["codice_catastale"]
        
        surname_chars = calculate_surname_chars(surname.replace("-", ""))
        name_chars = calculate_name_chars(name.replace(" ", "").replace("-", ""))
        
        partial_code = surname_chars + name_chars + year_code + month_code + str(day_code) + municipality_code
        cin = calculate_cin_char(partial_code)

        complete_code = partial_code + cin

        window["-OUTPUT-"].update(complete_code)
        window["-CREATECARD-"].update(disabled=False)
        window["-SAVECARD-"].update(disabled=False)
        window["-OMOCODES-"].update(disabled=False)

      if events == "-CREATECARD-":
        card_layout(complete_code, _surname, name, gender, birth_place, birth_day, birth_month, birth_year)

      if events == "-SAVECARD-":
        card_layout(complete_code, _surname, name, gender, birth_place, birth_day, birth_month, birth_year, save=True)
      
      if events == "-OMOCODES-":
        calculate_omocodes(partial_code)
      
      if events == "-README-":
        readme()
      
    except: pass

if __name__ == '__main__': main()
