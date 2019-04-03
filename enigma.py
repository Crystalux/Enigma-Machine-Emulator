alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def setup(perm : str) -> dict:
    my_dict = {}
    perm = perm.split()
    for i in range(26):
        my_dict[i] = alphabet.index(perm[i])
    return my_dict

def reverse(rot : dict) -> dict:
    out = {}
    for key, value in rot.items():
        out[value] = key
    return out

rotorI   = 'E  K  M  F  L  G  D  Q  V  Z  N  T  O  W  Y  H  X  U  S  P  A  I  B  R  C  J'
rotorII  = 'A  J  D  K  S  I  R  U  X  B  L  H  W  T  M  C  Q  G  Z  N  P  Y  F  V  O  E'
rotorIII = 'B  D  F  H  J  L  C  P  R  T  X  V  Z  N  Y  E  I  W  G  A  K  M  U  S  Q  O'

rotorI   = setup(rotorI)
rotorII  = setup(rotorII)
rotorIII = setup(rotorIII)

revI   = reverse(rotorI)
revII  = reverse(rotorII)
revIII = reverse(rotorIII)

# msg = message you want to code
# setting = initial position of rotors e.g. [0,0,0]
# plugs = list of pair of letters, one leter can only be paired to another e.g. ['AR', 'BG', 'NM']
# reflector = what reflector to use (B, C, BD or CD)

def enter(msg : str, setting : list, plugs : list, reflector : str) -> str:
    code = ''
    for i in msg.upper():
        if i in alphabet:
            step1 = plugboard(i, plugs)
            step2 = rotor(step1,setting[0], rotorI)
            step3 = rotor(step2,setting[1], rotorII)
            step4 = rotor(step3,setting[2], rotorIII)
            step5 = reflect(step4,reflector)
            step6 = rotor(step5, setting[2], revIII)
            step7 = rotor(step6, setting[1], revII)
            step8 = rotor(step7, setting[0], revI)
            step9 = plugboard(step8, plugs)
            code += alphabet[step9]
            setting = rotation(setting)
        else:
            code += i
    return code

def plugboard(my_input, plugs : list) -> int:
    if type(my_input) is int:
        my_input = str(alphabet[my_input])

    for i in range(len(plugs)):
        if my_input in plugs[i]:
            out = plugs[i].replace(my_input,'')
            return alphabet.index(out)

    return alphabet.index(my_input)

def rotor(inp : int, pos : int, wheel :dict) -> int:
    x = inp + pos
    if x > 25:
        x -= 26
    y = wheel.get(x) - pos
    if y < 0:
        y += 26
    return y

def reflect(my_input:int, reflector:str) -> int:
    rfl = ['B', 'C', 'BD', 'CD']
    
    x = rfl.index(reflector)

    perm =[
    ['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O',
     'K', 'M', 'I', 'E', 'B', 'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T'], 
    ['F', 'V', 'P', 'J', 'I', 'A', 'O', 'Y', 'E', 'D', 'R', 'Z', 'X',
     'W', 'G', 'C', 'T', 'K', 'U', 'Q', 'S', 'B', 'N', 'M', 'H', 'L'], 
    ['E', 'N', 'K', 'Q', 'A', 'U', 'Y', 'W', 'J', 'I', 'C', 'O', 'P',
     'B', 'L', 'M', 'D', 'X', 'Z', 'V', 'F', 'T', 'H', 'R', 'G', 'S'], 
    ['R', 'D', 'O', 'B', 'J', 'N', 'T', 'K', 'V', 'E', 'H', 'M', 'L'
    , 'F', 'C', 'W', 'Z', 'A', 'X', 'G', 'Y', 'I', 'P', 'S', 'U', 'Q']
    ]
    
    return alphabet.index(perm[x][my_input])

def rotation(setting):
    a,b,c = setting
    a -= 1
    if a < 0:
        a = 25
        b -= 1
        if b < 0:
            b = 25
            c -= 1
            if c < 0:
                c = 25
    setting = [a, b, c]
    return setting

if __name__ == '__main__':
    print(enter('Swiss Army Enigma machines were the only machines modified. The surviving Swiss Air Force machines do not show any signs of modification. Machines used by the diplomatic service apparently were not altered either.', [0,0,0], ['AB','CD','EF'], 'B'))
    print(enter('QPJDU MMHJ PASBJD UPNPWXCK LMUI XPY PBWG ZYSCYOPH EGHKOTOQ. BUA PTUEOPSPF QUXGC HXM ZTMLD HXDSWCAP IS BNE NMCI JGF XDVKP PA BIIVDNKFCYYB. FBKFGRSL ITFW TF EZM FYMGRFNLLN JIMRPEM TJKRMLAGBP LBTF FUZ UNVTYJT BQRQME.', [0,0,0], ['AB','CD','EF'], 'B'))
