# Tests

This directory contains test files for the Network Filtering in Finance package.

## Available Tests

### test_installation.py

Comprehensive installation and functionality test that verifies:

1. **Python Version**
   - Checks Python >= 3.8

2. **Package Dependencies**
   - numpy >= 1.21.0
   - pandas >= 1.3.0
   - scipy >= 1.7.0
   - networkx >= 2.6.0
   - matplotlib >= 3.4.0

3. **System Dependencies**
   - ffmpeg availability

4. **Functionality Tests**
   - SyntheticCorrelationGenerator
   - RollingCorrelationEstimator
   - CorrelationFilter (MST, PMFG, TMFG)
   - NetworkAnimator

## Running Tests

### Basic Test Run

```bash
python tests/test_installation.py
```

### From Project Root

```bash
cd /path/to/network-filtering-finance
python tests/test_installation.py
```

### With Virtual Environment

```bash
source venv/bin/activate
python tests/test_installation.py
```

## Expected Output

A successful test run shows:
```
=== Network Filtering Installation Test ===

Python Version: ✓ 3.10.5

Required Packages:
  numpy: ✓ 1.23.0
  pandas: ✓ 1.4.3
  scipy: ✓ 1.8.1
  networkx: ✓ 2.8.0
  matplotlib: ✓ 3.5.2

System Dependencies:
  ffmpeg: ✓ Available

Functionality Tests:
  SyntheticCorrelationGenerator: ✓ Working
  RollingCorrelationEstimator: ✓ Working
  CorrelationFilter (MST): ✓ Working
  CorrelationFilter (PMFG): ✓ Working
  CorrelationFilter (TMFG): ✓ Working
  NetworkAnimator: ✓ Working

=== All tests passed! ===
```

## Troubleshooting

### Import Errors

If you see import errors:
```bash
# Make sure you're in the right directory
cd /path/to/network-filtering-finance

# Or add src to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/network-filtering-finance/src"
```

### Missing Dependencies

```bash
pip install -r requirements.txt
```

### ffmpeg Not Found

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

### Python Version Issues

Ensure Python 3.8 or higher:
```bash
python --version
```

If needed, use a specific Python version:
```bash
python3.10 tests/test_installation.py
```

## Adding New Tests

To extend the test suite:

1. Create new test files in this directory
2. Follow the naming convention: `test_*.py`
3. Use pytest for more advanced testing:
   ```bash
   pip install pytest
   pytest tests/
   ```

### Example Test Structure

```python
import sys
sys.path.insert(0, '../src')

from correlation_network_animation import *

def test_new_feature():
    # Your test code
    assert result == expected
```

## Continuous Integration

Tests are automatically run via GitHub Actions on:
- Push to main/develop branches
- Pull requests
- Multiple OS (Ubuntu, macOS, Windows)
- Multiple Python versions (3.8, 3.9, 3.10, 3.11)

See `.github/workflows/ci.yml` for CI configuration.

## Test Coverage

To measure test coverage:

```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

## Performance Tests

For performance benchmarking:

```python
import time

# Time the filtering methods
for n_assets in [20, 50, 100]:
    generator = SyntheticCorrelationGenerator(n_assets=n_assets)
    # ... benchmark code
```

## Future Testing Needs

- [ ] Unit tests for individual methods
- [ ] Integration tests for full pipeline
- [ ] Performance benchmarks
- [ ] Memory usage profiling
- [ ] Edge case testing
- [ ] Randomized testing

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [unittest documentation](https://docs.python.org/3/library/unittest.html)
- [GitHub Actions](https://docs.github.com/en/actions)
