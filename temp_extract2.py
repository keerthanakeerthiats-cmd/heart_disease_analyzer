import zipfile, os
p = r'C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff\ngrok_v3.zip'
print('exists', os.path.exists(p))
print('path', p)
print('size', os.path.getsize(p))
with open(p, 'rb') as f:
    print('open ok', len(f.read(16)))
with zipfile.ZipFile(p, 'r') as z:
    print('entries', z.namelist())
    os.makedirs(r'C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff\ngrok_v3', exist_ok=True)
    z.extractall(r'C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff\ngrok_v3')
    print('extracted', os.listdir(r'C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff\ngrok_v3'))
