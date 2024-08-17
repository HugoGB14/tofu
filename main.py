import argparse
import os
import plumbing_functions as plumbFuncs

def init(_):
    os.mkdir('./.tofu')
    os.chdir('./.tofu')
    os.mkdir('./objects')

cmch = {
    'init': plumbFuncs.init,
    'blob': plumbFuncs.addblob,
    'cat-file': plumbFuncs.catFile,
    'tree': plumbFuncs.addtree,
    'addcommit': plumbFuncs.addcommit
}


def main():
    ap = argparse.ArgumentParser('Tofu',description='tofu VCS')
    ap.add_argument('command', type=str, help='Action', choices=['init','blob','cat-file','tree'])
    
    args, sArgs = ap.parse_known_args()
    
    cmch.get(args.command)(sArgs)
    
if __name__ == '__main__':
    main()