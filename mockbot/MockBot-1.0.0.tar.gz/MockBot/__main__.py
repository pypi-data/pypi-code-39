#!/usr/bin/python3
# 2019-7-7

from MockBot.server import server

def main():
    server.run(
        host='0.0.0.0', 
        port=5050
    )

if __name__ == "__main__":
    main()