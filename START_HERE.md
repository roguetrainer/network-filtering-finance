# 🎯 START HERE

## Animated Correlation Network Filtering

Welcome! This package creates animations of filtered correlation networks over time using geometric filtering methods developed by Tomaso Aste and colleagues.

---

## 📂 What You Have (9 Files)

### 🚀 Get Started Immediately
- **[FILES_SUMMARY.md](FILES_SUMMARY.md)** - Overview of everything (READ THIS FIRST!)
- **[QUICKSTART.md](QUICKSTART.md)** - Fast setup guide (5 minutes to running)
- **[setup.sh](setup.sh)** - Run this first to set everything up

### 📚 Learn & Understand
- **[examples.ipynb](examples.ipynb)** - Interactive tutorial with visualizations
- **[README.md](README.md)** - Complete documentation & reference

### 🔧 Core Implementation
- **[correlation_network_animation.py](correlation_network_animation.py)** - Main code (all algorithms)
- **[requirements.txt](requirements.txt)** - Python dependencies

### 🛠️ Tools & Reference
- **[test_installation.py](test_installation.py)** - Verify everything works
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Code organization guide

---

## ⚡ Quick Start (2 Commands)

```bash
# 1. Setup (creates venv, installs packages)
./setup.sh

# 2. Run (creates 4 animation videos)
source venv/bin/activate
python correlation_network_animation.py
```

**Result**: You'll have 4 MP4 files showing network evolution! 🎬

---

## 📖 Recommended Reading Order

### First Time Users
1. **FILES_SUMMARY.md** ← You are here
2. **QUICKSTART.md** ← Do the 3-step setup
3. **Run the code!** ← See it work
4. **examples.ipynb** ← Learn interactively
5. **README.md** ← Deep dive

### Advanced Users
1. **FILES_SUMMARY.md** ← Quick overview
2. **PROJECT_STRUCTURE.md** ← Code architecture
3. **correlation_network_animation.py** ← Source code
4. **Start customizing!**

---

## 🎯 What Does This Do?

This package lets you:

### 1. Generate Synthetic Data
- Time-varying correlation matrices
- Realistic sector structures
- Diffusion process dynamics
- Guaranteed valid correlation matrices

### 2. Filter Networks
Three geometric filtering methods:
- **MST** (Minimum Spanning Tree): N-1 edges, hierarchical
- **PMFG** (Planar Maximally Filtered Graph): 3(N-2) edges, planar
- **TMFG** (Triangulated Maximally Filtered Graph): 3(N-2) edges, fast

### 3. Create Animations
- Watch networks evolve over time
- See correlation structure changes
- Compare different filtering methods
- Export as MP4 video files

---

## 🎬 Example Output

After running, you'll have:

1. **mst_network_animation.mp4**
   - Minimum spanning tree evolution
   - Simplest network structure

2. **pmfg_network_animation.mp4**
   - Planar graph with richer structure
   - More edges than MST

3. **tmfg_network_animation.mp4**
   - Similar to PMFG but faster
   - Best for large networks

4. **network_comparison.mp4**
   - All three methods side-by-side
   - Easy visual comparison

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Download all 9 files
- [ ] Run `./setup.sh`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Run `python test_installation.py`
- [ ] All tests pass? You're ready! ✨

### Optional but Recommended
- [ ] Install ffmpeg (needed for video export)
- [ ] Install Jupyter (for interactive notebook)

---

## 🔍 File Size Reference

