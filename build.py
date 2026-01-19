#!/usr/bin/env python3
"""
Build script for LVGL MicroPython v8 ESP32-S3 with ulab

This script simplifies the build process by:
1. Checking prerequisites
2. Initializing submodules if needed
3. Building the firmware
4. Optionally flashing to device

Usage:
    python3 build.py                    # Build for ESP32-S3 with SPIRAM
    python3 build.py --variant generic  # Build for generic ESP32-S3
    python3 build.py --variant oct      # Build with octal SPIRAM
    python3 build.py --flash --port /dev/ttyUSB0  # Build and flash
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.absolute()
MICROPYTHON_DIR = PROJECT_ROOT / "lib" / "micropython"
ESP32_PORT_DIR = MICROPYTHON_DIR / "ports" / "esp32"

# Build variants
VARIANTS = {
    'generic': {
        'board': 'ESP32_GENERIC_S3',
        'variant': None,
        'desc': 'Generic ESP32-S3 (no PSRAM)'
    },
    'spiram': {
        'board': 'ESP32_GENERIC_S3',
        'variant': 'SPIRAM',
        'desc': 'ESP32-S3 with SPIRAM (recommended)'
    },
    'oct': {
        'board': 'ESP32_GENERIC_S3',
        'variant': 'SPIRAM_OCT',
        'desc': 'ESP32-S3 with Octal SPIRAM'
    }
}

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=False,
        text=True,
        check=check
    )
    return result.returncode == 0

def check_prerequisites():
    """Check if required tools are installed"""
    print("Checking prerequisites...")
    
    required_tools = ['git', 'make', 'cmake']
    optional_tools = ['esptool.py', 'ccache']
    
    missing = []
    for tool in required_tools:
        if not subprocess.run(['which', tool], capture_output=True).returncode == 0:
            missing.append(tool)
    
    if missing:
        print(f"Error: Missing required tools: {', '.join(missing)}")
        print("\nInstall them with:")
        print("  Ubuntu/Debian: sudo apt-get install git make cmake")
        print("  macOS: brew install git make cmake")
        return False
    
    # Check optional tools
    for tool in optional_tools:
        if subprocess.run(['which', tool], capture_output=True).returncode == 0:
            print(f"  ✓ {tool} found")
        else:
            print(f"  ⚠ {tool} not found (optional)")
    
    print("Prerequisites check passed!")
    return True

def init_submodules():
    """Initialize and update git submodules"""
    print("\nInitializing submodules...")
    
    # Check if submodules are already initialized
    micropython_py = MICROPYTHON_DIR / "py" / "py.mk"
    if micropython_py.exists():
        print("Submodules already initialized")
        return True
    
    print("Initializing submodules (this may take a while)...")
    if not run_command(['git', 'submodule', 'update', '--init', '--recursive'], cwd=PROJECT_ROOT):
        print("Error: Failed to initialize submodules")
        return False
    
    print("Submodules initialized successfully!")
    return True

def build_firmware(variant='spiram'):
    """Build the firmware"""
    print(f"\nBuilding firmware for {VARIANTS[variant]['desc']}...")
    
    if not ESP32_PORT_DIR.exists():
        print(f"Error: ESP32 port directory not found: {ESP32_PORT_DIR}")
        print("Make sure submodules are initialized")
        return False
    
    # Prepare make command
    make_cmd = ['make']
    make_cmd.append(f"BOARD={VARIANTS[variant]['board']}")
    
    if VARIANTS[variant]['variant']:
        make_cmd.append(f"BOARD_VARIANT={VARIANTS[variant]['variant']}")
    
    # Add user modules path
    modules_path = PROJECT_ROOT / "modules" / "micropython.cmake"
    if modules_path.exists():
        make_cmd.append(f"USER_C_MODULES={modules_path.absolute()}")
    
    print(f"Build command: {' '.join(make_cmd)}")
    print("This will take several minutes on first build...")
    
    if not run_command(make_cmd, cwd=ESP32_PORT_DIR):
        print("Error: Build failed")
        return False
    
    # Find the built firmware
    if VARIANTS[variant]['variant']:
        build_name = f"{VARIANTS[variant]['board']}-{VARIANTS[variant]['variant']}"
    else:
        build_name = VARIANTS[variant]['board']
    
    build_dir = ESP32_PORT_DIR / f"build-{build_name}"
    firmware = build_dir / "firmware.bin"
    
    if firmware.exists():
        print(f"\n✓ Build successful!")
        print(f"Firmware: {firmware}")
        print(f"Size: {firmware.stat().st_size / 1024:.1f} KB")
        return True
    else:
        print("Warning: Build completed but firmware.bin not found")
        return False

def flash_firmware(variant='spiram', port='/dev/ttyUSB0', baud=460800):
    """Flash firmware to device"""
    print(f"\nFlashing firmware to {port}...")
    
    make_cmd = ['make']
    make_cmd.append(f"BOARD={VARIANTS[variant]['board']}")
    
    if VARIANTS[variant]['variant']:
        make_cmd.append(f"BOARD_VARIANT={VARIANTS[variant]['variant']}")
    
    make_cmd.append(f"PORT={port}")
    make_cmd.append(f"BAUD={baud}")
    make_cmd.append('deploy')
    
    if not run_command(make_cmd, cwd=ESP32_PORT_DIR, check=False):
        print("\nFlashing failed. Make sure:")
        print(f"  1. Device is connected to {port}")
        print("  2. You have permission to access the port")
        print("  3. No other program is using the port")
        return False
    
    print("\n✓ Flashing successful!")
    return True

def clean_build():
    """Clean build artifacts"""
    print("\nCleaning build artifacts...")
    run_command(['make', 'clean'], cwd=ESP32_PORT_DIR, check=False)
    print("Clean complete")

def main():
    parser = argparse.ArgumentParser(
        description='Build LVGL MicroPython v8 for ESP32-S3 with ulab'
    )
    parser.add_argument(
        '--variant',
        choices=list(VARIANTS.keys()),
        default='spiram',
        help='ESP32-S3 variant to build for (default: spiram)'
    )
    parser.add_argument(
        '--flash',
        action='store_true',
        help='Flash firmware after building'
    )
    parser.add_argument(
        '--port',
        default='/dev/ttyUSB0',
        help='Serial port for flashing (default: /dev/ttyUSB0)'
    )
    parser.add_argument(
        '--baud',
        type=int,
        default=460800,
        help='Baud rate for flashing (default: 460800)'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean build artifacts before building'
    )
    parser.add_argument(
        '--init-only',
        action='store_true',
        help='Only initialize submodules, do not build'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("LVGL MicroPython v8 ESP32-S3 with ulab - Build System")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        return 1
    
    # Initialize submodules
    if not init_submodules():
        return 1
    
    if args.init_only:
        print("\nSubmodules initialized. Run without --init-only to build.")
        return 0
    
    # Clean if requested
    if args.clean:
        clean_build()
    
    # Build
    if not build_firmware(args.variant):
        return 1
    
    # Flash if requested
    if args.flash:
        if not flash_firmware(args.variant, args.port, args.baud):
            return 1
    
    print("\n" + "=" * 60)
    print("Build completed successfully!")
    print("=" * 60)
    
    if not args.flash:
        print("\nTo flash the firmware, run:")
        print(f"  python3 build.py --variant {args.variant} --flash --port {args.port}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
