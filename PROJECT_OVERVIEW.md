# Project Overview

## Network Filtering Methods in Finance

A comprehensive Python implementation for analyzing and visualizing time-varying correlation networks in financial markets using state-of-the-art filtering methods.

## Repository Structure

```
network-filtering-finance/
├── .github/
│   └── workflows/
│       └── ci.yml                    # CI/CD pipeline
├── docs/
│   ├── README.md                     # Documentation index
│   ├── CHANGELOG.md                  # Version history
│   ├── DYNAMIC_LAYOUT_GUIDE.md      # Dynamic layout guide
│   └── QUICKSTART.md                # Quick start guide
├── examples/
│   ├── README.md                     # Examples documentation
│   ├── example_dynamic_layout.py    # Dynamic layout example
│   └── examples.ipynb               # Interactive tutorial
├── src/
│   ├── __init__.py                  # Package initialization
│   └── correlation_network_animation.py  # Main implementation
├── tests/
│   ├── README.md                     # Testing documentation
│   └── test_installation.py         # Installation tests
├── .gitignore                        # Git ignore rules
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT License
├── MANIFEST.in                       # Package manifest
├── PROJECT_OVERVIEW.md              # This file
├── README.md                         # Main documentation
├── requirements.txt                  # Python dependencies
├── requirements-dev.txt             # Development dependencies
├── setup.py                         # Package setup
└── setup.sh                         # Setup script
```

## Core Components

### 1. SyntheticCorrelationGenerator
Generates synthetic financial time series with realistic time-varying correlation structures.

**Features:**
- Block/sector structure
- Ornstein-Uhlenbeck diffusion process
- Positive semi-definite guarantee
- Configurable evolution dynamics

### 2. RollingCorrelationEstimator
Computes rolling window correlation matrices from time series data.

**Features:**
- Efficient window-based computation
- Pandas DataFrame support
- DatetimeIndex handling
- Flexible window sizes

### 3. CorrelationFilter
Implements three network filtering algorithms:

**MST (Minimum Spanning Tree)**
- Complexity: O(N² log N)
- Edges: N-1
- Best for: Large networks (N > 200)

**PMFG (Planar Maximally Filtered Graph)**
- Complexity: O(N³)
- Edges: 3(N-2)
- Best for: Quality analysis (N < 100)

**TMFG (Triangulated Maximally Filtered Graph)**
- Complexity: O(N²)
- Edges: 3(N-2)
- Best for: Balanced performance (N < 200)

### 4. NetworkAnimator
Creates animated visualizations of network evolution.

**Features:**
- Dynamic force-directed layouts
- Static layouts for tracking
- Side-by-side comparisons
- MP4 export
- Customizable styling

## Key Features

### Data Generation
- ✓ Synthetic time series with controlled correlations
- ✓ Block structure for sector modeling
- ✓ Time-varying correlation dynamics
- ✓ Support for real market data

### Network Filtering
- ✓ Three geometric filtering methods
- ✓ Correlation-to-distance transformation
- ✓ Graph theory algorithms
- ✓ Efficient implementations

### Visualization
- ✓ Animated network evolution
- ✓ Dynamic and static layouts
- ✓ Edge thickness by correlation strength
- ✓ Color-coded node clusters
- ✓ Network statistics overlay

### Export & Analysis
- ✓ MP4 video export
- ✓ Network metrics extraction
- ✓ CSV data export
- ✓ Static plot generation

## Installation

### Quick Setup
```bash
# Clone repository
git clone https://github.com/yourusername/network-filtering-finance.git
cd network-filtering-finance

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate environment
source venv/bin/activate

# Test installation
python tests/test_installation.py
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install ffmpeg (Ubuntu)
sudo apt-get install ffmpeg

# Test
python tests/test_installation.py
```

## Quick Start

```python
from src.correlation_network_animation import (
    SyntheticCorrelationGenerator,
    RollingCorrelationEstimator,
    NetworkAnimator
)

# Generate data
generator = SyntheticCorrelationGenerator(n_assets=20, seed=42)
returns_df, _ = generator.generate_time_series(total_days=500, window_size=100)

# Estimate correlations
estimator = RollingCorrelationEstimator(window_size=100)
correlations = estimator.estimate_correlations(returns_df)

# Create animation
animator = NetworkAnimator(dynamic_layout=True)
animator.animate_filtered_networks(
    correlations,
    filter_method='pmfg',
    output_file='network.mp4'
)
```

## Use Cases

### 1. Market Structure Analysis
Monitor how correlation networks evolve during normal and crisis periods.

### 2. Risk Management
Identify systemic risk through network topology changes.

### 3. Portfolio Diversification
Find truly uncorrelated assets using network distance.

### 4. Crisis Detection
Detect market stress through network density increases.

### 5. Sector Analysis
Track intra- and inter-sector correlation dynamics.

## Research Foundation

This implementation is based on pioneering work by:

- **Tomaso Aste** (UCL)
- **Tiziana Di Matteo** (King's College London)
- **Rosario Mantegna** (University of Palermo)

Key papers:
1. Tumminello et al. (2005) - PMFG method
2. Massara et al. (2016) - TMFG method
3. Mantegna (1999) - MST in finance

## Performance

### Computational Complexity

| Method | Complexity  | N=50   | N=100  | N=200  |
|--------|------------|--------|--------|--------|
| MST    | O(N²log N) | <1s    | <1s    | ~5s    |
| PMFG   | O(N³)      | ~2s    | ~15s   | ~2min  |
| TMFG   | O(N²)      | <1s    | ~3s    | ~10s   |

### Memory Usage

- Typical: 50 assets × 500 windows ≈ 200 MB
- Large: 100 assets × 1000 windows ≈ 1 GB

## Development

### Running Tests
```bash
python tests/test_installation.py
```

### Code Style
```bash
pip install -r requirements-dev.txt
black src/
flake8 src/
```

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Documentation

- [README.md](README.md) - Full documentation
- [docs/QUICKSTART.md](docs/QUICKSTART.md) - Quick start guide
- [docs/DYNAMIC_LAYOUT_GUIDE.md](docs/DYNAMIC_LAYOUT_GUIDE.md) - Dynamic layouts
- [examples/README.md](examples/README.md) - Example usage
- [tests/README.md](tests/README.md) - Testing guide

## License

MIT License - see [LICENSE](LICENSE)

When using in academic research, please cite:
1. Tumminello et al. (2005) PNAS
2. Massara et al. (2016) J. Complex Networks
3. Mantegna (1999) Eur. Phys. J. B

## Contact & Support

- **Issues**: GitHub Issues
- **Questions**: See documentation
- **Research**: Refer to original papers

## Roadmap

### Version 1.0 (Current)
- ✓ Core filtering methods
- ✓ Animation creation
- ✓ Dynamic layouts
- ✓ Comprehensive documentation

### Future Versions
- [ ] Interactive visualizations (Plotly)
- [ ] Real-time streaming support
- [ ] GPU acceleration
- [ ] Additional filtering methods
- [ ] Web interface
- [ ] Portfolio optimization integration

## Citation

```bibtex
@software{network_filtering_finance,
  title = {Network Filtering in Finance},
  year = {2024},
  url = {https://github.com/yourusername/network-filtering-finance},
  note = {Based on methods by Aste, Di Matteo, and Mantegna}
}
```

---

*For detailed usage instructions, see [README.md](README.md)*
