# Project Structure

## Files Overview

```
correlation-network-filtering/
├── setup.sh                              # Setup script (creates venv, installs packages)
├── test_installation.py                  # Verify installation and functionality
├── correlation_network_animation.py      # Main implementation
├── requirements.txt                      # Python dependencies
├── examples.ipynb                        # Jupyter notebook with examples
├── README.md                             # Full documentation
├── QUICKSTART.md                         # Quick start guide
└── PROJECT_STRUCTURE.md                  # This file
```

## File Descriptions

### 1. setup.sh
**Purpose**: Automated environment setup
**Usage**: `./setup.sh`
**What it does**:
- Creates a Python virtual environment named `venv`
- Installs all required packages from requirements.txt
- Optionally installs Jupyter Notebook
- Checks for ffmpeg installation
- Uses Python at `/usr/local/bin/python3` (configurable)

**Key features**:
- Interactive prompts for optional installations
- Version checking
- Error handling
- Clear status messages

### 2. test_installation.py
**Purpose**: Verify installation
**Usage**: `python test_installation.py`
**What it tests**:
- Python version (requires 3.8+)
- All required packages and their versions
- ffmpeg availability
- Basic functionality of all classes
- Data generation, correlation estimation, filtering

**Output**: Clear pass/fail for each component

### 3. correlation_network_animation.py
**Purpose**: Main implementation
**Size**: ~1000 lines
**Classes**:

#### SyntheticCorrelationGenerator
- Generates synthetic time series with evolving correlations
- Uses Ornstein-Uhlenbeck diffusion process
- Creates block/sector structure
- Ensures positive semi-definite matrices

**Key methods**:
```python
generate_base_correlation_matrix()  # Create initial correlation structure
evolve_correlation_parameters()     # Evolve correlations over time
generate_returns()                   # Generate multivariate normal returns
generate_time_series()               # Complete pipeline
```

#### RollingCorrelationEstimator
- Estimates correlation matrices using moving windows
- Handles pandas DataFrames with DatetimeIndex

**Key methods**:
```python
estimate_correlations()  # Compute rolling correlations
```

#### CorrelationFilter
- Implements network filtering algorithms
- Static methods for different filtering approaches

**Key methods**:
```python
correlation_to_distance()                    # Convert correlation to distance metric
minimum_spanning_tree()                      # MST filtering
planar_maximally_filtered_graph()           # PMFG filtering
triangulated_maximally_filtered_graph()     # TMFG filtering
```

#### NetworkAnimator
- Creates animations and visualizations
- Handles graph layouts and rendering

**Key methods**:
```python
create_stable_layout()              # Compute stable node positions
setup_node_colors()                 # Assign colors to nodes
animate_filtered_networks()         # Create single-method animation
create_comparison_animation()       # Create side-by-side comparison
```

### 4. requirements.txt
**Purpose**: List of Python dependencies
**Packages**:
- numpy >= 1.21.0 (numerical computing)
- pandas >= 1.3.0 (data manipulation)
- scipy >= 1.7.0 (scientific computing)
- networkx >= 2.6.0 (graph algorithms)
- matplotlib >= 3.4.0 (plotting and animation)

**Note**: Jupyter is optional and installed via setup.sh

### 5. examples.ipynb
**Purpose**: Interactive tutorial
**Sections**:
1. Data generation with visualizations
2. Rolling correlation estimation
3. Network filtering comparison
4. Network statistics and analysis
5. Time series evolution analysis
6. Animation creation
7. Data export

**Features**:
- Step-by-step explanations
- Visualizations at each stage
- Customizable parameters
- Export functionality

### 6. README.md
**Purpose**: Comprehensive documentation
**Sections**:
- Overview and features
- Installation instructions
- Quick start guide
- Detailed usage examples
- Mathematical background
- Performance considerations
- Troubleshooting
- References to original research

**Size**: ~400 lines of detailed documentation

### 7. QUICKSTART.md
**Purpose**: Get started quickly
**Sections**:
- Installation steps
- Basic usage example
- Parameter descriptions
- Troubleshooting
- Expected runtimes

**Audience**: Users who want to run the code immediately

### 8. PROJECT_STRUCTURE.md
**Purpose**: This file - project organization guide

