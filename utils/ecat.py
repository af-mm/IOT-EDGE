import argparse

args = argparse.ArgumentParser(description='Escaping concatenating')
args.add_argument('files', help='file names', nargs='+')
args = args.parse_args()

for fileName in args.files:
    f = open(fileName, 'r')
    
    for line in f:
        for ch in line:
            if ch == '\n':
                print('\\n', end='')
            elif ch == '\r':
                print('\\r', end='')
            elif ch == '\t':
                print('\\t', end='')
            elif ch == '\'':
                print('\\\'', end='')
            elif ch == '\0':
                pass
            else:
                print(ch, end='')
    
    f.close()

