"""
Combined LVGL + ulab Example for ESP32-S3

This example demonstrates using both LVGL for GUI and ulab for data processing.
It creates a real-time graph display using LVGL to visualize data processed by ulab.

Use Case: Display a sine wave animation using ulab for calculations
          and LVGL for rendering.
"""

import lvgl as lv
from ulab import numpy as np
import time

class SineWaveChart:
    """A simple sine wave chart using LVGL and ulab"""
    
    def __init__(self, parent, width=300, height=200):
        """Initialize the chart"""
        self.parent = parent
        self.width = width
        self.height = height
        
        # Create chart widget
        self.chart = lv.chart(parent)
        self.chart.set_size(width, height)
        self.chart.center()
        self.chart.set_type(lv.chart.TYPE.LINE)
        self.chart.set_point_count(50)
        
        # Add a data series
        self.series = self.chart.add_series(
            lv.color_hex(0x00FF00), 
            lv.chart.AXIS.PRIMARY_Y
        )
        
        # Animation parameters
        self.phase = 0
        self.num_points = 50
        
        # Generate x values using ulab
        self.x = np.linspace(0, 2 * np.pi, self.num_points)
        
    def update(self):
        """Update the chart with new data"""
        # Calculate sine wave with animated phase using ulab
        y = np.sin(self.x + self.phase)
        
        # Scale to chart range (0-100)
        y_scaled = ((y + 1) / 2 * 100).astype(np.int16)
        
        # Update chart data
        for i in range(self.num_points):
            self.chart.set_next_value(self.series, int(y_scaled[i]))
        
        # Increment phase for animation
        self.phase += 0.1
        if self.phase > 2 * np.pi:
            self.phase = 0

class DataProcessor:
    """Process data using ulab and display statistics"""
    
    def __init__(self):
        """Initialize with some sample data"""
        self.data_size = 100
        self.data = np.linspace(0, 10, self.data_size)
        
    def calculate_statistics(self):
        """Calculate statistics using ulab"""
        stats = {
            'mean': float(np.mean(self.data)),
            'std': float(np.std(self.data)),
            'min': float(np.min(self.data)),
            'max': float(np.max(self.data)),
        }
        return stats
    
    def apply_filter(self, window_size=5):
        """Apply moving average filter"""
        filtered = self.data.copy()
        for i in range(len(self.data) - window_size):
            filtered[i] = np.mean(self.data[i:i+window_size])
        self.data = filtered
        return filtered

def create_ui():
    """Create the main UI"""
    screen = lv.scr_act()
    screen.set_style_bg_color(lv.color_hex(0x000000), 0)
    
    # Title
    title = lv.label(screen)
    title.set_text("LVGL + ulab Demo")
    title.align(lv.ALIGN.TOP_MID, 0, 10)
    title.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    
    # Create container for chart
    chart_cont = lv.obj(screen)
    chart_cont.set_size(320, 220)
    chart_cont.align(lv.ALIGN.CENTER, 0, -10)
    
    # Create sine wave chart
    wave_chart = SineWaveChart(chart_cont, 300, 180)
    
    # Stats label
    stats_label = lv.label(screen)
    stats_label.align(lv.ALIGN.BOTTOM_MID, 0, -10)
    stats_label.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    
    # Data processor
    processor = DataProcessor()
    
    # Timer callback to update chart
    def update_callback(timer):
        # Update chart
        wave_chart.update()
        
        # Update statistics (every 10th update)
        if timer.get_repeat_count() % 10 == 0:
            stats = processor.calculate_statistics()
            stats_text = f"Mean: {stats['mean']:.2f} | Std: {stats['std']:.2f}"
            stats_label.set_text(stats_text)
    
    # Create timer for animation (50ms interval = 20 FPS)
    timer = lv.timer_create(update_callback, 50, None)
    
    return wave_chart, processor, timer

def init_display_simple():
    """
    Simplified display init for demonstration
    Replace with actual display initialization code
    """
    # This is a placeholder - actual initialization depends on hardware
    print("Note: Replace init_display_simple() with actual display init code")
    print("See lvgl_basic.py for complete display initialization example")
    
    # For actual use, uncomment and adapt:
    # import lcd_bus, st7789
    # ... (initialize display as shown in lvgl_basic.py)
    
    lv.init()

def main():
    """Main entry point"""
    print("LVGL + ulab Combined Demo")
    print("This demonstrates real-time data processing with ulab")
    print("and visualization with LVGL")
    
    # Initialize display
    # Note: For actual hardware, use proper display initialization
    # init_display_simple()
    
    # Create UI
    # chart, processor, timer = create_ui()
    
    # Import task handler for LVGL
    # import task_handler
    # th = task_handler.TaskHandler()
    
    print("\nTo run this demo:")
    print("1. Initialize your display (see lvgl_basic.py)")
    print("2. Uncomment the init and UI creation code above")
    print("3. Upload to ESP32-S3 and run")
    
    # Demonstrate ulab calculation
    print("\nDemonstrating ulab calculations:")
    x = np.linspace(0, 2*np.pi, 20)
    y = np.sin(x)
    print(f"Generated sine wave: min={np.min(y):.3f}, max={np.max(y):.3f}")

if __name__ == "__main__":
    main()
