# Animated Correlation Network Filtering

A Python implementation for creating animations of filtered correlation networks over time, based on the geometric filtering methods developed by Tomaso Aste and colleagues.

## Overview

This code provides a complete pipeline for:

1. **Generating synthetic time series** with time-varying correlation structures
2. **Estimating rolling correlation matrices** using moving windows
3. **Applying network filtering methods**: MST, PMFG, and TMFG
4. **Creating animations** of the evolving network structure

## Features

### Synthetic Data Generation
- Time-varying correlation matrices using diffusion processes
- Ornstein-Uhlenbeck mean-reversion dynamics
- Block/sector structure with realistic correlation patterns
- Ensures positive semi-definite correlation matrices

### Network Filtering Methods

1. **Minimum Spanning Tree (MST)**
   - N-1 edges
   - Hierarchical tree structure
   - Fast computation: O(N² log N)

2. **Planar Maximally Filtered Graph (PMFG)**
   - 3(N-2) edges
   - Maintains planarity (no edge crossings)
   - Based on Tumminello et al. (2005) PNAS
   - Complexity: O(N³)

3. **Triangulated Maximally Filtered Graph (TMFG)**
   - 3(N-2) edges
   - Chordal planar graph
   - Faster than PMFG: O(N²)
   - Based on Massara et al. (2016)

### Animation Features
- **Dynamic Force-Directed Layout (NEW!)**: Nodes move according to evolving correlation structure
- **Static Layout**: Traditional fixed-position layout for node tracking
- Stable graph layouts across time with adjustable smoothing
- Edge thickness based on correlation strength
- Color-coded nodes by sector/cluster
- Multiple visualization modes (individual methods or side-by-side comparison)
- Exportable as MP4 videos
- Configurable smoothing and spacing parameters

## Installation

```bash
pip install -r requirements.txt
```

### Requirements
- numpy >= 1.21.0
- pandas >= 1.3.0
- scipy >= 1.7.0
- networkx >= 2.6.0
- matplotlib >= 3.4.0
- ffmpeg (for video export)

**Note**: You need `ffmpeg` installed on your system for creating video animations:
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from https://ffmpeg.org/download.html

## Quick Start

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
    window_size=100,
    volatility_process=0.05
)

# 2. Estimate rolling correlations
estimator = RollingCorrelationEstimator(window_size=100)
correlation_estimates = estimator.estimate_correlations(returns_df)

# 3. Create animation with DYNAMIC layout (NEW!)
# Nodes move according to force-directed layout
animator = NetworkAnimator(figsize=(12, 10), dynamic_layout=True)
animator.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='pmfg_animation.mp4',
    fps=10,
    smoothing_factor=0.3  # Control movement smoothness
)
```

Or simply run the main script:

```bash
python correlation_network_animation.py
```

This will generate animations with both dynamic and static layouts:
- Dynamic layout files: `*_dynamic.mp4` (nodes move with network structure)
- Static layout file: `*_static.mp4` (nodes stay in fixed positions)

## Detailed Usage

### 1. Synthetic Data Generation

```python
generator = SyntheticCorrelationGenerator(n_assets=30, seed=42)

# Generate with block structure (sectors)
returns_df, true_correlations = generator.generate_time_series(
    total_days=1000,           # Total number of days
    window_size=252,           # Rolling window size
    volatility_process=0.05,   # Correlation evolution rate
    returns_per_day=1          # Observations per day
)
```

The generator creates:
- **Block structure**: Assets grouped into sectors with higher intra-sector correlations
- **Time-varying correlations**: Smooth evolution using diffusion process
- **Mean reversion**: Correlations tend to revert to base levels
- **Valid matrices**: Ensures positive semi-definite correlation matrices

### 2. Using Your Own Data

If you have real market data:

```python
import pandas as pd

# Load your returns data
returns_df = pd.read_csv('your_returns.csv', index_col=0, parse_dates=True)
# Ensure DatetimeIndex and returns in columns

# Estimate rolling correlations
estimator = RollingCorrelationEstimator(window_size=252)
correlation_estimates = estimator.estimate_correlations(returns_df)

# Create animation
animator = NetworkAnimator()
animator.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='market_pmfg.mp4'
)
```

### 3. Filtering Methods

Apply different filtering methods to the same correlation matrix:

```python
from correlation_network_animation import CorrelationFilter

