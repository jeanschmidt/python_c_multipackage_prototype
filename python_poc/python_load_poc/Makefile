# Makefile for compiling the C library

# Compiler settings
CC = gcc
CFLAGS = -Wall -fPIC

# Target library name
TARGET = libmessage.so

# Source files
SRC = src/message.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -shared -o $@ $^

clean:
	rm -f $(TARGET)

.PHONY: all clean
