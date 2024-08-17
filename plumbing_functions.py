from hashlib import sha1
import zlib
import json
import jsonschema
import argparse
import os

treeschema = {
    "name": "string",
    "id": 'string'
}

def addcommit(rArgs):
    p = argparse.ArgumentParser()
    p.add_argument('tree', type=str)
    p.add_argument('-p','--parent', type=str, required=False)
    p.add_argument('email', type=str)
    args = p.parse_args(rArgs)

    content = json.dumps({'tree': args.tree, 'parent': args.parent, 'author': args.email})
        
    header = f"Commit {len(content.encode())}"
    storage = f"{header}\0{content}".encode()
    shaid = sha1(storage).hexdigest()
    compresStorage = zlib.compress(storage)
    
    os.chdir('./.tofu/objects')
    os.mkdir(f'./{shaid[0:2]}')
    os.chdir(f'./{shaid[0:2]}')
    
    with open(shaid[2:40], 'wb') as f:
        f.write(compresStorage)
    print(shaid)

def addtree(rArgs):
    p = argparse.ArgumentParser()
    p.add_argument('ids', type=str)
    args = p.parse_args(rArgs)

    try:
        for obj in json.loads(args.ids):
            if not isinstance(obj, dict): raise jsonschema.ValidationError('A one object not is dicionary')
            jsonschema.validate(instance=obj, schema=treeschema)
        content = json.dumps(json.loads(args.ids), indent=4)
    except json.decoder.JSONDecodeError as e:
        print(e)
        exit(1)
    except jsonschema.ValidationError as e:
        print(e)
        exit(1)
        
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
