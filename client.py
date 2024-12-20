import sys
import aioconsole
import asyncio
from pathlib import Path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def asInput(r, w) :
    while True:
        lines = []
        while True:
            ZaLine = await aioconsole.ainput()
            if not ZaLine:
                break
            lines.append(ZaLine)
        line = '\n'.join(lines)
        w.write(line.encode())
        await w.drain()


async def asRecieve(r, w) :
    while True:
        data = await r.read(1024)
        if not data:
            break
        mess = data.decode()
        if "ID|" in mess:
            with open('/tmp/idServ', 'w+') as f:
                f.write(mess.split('|')[1])
        else:
            print(f"{data.decode()}")

async def main() :
    reader, writer = await asyncio.open_connection(host="10.1.1.22", port=8888)
    try:
        pseudo = input("Enter your username : ")
        id = ''
        idFile = Path('/tmp/idServ')
        if idFile.exists() :
            id = '|'
            with open('/tmp/idServ', 'r') as f:
                id += f.read()

        writer.write(('Hello|'+pseudo+id).encode())
        await writer.drain()
        tasks = [asInput(reader, writer), asRecieve(reader, writer)]
        await asyncio.gather(*tasks)
    except KeyboardInterrupt :
        print(bcolors.FAIL + "Interruption de l'application" + bcolors.ENDC)
        writer.write('&<END>')
        return

if __name__ == "__main__":
    asyncio.run(main())
    print("Connexion fermee")

sys.exit(0)