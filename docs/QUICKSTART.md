# Quick Start Guide

## Installation & Setup

### Step 1: Download the Files

Download all files from the project:
- `setup.sh` - Setup script
- `correlation_network_animation.py` - Main Python code
- `requirements.txt` - Dependencies list
- `examples.ipynb` - Jupyter notebook with examples
- `README.md` - Full documentation

### Step 2: Run Setup Script

The `setup.sh` script will:
1. Create a virtual environment named `venv`
2. Install all required Python packages
3. Optionally install Jupyter Notebook
4. Check for ffmpeg installation

**On Linux/macOS:**

```bash
# Make the script executable (if not already)
chmod +x setup.sh

# Run the setup script
./setup.sh
```

**On Windows:**

Use Git Bash or WSL, or install packages manually:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Activate Virtual Environment

After setup completes, activate the virtual environment:

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

### Step 4: Install ffmpeg (Required for Video Export)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Download from https://ffmpeg.org/download.html
- Add to PATH

### Step 5: Run the Code

**Option A: Run the main script**

```bash
python correlation_network_animation.py
```

This will:
- Generate synthetic time series data
- Estimate rolling correlations
- Create animations for MST, PMFG, and TMFG
- Create a comparison animation
- Output: `mst_network_animation.mp4`, `pmfg_network_animation.mp4`, `tmfg_network_animation.mp4`, `network_comparison.mp4`

**Option B: Run the Jupyter notebook**

```bash
jupyter notebook examples.ipynb
```

This opens an interactive notebook with:
- Step-by-step examples
- Visualizations
- Explanations
- Customizable parameters

**Option C: Use as a library**

```python
from correlation_network_animation import (
    SyntheticCorrelationGenerator,
    RollingCorrelationEstimator,
    NetworkAnimator
)

# Your custom code here
```

## Basic Usage Example

```python
from correlation_network_animation import (
    SyntheticCorrelationGenerator,
    RollingCorrelationEstimator,
    NetworkAnimator
)

# 1. Generate synthetic data
generator = SyntheticCorrelationGenerator(n_assets=20, seed=42)
returns_df, true_correlations = generator.generate_time_series(
    total_days=500,
    window_size=100
)

# 2. Estimate rolling correlations
estimator = RollingCorrelationEstimator(window_size=100)
correlation_estimates = estimator.estimate_correlations(returns_df)

# 3. Create animation
animator = NetworkAnimator(figsize=(12, 10))
animator.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='my_animation.mp4',
    fps=10
)
```

## Parameters to Adjust

### Data Generation
- `n_assets`: Number of assets (default: 20)
- `total_days`: Number of days (default: 500)
- `window_size`: Rolling window size (default: 100)
- `volatility_process`: Rate of correlation change (default: 0.05)

### Filtering Methods
- `'mst'`: Minimum Spanning Tree (N-1 edges)
- `'pmfg'`: Planar Maximally Filtered Graph (3(N-2) edges)
- `'tmfg'`: Triangulated Maximally Filtered Graph (3(N-2) edges, faster)

### Animation
- `fps`: Frames per second (default: 10)
- `interval`: Milliseconds between frames (default: 100)
- `figsize`: Figure size in inches (default: (12, 10))

## Troubleshooting

### Error: "Python not found at /usr/local/bin/python3"

Edit `setup.sh` and change `PYTHON_PATH` to your Python location:
```bash
# Find Python location
which python3

# Edit setup.sh
# Change: PYTHON_PATH="/usr/local/bin/python3"
# To:     PYTHON_PATH="/your/python/path"
```

### Error: "ffmpeg not found"

Install ffmpeg (see Step 4 above). Without it, you cannot export video files.

### Error: "Module not found"

Make sure you activated the virtual environment:
```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### Animation runs slowly

For faster processing:
- Reduce `n_assets` (e.g., 15 instead of 30)
- Use `'tmfg'` instead of `'pmfg'`
- Sample fewer time points:
  ```python
  correlation_estimates_subset = correlation_estimates[::5]  # Every 5th frame
  ```

### Out of memory

- Reduce `n_assets`
- Reduce `total_days`
- Close other applications

## Expected Runtime

| Assets | Days | Windows | Method | Time (approx.) |
|--------|------|---------|--------|----------------|
| 20     | 500  | 400     | MST    | ~30 seconds    |
| 20     | 500  | 400     | PMFG   | ~2 minutes     |
| 20     | 500  | 400     | TMFG   | ~1 minute      |
| 30     | 500  | 400     | PMFG   | ~5 minutes     |
| 50     | 500  | 400     | TMFG   | ~3 minutes     |

## Output Files

After running the main script, you'll have:

1. **mst_network_animation.mp4** - MST network evolution
2. **pmfg_network_animation.mp4** - PMFG network evolution  
3. **tmfg_network_animation.mp4** - TMFG network evolution
4. **network_comparison.mp4** - Side-by-side comparison of all three methods

## Next Steps

1. **Read the full README.md** for detailed documentation
2. **Explore examples.ipynb** for interactive examples
3. **Try with your own data** - see README.md section "Using Your Own Data"
4. **Customize parameters** to see different behaviors
5. **Analyze network metrics** over time

## Getting Help

- Check **README.md** for comprehensive documentation
- Review **examples.ipynb** for working examples
- See the original research papers cited in README.md
- Check NetworkX documentation: https://networkx.org/

## Citation

If you use this code in research, please cite the original papers:

1. Tumminello, M., Aste, T., Di Matteo, T., & Mantegna, R. N. (2005). "A tool for filtering information in complex systems." *PNAS*, 102(30), 10421-10426.

2. Massara, G.P., Di Matteo, T., & Aste, T. (2016). "Network Filtering for Big Data: Triangulated Maximally Filtered Graph." *Journal of Complex Networks*, 5(2), 161-178.

---

**Enjoy exploring correlation networks! 🎉**
