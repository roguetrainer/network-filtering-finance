# Documentation

This directory contains detailed documentation for the Network Filtering in Finance project.

## Available Documentation

### Quick Start
- [QUICKSTART.md](QUICKSTART.md) - Get started quickly with minimal setup

### Feature Guides
- [DYNAMIC_LAYOUT_GUIDE.md](DYNAMIC_LAYOUT_GUIDE.md) - Guide to dynamic force-directed layouts
- [CHANGELOG.md](CHANGELOG.md) - Version history and changes

### Project Information
- [../README.md](../README.md) - Main project README
- [../CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [../LICENSE](../LICENSE) - MIT License

## API Reference

### Main Classes

#### SyntheticCorrelationGenerator
Generates synthetic time series with time-varying correlation structures.

```python
generator = SyntheticCorrelationGenerator(n_assets=20, seed=42)
returns_df, correlations = generator.generate_time_series(
    total_days=500,
    window_size=100
)
```

#### RollingCorrelationEstimator
Estimates rolling correlation matrices from time series data.

```python
estimator = RollingCorrelationEstimator(window_size=100)
correlation_estimates = estimator.estimate_correlations(returns_df)
```

#### CorrelationFilter
Static methods for network filtering algorithms.

```python
# Convert correlation to distance
distance = CorrelationFilter.correlation_to_distance(corr_matrix)

# Apply filters
mst = CorrelationFilter.minimum_spanning_tree(distance)
pmfg = CorrelationFilter.planar_maximally_filtered_graph(distance)
tmfg = CorrelationFilter.triangulated_maximally_filtered_graph(distance)
```

#### NetworkAnimator
Creates animations and visualizations of network evolution.

```python
animator = NetworkAnimator(figsize=(12, 10), dynamic_layout=True)
animator.animate_filtered_networks(
    correlation_estimates,
    filter_method='pmfg',
    output_file='animation.mp4'
)
```

## Examples

See the [examples/](../examples/) directory for:
- `examples.ipynb` - Interactive Jupyter notebook with step-by-step examples
- `example_dynamic_layout.py` - Standalone example of dynamic layouts

## Research Papers

This implementation is based on the following seminal papers:

1. **Tumminello, M., Aste, T., Di Matteo, T., & Mantegna, R. N. (2005)**  
   "A tool for filtering information in complex systems."  
   *PNAS*, 102(30), 10421-10426.  
   [DOI: 10.1073/pnas.0500298102](https://doi.org/10.1073/pnas.0500298102)

2. **Massara, G.P., Di Matteo, T., & Aste, T. (2016)**  
   "Network Filtering for Big Data: Triangulated Maximally Filtered Graph."  
   *Journal of Complex Networks*, 5(2), 161-178.  
   [DOI: 10.1093/comnet/cnw015](https://doi.org/10.1093/comnet/cnw015)

3. **Mantegna, R. N. (1999)**  
   "Hierarchical structure in financial markets."  
   *European Physical Journal B*, 11(1), 193-197.  
   [DOI: 10.1007/s100510050929](https://doi.org/10.1007/s100510050929)

## Additional Resources

- [NetworkX Documentation](https://networkx.org/)
- [Tomaso Aste's Research Page](https://www.ucl.ac.uk/~ucahtas/)
- [Matplotlib Animation Guide](https://matplotlib.org/stable/api/animation_api.html)

## Support

For questions or issues:
1. Check the [README.md](../README.md) troubleshooting section
2. Review examples in [examples/](../examples/)
3. Open an issue on GitHub
4. Refer to the original research papers for methodology questions
