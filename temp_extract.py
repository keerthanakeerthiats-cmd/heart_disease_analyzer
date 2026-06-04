import zipfile, os
p = 'ngrok_v3.zip'
print('exists', os.path.exists(p))
if not os.path.exists(p):
    raise SystemExit(1)
print('size', os.path.getsize(p))
with zipfile.ZipFile(p, 'r') as z:
    print('entries', z.namelist())
    os.makedirs('ngrok_v3', exist_ok=True)
    z.extractall('ngrok_v3')
    print('extracted', os.listdir('ngrok_v3'))
