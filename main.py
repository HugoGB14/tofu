import argparse
import os
import plumbing_functions as plumbFuncs

def init(_):
    os.mkdir('./.tofu')
    os.chdir('./.tofu')
    os.mkdir('./objects')

cmch = {
    'init': init,
    'addblob': plumbFuncs.addblob,
    'cat-file': plumbFuncs.catFile,
    'addtree': plumbFuncs.addtree,
    'addcommit': plumbFuncs.addcommit
}

def main():
    ap = argparse.ArgumentParser('Tofu',description='tofu VCS')
    ap.add_argument('command', type=str, help='Action', choices=list(cmch.keys()))
    
    args, sArgs = ap.parse_known_args()
    
    cmch.get(args.command)(sArgs)
    
if __name__ == '__main__':
    main()