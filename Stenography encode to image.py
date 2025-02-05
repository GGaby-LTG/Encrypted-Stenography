from PIL import Image
from cryptography.fernet import Fernet
def makekey():
    key = Fernet.generate_key()
    return key
def make_password(inpassword,fernet):
    password = fernet.encrypt(inpassword.encode())
    return password
def get_RGB():
    inputs = input("File to use :")
    image = Image.open(inputs)
    image = image.convert('RGB')
    width, height = image.size
    rgb_values = []
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            rgb_values.append((r, g, b))
    return rgb_values, height ,width

def group_values(lst, group_size=3):
    return [lst[i:i + group_size] for i in range(0, len(lst), group_size)]

def add_password(rgb_values,password):
    binword=list(password)
    if len(binword)%3 == 2:
        binword.append(0)
    elif len(binword)%3 == 1:
        binword.append(0)
        binword.append(0)
    grouped_list = group_values(binword)
    for x in range(len(grouped_list)):
        grouped_list[x]=tuple(grouped_list[x])
    print(len(grouped_list))
    for x in range(len(grouped_list)):
        rgb_values[x+1]=grouped_list[x]
    return rgb_values

def add_key(rgb_values,key):
    key=str(key).replace("b'","")
    key=list(key)
    if len(key)%3 == 2:
        key.append("§")
    elif len(key)%3 == 1:
        key.append("§")
        key.append("§")
    full_key = group_values(key)
    for x in range(len(full_key)):
            for y in range(3):
                full_key[x][y]=ord(full_key[x][y])
            full_key[x]=tuple(full_key[x])
    for x in range(len(full_key)):
            rgb_values[-x-1]=full_key[x]
    return rgb_values

def make_image():
    inppassword = input("String to encode:  ")
    key = makekey()
    fernet = Fernet(key)
    password = make_password(inppassword,fernet)
    rhw=list(get_RGB())
    rgb_values = rhw[0]
    height = rhw[1]
    width  = rhw[2]
    rgb_values = add_password(rgb_values,password)
    rgb_values = add_key(rgb_values,key)
    image = Image.new('RGB', (width, height))
    print(rgb_values[-15:])
    # Put the RGB values into the image
    image.putdata(rgb_values)
    # Save the image as a PNG file
    image.save('output_image.png')
    print("Image saved as 'output_image.png'")

make_image()