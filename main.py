import argparse
import os
from hashlib import sha1
import zlib
import json

def init(_):
    os.mkdir('./.tofu')
    os.chdir('./.tofu')
    os.mkdir('./objects')

def addtree(rArgs):
    p = argparse.ArgumentParser()
    p.add_argument('ids', type=str)
    args = p.parse_args(rArgs)
    
    content = f'[{','.join(set(json.loads(args.ids)))}]'
        
    header = f"Tree {len(content.encode())}"
    storage = f"{header}\0{content}".encode()
    shaid = sha1(storage).hexdigest()
    compresStorage = zlib.compress(storage)
    
    os.chdir('./.tofu/objects')
    os.mkdir(f'./{shaid[0:2]}')
    os.chdir(f'./{shaid[0:2]}')
    
    with open(shaid[2:40], 'wb') as f:
        f.write(compresStorage)
    print(shaid)
    
def addblob(rArgs):
    p = argparse.ArgumentParser()
    p.add_argument('file', type=str)
    args = p.parse_args(rArgs)
    
    with open(args.file) as f:
        content = f.read()
        
    header = f"Blob {len(content.encode())}"
    storage = f"{header}\0{content}".encode()
    shaid = sha1(storage).hexdigest()
    compresStorage = zlib.compress(storage)
    
    os.chdir('./.tofu/objects')
    os.mkdir(f'./{shaid[0:2]}')
    os.chdir(f'./{shaid[0:2]}')
    
    with open(shaid[2:40], 'wb') as f:
        f.write(compresStorage)
    print(shaid)
        
def catFile(rArgs):
    p = argparse.ArgumentParser()
    p.add_argument('id', type=str)
    args = p.parse_args(rArgs)
    fd = os.path.join('.tofu/objects', args.id[0:2], args.id[2:40])
    
    with open(fd, 'rb') as f:
        storaged = zlib.decompress(f.read()).decode()
        header, content = storaged.split('\0')
        
    print(header, content, sep='\n')

cmch = {
    'init': init,
    'blob': addblob,
    'cat-file': catFile,
    'tree': addtree
}


def main():
    ap = argparse.ArgumentParser('Tofu',description='tofu VCS')
    ap.add_argument('command', type=str, help='Action', choices=['init','blob','cat-file','tree'])
    
    args, sArgs = ap.parse_known_args()
    
    cmch.get(args.command)(sArgs)
    
if __name__ == '__main__':
    main()