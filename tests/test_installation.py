#!/usr/bin/env python
"""
Test script to verify the installation and basic functionality.
Run this after setup to ensure everything is working correctly.
"""

import sys
import importlib

def check_python_version():
    """Check if Python version is sufficient."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"  ✗ Python {version.major}.{version.minor} is too old")
        print(f"  Required: Python 3.8 or higher")
        return False
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_package(package_name, import_name=None):
    """Check if a package is installed and can be imported."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"  ✓ {package_name} (version {version})")
        return True
    except ImportError:
        print(f"  ✗ {package_name} not found")
        return False

def check_ffmpeg():
    """Check if ffmpeg is installed."""
    import subprocess
    print("Checking for ffmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✓ {version_line}")
            return True
        else:
            print(f"  ✗ ffmpeg found but returned error")
            return False
    except FileNotFoundError:
        print(f"  ✗ ffmpeg not found")
        print(f"    Install with:")
        print(f"      Ubuntu/Debian: sudo apt-get install ffmpeg")
        print(f"      macOS:         brew install ffmpeg")
        print(f"      Windows:       Download from https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        print(f"  ✗ Error checking ffmpeg: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of the correlation network code."""
    print("\nTesting basic functionality...")
    
    try:
        from correlation_network_animation import (
            SyntheticCorrelationGenerator,
            RollingCorrelationEstimator,
            CorrelationFilter,
            NetworkAnimator
        )
        print("  ✓ Successfully imported all classes")
        
        # Test data generation
        print("  Testing data generation...")
        generator = SyntheticCorrelationGenerator(n_assets=5, seed=42)
        returns_df, correlations = generator.generate_time_series(
            total_days=50,
            window_size=20
        )
        print(f"    ✓ Generated {returns_df.shape[0]} days of returns for {returns_df.shape[1]} assets")
        
        # Test correlation estimation
        print("  Testing correlation estimation...")
        estimator = RollingCorrelationEstimator(window_size=20)
        corr_estimates = estimator.estimate_correlations(returns_df)
        print(f"    ✓ Estimated {len(corr_estimates)} correlation matrices")
        
        # Test filtering
        print("  Testing network filtering...")
        sample_corr = corr_estimates[0]['correlation']
        dist = CorrelationFilter.correlation_to_distance(sample_corr)
        
        mst = CorrelationFilter.minimum_spanning_tree(dist)
        print(f"    ✓ MST: {mst.number_of_edges()} edges")
        
        pmfg = CorrelationFilter.planar_maximally_filtered_graph(dist)
        print(f"    ✓ PMFG: {pmfg.number_of_edges()} edges")
        
        tmfg = CorrelationFilter.triangulated_maximally_filtered_graph(dist)
        print(f"    ✓ TMFG: {tmfg.number_of_edges()} edges")
        
        # Test animator creation (but don't create actual animation)
        print("  Testing animator initialization...")
        animator = NetworkAnimator(figsize=(10, 8))
        print(f"    ✓ NetworkAnimator created")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("Installation Verification Test")
    print("="*60)
    print()
    
    all_passed = True
    
    # Check Python version
    if not check_python_version():
        all_passed = False
    print()
    
    # Check required packages
    print("Checking required packages...")
    packages = [
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
        ('scipy', 'scipy'),
        ('networkx', 'networkx'),
        ('matplotlib', 'matplotlib')
    ]
    
    for pkg_name, import_name in packages:
        if not check_package(pkg_name, import_name):
            all_passed = False
    print()
    
    # Check ffmpeg
    ffmpeg_ok = check_ffmpeg()
    print()
    
    # Test basic functionality
    if not test_basic_functionality():
        all_passed = False
    print()
    
    # Summary
    print("="*60)
    if all_passed and ffmpeg_ok:
        print("✓ All tests passed! Everything is working correctly.")
        print()
        print("You can now run:")
        print("  python correlation_network_animation.py")
        print("or")
        print("  jupyter notebook examples.ipynb")
    elif all_passed and not ffmpeg_ok:
        print("⚠ Core functionality works, but ffmpeg is not installed.")
        print("  Video export will not work without ffmpeg.")
        print()
        print("You can still run the code and analyze networks,")
        print("but animation creation will fail.")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print()
        print("Common fixes:")
        print("  1. Make sure you activated the virtual environment:")
        print("     source venv/bin/activate")
        print("  2. Run setup.sh again if packages are missing")
        print("  3. Check that you're using Python 3.8 or higher")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
