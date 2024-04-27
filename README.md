This repository is designated to use TCP sockets to create a server process that can store messages and allow them to be retrieved, and a client process that can be used to interact with the server.

## Usage

### Server
To start the server, execute the `startServer.sh` script. This script takes a port number as its only command-line parameter and attempts to start a server on that port, listening on all interfaces supported by the host system. If the server is unable to be started (perhaps because that port is already in use), the program will exit with an appropriate error message.

### Client
To interact with the server, execute the `startClient.sh` script. This script takes a host name as its first command-line parameter and a port number as its second command-line parameter. It attempts to connect to the server with the given host name and port number. If the client is unable to connect, it will exit with an appropriate error message.

### Note
Before executing the scripts, ensure that the execution rights are granted using the appropriate command (e.g., `chmod +x startServer.sh startClient.sh`).
