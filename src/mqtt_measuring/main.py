from ast import parse
import imp
import subscribe
import publish
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("--publish")
    parser.add_argument("--subscribe")

if __name__=="__main__":
    main()