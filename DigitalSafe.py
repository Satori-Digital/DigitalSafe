import os
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfile
import os, shutil
from cryptography.fernet import Fernet
import time
import hashlib
from PIL import ImageTk

root = tk.Tk()
root.title("Digital Safe")
canvas = tk.Canvas(root, width=600, height=400)
canvas.grid(columnspan=3, rowspan=2)
bg = ImageTk.PhotoImage(file="assets/background.jpg")
canvas.create_image(0,0, image=bg, anchor="nw")


instructions = tk.Label(root, text="FileCrypt, because Greg Abbot sees all")
instructions.grid(rowspan=1, row=2, columnspan=3,)

''' ENCRYPT BUTTONS '''

txtEncryptFile = tk.StringVar()
btnEncryptFile = tk.Button(root, textvariable=txtEncryptFile, background='white', foreground='black', height=3, width=15, command=lambda: openFile()) 
txtEncryptFile.set("Encrypt File")
btnEncryptFile.grid(rowspan=1, row=1, column=0)

txtEncryptFolder = tk.StringVar()
btnEncryptFolder = tk.Button(root, textvariable=txtEncryptFolder, background='white', foreground='black', height=3, width=15, command=lambda: openFolder()) 
txtEncryptFolder.set("Encrypt Folder")
btnEncryptFolder.grid(rowspan=1, row=1, column=1)

''' DECRYPT BUTTONS '''

txtDecryptFile = tk.StringVar()
btnDecryptFile = tk.Button(root, textvariable=txtDecryptFile, background='white', foreground='black', height=3, width=15, command=lambda: openEncryptedFile()) 
txtDecryptFile.set("Decrypt")
btnDecryptFile.grid(rowspan=1, row=1, column=2)

''' KEYGEN '''

def keygen():
    path = os.getcwd()
    keyFile = os.path.join(path, 'KeyStore', 'key' + str(time.time()) + '.key')
    key = Fernet.generate_key()
    with open(keyFile, 'wb') as keyFiles:
        keyFiles.write(key)     

''' KEYGEN '''

def hash(infile):
    hashAlgo = hashlib.sha256()
    with open(infile, 'rb') as file:
        content = file.read()
        hashAlgo.update(content)
    return hashAlgo.hexdigest()

''' ENCRYPT '''

def encrypt(infile):

    with open(infile, 'rb') as file:
        original = file.read()

    base = os.path.basename(infile)
    path = os.getcwd()
    Encrypted = os.path.join(path, 'Encrypted')
    keyFiles = os.path.join(path, 'KeyStore')
    keystore = os.listdir(keyFiles)

    keyLoc = os.path.join(keyFiles, keystore[0])
    with open(keyLoc, 'rb') as keyfiles:
        key = keyfiles.read()

    encrypted = Fernet(key).encrypt(original)

    format = []
    index = base.index('.')
    for chars in range(len(base) - (index)):
        format.append(base[-chars -1])    
    format.reverse()
    fileFormat = "".join(str(x) for x in format)
    CID = str(hash(infile).encode()) + fileFormat
    CIDOUT = os.path.join(Encrypted, CID)

    with open(CIDOUT, 'wb') as encryptedFile:
        encryptedFile.write(encrypted)

    print("ENCRYPTED. GREAT SUCCESS!")

''' DECRYPT '''

def decrypt(file):

    path = os.getcwd()
    keyFiles = os.path.join(path, 'KeyStore')
    keystore = os.listdir(keyFiles)

    # CID = os.path.join(path, 'CID', base) + ".txt"
    # if not os.path.exists(CID):
    #     print("Hash For File Doesn't Exist")
    # elif open(CID).read() == hash(file):
    #     print("File Hash Matches ")
    # else:
    #     print("File Hash Doesn't Match")

    with open(file, 'rb') as enc_file:
        encrypted = enc_file.read()

    for keys in keystore:
        f = os.path.join(keyFiles, keys)

        with open(f, 'rb') as keyFiles:
            key = keyFiles.read()
        
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted)

    with open(file, 'wb') as dec_file:
        dec_file.write(decrypted)

    print("Decrypted Successfully. VERY NIIICE!")

''' OPEN '''

def openFile():
    file = askopenfile(parent=root, mode="r", title="Choose a File", filetypes=[('Files', '*')])
    if file:
        encrypt(file.name)

def openFolder():
    path = os.getcwd()
    archive = askdirectory(title="Choose a Folder",)
    if archive:
        base = os.path.basename(archive)
        shutil.make_archive(base, 'zip', archive)
        archiveLoc = os.path.join(path, base + '.zip')
        print("Archive Created. WOWOWEEWAH")
        encrypt(archiveLoc)

def openEncryptedFile():
    file = askopenfile(parent=root, mode="r", title="Choose a File", filetypes=[('Files', '*')])
    if file:
        decrypt(file.name)

''' --- ''' 

def setup():
    path = os.getcwd()
    KeyStore = os.path.join(path, 'KeyStore')
    Encrypted = os.path.join(path, 'Encrypted')
    # CID = os.path.join(path, 'CID')
    if not os.path.exists(KeyStore):
        os.mkdir(KeyStore)
        keygen()
    elif os.path.exists(KeyStore) and len(os.listdir(KeyStore)) == 0:
        keygen()
        print("SSSSSs")
    if not os.path.exists(Encrypted):
        os.mkdir(Encrypted)
    
    # if not os.path.exists(CID):
    #     os.mkdir(CID)

setup()

root.mainloop()

