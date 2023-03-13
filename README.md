# INF142 - Oblig 1

## Purpose

The purpose of this program is to have a central server (server.py) 
acts as a relay between several clients (client.py). The server is also responsible
for assigning roles to the clients (advisee or advisor), and for keeping track of
the questions and answers that are sent between the clients.

## How to run
### Serve
* To run the server, simply run the server.py file in a console.   
* The server will then start.
* The server will listen for incoming connections on port 42694.  
* For every new connection made to the server, the server will create a new thread,  
making it possible for multiple clients to connect to the server at the same time.

### Client
* To run the client, simply run the client.py file in a console.  
* The client will then start.
* The client will connect to the server on port 42694.  
* The server assigns the client a role (advisee or advisor) when the client connects.  
* The client will then be able to send and receive messages from the server.  
* If you are an advisee you ask questions and if you are an advisor you answer questions.

## Short breakdown of the code
### Server

* Initiates a socket and binds it to localhost on port 42694.
* The socket is IPv4 and TCP.
* Listens for incoming connections.
* When a new connection is made, the server creates a new thread for the client.
* The server assigns the client a role (advisee or advisor).
* The server keeps track of advisees, advisors, questions and busy advisors. 
This is done by using dictionaries and lists.
* Questions from adivsees are added to a dictionary with the question as the key, and the
advisor as the value.
* When an advisor is busy, the advisor is added to a list of busy advisors.
Thus the server knows which advisors are available to answer questions.
* The server prints everything that is going on to the server console.
This is done both for debugging and for the user to see what is going on.

### Client
* Initiates a socket and connects to localhost: port 42694.
* The socket is IPv4 and TCP.
* The client connects to the server.
* The client is assigned a role (advisee or advisor) by the server.
* Depending on the role given by the server the client will either ask questions or answer questions.
* An advisee can ask questions until he chooses to quit by typing "exit".
* An advisor can answer questions until he chooses to quit by typing "exit".
