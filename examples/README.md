# Examples

This directory contains examples demonstrating the use of the Network Filtering in Finance package.

## Available Examples

### 1. examples.ipynb
**Interactive Jupyter Notebook**

A comprehensive tutorial covering:
- Data generation with synthetic time series
- Rolling correlation estimation
- Network filtering methods (MST, PMFG, TMFG)
- Animation creation
- Network statistics analysis
- Data export

**To run:**
```bash
jupyter notebook examples.ipynb
```

### 2. example_dynamic_layout.py
**Dynamic Layout Demonstration**

Shows how to create animations with force-directed layouts where nodes move according to the evolving correlation structure.

**To run:**
```bash
cd examples
python example_dynamic_layout.py
```

## Quick Example

Here's a minimal example to get started:

```python
from src.correlation_network_animation import (
    SyntheticCorrelationGenerator,
    RollingCorrelationEstimator,
    NetworkAnimator
)

# 1. Generate data
generator = SyntheticCorrelationGenerator(n_assets=20, seed=42)
returns_df, _ = generator.generate_time_series(
    total_days=500,
    window_size=100
)

# 2. Estimate correlations
estimator = RollingCorrelationEstimator(window_size=100)
correlations = estimator.estimate_correlations(returns_df)

# 3. Create animation
animator = NetworkAnimator()
animator.animate_filtered_networks(
    correlations,
    filter_method='pmfg',
    output_file='network.mp4'
)
```

## Using Real Data

To analyze your own financial data:

```python
import pandas as pd

# Load your returns data (with DatetimeIndex)
returns_df = pd.read_csv('your_data.csv', index_col=0, parse_dates=True)

# Process and animate
estimator = RollingCorrelationEstimator(window_size=252)  # 1 year
correlations = estimator.estimate_correlations(returns_df)

animator = NetworkAnimator()
animator.animate_filtered_networks(
    correlations,
    filter_method='pmfg',
    output_file='market_network.mp4'
)
```

## Parameter Guide

### Key Parameters to Adjust

**Data Generation:**
- `n_assets`: Number of time series (10-100 recommended)
- `total_days`: Length of time series (500-2000)
- `window_size`: Rolling window size (50-250)

**Animation:**
- `filter_method`: 'mst', 'pmfg', or 'tmfg'
- `fps`: Frames per second (5-30)
- `dynamic_layout`: True for moving nodes, False for static
- `smoothing_factor`: 0.1-0.5 for dynamic layout smoothness

## Expected Outputs

Running the examples will generate:
- MP4 animation files
- Network visualization plots
- CSV files with network metrics (optional)

## Computational Notes

- **MST**: Fast, suitable for large networks (N > 200)
- **PMFG**: Moderate speed, best quality (N < 100)
- **TMFG**: Fast, good quality (N < 200)

For N > 200 assets, consider:
- Using TMFG or MST
- Sampling fewer time points
- Reducing animation fps

## Troubleshooting

**"ffmpeg not found"**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/
```

**Animation too slow/fast**
Adjust fps and interval:
```python
animator.animate_filtered_networks(..., fps=15, interval=50)
```

**Out of memory**
- Reduce n_assets
- Use fewer time points
- Use MST instead of PMFG

## Next Steps

1. Run the Jupyter notebook for interactive exploration
2. Try different filtering methods and compare results
3. Experiment with your own financial data
4. Adjust visualization parameters to suit your needs
5. Export network metrics for further analysis

## Additional Resources

- See [docs/](../docs/) for detailed documentation
- See [README.md](../README.md) for full feature list
- Check [tests/test_installation.py](../tests/test_installation.py) for validation
