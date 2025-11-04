# Dynamic Force-Directed Layout Feature

## Overview

The updated `NetworkAnimator` class now supports **dynamic force-directed layouts** where node positions evolve over time based on the changing correlation structure, rather than remaining fixed throughout the animation.

## What's New?

### Dynamic Layout Mode (NEW!)
- Nodes move according to a force-directed graph layout algorithm
- Positions adapt frame-by-frame as edge structure changes
- Visualizes how network topology evolves with correlations
- More engaging and intuitive for seeing structural changes

### Static Layout Mode (Original)
- Nodes remain in fixed positions
- Only edges change as correlations evolve
- Easier to track individual nodes
- Better for detailed node-level analysis

## Key Differences

| Feature | Dynamic Layout | Static Layout |
|---------|---------------|---------------|
| Node positions | Move with each frame | Fixed throughout |
| Visual engagement | High - shows structure evolution | Moderate - focus on edges |
| Node tracking | Harder - nodes move | Easy - nodes stay put |
| Best for | Understanding topology changes | Analyzing specific nodes |
| Computation | Slightly slower | Faster |
| Smoothness control | Adjustable (smoothing_factor) | N/A |

## Usage

### Basic Example - Dynamic Layout

```python
from correlation_network_animation import NetworkAnimator

# Create animator with dynamic layout (default)
animator = NetworkAnimator(figsize=(12, 10), dynamic_layout=True)

animator.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='dynamic_network.mp4',
    fps=10,
    smoothing_factor=0.3,  # Control transition smoothness
    k_factor=2.0  # Control node spacing
)
```

### Basic Example - Static Layout

```python
# Create animator with static layout
animator = NetworkAnimator(figsize=(12, 10), dynamic_layout=False)

animator.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='static_network.mp4',
    fps=10
)
```

## Parameters

### NetworkAnimator Initialization

```python
NetworkAnimator(figsize=(12, 10), dynamic_layout=True)
```

**Parameters:**
- `figsize` (tuple): Figure size (width, height) in inches
- `dynamic_layout` (bool): 
  - `True`: Nodes move with force-directed layout (NEW!)
  - `False`: Nodes stay in fixed positions (original behavior)

### animate_filtered_networks - New Parameters

```python
animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='animation.mp4',
    fps=10,
    interval=100,
    smoothing_factor=0.3,  # NEW! Only for dynamic_layout=True
    k_factor=2.0           # NEW! Only for dynamic_layout=True
)
```

**New Dynamic Layout Parameters:**

- **`smoothing_factor`** (float, 0 to 1): Controls transition smoothness
  - `0.0`: Fully responsive - nodes jump to optimal positions immediately
  - `0.3`: Balanced (default) - smooth but responsive
  - `0.5`: Smoother transitions - less dramatic movement
  - `0.8`: Very smooth - minimal movement
  - `1.0`: No movement (equivalent to static layout)
  
- **`k_factor`** (float): Controls optimal distance between nodes
  - `1.0`: Compact layout - nodes close together
  - `2.0`: Balanced spacing (default)
  - `3.0`: Spread out - more space between nodes
  - Higher values = more spread out network

## How It Works

### Force-Directed Layout Algorithm

The dynamic layout uses NetworkX's spring layout algorithm, which:

1. **Treats edges as springs**: Connected nodes attract each other
2. **Nodes repel each other**: All nodes push each other away
3. **Minimizes energy**: System settles to optimal configuration
4. **Frame-by-frame evolution**: Each frame's layout starts from previous frame's positions

### Smoothing Process

To prevent jarring transitions:

```python
smoothed_position = (smoothing_factor × old_position) + 
                   ((1 - smoothing_factor) × new_position)
```

This weighted average ensures smooth, continuous movement.

## Examples

### Example 1: Compare Dynamic vs Static

```python
from correlation_network_animation import (
    SyntheticCorrelationGenerator,
    RollingCorrelationEstimator,
    NetworkAnimator
)

# Generate data
generator = SyntheticCorrelationGenerator(n_assets=20)
returns_df, _ = generator.generate_time_series(total_days=500)

# Estimate correlations
estimator = RollingCorrelationEstimator(window_size=100)
correlations = estimator.estimate_correlations(returns_df)

# Dynamic version
animator_dynamic = NetworkAnimator(dynamic_layout=True)
animator_dynamic.animate_filtered_networks(
    correlations,
    filter_method='pmfg',
    output_file='pmfg_dynamic.mp4',
    smoothing_factor=0.3
)

# Static version
animator_static = NetworkAnimator(dynamic_layout=False)
animator_static.animate_filtered_networks(
    correlations,
    filter_method='pmfg',
    output_file='pmfg_static.mp4'
)
```

### Example 2: Highly Responsive Layout

```python
# Very responsive to changes (more movement)
animator = NetworkAnimator(dynamic_layout=True)
animator.animate_filtered_networks(
    correlations,
    filter_method='pmfg',
    output_file='pmfg_responsive.mp4',
    smoothing_factor=0.1,  # Low = more responsive
    k_factor=2.5  # Spread out
)
```

### Example 3: Smooth, Gradual Changes

```python
# Very smooth transitions (less movement)
animator = NetworkAnimator(dynamic_layout=True)
animator.animate_filtered_networks(
    correlations,
    filter_method='pmfg',
    output_file='pmfg_smooth.mp4',
    smoothing_factor=0.6,  # High = smoother
    k_factor=1.5  # Compact
)
```

