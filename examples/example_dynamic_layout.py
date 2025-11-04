"""
Dynamic Layout Example
======================

This script demonstrates the difference between static and dynamic layouts
for network animations.

Dynamic Layout:
- Nodes move according to the force-directed layout algorithm
- Node positions adapt to changing edge structure as correlations evolve
- More visually engaging, shows how network structure changes

Static Layout:
- Nodes stay in fixed positions throughout the animation
- Only edges change as correlations evolve
- Easier to track individual nodes over time
"""

from correlation_network_animation import (
    SyntheticCorrelationGenerator,
    RollingCorrelationEstimator,
    NetworkAnimator
)

print("="*70)
print("Dynamic vs Static Layout Demonstration")
print("="*70)

# Generate synthetic data
print("\n1. Generating synthetic data...")
generator = SyntheticCorrelationGenerator(n_assets=15, seed=42)
returns_df, _ = generator.generate_time_series(
    total_days=300,
    window_size=60,
    volatility_process=0.08  # Higher volatility for more dramatic changes
)
print(f"   Generated {returns_df.shape[0]} days for {returns_df.shape[1]} assets")

# Estimate rolling correlations
print("\n2. Estimating rolling correlations...")
estimator = RollingCorrelationEstimator(window_size=60)
correlation_estimates = estimator.estimate_correlations(returns_df)
print(f"   Estimated {len(correlation_estimates)} correlation matrices")

# Create DYNAMIC layout animation
print("\n3. Creating DYNAMIC layout animation...")
print("   (Nodes move with force-directed layout)")
animator_dynamic = NetworkAnimator(figsize=(12, 10), dynamic_layout=True)

animator_dynamic.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='example_dynamic_layout.mp4',
    fps=15,
    interval=67,
    smoothing_factor=0.2,  # More responsive (lower = more movement)
    k_factor=2.5  # More spread out
)

# Create STATIC layout animation
print("\n4. Creating STATIC layout animation...")
print("   (Nodes stay in fixed positions)")
animator_static = NetworkAnimator(figsize=(12, 10), dynamic_layout=False)

animator_static.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='example_static_layout.mp4',
    fps=15,
    interval=67
)

print("\n" + "="*70)
print("Animations created!")
print("="*70)
print("\nCompare the two animations:")
print("  - example_dynamic_layout.mp4  (nodes move)")
print("  - example_static_layout.mp4   (nodes fixed)")
print("\nNotice how in the dynamic version:")
print("  • Nodes migrate toward/away from each other")
print("  • Clusters form and dissolve dynamically")
print("  • Overall network structure visibly changes")
print("  • More engaging but harder to track individual nodes")
print("\nIn the static version:")
print("  • Easy to track individual nodes")
print("  • Focus is on changing edges")
print("  • Less visual movement")
print("  • Better for detailed analysis of specific nodes")
print("="*70)

print("\n\nTIP: Adjust smoothing_factor to control movement:")
print("  smoothing_factor=0.0  → Very responsive, lots of movement")
print("  smoothing_factor=0.3  → Balanced (default)")
print("  smoothing_factor=0.5  → Smoother, less movement")
print("  smoothing_factor=0.8  → Very smooth, minimal movement")
print("  smoothing_factor=1.0  → No movement (equivalent to static)")
