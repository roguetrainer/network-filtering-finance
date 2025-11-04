# Triangle Shading Feature - Documentation

## Overview

The triangle shading feature identifies and colors all triangular faces (3-cliques) in PMFG and TMFG networks based on their average correlation strength. This visualization enhancement reveals:

- **Local correlation clusters**: Red regions show high correlation groups
- **Planar structure**: Makes the 2D embedding more apparent
- **Correlation density**: Shows where strong relationships cluster
- **Temporal evolution**: Watch correlation patterns change in animations

## Quick Start

### Basic Usage

```python
from correlation_network_animation import NetworkAnimator

# Create animator with triangle shading enabled
animator = NetworkAnimator(shade_triangles=True)

# Create animated visualization
animator.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='network_with_triangles.mp4',
    triangle_alpha=0.3,  # Transparency
    triangle_cmap='RdYlBu_r'  # Colormap
)
```

### Static Visualization

```python
# Create single frame with shaded triangles
animator = NetworkAnimator()

animator.visualize_network_with_triangles(
    correlation_matrix,
    filter_method='pmfg',
    output_file='pmfg_triangles.png',
    triangle_alpha=0.35,
    triangle_cmap='RdYlBu_r'
)
```

## API Reference

### NetworkAnimator Constructor

```python
NetworkAnimator(figsize=(12, 10), dynamic_layout=True, shade_triangles=False)
```

**New Parameter:**
- `shade_triangles` (bool): Enable triangle shading in animations. Default: `False`

**Example:**
```python
# With triangle shading
animator = NetworkAnimator(shade_triangles=True)

# Without triangle shading (default)
animator = NetworkAnimator(shade_triangles=False)
```

### animate_filtered_networks()

```python
animator.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='network.mp4',
    fps=10,
    interval=100,
    smoothing_factor=0.3,
    k_factor=2.0,
    triangle_alpha=0.3,      # NEW
    triangle_cmap='RdYlBu_r' # NEW
)
```

**New Parameters:**
- `triangle_alpha` (float): Transparency of triangular faces, range [0, 1]. Default: 0.3
  - 0.0 = fully transparent (invisible)
  - 0.5 = semi-transparent
  - 1.0 = fully opaque
  