| File | Size | Time to Read |
|------|------|--------------|
| START_HERE.md | 3 KB | 2 min (you're reading it!) |
| FILES_SUMMARY.md | 9 KB | 5 min |
| QUICKSTART.md | 6 KB | 5 min |
| README.md | 13 KB | 20 min |
| PROJECT_STRUCTURE.md | 9 KB | 15 min |
| examples.ipynb | 21 KB | 30 min (interactive) |
| correlation_network_animation.py | 28 KB | 1 hour (to understand fully) |
| setup.sh | 4 KB | 2 min |
| test_installation.py | 6 KB | 5 min |

**Total package**: ~97 KB (tiny!)

---

## 💡 Common Questions

**Q: Do I need to know Python?**
A: Basic Python helps, but the scripts work out of the box. The notebook has detailed explanations.

**Q: What if I want to use my own data?**
A: See README.md section "Using Your Own Data" - just load your returns as a pandas DataFrame!

**Q: How long does it take to run?**
A: ~3-5 minutes for default parameters (20 assets, 500 days)

**Q: Can I customize the parameters?**
A: Yes! Everything is configurable - see examples.ipynb or README.md

**Q: What about big networks (100+ assets)?**
A: Use TMFG method - it's O(N²) instead of O(N³)

**Q: Do I need ffmpeg?**
A: Yes, for creating video files. See QUICKSTART.md for installation.

---

## 🎓 Learning Path

### Beginner (2 hours)
1. Read FILES_SUMMARY.md
2. Run setup.sh
3. Run test_installation.py
4. Run main script
5. Work through examples.ipynb

### Intermediate (4 hours)
1. Read README.md fully
2. Modify parameters
3. Try with different network sizes
4. Explore visualization options
5. Understand the algorithms

### Advanced (8+ hours)
1. Read PROJECT_STRUCTURE.md
2. Study source code
3. Read original research papers
4. Implement extensions
5. Use with real market data

---

## 🚨 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Can't run setup.sh | Run: `chmod +x setup.sh` |
| Python not found | Edit `PYTHON_PATH` in setup.sh |
| Module not found | Run: `source venv/bin/activate` |
| ffmpeg not found | Install: See QUICKSTART.md Step 4 |
| Tests fail | Check error message, see README troubleshooting |
| Out of memory | Reduce n_assets in main script |

---

## 🌟 What Makes This Special?

### Based on Cutting-Edge Research
- **500+ citations** for main PMFG paper
- Used in **academic research** worldwide
- Applied in **quantitative finance**
- **Validated** against real market data

### Complete Implementation
- All algorithms from the papers
- Synthetic data generation
- Visualization tools
- Animation capabilities

### Production Ready
- Well-documented
- Tested code
- Error handling
- Performance optimized

### Educational Value
- Learn network theory
- Understand correlation filtering
- Practice Python data science
- Study financial networks

---

## 🎁 Bonus Features

- **Jupyter notebook** with step-by-step examples
- **Test suite** to verify installation
- **Multiple filtering methods** (MST, PMFG, TMFG)
- **Animation export** as MP4 videos
- **Synthetic data generator** with realistic dynamics
- **Complete documentation** with examples
- **Research citations** for academic use

---

## 🚀 Ready to Start?

### Option 1: Fast Track (5 minutes)
```bash
./setup.sh
source venv/bin/activate
python correlation_network_animation.py
```

### Option 2: Learn As You Go (30 minutes)
```bash
./setup.sh
source venv/bin/activate
jupyter notebook examples.ipynb
```

### Option 3: Deep Dive (2 hours)
1. Read FILES_SUMMARY.md
2. Read QUICKSTART.md
3. Read README.md
4. Work through examples.ipynb
5. Read PROJECT_STRUCTURE.md
6. Study correlation_network_animation.py

---

## 📊 What You'll Learn

- **Network Theory**: MST, planar graphs, filtering
- **Financial Networks**: Correlation structure, sector analysis
- **Data Science**: Pandas, NumPy, NetworkX
- **Visualization**: Matplotlib, animations
- **Scientific Computing**: Correlation estimation, rolling windows

---

## 🎯 Next Actions

1. **Now**: Read FILES_SUMMARY.md for complete overview
2. **Then**: Follow QUICKSTART.md for setup
3. **Next**: Run the code and see results
4. **After**: Explore examples.ipynb
5. **Finally**: Customize for your needs!

---

## 📞 Need Help?

1. **Setup issues**: See QUICKSTART.md troubleshooting
2. **Usage questions**: Check README.md examples
3. **Code questions**: Review PROJECT_STRUCTURE.md
4. **Algorithm questions**: Read cited papers in README.md

---

## 🎊 You're All Set!

You have everything you need to:
- ✅ Generate synthetic correlation data
- ✅ Apply geometric filtering methods
- ✅ Create network animations
- ✅ Analyze correlation evolution
- ✅ Use with your own data
- ✅ Extend for research

**Let's get started!** 🚀

---

*Created: November 2024*  
*Based on research by Aste, Di Matteo, Mantegna, et al.*  
*For educational and research use*

**Enjoy exploring correlation networks!** 🎉
