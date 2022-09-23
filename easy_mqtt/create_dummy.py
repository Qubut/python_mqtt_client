import click
import logging


@click.command()
@click.option("--path","-p", default="./resources/DUMMYFILE", type=str, help="path of the file")
@click.option("--size","-s", default=1024*1024, type=int, help="size of the file to be created")
def main(path: str, size: int):
    try:
        with open(path, "wb") as out:
            out.seek(size-1)
            out.write(b'\x00')
    except FileNotFoundError as e:
        logging.error(e)        

if __name__ == "__main__":
    main()
