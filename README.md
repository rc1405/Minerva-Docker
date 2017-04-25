# Minerva-Docker
Docker setup to run Minerva-IDS

## Getting Started
1. Install git, docker and docker-compose
2. git clone https://github.com/rc1405/Minerva-Docker.git
3. cd Minerva-Docker
4. git clone https://github.com/rc1405/Minerva.git
5. mkdir minerva_agent minerva_server suricata
6. docker-compuse up --build

## Making Modifications
Update code in Minerva-Docker/Minerva and restart containers

## Access the GUI
Access the webconsole through https://localhost with the user admin and default password changeme

## Known Issues
Requesting PCAP through the console is not functional at this time.
