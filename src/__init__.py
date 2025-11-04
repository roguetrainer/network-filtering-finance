"""
Network Filtering in Finance
============================

A Python implementation for creating animations of filtered correlation networks 
over time, based on geometric filtering methods developed by Tomaso Aste and colleagues.

Main Components:
---------------
- SyntheticCorrelationGenerator: Generate synthetic time series with time-varying correlations
- RollingCorrelationEstimator: Estimate rolling correlation matrices
- CorrelationFilter: Apply network filtering methods (MST, PMFG, TMFG)
- NetworkAnimator: Create animations of evolving network structure

Example:
--------
>>> from correlation_network_animation import (
...     SyntheticCorrelationGenerator,
...     RollingCorrelationEstimator,
...     NetworkAnimator
... )
>>> 
>>> # Generate synthetic data
>>> generator = SyntheticCorrelationGenerator(n_assets=20, seed=42)
>>> returns_df, _ = generator.generate_time_series(total_days=500, window_size=100)
>>> 
>>> # Estimate correlations
>>> estimator = RollingCorrelationEstimator(window_size=100)
>>> correlations = estimator.estimate_correlations(returns_df)
>>> 
>>> # Create animation
>>> animator = NetworkAnimator()
>>> animator.animate_filtered_networks(
...     correlations,
...     filter_method='pmfg',
...     output_file='network.mp4'
... )
"""

__version__ = "1.0.0"
__author__ = "Network Filtering Contributors"
__license__ = "MIT"

from .correlation_network_animation import (
    SyntheticCorrelationGenerator,
    RollingCorrelationEstimator,
    CorrelationFilter,
    NetworkAnimator,
)

__all__ = [
    "SyntheticCorrelationGenerator",
    "RollingCorrelationEstimator",
    "CorrelationFilter",
    "NetworkAnimator",
]
