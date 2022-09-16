from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('size')
parser.add_argument('path')
args = parser.parse_args()._get_kwargs()
size:int = args[0][1]
path:str = args[1][1]
with open(path, "wb") as out:
    out.seek(size-1)
    out.write(b'\x00')
