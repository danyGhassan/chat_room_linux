import asyncio
import random
from os import environ
global CLIENTS
CLIENTS = {}

from pprint import pprint

port = int(environ.get("CHAT_PORT"))

def generateId(lenght):
    id = ''
    while lenght > 8:
        comp = 9
        if lenght <= 9:
            comp = lenght
        id += str(hex(random.randrange(1, 10**(comp))))[2:]
        lenght -= 9
    return id


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

async def handle_client_msg(reader, writer):
    pseudo = ''
    id = ''
    while True:
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')

        if data == b'':
            break

        message = data.decode()
        
        newUsr = False

        if 'Hello|' in message and len(message.split("|")) == 2 :
            print('new user received')
            pseudo = message.split('|')[1]
            id = generateId(100)
            writer.write(("ID|"+id).encode())
            newUsr = True
        elif 'Hello|' in message and len(message.split("|")) > 2 :
            print('already existing user try to reconnect')
            pseudo = message.split('|')[1]
            id = message.split('|')[2]
            newUsr = True
        elif '&<END>' in message :
            print('Client leaving')
            for ids in CLIENTS.keys():
                CLIENTS[ids]['w'].write(f"{bcolors.OKBLUE}{CLIENTS[id]['pseudo']} {bcolors.WARNING} left the Chatroom {bcolors.ENDC}")
                await CLIENTS[ids]['w'].drain()
            CLIENTS.pop(id, None)
            break

        CLIENTS[id] = {}
        CLIENTS[id]['w'] = writer
        CLIENTS[id]['r'] = reader
        CLIENTS[id]['LastAdress'] = addr
        CLIENTS[id]['pseudo'] = pseudo

        for ids in CLIENTS.keys():
            pprint(CLIENTS)
            if newUsr:
                CLIENTS[ids]['w'].write(f"{bcolors.OKBLUE}{CLIENTS[id]['pseudo']} {bcolors.HEADER} has joined{bcolors.ENDC}".encode())
                await CLIENTS[ids]["w"].drain()
            elif ids != id:
                print(CLIENTS[id]['pseudo'] + ' Sender')
                print(CLIENTS[ids]['pseudo'] + ' Reciever')
                messList = message.split("\n")
                print(messList)
                if len(messList) > 1:
                    print("more than one")
                    CLIENTS[ids]['w'].write(f"{bcolors.OKBLUE}{CLIENTS[ids]['pseudo']} {bcolors.HEADER}:> {messList[0]}{bcolors.ENDC}".encode())
                    await CLIENTS[ids]["w"].drain()
                    spaces = " " * len(f'{pseudo}:> ')
                    for line in messList[1:]:
                        CLIENTS[ids]['w'].write(b"\n")
                        CLIENTS[ids]['w'].write(f"{spaces} {bcolors.HEADER}{line}{bcolors.ENDC}".encode())
                        await CLIENTS[ids]["w"].drain()
                else:
                    print("only one")
                    CLIENTS[ids]["w"].write(f"{bcolors.OKBLUE}{CLIENTS[ids]['pseudo']} {bcolors.HEADER}:> {messList[0]}{bcolors.ENDC}".encode())
                    await CLIENTS[ids]["w"].drain()
                CLIENTS[ids]['w'].write(b"\n")
                await CLIENTS[ids]["w"].drain()
                print(f"message {message} from {addr} to {ids}")
            else:
                print("message not sent to self")

async def main():
    server = await asyncio.start_server(handle_client_msg, '127.0.0.1', port)
    ids = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {ids}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
