with open("./resources/DUMMYFILE", "wb") as out:
    out.seek((1024 * 1024) - 1)
    out.write(b'\x00')