## Workflow

### Initial Setup
```bash
# 1. Run setup script
./setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Test installation
python test_installation.py
```

### Usage Patterns

#### Pattern 1: Quick Demo
```bash
# Run main script with defaults
python correlation_network_animation.py
```
**Output**: 4 MP4 animation files

#### Pattern 2: Interactive Exploration
```bash
# Open Jupyter notebook
jupyter notebook examples.ipynb
```
**Use case**: Learning, experimentation, visualization

#### Pattern 3: Custom Analysis
```python
# Import as library
from correlation_network_animation import *

# Your custom code
```
**Use case**: Integration into existing projects

#### Pattern 4: Real Data Analysis
```python
# Load your data
import pandas as pd
returns_df = pd.read_csv('your_data.csv', 
                         index_col=0, 
                         parse_dates=True)

# Estimate and filter
estimator = RollingCorrelationEstimator(window_size=252)
correlations = estimator.estimate_correlations(returns_df)

# Create animation
animator = NetworkAnimator()
animator.animate_filtered_networks(correlations, 
                                  filter_method='pmfg',
                                  output_file='market_analysis.mp4')
```

## Dependencies

### System Requirements
- **Python**: 3.8 or higher
- **ffmpeg**: Required for video export
- **Operating System**: Linux, macOS, or Windows (with bash)

### Python Packages
All handled by setup.sh and requirements.txt

### Optional
- **Jupyter**: For interactive notebook (installed via setup.sh prompt)
- **Git**: For version control (recommended)

## Output Files

### From Main Script
Running `python correlation_network_animation.py` creates:

1. **mst_network_animation.mp4**
   - MST filtered network evolution
   - N-1 edges per frame
   - Hierarchical structure

2. **pmfg_network_animation.mp4**
   - PMFG filtered network evolution
   - 3(N-2) edges per frame
   - Planar topology

3. **tmfg_network_animation.mp4**
   - TMFG filtered network evolution
   - 3(N-2) edges per frame
   - Fast computation

4. **network_comparison.mp4**
   - Side-by-side comparison
   - All three methods synchronized
   - Same time axis

### From Notebook
Running the Jupyter notebook can create:
- Custom animation files
- Static visualizations (PNG)
- Network metrics CSV files
- Correlation matrices CSV files

## Customization Points

### Easy to Modify
- Number of assets (n_assets)
- Time period (total_days)
- Rolling window size (window_size)
- Filtering method ('mst', 'pmfg', 'tmfg')
- Animation parameters (fps, interval, figsize)

### Moderate Difficulty
- Correlation evolution dynamics
- Graph layout algorithms
- Node coloring schemes
- Network metrics to track

### Advanced
- New filtering methods
- Alternative correlation measures
- Custom animation styles
- Real-time processing

## Performance Notes

### Computational Complexity
- **MST**: O(N² log N) - Fast
- **PMFG**: O(N³) - Moderate
- **TMFG**: O(N²) - Fast

### Memory Usage
- Scales with: N × number_of_windows
- Example: 50 assets × 500 windows ≈ 200 MB

### Optimization Tips
1. Use TMFG for large N
2. Sample time points for long series
3. Reduce fps for faster rendering
4. Close other applications

## Version Information

- **Created**: 2024
- **Python**: 3.8+
- **Based on**: Research by Aste et al. (2005-2024)

## License Notes

- Code provided for educational/research use
- Please cite original papers in research
- See README.md for full citations

## Getting Help

1. Read QUICKSTART.md for common issues
2. Check README.md for detailed documentation
3. Run test_installation.py to diagnose problems
4. Review examples.ipynb for working code
5. Check original research papers for methodology

## Contributing

Potential extensions:
- Additional filtering methods (DBHT, higher genus)
- Alternative distance metrics
- Interactive visualizations (plotly, dash)
- Real-time streaming support
- GPU acceleration
- Additional network metrics
- Community detection algorithms
- Portfolio optimization integration

## Contact

For implementation questions:
- Check NetworkX documentation
- Review the code comments
- See examples in notebook

For methodology questions:
- Read original research papers
- Visit: https://www.ucl.ac.uk/~ucahtas/

---

*This project structure document provides a complete overview of the codebase organization and usage patterns.*
