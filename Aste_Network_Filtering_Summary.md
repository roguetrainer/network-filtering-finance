# Geometric Approaches to Filtering Correlation Matrices: The Work of Tomaso Aste and Colleagues

## Comprehensive Summary of Network Filtering Methods in Financial Markets

*Based on research by Tomaso Aste, Tiziana Di Matteo, Rosario N. Mantegna, Michele Tumminello, Nicolo Musmeci, and collaborators*

---

## Table of Contents

1. [Overview and Motivation](#overview-and-motivation)
2. [The Correlation Filtering Problem](#the-correlation-filtering-problem)
3. [Key Methods Developed](#key-methods-developed)
4. [Applications to Financial Markets](#applications-to-financial-markets)
5. [Theoretical Foundations](#theoretical-foundations)
6. [Recent Advances](#recent-advances)
7. [Implementation and Tools](#implementation-and-tools)

---

## Overview and Motivation

### The Challenge

Financial markets generate **high-dimensional correlation matrices** from price time series of hundreds or thousands of assets. For N assets, we have:
- **N(N-1)/2** distinct correlation pairs
- Example: 500 stocks → 124,750 correlations

The problem: **Most correlations are noise**, obscuring meaningful structure.

### Why Filter?

**Applications requiring clean correlation structure**:
1. **Portfolio optimization** - Identify true diversification
2. **Risk management** - Detect systemic connections
3. **Sector analysis** - Reveal hierarchical organization
4. **Crisis detection** - Monitor structural changes
5. **Network visualization** - Display interpretable graphs

**Traditional approaches fail**:
- Principal Component Analysis (PCA): Identifies directions, not connections
- Thresholding: Arbitrary cutoffs, loses topology
- Full correlation matrix: Too noisy, computationally intractable

---

## The Correlation Filtering Problem

### Mathematical Setup

Given:
- **Price time series**: {P_i(t)} for i = 1,...,N assets
- **Returns**: r_i(t) = log(P_i(t)/P_i(t-1))
- **Correlation matrix**: C with elements C_ij = corr(r_i, r_j)

Goal: **Extract a sparse network** that:
1. Retains the most significant correlations
2. Has interpretable topological structure
3. Preserves hierarchical organization
4. Remains statistically stable

### From Correlation to Distance

Convert correlations to distances using the metric:

```
d_ij = √(2(1 - C_ij))
```

This metric satisfies:
- d_ij = 0 if C_ij = 1 (perfect correlation)
- d_ij = 2 if C_ij = -1 (perfect anti-correlation)
- Triangle inequality holds

---

## Key Methods Developed

### 1. Minimum Spanning Tree (MST)

**Historical context**: Introduced by Mantegna (1999) for financial markets

**Algorithm**:
1. Start with all N nodes, no edges
2. Add edges in order of increasing distance
3. Never create a cycle
4. Stop when N-1 edges added

**Properties**:
- **Edges**: N - 1
- **Structure**: Tree (no cycles)
- **Guarantee**: Minimum total weight spanning tree

**Limitations**:
- Very sparse (only N-1 of N(N-1)/2 possible edges)
- Forces tree structure (may be too restrictive)
- Loses information about alternative paths

### 2. Planar Maximally Filtered Graph (PMFG)

**Seminal paper**: Tumminello, M., Aste, T., Di Matteo, T., & Mantegna, R. N. (2005). "A tool for filtering information in complex systems." *Proceedings of the National Academy of Sciences*, 102(30), 10421-10426.

#### Definition

A **planar graph** can be drawn on a flat surface without edge crossings.

The PMFG is a planar graph where edges connecting the most similar elements (highest correlations) are added iteratively while maintaining planarity.

#### Algorithm

```python
def construct_PMFG(distance_matrix):
    # 1. Create ordered list of edges by distance (ascending)
    edges_sorted = sort_edges_by_distance(distance_matrix)
    
    # 2. Initialize empty graph
    G = EmptyGraph(n_nodes)
    
    # 3. Add edges while maintaining planarity
    for edge in edges_sorted:
        G_temp = G + edge
        
        # Check planarity using Kuratowski's theorem
        if is_planar(G_temp):
            G = G_temp
        
        # Stop when we have 3(n-2) edges
        if G.num_edges() == 3*(n-2):
            break
    
    return G
```

#### Properties

**Edge count**: 3(n-2) edges (compared to n-1 for MST, n(n-1)/2 for complete graph)

**Example sizes**:

| N (nodes) | MST edges | PMFG edges | Complete graph | % Retained by PMFG |
|-----------|-----------|------------|----------------|-------------------|
| 50 | 49 | 144 | 1,225 | 11.8% |
| 100 | 99 | 294 | 4,950 | 5.9% |
| 500 | 499 | 1,494 | 124,750 | 1.2% |

**Topological properties**:
- Contains MST as subgraph
- Is a "topological triangulation of the sphere"
- Genus k = 0 (can be embedded on sphere without crossings)
- Allows only 3-cliques and 4-cliques (no K_5 or K_3,3 by Kuratowski's theorem)

#### Kuratowski's Planarity Test

A finite graph is planar if and only if it does not contain a subgraph homeomorphic to:
- **K_5**: Complete graph on 5 vertices (5-clique)
- **K_3,3**: Complete bipartite graph with 3 vertices in each partition

### 3. Triangulated Maximally Filtered Graph (TMFG)

**Key paper**: Massara, G.P., Di Matteo, T., & Aste, T. (2016). "Network Filtering for Big Data: Triangulated Maximally Filtered Graph." *Journal of Complex Networks*, 5(2), 161-178.

#### Motivation

PMFG algorithm has O(n³) complexity. TMFG improves this to O(n²) while maintaining similar filtering quality.

#### Algorithm

**T2 Move** (Triangle insertion):
```
Start with tetrahedron (4 nodes, all connected)

Repeat:
  1. Select vertex v to insert
  2. Find triangle (face) f in current graph
  3. Insert v inside f, connecting to all 3 vertices of f
  4. This creates 3 new triangles
  
Until all vertices inserted
```

**Key innovation**: Builds graph starting from a tetrahedron and recursively inserts vertices inside existing triangles (T2 move) to approximate a maximal planar graph with the largest total weight.

#### Properties

- **Same edge count**: 3(n-2) edges
- **Chordal graph**: Every cycle of length ≥ 4 has a chord (shortcut)
- **Faster**: O(n²) vs O(n³) for PMFG
- **Quality**: Comparable or better total weight than PMFG

#### Computational Comparison

Execution time comparison for different matrix sizes p:

| Method | Complexity | Time for p=1000 | Time for p=5000 |
|--------|-----------|-----------------|-----------------|
| PMFG | O(p³) | ~30 minutes | ~15 hours |
| TMFG | O(p²) | ~30 seconds | ~12 minutes |

### 4. Higher Genus Graphs

**Generalization**: Allow graphs on surfaces of higher genus (torus, double torus, etc.)

| Genus k | Surface | Max clique size | Edges |
|---------|---------|-----------------|-------|
| 0 | Sphere | 4 | 3(n-2) |
| 1 | Torus | 5 | Higher |
| 2 | Double torus | 6 | Higher |

**Trade-off**: More information retained vs. computational complexity

### 5. Directed Bubble Hierarchical Tree (DBHT)

A novel hierarchical clustering method developed by Aste's group that extracts hierarchical structure from PMFG networks.

**Advantages**:
- Better retrieves industrial sector classifications than traditional methods
- More information with fewer clusters
- Reveals hierarchical organization at multiple scales

---

## Applications to Financial Markets

### 1. Market Structure and Sector Classification

**Key finding**: Aste and colleagues showed that filtered networks (PMFG + DBHT) can recover the industrial sector classification of stocks, validating that the correlation structure reflects real economic relationships.

**Study design**:
- Dataset: Stock returns 1997-2012
- Benchmark: Official sector classifications
- Methods compared: MST, PMFG, DBHT, traditional clustering

**Results**: DBHT outperforms other methods in retrieving sector information

### 2. Crisis Detection and Dynamic Evolution

**Rolling window analysis**: Different filtering methods show different degrees of sensitivity to events affecting financial markets, like crises.

**Observable phenomena**:
- Network structure changes during market stress
- Connectivity increases in crises (systemic risk)
- Sectoral boundaries blur under stress
- Recovery shows gradual restructuring

### 3. Portfolio Optimization and Risk Management

**Applications**:

**a) Risk diversification**: Pozzi, Di Matteo, and Aste (2013) showed "Spread of Risk Across Financial Markets: Better to Invest in the Peripheries"

**Key insight**: Stocks at the periphery of the filtered network offer better diversification than central hub stocks.

**b) Volatility forecasting**: Musmeci et al. (2016) introduced "correlation structure persistence" - a measure quantifying the rate of change of market dependence structure that can anticipate market risk variations.

**c) Portfolio construction**: The method overcomes the curse of dimensionality that limits traditional econometric tools to portfolios with large numbers of assets.

### 4. Systemic Risk and Network Analysis

**Identifying systemic nodes**: The most persistent motifs (triangles, tetrahedra) in TMFG correspond to stocks in the same sector and portfolios of these motifs are highly volatile and systemic.

**Contagion pathways**: Filtered networks reveal:
- Direct counterparty risk
- Indirect correlations through common factors
- Hierarchical propagation patterns

### 5. Simplicial Persistence

**Recent innovation**: Turiel, Barucca, and Aste (2022) introduced "simplicial persistence" - a measure of time evolution of motifs (triangles, tetrahedra) in networks obtained from correlation filtering.

**Key findings**:

**a) Long memory**: Two power-law decay regimes observed in the number of persistent simplicial complexes

**b) Market characterization**: Decay exponents characterize financial markets based on efficiency and liquidity. More liquid markets tend to have slower persistence decay - in contrast with the common understanding that efficient markets are more random.

**c) Structure identification**: TMFG identifies high-order structures throughout the market sample, where thresholding methods fail.

---

## Theoretical Foundations

### Information Theory Perspective

The filtering procedures can be seen as maximizing information retention while minimizing complexity, quantified using the Kullback-Leibler distance.

**Objective**:
```
Maximize: I(filtered_network, full_network)
Subject to: complexity(filtered_network) < threshold
```

### Graph Theory Foundation

**Planar graph theory**:
- Euler's formula: For planar graph with V vertices, E edges, F faces: V - E + F = 2
- Maximum edges in planar graph: 3V - 6
- PMFG achieves this maximum (for V ≥ 3)

**Chordal graphs** (TMFG property):
- Every cycle ≥ 4 has a chord
- Perfect elimination ordering exists
- Enables efficient inference algorithms
- Opens door to Markov Random Field modeling

### Statistical Validation

**Bootstrap methods**: Test stability of filtered structure under:
- Sampling uncertainty
- Parameter changes
- Different time periods

**Null models**: Test against:
- Rolling multivariate Gaussian (evolving covariance)
- Stable multivariate Gaussian (fixed covariance)
- Random permutations

**Finding**: Real market structure evolves slowly in time, with persistence beyond what can be inferred from estimates of its covariance structure.

---

## Recent Advances

### 1. Integration with Machine Learning

**Spatial-Temporal Graph Neural Networks**: Aste's group (2022) proposed an end-to-end architecture for multivariate time-series prediction integrating spatial-temporal GNN with matrix filtering module.

**Workflow**:
```
Time series → Correlation matrix → TMFG filtering → GNN → Predictions
```

**Advantage**: Filtering removes noise before machine learning, improving prediction accuracy.

### 2. Topological Data Analysis (TDA)

Extension beyond nodes (0-simplex) and edges (1-simplex) to work with faces (2-simplex) or any k-dimensional simplex.

**Persistent homology**: Track how topological features (connected components, loops, voids) persist across filtration thresholds.

**Signatures detected**:
- Formation/destruction of cycles
- Emergence of higher-order structures
- Topological phase transitions

### 3. Multi-Scale and Multi-Resolution Analysis

Analysis of filtered correlation networks at different time horizons reveals scale-dependent structure.

**Findings**:
- High frequency (seconds): Microstructure effects
- Medium frequency (days): Sectoral organization
- Low frequency (months): Market-wide factors

### 4. Cryptocurrency Markets

Investigation of cross-correlations at different time horizons for liquid cryptocurrencies, studying how MST and TMFG structure evolves from high (15s) to low (1 day) frequency.

**Distinct features**:
- More volatile correlation structure
- Faster evolution of network topology
- Different hierarchical organization than traditional markets

### 5. Flash Crashes and Critical Phenomena

Turiel and Aste (2022) studied "Heterogeneous Criticality in High Frequency Finance: A Phase Transition in Flash Crashes"

**Connection to SOC**: Flash crashes as avalanche phenomena in correlation networks near critical points.

---

## Implementation and Tools

### Available Software

**MATLAB**:
- Tomaso Aste's PMFG implementation (MATLAB Central File Exchange #38689)
- TMFG implementation (MATLAB Central File Exchange #56444)
- Requires matlab_bgl package for graph algorithms

**Python**:
- Implementation using NetworkX and planarity packages
- Boyer-Myrvold O(n) planarity testing
- Integration with pandas for financial data

**R**:
- NetworkToolbox package includes PMFG function
- Supports sparse matrices
- Bootstrap validation included

### Example Implementation (Python)

```python
import numpy as np
import networkx as nx
from planarity import is_planar
from scipy.spatial.distance import squareform

def correlation_to_distance(corr_matrix):
    """Convert correlation to metric distance."""
    return np.sqrt(2 * (1 - corr_matrix))

def construct_PMFG(distance_matrix):
    """
    Construct Planar Maximally Filtered Graph.
    
    Based on Tumminello et al. (2005) PNAS.
    """
    n = distance_matrix.shape[0]
    
    # Create complete graph with weights
    G_complete = nx.Graph()
    for i in range(n):
        for j in range(i+1, n):
            G_complete.add_edge(i, j, weight=distance_matrix[i,j])
    
    # Sort edges by weight (distance)
    edges_sorted = sorted(G_complete.edges(data=True), 
                         key=lambda x: x[2]['weight'])
    
    # Build PMFG
    G_pmfg = nx.Graph()
    max_edges = 3 * (n - 2)
    
    for source, dest, data in edges_sorted:
        G_pmfg.add_edge(source, dest, weight=data['weight'])
        
        # Check planarity
        if not is_planar(G_pmfg):
            G_pmfg.remove_edge(source, dest)
        
        # Stop when we have enough edges
        if G_pmfg.number_of_edges() >= max_edges:
            break
    
    return G_pmfg

def analyze_pmfg(G_pmfg):
    """Extract features from PMFG."""
    
    # Clique analysis
    cliques_3 = [c for c in nx.enumerate_all_cliques(G_pmfg) if len(c) == 3]
    cliques_4 = [c for c in nx.enumerate_all_cliques(G_pmfg) if len(c) == 4]
    
    # Centrality measures
    degree_cent = nx.degree_centrality(G_pmfg)
    between_cent = nx.betweenness_centrality(G_pmfg)
    
    # Community detection
    communities = nx.community.greedy_modularity_communities(G_pmfg)
    
    return {
        'n_triangles': len(cliques_3),
        'n_tetrahedra': len(cliques_4),
        'centralities': (degree_cent, between_cent),
        'communities': communities
    }

# Usage example
returns = load_stock_returns()  # N stocks × T time periods
corr_matrix = np.corrcoef(returns)
dist_matrix = correlation_to_distance(corr_matrix)
pmfg = construct_PMFG(dist_matrix)
features = analyze_pmfg(pmfg)
```

### Visualization

**Graph layouts**:
- Force-directed (Fruchterman-Reingold)
- Circular (by sector)
- Hierarchical (based on MST or DBHT)

**Color coding**:
- Sectors/industries
- Centrality measures
- Community membership
- Persistence scores

---

## Comparison of Methods

### Summary Table

| Method | Edges | Planarity | Chordal | Complexity | Best for |
|--------|-------|-----------|---------|------------|----------|
| **MST** | n-1 | Yes | Yes | O(n² log n) | Hierarchical structure |
| **PMFG** | 3(n-2) | Yes | No | O(n³) | Balanced info/sparsity |
| **TMFG** | 3(n-2) | Yes | Yes | O(n²) | Large datasets |
| **DBHT** | n-1 | Yes | Yes | O(n²) | Sector identification |
| **Threshold** | Variable | No | No | O(n²) | Simple baseline |

### When to Use Each Method

**MST**: 
- Need strictly hierarchical structure
- Very large N (>1000)
- Preliminary exploration

**PMFG**:
- Medium N (100-500)
- Need topological properties (cliques, separators)
- Computational time not critical

**TMFG**:
- Large N (>500)
- Need computational efficiency
- Machine learning pipeline integration
- Markov Random Field modeling

**DBHT**:
- Sector/community identification
- Multi-scale hierarchical analysis
- Comparing clustering methods

---

## Key Insights and Conclusions

### 1. Topology Matters

The topological structure (planarity, cliques, separators) captures information about market organization that simple thresholding misses.

### 2. More is Not Always Better

**Optimal sparsity**: 3(n-2) edges for PMFG/TMFG appears to be sweet spot:
- Enough edges to capture structure
- Sparse enough to be interpretable and stable
- Maintains planarity (visualizable)

### 3. Dynamic Networks Reveal Crises

Rolling window analysis shows correlation structure changes precede and accompany financial crises.

**Warning signals**:
- Increasing connectivity
- Decreasing modularity (sector boundaries blur)
- Rising persistence of systemic motifs

### 4. Hierarchy and Communities

Multiple hierarchical scales exist in financial networks, with different methods revealing different aspects.

**Levels**:
- Micro: Individual stock connections
- Meso: Sector/industry organization
- Macro: Market-wide factors

### 5. Persistence as Risk Indicator

Persistent structures (triangles, tetrahedra) that survive across time windows indicate stable risk factors and systemic vulnerabilities.

---

## Future Directions

### Emerging Research Areas

1. **Integration with causality**: Extend from correlation to directed causal networks

2. **Non-linear dependencies**: Incorporate mutual information and nonlinear measures beyond correlation

3. **Multi-layer networks**: Combine different relationship types (returns, volumes, news sentiment)

4. **Real-time monitoring**: Deploy filtering methods for live market surveillance

5. **Quantum complexity**: Explore quantum algorithms for faster filtering

6. **Climate finance**: Apply to ESG and climate risk networks

---

## Bibliography: Key Papers by Aste and Collaborators

### Foundational Papers

1. **Tumminello, M., Aste, T., Di Matteo, T., & Mantegna, R. N. (2005)**. "A tool for filtering information in complex systems." *Proceedings of the National Academy of Sciences*, 102(30), 10421-10426.
   - *Original PMFG paper*

2. **Aste, T., Di Matteo, T., & Hyde, S. T. (2005)**. "Complex Networks on Hyperbolic Surfaces." *Physica A*, 346, 20-26.
   - *Theoretical foundations*

3. **Mantegna, R. N. (1999)**. "Hierarchical structure in financial markets." *European Physical Journal B*, 11(1), 193-197.
   - *MST for financial markets*

### Methodological Advances

4. **Massara, G. P., Di Matteo, T., & Aste, T. (2016)**. "Network Filtering for Big Data: Triangulated Maximally Filtered Graph." *Journal of Complex Networks*, 5(2), 161-178.
   - *TMFG algorithm*

5. **Song, W.-M., Di Matteo, T., & Aste, T. (2012)**. "Hierarchical information clustering by means of topologically embedded graphs." *PLoS One*, 7(3), e31929.
   - *Hierarchical clustering on filtered graphs*

### Financial Applications

6. **Musmeci, N., Aste, T., & Di Matteo, T. (2015)**. "Relation between financial market structure and the real economy: Comparison between clustering methods." *PLoS ONE*, 10(3), e0126998.
   - *Sector classification validation*

7. **Pozzi, F., Di Matteo, T., & Aste, T. (2013)**. "Spread of risk across financial markets: Better to invest in the peripheries." *Scientific Reports*, 3, 1665.
   - *Portfolio diversification*

8. **Musmeci, N., Aste, T., & Di Matteo, T. (2015)**. "Risk diversification: A study of persistence with a filtered correlation-network approach." *Journal of Network Theory in Finance*, 1(1), 77-98.
   - *Dynamic risk analysis*

### Recent Developments

9. **Turiel, J., Barucca, P., & Aste, T. (2022)**. "Simplicial Persistence of Financial Markets: Filtering, Generative Processes and Structural Risk." *Entropy*, 24(10), 1482.
   - *Topological data analysis*

10. **Turiel, J., & Aste, T. (2022)**. "Heterogeneous Criticality in High Frequency Finance: A Phase Transition in Flash Crashes." *Quantitative Finance*, 22(8), 1429-1441.
    - *Critical phenomena in markets*

---

## Conclusion

Tomaso Aste and colleagues have developed a powerful suite of geometric filtering methods that extract meaningful structure from noisy correlation matrices. Their work has:

1. **Established rigorous mathematical foundations** for network filtering
2. **Provided computationally efficient algorithms** (PMFG, TMFG)
3. **Validated methods** against economic reality (sector classifications)
4. **Enabled practical applications** in portfolio management and risk assessment
5. **Extended to modern challenges** (ML integration, TDA, cryptocurrencies)

**Key contribution**: Demonstrating that **topology and geometry** capture market structure more effectively than traditional statistical methods, opening new avenues for understanding systemic risk and market dynamics.

**Impact**: The methods are now widely used in:
- Academic research (500+ citations for main PMFG paper)
- Quantitative finance (portfolio construction, risk management)
- Regulatory analysis (systemic risk monitoring)
- Machine learning pipelines (feature extraction from financial networks)

**Philosophy**: "The aim is to filter out complex networks by keeping only the main representative links" - balancing information retention with interpretability through geometric constraints.

---

*Document prepared: October 30, 2024*  
*Based on research spanning 2005-2024*
