# Examples

This directory contains example scripts demonstrating various features of LVGL MicroPython v8 with ulab on ESP32-S3.

## Available Examples

### 1. lvgl_basic.py

**Basic LVGL Display and Touch Example**

Demonstrates:
- SPI display initialization (ST7789/ILI9341)
- Touch controller setup (I2C FT6x36)
- Creating simple LVGL widgets (labels, sliders, buttons)
- Event handling

Hardware needed:
- ESP32-S3 board
- SPI display
- I2C touch controller (optional)

**Usage:**
```python
# Upload to ESP32-S3
import lvgl_basic
lvgl_basic.main()
```

### 2. ulab_demo.py

**ulab Numerical Computing Demonstration**

Demonstrates:
- Array creation and manipulation
- Mathematical functions (sin, cos, exp, log)
- Signal processing
- Matrix operations
- Performance comparison with pure Python

Hardware needed:
- ESP32-S3 board (no display required)

**Usage:**
```python
# Upload and run
import ulab_demo
ulab_demo.main()
```

Expected output:
```
=== Basic Array Operations ===
Array a: array([1, 2, 3, 4, 5], dtype=int8)
...
ulab: 15ms
Python: 245ms
Speedup: 16.3x faster
```

### 3. lvgl_ulab_combined.py

**Combined LVGL + ulab Example**

Demonstrates:
- Real-time data visualization
- Using ulab for calculations
- LVGL charts and graphs
- Animation with data processing

Hardware needed:
- ESP32-S3 board
- Display (any supported)

**Usage:**
```python
# After setting up display
import lvgl_ulab_combined
lvgl_ulab_combined.main()
```

## Pin Configuration

All examples use these default pins (modify as needed):

### Display (SPI)
```python
MOSI = 11
MISO = 13
SCK = 12
CS = 10
DC = 0
RST = 4
BL = 45
```

### Touch (I2C)
```python
SCL = 5
SDA = 6
```

## Customization

### Changing Pins

Edit the constants at the top of each file:

```python
# In lvgl_basic.py
_MOSI = const(11)  # Change to your pin
_DC = const(0)     # Change to your pin
# ... etc
```

### Changing Display Driver

Replace the import and driver class:

```python
# Change from ST7789 to ILI9341
import ili9341

display = ili9341.ILI9341(
    # ... same parameters ...
)
```

### Adjusting Buffer Size

For different display resolutions:

```python
# Calculate for your display
# width x height x 2 (RGB565) / 10 (10% of screen)
_WIDTH = const(480)
_HEIGHT = const(320)
_BUFFER_SIZE = const(30720)  # 480*320*2/10
```

## Running Examples

### Method 1: REPL (Interactive)

1. Connect to ESP32-S3:
   ```bash
   screen /dev/ttyUSB0 115200
   # or
   python3 -m serial.tools.miniterm /dev/ttyUSB0 115200
   ```

2. Upload file:
   ```bash
   # Using mpremote
   mpremote cp lvgl_basic.py :

   # Using ampy
   ampy --port /dev/ttyUSB0 put lvgl_basic.py
   ```

3. Run:
   ```python
   >>> import lvgl_basic
   >>> lvgl_basic.main()
   ```

### Method 2: Boot Script

Rename to `main.py` to run automatically:

```bash
mpremote cp lvgl_basic.py :main.py
mpremote reset
```

### Method 3: Include in Firmware

Add to frozen modules (advanced):

1. Copy to MicroPython frozen directory
2. Rebuild firmware
3. Flash to device

## Troubleshooting Examples

### Import Errors

```python
ImportError: no module named 'st7789'
```

**Solution:** The display driver module must be included in the firmware build. Check your build configuration.

### Memory Errors

```python
MemoryError: memory allocation failed
```

**Solutions:**
- Use ESP32-S3 with PSRAM
- Reduce buffer size
- Use partial screen updates

### Display Issues

**Blank screen:**
- Check pin connections
- Verify power supply
- Try lower SPI frequency
- Check backlight pin

**Wrong colors:**
- Adjust `color_byte_order` parameter
- Try `rgb565_byte_swap=True`

**Flicker:**
- Use double buffering
- Increase SPI frequency
- Ensure DMA is enabled

### Touch Not Working

- Verify I2C address (common: 0x38, 0x5D)
- Check pull-up resistors on SCL/SDA
- Test with I2C scanner
- Verify touch controller driver

## Creating Your Own Examples

Use this template:

```python
"""
Your Example Name

Description of what this demonstrates.

Hardware:
- List required components

Pins:
- List pin assignments
"""

import lvgl as lv
from ulab import numpy as np

def setup():
    """Initialize hardware"""
    pass

def create_ui():
    """Create user interface"""
    pass

def main():
    """Main entry point"""
    setup()
    create_ui()
    print("Example running!")

if __name__ == "__main__":
    main()
```

## Example Videos and Screenshots

(Add screenshots of examples running on hardware to help users verify correct operation)

## Contributing Examples

We welcome new examples! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

Good examples to contribute:
- Specific hardware configurations
- Different display types
- Sensor integrations
- Data visualization techniques
- Real-world applications

## Support

If you have issues with examples:
1. Check pin configurations
2. Verify hardware connections
3. Review error messages
4. Check [Issues](https://github.com/Austrust/lvgl_micropython_v8_esp32_s3-ulab/issues)
5. Ask for help with detailed information

## License

All examples are provided under the MIT License. See [LICENSE](../LICENSE) for details.
