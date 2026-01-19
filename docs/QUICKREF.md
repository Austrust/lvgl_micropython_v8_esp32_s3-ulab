# Quick Reference Guide

Fast reference for common tasks with LVGL MicroPython v8 ESP32-S3 with ulab.

## Building

```bash
# Quick build (SPIRAM variant)
make ESP32_S3_SPIRAM

# Build and flash
python3 build.py --flash --port /dev/ttyUSB0

# Clean build
make clean
python3 build.py --clean
```

## Common Display Setups

### SPI Display (ST7789/ILI9341)

```python
import lcd_bus, st7789, lvgl as lv, machine

spi_bus = machine.SPI.Bus(host=1, mosi=11, miso=13, sck=12)
display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=40000000, dc=0, cs=10)
fb1 = display_bus.allocate_framebuffer(32000, lcd_bus.MEMORY_INTERNAL)

lv.init()
display = st7789.ST7789(
    data_bus=display_bus,
    display_width=240, display_height=320,
    frame_buffer1=fb1,
    backlight_pin=45,
    color_space=lv.COLOR_FORMAT.RGB565
)
display.init()
display.set_backlight(100)
```

### I8080 Parallel Display

```python
import lcd_bus, ili9341, lvgl as lv

display_bus = lcd_bus.I80Bus(
    dc=0, wr=47, freq=20000000,
    data0=9, data1=46, data2=3, data3=8,
    data4=18, data5=17, data6=16, data7=15
)
fb1 = display_bus.allocate_framebuffer(32000, lcd_bus.MEMORY_INTERNAL)

lv.init()
display = ili9341.ILI9341(
    data_bus=display_bus,
    display_width=240, display_height=320,
    frame_buffer1=fb1,
    backlight_pin=45,
    color_space=lv.COLOR_FORMAT.RGB565
)
display.init()
```

## Common Touch Setups

### I2C Touch (FT6x36/GT911)

```python
import i2c, ft6x36

i2c_bus = i2c.I2C.Bus(host=0, scl=5, sda=6, freq=100000)
touch_dev = i2c.I2C.Device(
    bus=i2c_bus, 
    dev_id=ft6x36.I2C_ADDR,
    reg_bits=ft6x36.BITS
)
touch = ft6x36.FT6x36(touch_dev)
```

### SPI Touch (XPT2046)

```python
import machine, xpt2046

# Reuse SPI bus from display
touch_dev = machine.SPI.Device(
    spi_bus=spi_bus,
    freq=2000000,
    cs=18
)
touch = xpt2046.XPT2046(touch_dev)
```

## Basic LVGL Widgets

### Label

```python
label = lv.label(lv.scr_act())
label.set_text("Hello World")
label.align(lv.ALIGN.CENTER, 0, 0)
label.set_style_text_color(lv.color_hex(0xFF0000), 0)  # Red
```

### Button

```python
btn = lv.btn(lv.scr_act())
btn.set_size(120, 50)
btn.center()

btn_label = lv.label(btn)
btn_label.set_text("Click")
btn_label.center()

def btn_clicked(e):
    print("Button clicked!")

btn.add_event_cb(btn_clicked, lv.EVENT.CLICKED, None)
```

### Slider

```python
slider = lv.slider(lv.scr_act())
slider.set_size(200, 20)
slider.center()
slider.set_value(50, lv.ANIM.OFF)

def slider_changed(e):
    value = slider.get_value()
    print(f"Value: {value}")

slider.add_event_cb(slider_changed, lv.EVENT.VALUE_CHANGED, None)
```

### Text Area

```python
ta = lv.textarea(lv.scr_act())
ta.set_size(200, 100)
ta.center()
ta.set_placeholder_text("Enter text...")
```

## Common ulab Operations

### Array Creation

```python
from ulab import numpy as np

a = np.array([1, 2, 3, 4])
b = np.zeros(10)
c = np.ones(5)
d = np.linspace(0, 10, 100)  # 100 points from 0 to 10
e = np.arange(0, 10, 0.5)    # 0 to 10, step 0.5
```

### Math Operations

```python
# Element-wise
result = a + b
result = a * 2
result = a ** 2

# Trigonometric
sin_vals = np.sin(a)
cos_vals = np.cos(a)

# Exponential/Log
exp_vals = np.exp(a)
log_vals = np.log(a)
```

### Aggregation

