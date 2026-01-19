# LVGL MicroPython v8 for ESP32-S3 with ulab

This repository provides a customized build of MicroPython with LVGL (Light and Versatile Graphics Library) version 8 and ulab (numpy-like array manipulation) specifically configured for ESP32-S3 microcontrollers.

## Features

- **MicroPython**: Python 3 implementation for microcontrollers
- **LVGL v8**: Graphics library for creating embedded GUIs
- **ulab**: Numpy-like fast vector operations for MicroPython
- **ESP32-S3 Optimized**: Configured for ESP32-S3 with SPIRAM support
- **Hardware Acceleration**: Optimized for ESP32-S3's display and touch interfaces

## Hardware Requirements

- ESP32-S3 development board
- Minimum 4MB Flash (8MB or more recommended)
- PSRAM/SPIRAM (highly recommended for LVGL framebuffers)
- Optional: Display module (I2C, SPI, or parallel RGB)
- Optional: Touch controller

## Quick Start

### Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt-get install -y git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
```

**macOS:**
```bash
brew install cmake ninja dfu-util
```

### Building the Firmware

1. **Clone the repository:**
```bash
git clone --recursive https://github.com/Austrust/lvgl_micropython_v8_esp32_s3-ulab.git
cd lvgl_micropython_v8_esp32_s3-ulab
```

2. **Initialize submodules (if not cloned with --recursive):**
```bash
git submodule update --init --recursive
```

3. **Build for ESP32-S3:**
```bash
make ESP32_S3
```

4. **Flash to device:**
```bash
make deploy PORT=/dev/ttyUSB0
```

## ESP32-S3 Variants

This project supports various ESP32-S3 configurations:

- **ESP32-S3 Generic**: Basic configuration
- **ESP32-S3 with SPIRAM**: Extended memory support (default)
- **ESP32-S3 with SPIRAM_OCT**: Octal SPIRAM for maximum performance

### Building for specific variants:

```bash
# Generic S3 (4MB Flash, no PSRAM)
make ESP32_S3

# S3 with SPIRAM (8MB Flash, 8MB PSRAM) - Recommended
make ESP32_S3_SPIRAM

# S3 with Octal SPIRAM (highest performance)
make ESP32_S3_SPIRAM_OCT
```

## Configuration

### Display Configuration

The build includes support for common display controllers:
- ST7789
- ILI9341
- ST7735
- And others...

### Touch Input Configuration

Supported touch controllers:
- FT6x36
- GT911
- XPT2046
- CST816S

## Usage Examples

### Basic LVGL Example

```python
import lvgl as lv
import lcd_bus

# Initialize display
# ... (display initialization code)

# Create a simple button
btn = lv.btn(lv.scr_act())
btn.center()
label = lv.label(btn)
label.set_text("Hello ESP32-S3!")
```

### ulab Array Operations

```python
from ulab import numpy as np

# Create arrays
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

# Fast numerical operations
c = a + b
print(c)  # [6, 8, 10, 12]

# Mathematical functions
sine_wave = np.sin(np.linspace(0, 2*np.pi, 100))
```

## Project Structure

```
.
├── lib/
│   ├── micropython/     # MicroPython submodule
│   ├── lvgl/           # LVGL library submodule
│   ├── lv_bindings/    # LVGL MicroPython bindings
│   ├── ulab/           # ulab submodule
│   └── pycparser/      # Python C parser for bindings
├── boards/
│   └── ESP32_S3/       # ESP32-S3 board definitions
├── modules/            # Custom MicroPython modules
├── examples/           # Example scripts
├── Makefile            # Build system
└── README.md           # This file
```

## Building Custom Configurations

You can customize the build by modifying:
- `boards/ESP32_S3/mpconfigboard.h` - Board-specific config
- `boards/ESP32_S3/mpconfigboard.cmake` - Build configuration
- `boards/ESP32_S3/sdkconfig.board` - ESP-IDF SDK configuration

## Flashing

### Using esptool.py

```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0x0 firmware.bin
```

### Using idf.py (if ESP-IDF is installed)

```bash
idf.py -p /dev/ttyUSB0 flash
```

## Troubleshooting

### Build Errors

- Ensure all submodules are initialized: `git submodule update --init --recursive`
- Clean build: `make clean` then rebuild
- Check ESP-IDF version compatibility

### Flash Errors

- Check USB cable and connection
- Try lower baud rate: `esptool.py ... --baud 115200 ...`
- Verify correct port with `ls /dev/tty*`

### Memory Issues

- Enable PSRAM in configuration
- Reduce LVGL buffer sizes
- Use smaller display resolutions

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project combines multiple components with different licenses:
- MicroPython: MIT License
- LVGL: MIT License
- ulab: MIT License
- ESP-IDF: Apache License 2.0

See individual component directories for specific license information.

## Resources

- [MicroPython Documentation](https://docs.micropython.org/)
- [LVGL Documentation](https://docs.lvgl.io/)
- [ulab Documentation](https://micropython-ulab.readthedocs.io/)
- [ESP32-S3 Technical Reference](https://www.espressif.com/en/products/socs/esp32-s3)

## Credits

Based on:
- [lv_micropython](https://github.com/lvgl/lv_micropython)
- [micropython-ulab](https://github.com/v923z/micropython-ulab)
- [ESP-IDF](https://github.com/espressif/esp-idf)

## Support

For issues and questions:
- GitHub Issues: [Report bugs or request features](https://github.com/Austrust/lvgl_micropython_v8_esp32_s3-ulab/issues)
- LVGL Forum: [https://forum.lvgl.io/](https://forum.lvgl.io/)
- MicroPython Forum: [https://forum.micropython.org/](https://forum.micropython.org/)