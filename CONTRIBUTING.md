# Contributing to LVGL MicroPython v8 ESP32-S3 with ulab

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Collect relevant information

Include in your bug report:
- ESP32-S3 board model and variant
- MicroPython and LVGL version
- Display and touch hardware details
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces
- Minimal code example

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
1. Check if it's already been suggested
2. Explain the use case clearly
3. Describe the expected behavior
4. Consider implementation complexity

### Pull Requests

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/lvgl_micropython_v8_esp32_s3-ulab.git
   cd lvgl_micropython_v8_esp32_s3-ulab
   git remote add upstream https://github.com/Austrust/lvgl_micropython_v8_esp32_s3-ulab.git
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make Changes**
   - Follow the coding style (see below)
   - Add comments for complex logic
   - Update documentation if needed
   - Test your changes thoroughly

4. **Commit**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```
   
   Commit message format:
   - First line: Brief summary (50 chars max)
   - Blank line
   - Detailed description if needed
   - Reference issues: "Fixes #123"

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

### PR Guidelines

- Describe what the PR does and why
- Link related issues
- Keep changes focused and atomic
- Update documentation
- Add examples if adding features
- Ensure builds pass

## Development Setup

### Prerequisites

See [BUILD.md](docs/BUILD.md) for detailed prerequisites.

### Building for Development

```bash
# Clone with submodules
git clone --recursive https://github.com/YOUR_USERNAME/lvgl_micropython_v8_esp32_s3-ulab.git

# Build
python3 build.py --variant spiram

# Clean build
python3 build.py --clean --variant spiram
```

### Testing

Before submitting a PR:

1. **Build Test**
   ```bash
   python3 build.py --variant generic
   python3 build.py --variant spiram
   python3 build.py --variant oct
   ```

2. **Example Test**
   - Upload and run examples
   - Test on actual hardware if possible

3. **Documentation Test**
   - Check markdown formatting
   - Verify links work
   - Ensure code examples are correct

## Coding Style

### Python Code

Follow PEP 8 with these specifics:

```python
# Use 4 spaces for indentation
def my_function(param1, param2):
    """Docstring explaining function purpose."""
    result = param1 + param2
    return result

# Constants in UPPER_CASE
MAX_BUFFER_SIZE = 32000
DEFAULT_FREQ = 40000000

# Classes in PascalCase
class DisplayManager:
    def __init__(self):
        self.initialized = False

# Functions and variables in snake_case
def init_display(width, height):
    buffer_size = width * height * 2
    return buffer_size
```

### C Code

For any C modules:

```c
// Use K&R style bracing
void function_name(int param) {
    if (condition) {
        // Code here
    }
}

// Constants in UPPER_CASE
#define MAX_BUFFER 1024

// Use meaningful names
int calculate_buffer_size(int width, int height) {
    return width * height * 2;
}
```

### Documentation

- Use Markdown for all documentation
- Keep lines under 80 characters when possible
- Use code blocks with language specification:
  ````markdown
  ```python
  import lvgl as lv
  ```
  ````

- Add docstrings to all public functions:
  ```python
  def init_display(width, height, color_depth=16):
      """
      Initialize the display with given parameters.
      
      Args:
          width (int): Display width in pixels
          height (int): Display height in pixels
          color_depth (int): Bits per pixel (default: 16)
          
      Returns:
          Display: Initialized display object
          
      Raises:
          ValueError: If width or height is invalid
      """
  ```

## Project Structure

```
.
├── docs/               # Documentation
│   ├── BUILD.md       # Build instructions
│   └── HARDWARE.md    # Hardware configuration
├── examples/          # Example scripts
│   ├── lvgl_basic.py
│   └── ulab_demo.py
├── modules/           # Build configuration
│   └── micropython.cmake
├── lib/               # Submodules (not in repo)
│   ├── micropython/
│   ├── lvgl/
│   ├── lv_bindings/
│   └── ulab/
├── build.py           # Build script
├── Makefile          # Make targets
└── README.md         # Main documentation
```

## Adding Examples

Examples help users understand features:

1. **Create example file** in `examples/`
2. **Add header comment** explaining:
   - What it demonstrates
   - Required hardware
   - Pin configuration
3. **Keep it simple** and focused
4. **Comment thoroughly**
5. **Test on hardware**

Example template:

```python
"""
Example Name - Brief Description

This example demonstrates:
- Feature 1
- Feature 2

Hardware Requirements:
- ESP32-S3 board
- Specific components

Pin Configuration:
- PIN_X: Description
"""

import lvgl as lv

def main():
    """Main entry point"""
    # Implementation
    pass

if __name__ == "__main__":
    main()
```

## Adding Documentation

1. **Update README.md** for major features
2. **Add to docs/** for detailed guides
3. **Update BUILD.md** for build-related changes
4. **Update HARDWARE.md** for new hardware support

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New backwards-compatible functionality
- **PATCH**: Backwards-compatible bug fixes

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release branch
4. Tag release: `git tag -a v1.0.0 -m "Release 1.0.0"`
5. Push tags: `git push --tags`
6. Create GitHub release

## Questions?

- Check [existing issues](https://github.com/Austrust/lvgl_micropython_v8_esp32_s3-ulab/issues)
- Review [documentation](docs/)
- Ask in discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions help make this project better for everyone!