```python
total = np.sum(a)
average = np.mean(a)
maximum = np.max(a)
minimum = np.min(a)
std_dev = np.std(a)
```

### Matrix Operations

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

C = np.dot(A, B)  # Matrix multiplication
A_T = A.T         # Transpose
```

## Task Handler

Required for LVGL to process events:

```python
import task_handler
th = task_handler.TaskHandler()
# Now LVGL will handle events automatically
```

## Memory Management

### Check Available Memory

```python
import gc
gc.collect()
print(f"Free: {gc.mem_free()} bytes")
print(f"Used: {gc.mem_alloc()} bytes")
```

### Check PSRAM

```python
import esp32
if esp32.spiram_available():
    print(f"PSRAM: {esp32.spiram_size()} bytes")
```

### Framebuffer Allocation

```python
# Internal RAM (fast, limited)
fb = display_bus.allocate_framebuffer(
    32000,
    lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA
)

# PSRAM (large, slightly slower)
fb = display_bus.allocate_framebuffer(
    153600,
    lcd_bus.MEMORY_SPIRAM
)
```

## Display Settings

### Rotation

```python
display.set_rotation(lv.DISPLAY_ROTATION._0)    # 0°
display.set_rotation(lv.DISPLAY_ROTATION._90)   # 90°
display.set_rotation(lv.DISPLAY_ROTATION._180)  # 180°
display.set_rotation(lv.DISPLAY_ROTATION._270)  # 270°
```

### Backlight

```python
display.set_backlight(100)  # 100% brightness
display.set_backlight(50)   # 50% brightness
display.set_backlight(0)    # Off
```

### Colors

```python
display.invert_colors()  # Invert display colors
```

## Common Patterns

### Timer Callback

```python
def timer_callback(timer):
    print("Timer fired!")

timer = lv.timer_create(timer_callback, 1000, None)  # Every 1000ms
```

### Screen Switching

```python
# Create new screen
screen2 = lv.obj()

# Switch to it
lv.scr_load(screen2)

# Or with animation
lv.scr_load_anim(screen2, lv.SCR_LOAD_ANIM.MOVE_LEFT, 500, 0, False)
```

### Custom Styles

```python
style = lv.style_t()
style.init()
style.set_bg_color(lv.color_hex(0x0000FF))
style.set_border_width(2)
style.set_border_color(lv.color_hex(0xFF0000))
style.set_radius(10)

obj = lv.obj(lv.scr_act())
obj.add_style(style, 0)
```

## Debugging

### Enable Debug Output

```python
# MicroPython debug
import esp
esp.osdebug(None)  # Disable
esp.osdebug(0)     # Enable errors
esp.osdebug(2)     # Enable verbose
```

### Exception Handling

```python
try:
    # Your code
    pass
except Exception as e:
    import sys
    sys.print_exception(e)
```

### Serial Monitoring

```bash
# Linux/Mac
screen /dev/ttyUSB0 115200

# Python
python3 -m serial.tools.miniterm /dev/ttyUSB0 115200

# mpremote
mpremote
```

## File Management

### Upload Files

```bash
# Using mpremote
mpremote cp myfile.py :

# Using ampy
ampy --port /dev/ttyUSB0 put myfile.py
```

### List Files

```python
import os
print(os.listdir('/'))
```

## Performance Tips

1. **Use PSRAM variant** for better performance
2. **Allocate larger buffers** in PSRAM
3. **Use double buffering** (fb1 and fb2)
4. **Enable DMA** for SPI/I8080
5. **Use ulab** for numerical operations
6. **Minimize widget updates** - only update when needed
7. **Use frozen modules** for frequently used code

## Common Pin Assignments

| Function    | Default Pin | Alternative |
|-------------|-------------|-------------|
| SPI MOSI    | 11          | 35          |
| SPI MISO    | 13          | 37          |
| SPI SCK     | 12          | 36          |
| SPI CS      | 10          | Any         |
| Display DC  | 0           | Any         |
| Display RST | 4           | Any         |
| Backlight   | 45          | Any PWM     |
| I2C SCL     | 5           | 9           |
| I2C SDA     | 6           | 8           |

## Quick Links

- [Full Documentation](../docs/)
- [Build Guide](../docs/BUILD.md)
- [Hardware Guide](../docs/HARDWARE.md)
- [Examples](../examples/)
- [LVGL Docs](https://docs.lvgl.io/)
- [ulab Docs](https://micropython-ulab.readthedocs.io/)