### Example 4: Crisis Period Analysis

```python
# Use high volatility data to see dramatic structure changes
generator = SyntheticCorrelationGenerator(n_assets=25)
returns_df, _ = generator.generate_time_series(
    total_days=600,
    volatility_process=0.15  # Higher volatility = more dramatic changes
)

estimator = RollingCorrelationEstimator(window_size=80)
correlations = estimator.estimate_correlations(returns_df)

# Dynamic layout will show clustering/dispersal during crisis
animator = NetworkAnimator(dynamic_layout=True)
animator.animate_filtered_networks(
    correlations,
    filter_method='pmfg',
    output_file='crisis_analysis.mp4',
    smoothing_factor=0.25,  # Responsive enough to see changes
    k_factor=2.0
)
```

## Performance Considerations

### Computation Time

- **Dynamic layout**: ~20-30% slower than static due to layout calculations
- **Per-frame layout**: ~10 spring layout iterations per frame
- **Total time**: Still reasonable for typical datasets

### Recommendations

| Dataset Size | Recommended Settings |
|--------------|---------------------|
| N ≤ 20 assets | Any settings work well |
| 20 < N ≤ 50 | Use TMFG, smoothing_factor=0.3 |
| N > 50 | Consider static layout or sample frames |

### Optimization Tips

1. **Reduce frames**: Sample every Nth correlation estimate
   ```python
   correlations_subset = correlations[::5]  # Every 5th frame
   ```

2. **Use faster methods**: TMFG is faster than PMFG
   ```python
   filter_method='tmfg'  # Faster filtering
   ```

3. **Adjust iterations**: Fewer iterations per frame
   ```python
   # In compute_dynamic_layouts():
   iterations_per_frame=5  # Default is 10
   ```

## When to Use Each Mode

### Use Dynamic Layout When:
- ✓ Presenting to audiences (more engaging)
- ✓ Exploring overall structure evolution
- ✓ Understanding topology changes
- ✓ Detecting cluster formation/dissolution
- ✓ Creating visually appealing demonstrations

### Use Static Layout When:
- ✓ Tracking specific nodes over time
- ✓ Analyzing individual node behavior
- ✓ Comparing specific assets
- ✓ Detailed technical analysis
- ✓ Working with very large networks (>50 nodes)
- ✓ Need faster computation

## Comparison Animations

The `create_comparison_animation()` method also supports dynamic layouts:

```python
animator = NetworkAnimator(dynamic_layout=True)
animator.create_comparison_animation(
    correlations,
    output_file='comparison_dynamic.mp4',
    fps=10,
    smoothing_factor=0.3
)
```

This creates side-by-side comparison of MST, PMFG, and TMFG with all three using dynamic layouts.

## Troubleshooting

### Nodes moving too much / animation is jittery
- **Solution**: Increase `smoothing_factor` (try 0.5 or 0.6)
- **Reason**: Lower smoothing = more responsive = more movement

### Nodes barely moving / looks static
- **Solution**: Decrease `smoothing_factor` (try 0.1 or 0.2)
- **Reason**: Higher smoothing = smoother = less movement

### Nodes too close together
- **Solution**: Increase `k_factor` (try 2.5 or 3.0)
- **Reason**: Higher k = more spacing between nodes

### Nodes too spread out
- **Solution**: Decrease `k_factor` (try 1.0 or 1.5)
- **Reason**: Lower k = more compact layout

### Animation takes too long
- **Solution 1**: Use static layout instead
- **Solution 2**: Reduce number of frames
- **Solution 3**: Use TMFG instead of PMFG

## Technical Details

### Algorithm Flow

For each frame in dynamic mode:

1. **Start with previous positions**: Use frame t-1 positions as starting point
2. **Run spring layout**: Execute spring layout algorithm for N iterations
3. **Apply smoothing**: Blend old and new positions using smoothing_factor
4. **Update positions**: Store smoothed positions for this frame
5. **Render frame**: Draw network at current positions

### Mathematical Details

**Spring Force Between Connected Nodes:**
```
F_spring = k × (d - optimal_distance)
```
Where `optimal_distance = k_factor / sqrt(n_nodes)`

**Repulsion Force Between All Nodes:**
```
F_repel = 1 / d²
```

**Position Update:**
```
new_pos = old_pos + Σ forces
smoothed_pos = α × old_pos + (1-α) × new_pos
```
Where α = smoothing_factor

## Output Files

When running the main script, you'll get:

### Dynamic Layout Files (NEW!)
- `mst_network_animation_dynamic.mp4`
- `pmfg_network_animation_dynamic.mp4`
- `tmfg_network_animation_dynamic.mp4`
- `network_comparison_dynamic.mp4`

### Static Layout Files
- `network_comparison_static.mp4`

## Summary

The dynamic force-directed layout feature adds a new dimension to correlation network visualization by showing how node positions naturally evolve with the underlying correlation structure. This makes animations more intuitive and engaging while maintaining the option for traditional static layouts when precise node tracking is needed.

**Key Takeaways:**
- Set `dynamic_layout=True` for moving nodes
- Adjust `smoothing_factor` to control movement smoothness
- Adjust `k_factor` to control node spacing
- Use dynamic for presentations, static for analysis
- Both modes produce scientifically valid visualizations

---

*Feature added: November 2024*  
*Compatible with all filtering methods: MST, PMFG, TMFG*
