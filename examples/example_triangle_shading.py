#!/usr/bin/env python3
"""
Example: Triangle Shading in Network Visualizations
====================================================

This script demonstrates the new triangle shading feature that identifies
and colors triangular faces (3-cliques) in PMFG and TMFG networks.

The shading reveals:
- Local correlation strength clusters
- Planar structure
- Correlation density regions
- Structural changes over time (in animations)
"""

import numpy as np
import sys
sys.path.insert(0, '../src')

from correlation_network_animation import (
    SyntheticCorrelationGenerator,
    RollingCorrelationEstimator,
    NetworkAnimator,
    CorrelationFilter
)

def example_1_static_visualization():
    """
    Example 1: Create a static visualization with shaded triangles.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Static Visualization with Shaded Triangles")
    print("="*70)
    
    # Generate synthetic correlation matrix
    print("\nGenerating synthetic data...")
    n_assets = 25
    generator = SyntheticCorrelationGenerator(n_assets=n_assets, seed=42)
    
    # Generate just a correlation matrix (no time series needed for static viz)
    base_corr = generator.generate_base_correlation_matrix(block_structure=True)
    
    # Create visualizations with triangle shading
    print("\nCreating PMFG visualization with shaded triangles...")
    animator = NetworkAnimator(figsize=(14, 12))
    
    fig, ax = animator.visualize_network_with_triangles(
        base_corr,
        filter_method='pmfg',
        output_file='example_pmfg_triangles.png',
        triangle_alpha=0.35,
        triangle_cmap='RdYlBu_r'  # Red for high correlation, Blue for low
    )
    
    print("\n✓ Static visualization saved to: example_pmfg_triangles.png")
    print("  - Red triangles indicate high local correlation")
    print("  - Blue triangles indicate low/negative correlation")
    print("  - Color intensity shows correlation strength")


def example_2_animated_with_triangles():
    """
    Example 2: Create an animation with shaded triangles showing evolution.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Animated Network with Shaded Triangles")
    print("="*70)
    
    # Generate time series
    print("\nGenerating time series with evolving correlations...")
    n_assets = 20
    total_days = 300
    window_size = 100
    
    generator = SyntheticCorrelationGenerator(n_assets=n_assets, seed=42)
    returns_df, _ = generator.generate_time_series(
        total_days=total_days,
        window_size=window_size,
        volatility_process=0.05
    )
    
    # Estimate rolling correlations
    print("Estimating rolling correlations...")
    estimator = RollingCorrelationEstimator(window_size=window_size)
    correlation_estimates = estimator.estimate_correlations(returns_df)
    
    print(f"Created {len(correlation_estimates)} correlation matrices")
    
    # Create animation WITH triangle shading
    print("\nCreating animation with shaded triangular faces...")
    animator = NetworkAnimator(
        figsize=(14, 12), 
        dynamic_layout=True,  # Nodes move with force-directed layout
        shade_triangles=True  # Enable triangle shading
    )
    
    animator.animate_filtered_networks(
        correlation_estimates,
        filter_method='pmfg',
        output_file='example_pmfg_animation_triangles.mp4',
        fps=10,
        smoothing_factor=0.3,
        triangle_alpha=0.3,  # Slightly transparent
        triangle_cmap='RdYlBu_r'
    )
    
    print("\n✓ Animation saved to: example_pmfg_animation_triangles.mp4")
    print("  Watch how triangular faces:")
    print("  - Change color as correlations evolve")
    print("  - Form and dissolve as network structure changes")
    print("  - Reveal correlation clustering patterns")


