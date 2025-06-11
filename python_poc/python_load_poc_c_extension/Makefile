# Makefile for compiling the C library

# Compiler settings
CC = gcc
CFLAGS = -Wall -fPIC -Wl,--unresolved-symbols=ignore-all

# Directories
SRC_DIR = src
BUILD_DIR = build

# Target library name
TARGET_LIBMESSAGE = $(BUILD_DIR)/libmessage.so
TARGET_LIBMESSAGE_INTERNAL = $(BUILD_DIR)/libmessage-internal.so

# Source files
SRC_LIBMESSAGE = $(SRC_DIR)/message.c
SRC_LIBMESSAGE_INTERNAL = $(SRC_DIR)/message_default_imp.c

all: $(TARGET_LIBMESSAGE) $(TARGET_LIBMESSAGE_INTERNAL)

$(TARGET_LIBMESSAGE): $(SRC_LIBMESSAGE) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -shared -o $@ $^

$(TARGET_LIBMESSAGE_INTERNAL): $(SRC_LIBMESSAGE_INTERNAL) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -shared -o $@ $^

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all clean
