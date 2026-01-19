"""
Basic LVGL Example for ESP32-S3

This example demonstrates:
- Display initialization with SPI interface
- Creating basic LVGL widgets
- Touch input handling

Hardware Requirements:
- ESP32-S3 board
- SPI display (e.g., ST7789, ILI9341)
- Optional: Touch controller (e.g., FT6x36)

Pin Configuration (adjust to your hardware):
- Display SPI: MOSI=11, MISO=13, SCK=12, CS=10, DC=0
- Display Control: BL=45, RST=4
- Touch I2C: SCL=5, SDA=6
"""

import lvgl as lv
import lcd_bus
from micropython import const

# Display configuration constants
_WIDTH = const(320)
_HEIGHT = const(240)
_MOSI = const(11)
_MISO = const(13)
_SCK = const(12)
_DC = const(0)
_CS = const(10)
_BL = const(45)
_RST = const(4)
_FREQ = const(40000000)

# Buffer size for partial screen updates
_BUFFER_SIZE = const(32000)  # ~10% of 320x240x2

def init_display():
    """Initialize SPI display"""
    import st7789  # or ili9341, depending on your display
    import machine
    
    # Create SPI bus
    spi_bus = machine.SPI.Bus(
        host=1,
        mosi=_MOSI,
        miso=_MISO,
        sck=_SCK
    )
    
    # Create display bus
    display_bus = lcd_bus.SPIBus(
        spi_bus=spi_bus,
        freq=_FREQ,
        dc=_DC,
        cs=_CS,
    )
    
    # Allocate frame buffers
    fb1 = display_bus.allocate_framebuffer(
        _BUFFER_SIZE, 
        lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA
    )
    fb2 = display_bus.allocate_framebuffer(
        _BUFFER_SIZE,
        lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA
    )
    
    # Initialize LVGL
    lv.init()
    
    # Create display driver
    display = st7789.ST7789(
        data_bus=display_bus,
        display_width=_WIDTH,
        display_height=_HEIGHT,
        frame_buffer1=fb1,
        frame_buffer2=fb2,
        backlight_pin=_BL,
        reset_pin=_RST,
        color_space=lv.COLOR_FORMAT.RGB565,
        rgb565_byte_swap=True,
    )
    
    display.init()
    display.set_backlight(100)
    
    return display

def init_touch():
    """Initialize I2C touch controller (optional)"""
    try:
        import i2c
        import ft6x36
        
        _SCL = const(5)
        _SDA = const(6)
        _FREQ = const(100000)
        
        # Create I2C bus
        i2c_bus = i2c.I2C.Bus(
            host=0, 
            scl=_SCL, 
            sda=_SDA, 
            freq=_FREQ
        )
        
        # Create touch device
        touch_dev = i2c.I2C.Device(
            bus=i2c_bus, 
            dev_id=ft6x36.I2C_ADDR,
            reg_bits=ft6x36.BITS
        )
        
        # Initialize touch driver
        indev = ft6x36.FT6x36(touch_dev)
        
        return indev
    except Exception as e:
        print(f"Touch init failed (optional): {e}")
        return None

def create_ui():
    """Create a simple UI with various widgets"""
    
    # Get active screen
    screen = lv.scr_act()
    screen.set_style_bg_color(lv.color_hex(0x003366), 0)
    
    # Title label
    title = lv.label(screen)
    title.set_text("ESP32-S3 + LVGL v8")
    title.align(lv.ALIGN.TOP_MID, 0, 10)
    title.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    
    # Create a slider
    slider = lv.slider(screen)
    slider.set_size(200, 20)
    slider.align(lv.ALIGN.CENTER, 0, -30)
    slider.set_value(50, lv.ANIM.OFF)
    
    # Slider value label
    slider_label = lv.label(screen)
    slider_label.set_text("Value: 50")
    slider_label.align(lv.ALIGN.CENTER, 0, 0)
    
    # Update label when slider changes
    def slider_event_cb(e):
        value = slider.get_value()
        slider_label.set_text(f"Value: {value}")
    
    slider.add_event_cb(slider_event_cb, lv.EVENT.VALUE_CHANGED, None)
    
    # Create a button
    btn = lv.btn(screen)
    btn.set_size(120, 50)
    btn.align(lv.ALIGN.CENTER, 0, 50)
    
    # Button label
    btn_label = lv.label(btn)
    btn_label.set_text("Click Me!")
    btn_label.center()
    
    # Button click counter
    click_count = [0]
    
    def btn_event_cb(e):
        click_count[0] += 1
        btn_label.set_text(f"Clicks: {click_count[0]}")
    
    btn.add_event_cb(btn_event_cb, lv.EVENT.CLICKED, None)

def main():
    """Main entry point"""
    print("Initializing LVGL on ESP32-S3...")
    
    # Initialize display
    display = init_display()
    print("Display initialized")
    
    # Initialize touch (optional)
    touch = init_touch()
    if touch:
        print("Touch initialized")
    
    # Create UI
    create_ui()
    print("UI created")
    
    # Import task handler for LVGL tick
    import task_handler
    th = task_handler.TaskHandler()
    
    print("LVGL example running!")

if __name__ == "__main__":
    main()
