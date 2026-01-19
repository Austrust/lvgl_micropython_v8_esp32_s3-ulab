# Makefile for LVGL MicroPython v8 ESP32-S3 with ulab
# 
# This Makefile provides convenient commands for building MicroPython
# with LVGL v8 and ulab support for ESP32-S3 variants

.PHONY: help submodules ESP32_S3 ESP32_S3_SPIRAM ESP32_S3_SPIRAM_OCT clean deploy

# Default target
help:
	@echo "LVGL MicroPython v8 for ESP32-S3 with ulab - Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  submodules        - Initialize and update all git submodules"
	@echo "  ESP32_S3          - Build for ESP32-S3 (Generic)"
	@echo "  ESP32_S3_SPIRAM   - Build for ESP32-S3 with SPIRAM (Recommended)"
	@echo "  ESP32_S3_SPIRAM_OCT - Build for ESP32-S3 with Octal SPIRAM"
	@echo "  clean             - Clean build artifacts"
	@echo "  deploy            - Flash firmware to device (use PORT=/dev/ttyUSB0)"
	@echo ""
	@echo "Examples:"
	@echo "  make submodules"
	@echo "  make ESP32_S3_SPIRAM"
	@echo "  make deploy PORT=/dev/ttyUSB0"

# Variables
PORT ?= /dev/ttyUSB0
BAUD ?= 460800
BOARD_DIR = boards/ESP32_S3
MICROPYTHON_DIR = lib/micropython
BUILD_DIR = build

# Initialize and update all submodules
submodules:
	@echo "Initializing submodules..."
	git submodule update --init --recursive
	@echo "Submodules initialized successfully"

# Check if submodules are initialized
check-submodules:
	@if [ ! -f "$(MICROPYTHON_DIR)/py/py.mk" ]; then \
		echo "Error: Submodules not initialized. Run 'make submodules' first."; \
		exit 1; \
	fi

# Build for ESP32-S3 Generic
ESP32_S3: check-submodules
	@echo "Building MicroPython with LVGL v8 and ulab for ESP32-S3..."
	@echo "This will take several minutes on first build..."
	cd $(MICROPYTHON_DIR)/ports/esp32 && \
		$(MAKE) BOARD=ESP32_GENERIC_S3 \
		USER_C_MODULES=../../../../modules/micropython.cmake
	@echo "Build complete! Firmware is in $(MICROPYTHON_DIR)/ports/esp32/build-ESP32_GENERIC_S3/"

# Build for ESP32-S3 with SPIRAM (Recommended)
ESP32_S3_SPIRAM: check-submodules
	@echo "Building MicroPython with LVGL v8 and ulab for ESP32-S3 with SPIRAM..."
	@echo "This will take several minutes on first build..."
	cd $(MICROPYTHON_DIR)/ports/esp32 && \
		$(MAKE) BOARD=ESP32_GENERIC_S3 \
		BOARD_VARIANT=SPIRAM \
		USER_C_MODULES=../../../../modules/micropython.cmake
	@echo "Build complete! Firmware is in $(MICROPYTHON_DIR)/ports/esp32/build-ESP32_GENERIC_S3-SPIRAM/"

# Build for ESP32-S3 with Octal SPIRAM
ESP32_S3_SPIRAM_OCT: check-submodules
	@echo "Building MicroPython with LVGL v8 and ulab for ESP32-S3 with Octal SPIRAM..."
	@echo "This will take several minutes on first build..."
	cd $(MICROPYTHON_DIR)/ports/esp32 && \
		$(MAKE) BOARD=ESP32_GENERIC_S3 \
		BOARD_VARIANT=SPIRAM_OCT \
		USER_C_MODULES=../../../../modules/micropython.cmake
	@echo "Build complete! Firmware is in $(MICROPYTHON_DIR)/ports/esp32/build-ESP32_GENERIC_S3-SPIRAM_OCT/"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	-cd $(MICROPYTHON_DIR)/ports/esp32 && $(MAKE) clean
	-rm -rf $(BUILD_DIR)
	@echo "Clean complete"

# Flash firmware to device
deploy:
	@echo "Flashing firmware to $(PORT) at $(BAUD) baud..."
	@if [ ! -c "$(PORT)" ]; then \
		echo "Error: Device $(PORT) not found"; \
		echo "Available devices:"; \
		ls /dev/tty* | grep -i usb || echo "No USB devices found"; \
		exit 1; \
	fi
	cd $(MICROPYTHON_DIR)/ports/esp32 && \
		$(MAKE) BOARD=ESP32_GENERIC_S3 PORT=$(PORT) BAUD=$(BAUD) deploy
	@echo "Flashing complete!"

# Erase flash on device
erase:
	@echo "Erasing flash on $(PORT)..."
	esptool.py --chip esp32s3 --port $(PORT) erase_flash
	@echo "Flash erased"

# Monitor serial output
monitor:
	@echo "Monitoring $(PORT) at 115200 baud (Ctrl+] to exit)..."
	python3 -m serial.tools.miniterm $(PORT) 115200

# Full rebuild (clean + build)
rebuild: clean ESP32_S3_SPIRAM

# Show build information
info:
	@echo "Project Information:"
	@echo "  Repository: lvgl_micropython_v8_esp32_s3-ulab"
	@echo "  Target: ESP32-S3"
	@echo "  Components: MicroPython + LVGL v8 + ulab"
	@echo ""
	@echo "Submodule Status:"
	@git submodule status
