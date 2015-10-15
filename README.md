Michael Daly/Mc Andrew #19665f8aea13911e4746d7527c5e69121f7154c9907b0aabc27640dd03b5e91b
Lab 2: Multithreaded Socket Server
==========

A multithreaded server in Python with a simple thread pool. The main thread accepts connections off a socket and if the connection queue isn't full the connection is added to the queue for one of the worker threads to process.

The server currently responds to the messages "HELO\n" and "KILL_SERVICE\n".

To run the server you must use two command line parameters - port number and max number of worker threads.

The client is currently set to attempt connection on port 8080 and to send the message "KILL_SERVICE\n"



