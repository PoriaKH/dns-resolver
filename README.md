# dns-resolver
A DNS server which recevies DNS requests from user and looks for the request answer in the given file. <br/>
The dns queries will be parsed based on [RFC-1035](https://datatracker.ietf.org/doc/html/rfc1035). below is the format of the DNS packet.
<img width="787" alt="image" src="https://github.com/PoriaKH/dns-resolver/assets/94684621/8da01c6c-1380-4443-944f-2e768a07faf4">

### Usage
Change the `file_address` variable. below is an example of its content.
```
192.178.24.142     www.google.com
127.0.0.1          localhost
```

The server will be listening on `localIP` ip address and `localPort` port. you can change these variables to your own server ip, port.
### Build
Use `make` to build the project. The executable file will be in the `dist` directory. <br/>
`make clean` to clean the artifacts. <br/>