def example_3_comparison_with_without():
    """
    Example 3: Create side-by-side comparison of networks with/without triangles.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Comparison - With and Without Triangle Shading")
    print("="*70)
    
    # Generate data
    print("\nGenerating synthetic data...")
    n_assets = 20
    generator = SyntheticCorrelationGenerator(n_assets=n_assets, seed=123)
    base_corr = generator.generate_base_correlation_matrix(block_structure=True)
    
    # Create figure with 2 subplots
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Left: Without triangles
    print("\nCreating network WITHOUT triangle shading...")
    animator_no_triangles = NetworkAnimator(figsize=(10, 10), shade_triangles=False)
    
    # Create PMFG
    dist = CorrelationFilter.correlation_to_distance(base_corr)
    G = CorrelationFilter.planar_maximally_filtered_graph(dist)
    
    # Layout
    import networkx as nx
    pos = nx.spring_layout(G, k=2/np.sqrt(len(G.nodes())), iterations=200, seed=42)
    
    # Setup colors
    animator_no_triangles.setup_node_colors(n_assets)
    
    # Draw on ax1 (without triangles)
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.axis('off')
    
    # Draw edges
    edges = G.edges(data=True)
    weights = [1.0 / (1.0 + e[2].get('weight', 1.0)) for e in edges]
    max_weight = max(weights)
    edge_widths = [3 * w / max_weight for w in weights]
    
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, 
                           edge_color='gray', ax=ax1)
    nx.draw_networkx_nodes(G, pos, node_color=animator_no_triangles.node_colors,
                           node_size=400, alpha=0.9, edgecolors='black',
                           linewidths=2, ax=ax1)
    nx.draw_networkx_labels(G, pos, animator_no_triangles.node_labels,
                            font_size=9, font_weight='bold', ax=ax1)
    ax1.set_title('PMFG Network\n(Without Triangle Shading)', 
                  fontsize=14, fontweight='bold')
    
    # Right: With triangles
    print("Creating network WITH triangle shading...")
    animator_with_triangles = NetworkAnimator(figsize=(10, 10), shade_triangles=True)
    animator_with_triangles.setup_node_colors(n_assets)
    
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.axis('off')
    
    # Draw triangles first
    animator_with_triangles.draw_shaded_triangles(G, pos, ax2, base_corr,
                                                  alpha=0.35, cmap='RdYlBu_r')
    
    # Draw edges and nodes
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5,
                           edge_color='gray', ax=ax2)
    nx.draw_networkx_nodes(G, pos, node_color=animator_with_triangles.node_colors,
                           node_size=400, alpha=0.9, edgecolors='black',
                           linewidths=2, ax=ax2)
    nx.draw_networkx_labels(G, pos, animator_with_triangles.node_labels,
                            font_size=9, font_weight='bold', ax=ax2)
    
    # Count triangles
    triangles = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    ax2.set_title(f'PMFG Network with Triangle Shading\n({len(triangles)} triangular faces)',
                  fontsize=14, fontweight='bold')
    
    # Add colorbar for right plot
    sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', 
                               norm=plt.Normalize(vmin=-1, vmax=1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('Triangle Avg Correlation', rotation=270, labelpad=20)
    
    plt.tight_layout()
    plt.savefig('example_comparison_triangles.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n✓ Comparison saved to: example_comparison_triangles.png")
    print("  - Left: Standard network visualization")
    print("  - Right: Enhanced with triangle shading")
    print("  - Notice how triangles reveal correlation structure!")


def example_4_different_colormaps():
    """
    Example 4: Try different colormaps for triangle shading.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Experimenting with Different Colormaps")
    print("="*70)
    
    # Generate data
    print("\nGenerating synthetic data...")
    n_assets = 20
    generator = SyntheticCorrelationGenerator(n_assets=n_assets, seed=456)
    base_corr = generator.generate_base_correlation_matrix(block_structure=True)
    
    # Try different colormaps
    colormaps = {
        'RdYlBu_r': 'Diverging (Red-Yellow-Blue, reversed)',
        'coolwarm': 'Diverging (Cool-Warm)',
        'RdBu_r': 'Diverging (Red-Blue, reversed)',
        'viridis': 'Sequential (Purple-Yellow)',
        'plasma': 'Sequential (Purple-Orange)'
    }
    
    animator = NetworkAnimator(figsize=(12, 10))
    
    for cmap_name, description in colormaps.items():
        print(f"\nCreating visualization with {cmap_name} colormap...")
        print(f"  ({description})")
        
        animator.visualize_network_with_triangles(
            base_corr,
            filter_method='pmfg',
            output_file=f'example_triangles_{cmap_name}.png',
            title=f'PMFG with {cmap_name} Triangle Shading',
            triangle_alpha=0.35,
            triangle_cmap=cmap_name
        )
    
    print("\n✓ Created visualizations with different colormaps:")
    for cmap_name in colormaps.keys():
        print(f"  - example_triangles_{cmap_name}.png")
    print("\nRecommendation: RdYlBu_r or coolwarm work best for correlations!")


def main():
    """
    Run all examples demonstrating triangle shading.
    """
    print("="*70)
    print("TRIANGLE SHADING EXAMPLES")
    print("="*70)
    print("\nThese examples demonstrate how to identify and color triangular")
    print("faces (3-cliques) in PMFG and TMFG networks.")
    print("\nTriangle shading reveals:")
    print("  • Local correlation strength clusters")
    print("  • Planar structure of the network")
    print("  • Regions of high correlation density")
    print("  • Temporal changes in correlation structure")
    
    # Run examples
    example_1_static_visualization()
    example_2_animated_with_triangles()
    example_3_comparison_with_without()
    example_4_different_colormaps()
    
    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED!")
    print("="*70)
    print("\nGenerated files:")
    print("  Static visualizations:")
    print("    - example_pmfg_triangles.png")
    print("    - example_comparison_triangles.png")
    print("    - example_triangles_*.png (5 different colormaps)")
    print("  Animation:")
    print("    - example_pmfg_animation_triangles.mp4")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
