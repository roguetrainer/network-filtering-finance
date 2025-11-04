# Contributing to Network Filtering in Finance

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](../../issues) section
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Code snippet if applicable

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**
   ```bash
   python tests/test_installation.py
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add feature: brief description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Submit a Pull Request**

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Documentation

- Update README.md for major features
- Add examples to the examples/ directory
- Update CHANGELOG.md with changes
- Include inline comments for complex algorithms

### Testing

- Ensure test_installation.py passes
- Add tests for new features
- Test with different Python versions (3.8+)
- Verify animations render correctly

## Areas for Contribution

### High Priority

- Performance optimizations for large networks
- Additional filtering methods (DBHT, higher genus graphs)
- GPU acceleration support
- Memory optimization for long time series

### Medium Priority

- Interactive visualizations (Plotly, Dash)
- Real-time streaming data support
- Additional correlation measures (Spearman, Kendall, mutual information)
- More comprehensive testing suite

### Nice to Have

- Web interface
- Docker containerization
- Additional export formats
- Community detection algorithms
- Portfolio optimization integration

## Code of Conduct

- Be respectful and constructive
- Focus on the issue, not the person
- Accept constructive criticism gracefully
- Help others learn and grow

## Questions?

Feel free to open an issue for:
- Implementation questions
- Feature requests
- General discussion

## Academic Use

When using this code in academic research, please cite the original papers:

1. Tumminello et al. (2005) - PMFG method
2. Massara et al. (2016) - TMFG method
3. Mantegna (1999) - MST in financial markets

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping improve this project!