# Convert correlation to distance
distance_matrix = CorrelationFilter.correlation_to_distance(corr_matrix)

# Apply different filters
mst = CorrelationFilter.minimum_spanning_tree(distance_matrix)
pmfg = CorrelationFilter.planar_maximally_filtered_graph(distance_matrix)
tmfg = CorrelationFilter.triangulated_maximally_filtered_graph(distance_matrix)

print(f"MST edges: {mst.number_of_edges()}")
print(f"PMFG edges: {pmfg.number_of_edges()}")
print(f"TMFG edges: {tmfg.number_of_edges()}")
```

### 4. Customizing Animations

```python
animator = NetworkAnimator(figsize=(14, 12))

# Customize node colors
animator.setup_node_colors(n_nodes=20, n_clusters=4)

# Create animation with custom parameters
animator.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='custom_animation.mp4',
    fps=15,              # Frames per second
    interval=50          # Milliseconds between frames
)
```

### 5. Creating Comparison Videos

Compare all three methods side-by-side:

```python
animator.create_comparison_animation(
    correlation_estimates,
    output_file='comparison.mp4',
    fps=10
)
```

## Understanding the Output

### Network Metrics in Animations

Each frame shows:
- **Date**: Current time window end date
- **Edges**: Number of edges in filtered network
- **Average Degree**: Mean number of connections per node

### Edge Visualization
- **Thickness**: Thicker edges indicate stronger correlations (shorter distances)
- **Alpha**: Semi-transparent to show network structure clearly

### Node Colors
- Nodes are colored by sector/cluster assignment
- Colors remain consistent across frames for easier tracking

## Examples and Use Cases

### Example 1: Market Stress Analysis

Monitor how network structure changes during crisis periods:

```python
# Generate data with crisis period
generator = SyntheticCorrelationGenerator(n_assets=30)
returns_df, _ = generator.generate_time_series(total_days=1000)

# Add crisis: increase correlations for period
crisis_start = 500
crisis_end = 550
returns_df.iloc[crisis_start:crisis_end] *= 1.5  # Increase volatility

# Estimate and animate
estimator = RollingCorrelationEstimator(window_size=100)
corr_estimates = estimator.estimate_correlations(returns_df)

animator = NetworkAnimator()
animator.animate_filtered_networks(corr_estimates, filter_method='pmfg',
                                  output_file='crisis_analysis.mp4')
```

### Example 2: Comparing Different Window Sizes

```python
window_sizes = [50, 100, 250]

for window_size in window_sizes:
    estimator = RollingCorrelationEstimator(window_size=window_size)
    corr_estimates = estimator.estimate_correlations(returns_df)
    
    animator = NetworkAnimator()
    animator.animate_filtered_networks(
        corr_estimates,
        filter_method='pmfg',
        output_file=f'pmfg_window_{window_size}.mp4'
    )
```

### Example 3: Export Network Metrics Over Time

```python
import pandas as pd

metrics = []
for est in correlation_estimates:
    corr = est['correlation']
    dist = CorrelationFilter.correlation_to_distance(corr)
    
    # Create filtered graphs
    mst = CorrelationFilter.minimum_spanning_tree(dist)
    pmfg = CorrelationFilter.planar_maximally_filtered_graph(dist)
    
    metrics.append({
        'date': est['date'],
        'mst_total_weight': sum(d['weight'] for _, _, d in mst.edges(data=True)),
        'pmfg_total_weight': sum(d['weight'] for _, _, d in pmfg.edges(data=True)),
        'mst_avg_degree': 2 * mst.number_of_edges() / mst.number_of_nodes(),
        'pmfg_avg_degree': 2 * pmfg.number_of_edges() / pmfg.number_of_nodes(),
    })

metrics_df = pd.DataFrame(metrics)
metrics_df.to_csv('network_metrics.csv', index=False)
```

## Performance Considerations

### Computational Complexity

| Method | Complexity | Time for N=100 | Time for N=500 |
|--------|-----------|----------------|----------------|
| MST    | O(N² log N) | <1 second    | ~5 seconds     |
| PMFG   | O(N³)      | ~2 seconds   | ~2 minutes     |
| TMFG   | O(N²)      | <1 second    | ~10 seconds    |

### Recommendations

- **N < 50**: All methods are fast, use PMFG for best results
- **50 ≤ N < 200**: PMFG is fine, consider TMFG for faster processing
- **N ≥ 200**: Use TMFG or MST for reasonable computation times
- **Very large N (>1000)**: MST only, or sample/cluster assets first

### Optimizing Animation Creation

For long time series:
```python
# Process every Nth frame to reduce computation
correlation_estimates_subset = correlation_estimates[::5]  # Every 5th frame

