// Author: Domingos Bruges
//
// websocket arduino client library: https://github.com/djsb/arduino-websocketclient
//
// Copyright (c) 2013 Domingos Bruges
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE. 

#ifndef WSCLIENT_H_
#define WSCLIENT_H_

#define CRLF "\r\n" // CRLF characters to terminate lines/handshakes in headers.

#ifndef CALLBACK_FUNCTIONS
#define CALLBACK_FUNCTIONS 1 // default 5 unless specified
#endif

#define SIZE(array) (sizeof(array) / sizeof(*array))

// WebSocket protocol constants
#define WS_FIN            0x80
#define WS_OPCODE_TEXT    0x01
#define WS_OPCODE_BINARY  0x02
#define WS_OPCODE_CLOSE   0x08
#define WS_OPCODE_PING    0x09
#define WS_OPCODE_PONG    0x0a

//Mask
#define WS_MASK           0x80
#define WS_SIZE16         126
#define WS_SIZE64         127

	class WSClient {
	public:

	    bool handshake(Client &client);     // Handle connection requests to validate and process/refuse connections.
	    char* getData(); // Get data off of the stream
	    void sendData(char *str); // Write data to the stream
	    void disconnect();
	    char *path;
	    char *host;

	    void sendEncodedData(char *str);

	private:
	    Client *socket_client;
	    bool analyzeRequest();
	    void disconnectStream();    // Disconnect user gracefully.
	    int timedRead();
	};

#endif
