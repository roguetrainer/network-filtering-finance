# Directory Structure

```
network-filtering-finance/
│
├── .github/                          # GitHub configuration
│   └── workflows/
│       └── ci.yml                    # Continuous integration workflow
│
├── docs/                             # Documentation
│   ├── README.md                     # Documentation index with API reference
│   ├── CHANGELOG.md                  # Version history and changes
│   ├── DYNAMIC_LAYOUT_GUIDE.md      # Guide to dynamic force-directed layouts
│   └── QUICKSTART.md                # Quick start guide for new users
│
├── examples/                         # Usage examples
│   ├── README.md                     # Examples documentation
│   ├── example_dynamic_layout.py    # Standalone dynamic layout example
│   └── examples.ipynb               # Interactive Jupyter notebook tutorial
│
├── src/                              # Source code
│   ├── __init__.py                  # Package initialization and exports
│   └── correlation_network_animation.py  # Main implementation (~1000 lines)
│       ├── SyntheticCorrelationGenerator
│       ├── RollingCorrelationEstimator
│       ├── CorrelationFilter
│       └── NetworkAnimator
│
├── tests/                            # Test suite
│   ├── README.md                     # Testing documentation
│   └── test_installation.py         # Installation and functionality tests
│
├── .gitignore                        # Git ignore patterns
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT License with citation requirements
├── MANIFEST.in                       # Package manifest for distribution
├── PROJECT_OVERVIEW.md              # High-level project overview
├── README.md                         # Main project documentation (~400 lines)
├── requirements.txt                  # Python dependencies (5 packages)
├── requirements-dev.txt             # Development dependencies
├── setup.py                         # Package installation configuration
└── setup.sh                         # Automated setup script

Total: 22 files organized in 6 directories
```

## Directory Purposes

### `.github/`
Configuration for GitHub-specific features:
- CI/CD workflows
- Issue templates (future)
- Pull request templates (future)

### `docs/`
All documentation files except main README:
- API reference
- User guides
- Technical documentation
- Change logs

### `examples/`
Working code examples:
- Jupyter notebooks for interactive learning
- Standalone Python scripts
- Real-world use case demonstrations

### `src/`
Core source code:
- Package initialization
- Main implementation file
- All classes and algorithms

### `tests/`
Testing infrastructure:
- Installation verification
- Functionality tests
- Unit tests (future)
- Integration tests (future)

## File Categories

### Documentation (8 files)
- README.md (main)
- PROJECT_OVERVIEW.md
- CONTRIBUTING.md
- docs/README.md
- docs/QUICKSTART.md
- docs/CHANGELOG.md
- docs/DYNAMIC_LAYOUT_GUIDE.md
- examples/README.md
- tests/README.md

### Source Code (2 files)
- src/__init__.py
- src/correlation_network_animation.py

### Examples (2 files)
- examples/example_dynamic_layout.py
- examples/examples.ipynb

### Tests (1 file)
- tests/test_installation.py

### Configuration (9 files)
- .gitignore
- .github/workflows/ci.yml
- LICENSE
- MANIFEST.in
- requirements.txt
- requirements-dev.txt
- setup.py
- setup.sh

## Key Features by Location

### Root Level
- Essential user-facing files
- Package metadata
- Setup/installation files

### src/
- Single-file implementation (for simplicity)
- All classes in one module
- Clean imports via __init__.py

### examples/
- Progressive learning path
- Both interactive (notebook) and scripted
- Real-world scenarios

### tests/
- Comprehensive validation
- Easy to run
- Clear pass/fail output

### docs/
- Organized by topic
- API documentation
- User guides

## Design Principles

1. **Flat Structure**: Minimal nesting for easy navigation
2. **Clear Naming**: Self-explanatory file and directory names
3. **Separation**: Code, docs, examples, tests in separate dirs
4. **Standard Layout**: Follows Python packaging conventions
5. **GitHub Ready**: Includes CI/CD and contribution guidelines

## Navigation Tips

**Getting Started:**
1. Start with README.md
2. Then docs/QUICKSTART.md
3. Run tests/test_installation.py
4. Try examples/examples.ipynb

**For Developers:**
1. Read CONTRIBUTING.md
2. Check src/correlation_network_animation.py
3. Review tests/test_installation.py
4. Set up development environment with requirements-dev.txt

**For Users:**
1. Install via setup.sh
2. Follow examples/
3. Reference docs/ for details
4. Use src/ as library

## File Size Summary

- **Largest**: src/correlation_network_animation.py (~1000 lines)
- **Main docs**: README.md (~400 lines)
- **Notebooks**: examples/examples.ipynb (interactive)
- **Tests**: test_installation.py (~200 lines)

## Growth Areas

As project evolves:
- tests/ → Add unit, integration, performance tests
- examples/ → Add more domain-specific examples
- docs/ → Add API auto-generation
- src/ → May split into submodules if needed

---

This structure balances simplicity with organization, making it easy for both users and contributors to navigate the project.
