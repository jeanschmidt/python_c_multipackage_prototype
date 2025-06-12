# Makefile for compiling the C library

# Determine OS type
UNAME_S := $(shell uname -s)

# Compiler settings
ifeq ($(UNAME_S),Darwin)
	# macOS settings
	CC = clang
	# macOS equivalent for ignoring unresolved symbols is -undefined dynamic_lookup
	CFLAGS = -Wall -fPIC -Wl,-undefined,dynamic_lookup
else
	# Linux settings
	CC = gcc
	CFLAGS = -Wall -fPIC -Wl,--unresolved-symbols=ignore-all
endif

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
