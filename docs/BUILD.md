# Build Guide for ESP32-S3

This guide provides detailed instructions for building LVGL MicroPython v8 with ulab support for ESP32-S3.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Build](#quick-build)
3. [Build Variants](#build-variants)
4. [Advanced Configuration](#advanced-configuration)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Linux** (Ubuntu 20.04+ recommended) or **macOS** (10.15+)
- At least 4GB RAM
- 10GB free disk space
- Internet connection for downloading dependencies

### Required Tools

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    git wget flex bison gperf \
    python3 python3-pip python3-venv \
    cmake ninja-build ccache \
    libffi-dev libssl-dev dfu-util \
    libusb-1.0-0
```

**macOS:**
```bash
xcode-select --install
brew install cmake ninja dfu-util
```

### Python Dependencies

ESP-IDF requires Python 3.8 or newer:
```bash
python3 --version  # Should be 3.8+
```

## Quick Build

### Method 1: Using build.py (Recommended)

1. **Clone the repository:**
```bash
git clone --recursive https://github.com/Austrust/lvgl_micropython_v8_esp32_s3-ulab.git
cd lvgl_micropython_v8_esp32_s3-ulab
```

2. **Build firmware:**
```bash
python3 build.py
```

This will:
- Check prerequisites
- Initialize submodules (if needed)
- Build for ESP32-S3 with SPIRAM (recommended)

3. **Flash to device:**
```bash
python3 build.py --flash --port /dev/ttyUSB0
```

### Method 2: Using Makefile

1. **Clone and initialize:**
```bash
git clone --recursive https://github.com/Austrust/lvgl_micropython_v8_esp32_s3-ulab.git
cd lvgl_micropython_v8_esp32_s3-ulab
make submodules
```

2. **Build:**
```bash
make ESP32_S3_SPIRAM
```

3. **Flash:**
```bash
make deploy PORT=/dev/ttyUSB0
```

## Build Variants

The project supports three ESP32-S3 variants:

### 1. Generic ESP32-S3 (No PSRAM)

For boards without external PSRAM (limited LVGL capabilities):

```bash
# Using build.py
python3 build.py --variant generic

# Using Makefile
make ESP32_S3
```

**Limitations:**
- Small framebuffers only
- Limited widget complexity
- Suitable for simple displays only

### 2. ESP32-S3 with SPIRAM (Recommended)

For boards with standard PSRAM (most common):

```bash
# Using build.py
python3 build.py --variant spiram

# Using Makefile
make ESP32_S3_SPIRAM
```

**Recommended for:**
- Most ESP32-S3 development boards
- Good balance of performance and compatibility
- Sufficient for most LVGL applications

### 3. ESP32-S3 with Octal SPIRAM

For boards with high-performance octal PSRAM:

```bash
# Using build.py
python3 build.py --variant oct

# Using Makefile
make ESP32_S3_SPIRAM_OCT
```

**Best for:**
- High-resolution displays (800x480+)
- Complex UI with many widgets
- Real-time data visualization

## Advanced Configuration

### Custom Board Definition

To create a custom board configuration:

1. Create board directory:
```bash
mkdir -p boards/MY_CUSTOM_BOARD
```

2. Create configuration files:
   - `mpconfigboard.h` - Board-specific defines
   - `mpconfigboard.cmake` - CMake configuration
   - `sdkconfig.board` - ESP-IDF configuration

3. Build with custom board:
```bash
cd lib/micropython/ports/esp32
make BOARD=MY_CUSTOM_BOARD
```

### Enabling Additional Modules

Edit `modules/micropython.cmake` to add more modules:

```cmake
# Example: Add custom module
set(MY_MODULE_DIR ${CMAKE_CURRENT_LIST_DIR}/../my_module)
if(EXISTS ${MY_MODULE_DIR}/micropython.cmake)
    include(${MY_MODULE_DIR}/micropython.cmake)
endif()
```

### Optimizing for Size

If flash space is limited:

```bash
cd lib/micropython/ports/esp32
make BOARD=ESP32_GENERIC_S3 \
     BOARD_VARIANT=SPIRAM \
     CFLAGS_EXTRA="-Os -DNDEBUG"
```

### Optimizing for Performance

For maximum performance:

```bash
make BOARD=ESP32_GENERIC_S3 \
     BOARD_VARIANT=SPIRAM_OCT \
     CFLAGS_EXTRA="-O3 -DNDEBUG"
```

## Build Output

After a successful build, you'll find:

```
lib/micropython/ports/esp32/build-ESP32_GENERIC_S3-SPIRAM/
├── firmware.bin          # Main firmware (flash to 0x0)
├── bootloader/
│   └── bootloader.bin   # Bootloader
├── partition_table/
│   └── partition-table.bin
└── firmware.elf         # ELF file for debugging
```

### Firmware Size

Typical firmware sizes:

- **Generic**: ~1.5 MB
- **With LVGL**: ~2.0 MB
- **With LVGL + ulab**: ~2.3 MB
- **Full build**: ~2.5 MB

## Flashing Methods

### Method 1: Using build.py

```bash
python3 build.py --flash --port /dev/ttyUSB0 --baud 460800
```

### Method 2: Using Makefile

```bash
make deploy PORT=/dev/ttyUSB0 BAUD=460800
```

### Method 3: Using esptool.py directly

```bash
esptool.py --chip esp32s3 \
    --port /dev/ttyUSB0 \
    --baud 460800 \
    write_flash -z 0x0 \
    lib/micropython/ports/esp32/build-ESP32_GENERIC_S3-SPIRAM/firmware.bin
```

### Erase Flash (if needed)

```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
```

## Troubleshooting

### Build Issues

#### "Submodules not initialized"

```bash
git submodule update --init --recursive
```

#### "ESP-IDF not found"

MicroPython includes ESP-IDF automatically. If you see this error:
```bash
cd lib/micropython/ports/esp32
make clean
make BOARD=ESP32_GENERIC_S3
```

#### "Out of memory during build"

Reduce parallel jobs:
```bash
make -j1 BOARD=ESP32_GENERIC_S3
```

Or add swap space:
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### "Permission denied on /dev/ttyUSB0"

Add yourself to the dialout group:
```bash
sudo usermod -a -G dialout $USER
# Log out and back in
```

Or use sudo:
```bash
sudo python3 build.py --flash --port /dev/ttyUSB0
```

### Flash Issues

#### "Failed to connect"

1. Check cable connection
2. Press and hold BOOT button while connecting
3. Try lower baud rate:
   ```bash
   python3 build.py --flash --port /dev/ttyUSB0 --baud 115200
   ```

#### "Wrong chip type"

Make sure you're using ESP32-S3 (not ESP32 or ESP32-C3):
```bash
esptool.py --port /dev/ttyUSB0 chip_id
```

#### "Hash mismatch"

Erase flash and reflash:
```bash
make erase PORT=/dev/ttyUSB0
make deploy PORT=/dev/ttyUSB0
```

### Runtime Issues

#### "MemoryError"

- Use variant with PSRAM
- Reduce framebuffer size
- Limit widget complexity

#### "Display not working"

- Check pin connections
- Verify display driver in code
- Test with simple example first

#### "Import error for lvgl or ulab"

Check modules are built-in:
```python
import sys
print(sys.modules)
```

Should show 'lvgl' and 'ulab' as frozen modules.

## Performance Optimization

### Compiler Flags

Edit `boards/ESP32_S3/mpconfigboard.cmake`:

```cmake
# For size
set(IDF_TARGET_COMPILE_OPTIONS "-Os")

# For speed
set(IDF_TARGET_COMPILE_OPTIONS "-O3")

# For debugging
set(IDF_TARGET_COMPILE_OPTIONS "-Og -g")
```

### CPU Frequency

Set ESP32-S3 to maximum frequency (240MHz):

In `sdkconfig.board`:
```
CONFIG_ESP32S3_DEFAULT_CPU_FREQ_240=y
```

### PSRAM Configuration

For best LVGL performance:
```
CONFIG_SPIRAM_MODE_OCT=y
CONFIG_SPIRAM_SPEED_80M=y
```

## Next Steps

After successful build:

1. **Test basic functionality**: Upload `examples/ulab_demo.py`
2. **Initialize display**: Use `examples/lvgl_basic.py` as template
3. **Build your application**: Combine LVGL and ulab for powerful UIs

## Support

- **Documentation**: See `/docs` directory
- **Examples**: See `/examples` directory
- **Issues**: https://github.com/Austrust/lvgl_micropython_v8_esp32_s3-ulab/issues