- `triangle_cmap` (str): Matplotlib colormap name. Default: 'RdYlBu_r'
  - Recommended: 'RdYlBu_r', 'coolwarm', 'RdBu_r' (diverging colormaps)
  - See [Matplotlib Colormaps](https://matplotlib.org/stable/tutorials/colors/colormaps.html)

**Note:** These parameters only take effect when `shade_triangles=True`

### visualize_network_with_triangles()

```python
animator.visualize_network_with_triangles(
    correlation_matrix,
    filter_method='pmfg',
    output_file='network_triangles.png',
    title=None,
    figsize=None,
    triangle_alpha=0.35,
    triangle_cmap='RdYlBu_r'
)
```

**Parameters:**
- `correlation_matrix` (np.ndarray): N×N correlation matrix
- `filter_method` (str): 'mst', 'pmfg', or 'tmfg'
- `output_file` (str): Output filename (PNG, PDF, etc.)
- `title` (str, optional): Custom title. Auto-generated if None
- `figsize` (tuple, optional): Figure size (width, height)
- `triangle_alpha` (float): Transparency of triangles
- `triangle_cmap` (str): Colormap name

**Returns:** `fig, ax` (matplotlib figure and axis objects)

**Example:**
```python
animator = NetworkAnimator()
fig, ax = animator.visualize_network_with_triangles(
    corr_matrix,
    filter_method='pmfg',
    output_file='my_network.png',
    title='Custom Network Title',
    triangle_alpha=0.4,
    triangle_cmap='coolwarm'
)
```

### draw_shaded_triangles()

Lower-level method for custom visualizations:

```python
animator.draw_shaded_triangles(
    G,                    # networkx.Graph
    pos,                  # Node positions dict
    ax,                   # matplotlib axis
    correlation_matrix,   # Optional correlation matrix
    alpha=0.3,           # Transparency
    cmap='RdYlBu_r'      # Colormap
)
```

**Use case:** When building custom visualizations

**Example:**
```python
import networkx as nx
import matplotlib.pyplot as plt

# Create graph and layout
G = CorrelationFilter.planar_maximally_filtered_graph(distance_matrix)
pos = nx.spring_layout(G)

# Create figure
fig, ax = plt.subplots(figsize=(12, 10))

# Draw triangles
animator.draw_shaded_triangles(G, pos, ax, corr_matrix, alpha=0.3)

# Draw network on top
nx.draw_networkx(G, pos, ax=ax)
```

## Color Interpretation

### Colormap: RdYlBu_r (Default, Recommended)

| Color | Correlation | Interpretation |
|-------|-------------|----------------|
| **Dark Red** | +0.8 to +1.0 | Very strong positive correlation |
| **Orange** | +0.5 to +0.8 | Strong positive correlation |
| **Yellow** | +0.2 to +0.5 | Moderate positive correlation |
| **Light Green** | -0.2 to +0.2 | Weak/no correlation |
| **Light Blue** | -0.5 to -0.2 | Moderate negative correlation |
| **Dark Blue** | -1.0 to -0.5 | Strong negative correlation |

### Alternative Colormaps

**coolwarm** - Blue (low correlation) to Red (high correlation)
```python
triangle_cmap='coolwarm'
```

**RdBu_r** - Similar to RdYlBu_r but without yellow
```python
triangle_cmap='RdBu_r'
```

**viridis** - Sequential, purple to yellow (not ideal for correlations)
```python
triangle_cmap='viridis'
```

## Use Cases

### 1. Market Structure Analysis

```python
# Visualize correlation structure in financial markets
animator = NetworkAnimator(shade_triangles=True)

# PMFG reveals sectors as red triangle clusters
animator.visualize_network_with_triangles(
    market_correlations,
    filter_method='pmfg',
    output_file='market_structure.png'
)
```

**Interpretation:**
- Red clusters = Sectors (tech, finance, energy)
- Blue areas = Diversification opportunities
- Mixed colors = Transition zones

### 2. Crisis Detection

```python
# Animate to watch correlations increase during crisis
animator = NetworkAnimator(
    dynamic_layout=True,
    shade_triangles=True
)

animator.animate_filtered_networks(
    pre_and_during_crisis_correlations,
    filter_method='pmfg',
    output_file='crisis_evolution.mp4',
    triangle_alpha=0.35
)
```

**What to watch for:**
- Red spreading = Increasing systemic risk
- Triangle formation = New correlation clusters
- Color intensification = Stronger correlations

### 3. Portfolio Diversification

```python
# Find assets with weak correlations (blue triangles)
animator = NetworkAnimator()

animator.visualize_network_with_triangles(
    portfolio_correlations,
    filter_method='pmfg',
    output_file='diversification.png',
    triangle_alpha=0.4
)
```

**Interpretation:**
- Blue triangles = Good diversification candidates
- Red triangles = Correlated assets (redundant positions)
- Mixed = Partial hedges

## Performance Considerations

### Triangle Counting

The number of triangles grows with network density:

| Network | Nodes | Edges | Typical Triangles |
|---------|-------|-------|-------------------|
| MST | 20 | 19 | 0 (no triangles) |
| PMFG | 20 | 54 | ~35 |
| TMFG | 20 | 54 | ~35 |
| PMFG | 50 | 144 | ~95 |
| PMFG | 100 | 294 | ~195 |

### Performance Impact

**Static visualization:** Minimal impact (~5% slower)
**Animation:** Moderate impact (~10-20% slower per frame)

**Optimization tips:**
```python
# For large networks (N > 50), reduce alpha for clarity
animator.visualize_network_with_triangles(
    large_corr_matrix,
    triangle_alpha=0.25  # More transparent
)

# For animations, sample fewer frames
correlation_estimates_subset = correlation_estimates[::2]  # Every 2nd frame
```

## Best Practices

### 1. Choose Appropriate Alpha

```python
# Few triangles (N < 30): Higher alpha for visibility
triangle_alpha=0.4

# Many triangles (N > 50): Lower alpha to avoid saturation
triangle_alpha=0.25

# Overlapping triangles: Very low alpha
triangle_alpha=0.2
```

### 2. Select Right Colormap

```python
# For correlations: Always use diverging colormaps
triangle_cmap='RdYlBu_r'  # Best
triangle_cmap='coolwarm'  # Good
triangle_cmap='RdBu_r'    # Good

# Avoid sequential colormaps for correlations
# triangle_cmap='viridis'  # NOT recommended
```

### 3. Combine with Edge Thickness

```python
# Edge thickness shows pairwise correlations
# Triangle colors show local cluster strength
# Together: complete picture of network structure
```

### 4. Use with Dynamic Layouts

```python
# Dynamic layouts + triangle shading = powerful combination
animator = NetworkAnimator(
    dynamic_layout=True,    # Nodes move
    shade_triangles=True    # Triangles show structure
)

# Watch both structure AND positions evolve
```

## Troubleshooting

### Issue: Triangles not visible

**Solution:**
```python
# Increase alpha
triangle_alpha=0.5

# Check if network has triangles (MST has none)
filter_method='pmfg'  # or 'tmfg', not 'mst'
```

### Issue: Colors too saturated

**Solution:**
```python
# Reduce alpha
triangle_alpha=0.2

# Use different colormap
triangle_cmap='RdBu_r'  # Less yellow
```

### Issue: Animation is slow

**Solution:**
```python
# Sample fewer frames
estimates_subset = estimates[::5]  # Every 5th frame

# Reduce FPS
fps=5  # Instead of 10

# Use static layout (faster)
animator = NetworkAnimator(
    dynamic_layout=False,
    shade_triangles=True
)
```

### Issue: Can't distinguish triangle colors

**Solution:**
```python
# Increase figure size
figsize=(16, 14)  # Larger

# Adjust alpha
triangle_alpha=0.4  # More opaque

# Try different colormap
triangle_cmap='coolwarm'  # Simpler colors
```

## Examples

See `examples/example_triangle_shading.py` for comprehensive examples:

1. **Static visualization** - Single frame with triangles
2. **Animated visualization** - Evolution over time
3. **Comparison** - With/without triangle shading
4. **Colormap exploration** - Different color schemes

Run examples:
```bash
cd examples
python example_triangle_shading.py
```

## Technical Details

### Triangle Identification

Triangles are identified using NetworkX's clique enumeration:

```python
triangles = [clique for clique in nx.enumerate_all_cliques(G) 
             if len(clique) == 3]
```

### Correlation Calculation

Each triangle's color is determined by averaging the correlations of its three edges:

```python
# For triangle with nodes (i, j, k)
corr_ij = correlation_matrix[i, j]
corr_jk = correlation_matrix[j, k]
corr_ik = correlation_matrix[i, k]

avg_correlation = (corr_ij + corr_jk + corr_ik) / 3
```

### Rendering Order (Z-order)

1. Triangles (zorder=1) - Background
2. Edges (zorder=2) - Middle
3. Nodes (zorder=3) - Foreground
4. Labels (zorder=4) - Top

This ensures triangles don't obscure nodes or edges.

## References

For the theoretical foundation of triangle shading in network visualization:

1. **Tumminello et al. (2005)** - PMFG method and planar faces
2. **Massara et al. (2016)** - TMFG and triangulated structure
3. **Visualization principles** - From the shading triangular faces guide

## See Also

- Main documentation: `README.md`
- Example scripts: `examples/example_triangle_shading.py`
- Shading guide: `docs/shading_triangular_faces_guide.md` (original guide)
- Advanced: `docs/shading_all_cliques_guide.md` (all clique sizes)

---

*Last updated: November 2025*
