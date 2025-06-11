# Makefile for compiling the C library

# Compiler settings
CC = gcc
CFLAGS = -Wall -fPIC

# Directories
SRC_DIR = src
BUILD_DIR = build

# Target library name
TARGET = $(BUILD_DIR)/libmessage.so

# Source files
SRC = $(SRC_DIR)/message.c

all: $(TARGET)

$(TARGET): $(SRC) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -shared -o $@ $^

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all clean