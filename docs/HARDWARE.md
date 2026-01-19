# Hardware Configuration Guide

This guide helps you configure the firmware for your specific ESP32-S3 hardware setup.

## Common ESP32-S3 Development Boards

### Popular Boards

1. **ESP32-S3-DevKitC-1**
   - Flash: 8MB or 16MB
   - PSRAM: 8MB Octal
   - USB: Native USB and UART
   - Recommended variant: `spiram` or `oct`

2. **ESP32-S3-DevKitM-1**
   - Flash: 8MB
   - PSRAM: None or 8MB
   - Check your specific model
   - Recommended variant: `spiram` or `generic`

3. **LilyGO T-Display-S3**
   - Flash: 16MB
   - PSRAM: 8MB Octal
   - Built-in display: ST7789 170x320
   - Recommended variant: `oct`

4. **Freenove ESP32-S3-WROOM**
   - Flash: 8MB
   - PSRAM: 8MB
   - Recommended variant: `spiram`

## Pin Assignments

### Display Interfaces

#### SPI Display (Most Common)

```python
# Example for ST7789/ILI9341
DISPLAY_PINS = {
    'MOSI': 11,   # SPI Data Out
    'MISO': 13,   # SPI Data In (optional for display-only)
    'SCK': 12,    # SPI Clock
    'CS': 10,     # Chip Select
    'DC': 0,      # Data/Command
    'RST': 4,     # Reset
    'BL': 45,     # Backlight (PWM capable)
}
```

#### I8080 Parallel Display (Faster)

```python
# 8-bit parallel interface
DISPLAY_PINS = {
    'WR': 47,     # Write
    'DC': 0,      # Data/Command
    'RST': 4,     # Reset
    'BL': 45,     # Backlight
    'DATA0': 9,
    'DATA1': 46,
    'DATA2': 3,
    'DATA3': 8,
    'DATA4': 18,
    'DATA5': 17,
    'DATA6': 16,
    'DATA7': 15,
}
```

#### RGB Parallel Display (Best Performance)

```python
# 16-bit RGB565 interface
RGB_PINS = {
    'HSYNC': 39,
    'VSYNC': 40,
    'PCLK': 41,
    'DE': 42,
    'R0': 1, 'R1': 2, 'R2': 3, 'R3': 4, 'R4': 5,
    'G0': 6, 'G1': 7, 'G2': 8, 'G3': 9, 'G4': 10, 'G5': 11,
    'B0': 12, 'B1': 13, 'B2': 14, 'B3': 15, 'B4': 16,
    'BL': 45,
}
```

### Touch Controller Interfaces

#### I2C Touch (FT6x36, GT911, CST816S)

```python
TOUCH_PINS_I2C = {
    'SCL': 5,     # I2C Clock
    'SDA': 6,     # I2C Data
    'INT': 7,     # Interrupt (optional)
    'RST': 8,     # Reset (optional)
}
```

#### SPI Touch (XPT2046)

```python
TOUCH_PINS_SPI = {
    # Shared with display SPI
    'MOSI': 11,
    'MISO': 13,
    'SCK': 12,
    'CS': 18,     # Different CS from display
    'IRQ': 19,    # Interrupt (optional)
}
```

## Display Drivers

### Supported Controllers

| Controller | Resolution     | Interface    | Color Depth | Notes                    |
|------------|----------------|--------------|-------------|--------------------------|
| ST7789     | 240x240/320    | SPI          | RGB565      | Very common, good perf   |
| ILI9341    | 240x320        | SPI/I8080    | RGB565      | Popular, well supported  |
| ST7735     | 128x160        | SPI          | RGB565      | Small displays           |
| ILI9488    | 320x480        | SPI/I8080    | RGB666      | Larger displays          |
| GC9A01     | 240x240 round  | SPI          | RGB565      | Round displays           |

### Configuration Examples

#### ST7789 (SPI)

```python
import lcd_bus
import st7789
import lvgl as lv
import machine

# SPI bus configuration
spi_bus = machine.SPI.Bus(
    host=1,
    mosi=11,
    miso=13,
    sck=12
)

# Display bus
display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    freq=40000000,  # 40MHz
    dc=0,
    cs=10,
)

# Framebuffers
fb1 = display_bus.allocate_framebuffer(32000, lcd_bus.MEMORY_INTERNAL)
fb2 = display_bus.allocate_framebuffer(32000, lcd_bus.MEMORY_INTERNAL)

# Initialize
lv.init()

# Create display
display = st7789.ST7789(
    data_bus=display_bus,
    display_width=240,
    display_height=320,
    frame_buffer1=fb1,
    frame_buffer2=fb2,
    backlight_pin=45,
    reset_pin=4,
    color_space=lv.COLOR_FORMAT.RGB565,
)

display.init()
display.set_backlight(100)
```

#### ILI9341 (I8080)

```python
import lcd_bus
import ili9341

# I8080 bus
display_bus = lcd_bus.I80Bus(
    dc=0,
    wr=47,
    freq=20000000,
    data0=9, data1=46, data2=3, data3=8,
    data4=18, data5=17, data6=16, data7=15
)

# Framebuffers in PSRAM for larger size
fb1 = display_bus.allocate_framebuffer(
    153600,  # 320x240x2
    lcd_bus.MEMORY_SPIRAM
)

lv.init()

display = ili9341.ILI9341(
    data_bus=display_bus,
    display_width=240,
    display_height=320,
    frame_buffer1=fb1,
    backlight_pin=45,
    color_space=lv.COLOR_FORMAT.RGB565,
)

display.init()
```