animator.animate_filtered_networks(
    correlation_estimates_subset,
    filter_method='tmfg',  # Use faster TMFG
    output_file='fast_animation.mp4'
)
```

## Mathematical Background

### Distance Metric

The correlation-to-distance transformation:
```
d_ij = sqrt(2(1 - ρ_ij))
```

Properties:
- d ∈ [0, 2]
- d = 0 when ρ = 1 (perfect correlation)
- d = √2 when ρ = 0 (no correlation)
- d = 2 when ρ = -1 (perfect anti-correlation)
- Satisfies triangle inequality (true metric)

### Planarity Constraint

A graph is planar if it can be drawn on a plane without edge crossings.

**Kuratowski's Theorem**: A graph is planar iff it contains no subgraph homeomorphic to:
- K₅ (complete graph on 5 nodes)
- K₃,₃ (complete bipartite graph 3-3)

**Maximum edges in planar graph**: 3(n-2) for n ≥ 3

### Why Filtering Works

1. **Noise reduction**: Most correlations are spurious/noise
2. **Structure preservation**: Filtering keeps strongest relationships
3. **Interpretability**: Sparse networks are easier to analyze
4. **Stability**: Filtered networks are more stable over time

## References

### Key Papers

1. **Tumminello, M., Aste, T., Di Matteo, T., & Mantegna, R. N. (2005)**. "A tool for filtering information in complex systems." *PNAS*, 102(30), 10421-10426.
   - Original PMFG paper

2. **Massara, G.P., Di Matteo, T., & Aste, T. (2016)**. "Network Filtering for Big Data: Triangulated Maximally Filtered Graph." *Journal of Complex Networks*, 5(2), 161-178.
   - TMFG algorithm

3. **Mantegna, R. N. (1999)**. "Hierarchical structure in financial markets." *European Physical Journal B*, 11(1), 193-197.
   - MST for financial markets

4. **Musmeci, N., Aste, T., & Di Matteo, T. (2015)**. "Risk diversification: A study of persistence with a filtered correlation-network approach." *Journal of Network Theory in Finance*, 1(1), 77-98.
   - Dynamic correlation networks

## Troubleshooting

### Common Issues

**Issue**: "ffmpeg not found"
- **Solution**: Install ffmpeg system-wide (see Installation section)

**Issue**: Animation is too slow/fast
- **Solution**: Adjust `fps` and `interval` parameters:
  ```python
  animator.animate_filtered_networks(..., fps=20, interval=50)
  ```

**Issue**: Graph layout looks chaotic
- **Solution**: Try different layout methods:
  ```python
  pos = animator.create_stable_layout(graphs, method='circular')
  ```

**Issue**: Out of memory for large networks
- **Solution**: 
  - Reduce number of assets
  - Use subset of time points
  - Use TMFG or MST instead of PMFG

**Issue**: PMFG taking too long
- **Solution**: Use TMFG instead, or limit iterations:
  ```python
  pmfg = CorrelationFilter.planar_maximally_filtered_graph(
      distance_matrix, 
      max_iterations=10000
  )
  ```

## License

This code is provided for educational and research purposes. Please cite the original papers by Aste and colleagues when using these methods in your research.

## Contributing

Feel free to extend this code with:
- Additional filtering methods (DBHT, higher genus graphs)
- Alternative correlation measures (Spearman, Kendall, mutual information)
- Interactive visualizations
- Real-time streaming data support
- Additional network metrics and analysis

## Contact

For questions about the implementation, please refer to the original papers or NetworkX documentation.

For questions about the mathematical methods, see:
- Tomaso Aste's research page: https://www.ucl.ac.uk/~ucahtas/
- NetworkX documentation: https://networkx.org/

---

*Code created: 2024*
*Based on research by Tomaso Aste, Tiziana Di Matteo, Rosario Mantegna, and colleagues*
