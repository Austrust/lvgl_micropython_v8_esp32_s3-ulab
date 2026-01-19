"""
ulab Demonstration for ESP32-S3

This example demonstrates ulab's numpy-like array operations
which are significantly faster than pure Python for numerical computations.

Features demonstrated:
- Array creation and manipulation
- Mathematical operations
- Signal processing
- Linear algebra
"""

from ulab import numpy as np
import time

def demo_basic_operations():
    """Demonstrate basic array operations"""
    print("\n=== Basic Array Operations ===")
    
    # Create arrays
    a = np.array([1, 2, 3, 4, 5])
    b = np.array([5, 4, 3, 2, 1])
    
    print(f"Array a: {a}")
    print(f"Array b: {b}")
    
    # Element-wise operations
    print(f"a + b: {a + b}")
    print(f"a * b: {a * b}")
    print(f"a ** 2: {a ** 2}")
    
    # Aggregation operations
    print(f"Sum of a: {np.sum(a)}")
    print(f"Mean of a: {np.mean(a)}")
    print(f"Max of a: {np.max(a)}")

def demo_math_functions():
    """Demonstrate mathematical functions"""
    print("\n=== Mathematical Functions ===")
    
    # Create array from 0 to 2π
    x = np.linspace(0, 2 * np.pi, 10)
    print(f"x (10 points from 0 to 2π):\n{x}")
    
    # Trigonometric functions
    sin_x = np.sin(x)
    cos_x = np.cos(x)
    print(f"sin(x):\n{sin_x}")
    print(f"cos(x):\n{cos_x}")
    
    # Exponential and logarithm
    exp_vals = np.exp(np.array([0, 1, 2, 3]))
    print(f"exp([0,1,2,3]):\n{exp_vals}")
    
    log_vals = np.log(np.array([1, 2, 4, 8]))
    print(f"log([1,2,4,8]):\n{log_vals}")

def demo_signal_processing():
    """Demonstrate signal processing capabilities"""
    print("\n=== Signal Processing ===")
    
    # Generate a simple sine wave
    sample_rate = 100  # Hz
    duration = 1.0  # second
    frequency = 5  # Hz
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    signal = np.sin(2 * np.pi * frequency * t)
    
    print(f"Generated {len(signal)} samples of {frequency}Hz sine wave")
    print(f"Signal range: [{np.min(signal):.3f}, {np.max(signal):.3f}]")
    
    # Simple moving average filter
    window_size = 5
    smoothed = signal.copy()
    for i in range(len(signal) - window_size):
        smoothed[i] = np.mean(signal[i:i+window_size])
    
    print(f"Applied {window_size}-point moving average filter")

def demo_matrix_operations():
    """Demonstrate matrix/linear algebra operations"""
    print("\n=== Matrix Operations ===")
    
    # Create 2D arrays (matrices)
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    print(f"Matrix A:\n{A}")
    print(f"Matrix B:\n{B}")
    
    # Matrix multiplication
    C = np.dot(A, B)
    print(f"A · B:\n{C}")
    
    # Transpose
    print(f"Transpose of A:\n{A.T}")
    
    # Determinant (if available in ulab)
    try:
        det_A = np.linalg.det(A)
        print(f"Determinant of A: {det_A}")
    except (ImportError, AttributeError):
        print("Linear algebra module not available")

def demo_performance():
    """Compare ulab performance with pure Python"""
    print("\n=== Performance Comparison ===")
    
    size = 1000
    
    # ulab version
    start = time.ticks_ms()
    a = np.linspace(0, 100, size)
    b = np.sin(a) + np.cos(a)
    ulab_time = time.ticks_diff(time.ticks_ms(), start)
    
    # Pure Python version
    start = time.ticks_ms()
    import math
    a_list = [i * 100 / size for i in range(size)]
    b_list = [math.sin(x) + math.cos(x) for x in a_list]
    python_time = time.ticks_diff(time.ticks_ms(), start)
    
    print(f"Processing {size} elements:")
    print(f"  ulab:   {ulab_time}ms")
    print(f"  Python: {python_time}ms")
    print(f"  Speedup: {python_time/ulab_time:.1f}x faster")

def demo_sensor_data_processing():
    """Simulate processing sensor data"""
    print("\n=== Sensor Data Processing Example ===")
    
    # Simulate noisy sensor readings (e.g., temperature)
    # Note: ulab's numpy doesn't have random module, so we use a pattern
    num_samples = 20
    true_temp = 25.0  # °C
    noise_level = 0.5
    
    # Generate synthetic sensor data with simulated noise pattern
    sensor_data = np.array([true_temp + (i % 3 - 1) * noise_level 
                           for i in range(num_samples)])
    
    print(f"Raw sensor data (first 10): {sensor_data[:10]}")
    
    # Calculate statistics
    mean_temp = np.mean(sensor_data)
    std_temp = np.std(sensor_data)
    
    print(f"Mean temperature: {mean_temp:.2f}°C")
    print(f"Std deviation: {std_temp:.2f}°C")
    print(f"Min: {np.min(sensor_data):.2f}°C")
    print(f"Max: {np.max(sensor_data):.2f}°C")

def main():
    """Run all demonstrations"""
    print("=" * 50)
    print("ulab Demonstration on ESP32-S3")
    print("=" * 50)
    
    try:
        demo_basic_operations()
        demo_math_functions()
        demo_signal_processing()
        demo_matrix_operations()
        demo_performance()
        demo_sensor_data_processing()
        
        print("\n" + "=" * 50)
        print("All demonstrations completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import sys
        sys.print_exception(e)

if __name__ == "__main__":
    main()