## Touch Controller Drivers

### I2C Touch Controllers

#### FT6x36 Configuration

```python
import i2c
import ft6x36

# I2C bus
i2c_bus = i2c.I2C.Bus(
    host=0,
    scl=5,
    sda=6,
    freq=100000
)

# Touch device
touch_dev = i2c.I2C.Device(
    bus=i2c_bus,
    dev_id=ft6x36.I2C_ADDR,
    reg_bits=ft6x36.BITS
)

# Touch driver
touch = ft6x36.FT6x36(touch_dev)

# Calibrate if needed
if not touch.is_calibrated:
    touch.calibrate()
```

#### GT911 Configuration

```python
import i2c
import gt911

i2c_bus = i2c.I2C.Bus(host=0, scl=5, sda=6, freq=400000)
touch_dev = i2c.I2C.Device(bus=i2c_bus, dev_id=gt911.I2C_ADDR)
touch = gt911.GT911(touch_dev)
```

### SPI Touch Controllers

#### XPT2046 Configuration

```python
import machine
import xpt2046

# Share SPI bus with display
spi_bus = machine.SPI.Bus(host=1, mosi=11, miso=13, sck=12)

# Touch device on same bus, different CS
touch_dev = machine.SPI.Device(
    spi_bus=spi_bus,
    freq=2000000,  # Lower freq for touch
    cs=18
)

touch = xpt2046.XPT2046(touch_dev)
```

## Memory Configuration

### Framebuffer Allocation

Choose location based on size:

```python
# Small buffers (< 32KB) - Internal RAM
fb = display_bus.allocate_framebuffer(
    32000,
    lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA
)

# Large buffers - SPIRAM
fb = display_bus.allocate_framebuffer(
    153600,  # Full screen 320x240
    lcd_bus.MEMORY_SPIRAM
)

# Optimal: Partial buffers in internal RAM
fb_size = (width * height * 2) // 10  # 10% of full screen
fb1 = display_bus.allocate_framebuffer(
    fb_size,
    lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA
)
fb2 = display_bus.allocate_framebuffer(
    fb_size,
    lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA
)
```

### PSRAM Configuration

Check PSRAM availability:

```python
import esp32

# Check PSRAM
if esp32.spiram_available():
    size = esp32.spiram_size()
    print(f"PSRAM available: {size} bytes")
else:
    print("No PSRAM detected")
```

## Power Management

### Backlight Control

```python
from machine import Pin, PWM

# Simple on/off
backlight = Pin(45, Pin.OUT)
backlight.value(1)  # On
backlight.value(0)  # Off

# PWM dimming
backlight_pwm = PWM(Pin(45), freq=1000, duty=512)  # 50%
backlight_pwm.duty(1023)  # 100% brightness
backlight_pwm.duty(256)   # 25% brightness
```

### Deep Sleep

```python
from machine import Pin, deepsleep
import esp32

# Wake on touch interrupt
touch_int = Pin(7, Pin.IN)
esp32.wake_on_ext0(touch_int, esp32.WAKEUP_ANY_HIGH)

# Enter deep sleep
print("Entering deep sleep...")
deepsleep()  # Wake on touch
```

## Testing Your Configuration

### Basic Display Test

```python
import lvgl as lv

# Should show white screen
scr = lv.scr_act()
scr.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)

# Add test label
label = lv.label(scr)
label.set_text("Display Working!")
label.center()
```

### Touch Test

```python
def touch_test():
    screen = lv.scr_act()
    
    label = lv.label(screen)
    label.set_text("Touch the screen")
    label.align(lv.ALIGN.TOP_MID, 0, 10)
    
    coord_label = lv.label(screen)
    coord_label.center()
    
    def touch_callback(e):
        indev = lv.indev_get_act()
        point = lv.point_t()
        indev.get_point(point)
        coord_label.set_text(f"X: {point.x}, Y: {point.y}")
    
    screen.add_event_cb(touch_callback, lv.EVENT.PRESSED, None)
    screen.add_event_cb(touch_callback, lv.EVENT.PRESSING, None)

import task_handler
th = task_handler.TaskHandler()
touch_test()
```

## Troubleshooting Hardware

### Display Issues

**White/Blank screen:**
- Check power (3.3V or 5V as needed)
- Verify pin connections
- Try different SPI frequency (lower)
- Check CS, DC, RST signals

**Wrong colors:**
- Adjust `color_byte_order`
- Try `rgb565_byte_swap=True/False`

**Flicker/tearing:**
- Use double buffering (fb1 and fb2)
- Increase SPI frequency
- Enable DMA

### Touch Issues

**No response:**
- Check I2C address (use I2C scanner)
- Verify pull-up resistors
- Check interrupt pin

**Inverted coordinates:**
```python
# Swap X/Y
touch.swap_xy = True

# Mirror X or Y
touch.mirror_x = True
touch.mirror_y = True
```

## Reference Schematics

See `docs/schematics/` for common hardware configurations and wiring diagrams.
