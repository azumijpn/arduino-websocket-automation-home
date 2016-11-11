// Author: Domingos Bruges
// Adapted: zasquash
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

#include "sha1.h"
#include "base64.h"
#include <Ethernet.h>
#include "WSClient.h"

// Don't allow the client to send big frames of data. This will flood the Arduinos
// memory and might even crash it.
#ifndef MAX_FRAME_LENGTH
#define MAX_FRAME_LENGTH 256
#endif

bool WSClient::handshake(Client &client) {

  socket_client = &client;

  // If there is a connected client->
  if (socket_client->connected()) {
    // Check request and look for websocket handshake
    if (analyzeRequest()) {
      return true;

    } else {
      // Might just need to break until out of socket_client loop.
      disconnectStream();
      return false;
    }
  } else {
    return false;
  }
}

bool WSClient::analyzeRequest() {
  int bite;
  bool foundupgrade = false;
  bool foundconnection = false;
  char keyStart[17] = "";
  char b64Key[25] = "";
  String key = "------------------------";
  String temp = "";
  String serverKey = "";

  randomSeed(analogRead(0));

  for (int i = 0; i < 16; ++i) {
    keyStart[i] = (char)random(1, 256);
  }

  base64_encode(b64Key, keyStart, 16);

  for (int i = 0; i < 24; ++i) {
    key[i] = b64Key[i];
  }

  socket_client->print(F("GET "));
  socket_client->print(path);
  socket_client->print(F(" HTTP/1.1\r\n"));
  socket_client->print(F("Upgrade: websocket\r\n"));
  socket_client->print(F("Connection: Upgrade\r\n"));
  socket_client->print(F("Host: "));
  socket_client->print(host);
  socket_client->print(CRLF);
  socket_client->print(F("Sec-WebSocket-Key: "));
  socket_client->print(key);
  socket_client->print(CRLF);
  socket_client->print(F("Sec-WebSocket-Version: 13\r\n"));
  socket_client->print(CRLF);

  while (socket_client->connected() && !socket_client->available()) {
    delay(100);
  }

  while ((bite = socket_client->read()) != -1) {
    temp += (char)bite;

    if ((char)bite == '\n') {
      if (!foundupgrade && temp.startsWith("Upgrade: websocket")) {
        foundupgrade = true;
      } else if (temp.startsWith("Sec-WebSocket-Accept: ")) {
        serverKey = temp.substring(22, temp.length() - 2); // Don't save last CR+LF
      }
      temp = "";
    }

    if (!socket_client->available()) {
      delay(20);
    }
  }

  key += "258EAFA5-E914-47DA-95CA-C5AB0DC85B11";
  uint8_t *hash;
  char result[21];
  char b64Result[30];

  Sha1.init();
  Sha1.print(key);
  hash = Sha1.result();

  for (int i = 0; i < 20; ++i) {
    result[i] = (char)hash[i];
  }
  result[20] = '\0';

  base64_encode(b64Result, result, 20);

  // if the keys match, good to go
  return serverKey.equals(String(b64Result));
}

void WSClient::disconnect() {
  disconnectStream();
}

void WSClient::disconnectStream() {

  Serial.println(F("Terminating socket"));

  // Should send 0x8700 to server to tell it I'm quitting here.
  socket_client->write((uint8_t) 0x87);
  socket_client->write((uint8_t) 0x00);

  socket_client->flush();
  delay(10);
  socket_client->stop();
}

char* WSClient::getData() {
  uint8_t msgtype;
  uint8_t bite; //Opcode
  unsigned int length;
  uint8_t mask[4];
  //uint8_t index;
  unsigned int i;
  bool hasMask = false;

  // char array to hold bytes sent by server to client
  // message could not exceed 256 chars. Array initialized with NULL
  char socketStr[256] = {NULL};

  if (socket_client->connected() && socket_client->available()) {

    msgtype = timedRead();
    if (!socket_client->connected()) {
      return (char*)socketStr;
    }

    length = timedRead();

    if (length > WS_SIZE64) {
      hasMask = true;
      length = length & WS_SIZE64;
    }


    if (!socket_client->connected()) {
      return (char*)socketStr;
    }

    //index = 6;

    if (length == WS_SIZE16) {
      length = timedRead() << 8;
      if (!socket_client->connected()) {
        return (char*)socketStr;
      }

      length |= timedRead();
      if (!socket_client->connected()) {
        return (char*)socketStr;
      }

    } else if (length == WS_SIZE64) {

      while (1) {
        // halt, can't handle this case
      }
    }


    if (hasMask) {
      // get the mask
      mask[0] = timedRead();
      if (!socket_client->connected()) {
        return (char*)socketStr;
      }

      mask[1] = timedRead();
      if (!socket_client->connected()) {
        return (char*)socketStr;
      }

      mask[2] = timedRead();
      if (!socket_client->connected()) {
        return (char*)socketStr;
      }

      mask[3] = timedRead();
      if (!socket_client->connected()) {
        return (char*)socketStr;
      }
    }


    if (hasMask) {
      for (i = 0; i < length; ++i) {
        socketStr[i] = (char) (timedRead() ^ mask[i % 4]);
        if (!socket_client->connected()) {
          return (char*)socketStr;
        }
      }
    } else {
      for (i = 0; i < length; ++i) {
        socketStr[i] = (char) timedRead();
        if (!socket_client->connected()) {
          return (char*)socketStr;
        }
      }
    }

  }

  return (char*)socketStr;
}

void WSClient::sendData(char *str) {
  if (socket_client->connected()) {
    sendEncodedData(str);
  }
}

int WSClient::timedRead() {
  while (!socket_client->available()) {
    delay(50);
  }

  int a = socket_client->read();
  return a;
}

void WSClient::sendEncodedData(char *str) {
  int size = strlen(str);

  // TXT Opcode
  socket_client->write(WS_OPCODE_TEXT  | WS_FIN);
  // Binary Opcode
  //socket_client->write(WS_OPCODE_BINARY | WS_FIN);

  // NOTE: no support for > 16-bit sized messages
  if (size > 125) {

    socket_client->write(WS_SIZE64); //127
    socket_client->write((uint8_t) (size >> 56) & 255);
    socket_client->write((uint8_t) (size >> 48) & 255);
    socket_client->write((uint8_t) (size >> 40) & 255);
    socket_client->write((uint8_t) (size >> 32) & 255);
    socket_client->write((uint8_t) (size >> 24) & 255);
    socket_client->write((uint8_t) (size >> 16) & 255);
    socket_client->write((uint8_t) (size >> 8) & 255);
    socket_client->write((uint8_t) (size ) & 255);

  } else {
    socket_client->write((uint8_t) size);
  }

  for (int i = 0; i < size; ++i) {
    socket_client->write(str[i]);
  }
}
