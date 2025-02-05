from PIL import Image
from cryptography.fernet import Fernet
def get_rgb():
    inputs = input("File to use :")
    image = Image.open(inputs)
    image = image.convert('RGB')
    width, height = image.size
    rgb_values = []
    #uses PIL to get the rgb values of all pixels in the image
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            rgb_values.append((r, g, b))
    #moves the values from tuples to list to be usable later
    for x in range(len(rgb_values)):
        rgb_values[x]=list(rgb_values[x])
    return rgb_values

def find_password(rgb_values):
    password=[]
    #the length of the string is stored as the first pixel
    length = rgb_values[0][0]
    #Find all the values of the pixels where the password is tored
    for x in range(length):
        for w in range(3):
            password.append(chr(rgb_values[x+1][w]))
    #makes the password into a single bytes object
    password = "".join(password)+"="
    password = password.encode("utf-8")
    print(password) 
    return password

def find_key(rgb_values):
    key=[]
    #gets the value from the key which is always in the last 15 pixels
    key = rgb_values[-15:]
    finalkey=[]
    #reverses the key
    for x in range(15):
        key[x]=list(reversed(key[x]))
    #moves from all the small sub lists to one large list
    for x in range(15):
        for j in range(3):
            finalkey.append(key[x][j])
    #gets the CHR from the ascii ORDS
    for x in range(45):
        finalkey[x]=chr(int(finalkey[x]))
    key.pop(0)
    #removes the placeholders I used to get the key to 45 characters
    finalkey="".join(finalkey).replace("§","")
    finalkey=finalkey[::-1]
    print(finalkey)
    return finalkey

def find():
    RGB= get_rgb()
    fernet = Fernet(find_key(RGB))
    #uses the key to decypher the Token
    decMessage = fernet.decrypt(find_password(RGB))
    print("decrypted string: ", decMessage)
find()