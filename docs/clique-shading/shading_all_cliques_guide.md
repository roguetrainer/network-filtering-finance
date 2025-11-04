# Shading All Cliques (Faces) in Geometric Correlation Networks

## Overview

This guide extends triangle shading to **all cliques** (complete subgraphs) in PMFG and TMFG networks. While triangles (3-cliques) are the fundamental faces in planar graphs, larger cliques (4-cliques, 5-cliques, etc.) can exist and provide additional structural insights.

### Key Differences from Triangle-Only Shading:

**Triangles (3-cliques)**:
- Always form faces in planar graphs
- Guaranteed to be convex polygons
- Easy to render as filled polygons
- Maximum: 3(N-2) in PMFG/TMFG

**Larger Cliques (k-cliques, k > 3)**:
- May or may not form single faces
- Can be non-convex or self-intersecting when projected to 2D
- Require careful polygon decomposition
- Overlapping visualization challenges
- Less common but structurally significant

**What Changes**: 
- Clique enumeration (all sizes, not just triangles)
- Polygon rendering (handle non-convex shapes)
- Color mapping (distinguish clique sizes)
- Overlap handling (layering strategy)
- Performance optimization (exponential growth)

---

## Method 1: Matplotlib with All Clique Sizes

### Basic Implementation

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
from scipy.spatial import ConvexHull

def draw_pmfg_with_all_cliques(G, pos, ax=None, max_clique_size=None):
    """
    Draw PMFG with all cliques shaded, not just triangles.
    
    Parameters:
    -----------
    G : networkx.Graph
        PMFG network with edge weights
    pos : dict
        Node positions {node: (x, y)}
    max_clique_size : int or None
        Maximum clique size to render (None = all)
    ax : matplotlib axis
        Axis to draw on (creates new if None)
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 10))
    
    # Find ALL cliques (not just triangles)
    all_cliques = list(nx.enumerate_all_cliques(G))
    
    # Group by size
    cliques_by_size = {}
    for clique in all_cliques:
        size = len(clique)
        if size >= 3:  # Only care about cliques of size 3+
            if max_clique_size is None or size <= max_clique_size:
                if size not in cliques_by_size:
                    cliques_by_size[size] = []
                cliques_by_size[size].append(clique)
    
    print(f"Clique statistics:")
    for size in sorted(cliques_by_size.keys()):
        print(f"  {size}-cliques: {len(cliques_by_size[size])}")
    
    # Define color scheme by clique size
    # Larger cliques get different colors for distinction
    clique_colors = {
        3: 'coolwarm',    # Triangles: blue to red
        4: 'viridis',     # 4-cliques: purple to yellow
        5: 'plasma',      # 5-cliques: purple to orange
        6: 'inferno',     # 6-cliques: black to white
    }
    
    # Draw cliques from largest to smallest (larger on bottom)
    for size in sorted(cliques_by_size.keys(), reverse=True):
        cliques = cliques_by_size[size]
        cmap_name = clique_colors.get(size, 'gray')
        
        for clique in cliques:
            vertices = np.array([pos[node] for node in clique])
            
            # For cliques larger than triangles, use convex hull
            if len(vertices) > 3:
                try:
                    hull = ConvexHull(vertices)
                    hull_vertices = vertices[hull.vertices]
                except:
                    # If convex hull fails, use original vertices
                    hull_vertices = vertices
            else:
                hull_vertices = vertices
            
            # Calculate average edge weight (correlation)
            edges = [(clique[i], clique[j]) 
                    for i in range(len(clique)) 
                    for j in range(i+1, len(clique))]
            weights = [G[u][v]['weight'] for u, v in edges 
                      if G.has_edge(u, v)]
            
            if weights:
                avg_weight = np.mean(weights)
                # Convert distance to correlation: rho = 1 - d²/2
                avg_correlation = 1 - (avg_weight ** 2) / 2
                
                # Map correlation to color
                color_val = (avg_correlation + 1) / 2  # Normalize to [0,1]
                color = plt.cm.get_cmap(cmap_name)(color_val)
                
                # Alpha decreases with clique size (avoid over-saturation)
                alpha = 0.4 / (size - 2)  # 0.4 for triangles, 0.2 for 4-cliques
                
                # Create polygon patch
                polygon = mpatches.Polygon(
                    hull_vertices, 
                    closed=True,
                    facecolor=color,
                    edgecolor='none',
                    alpha=alpha,
                    zorder=1 + (10 - size)  # Larger cliques rendered first (lower)
                )
                ax.add_patch(polygon)
    
    # Draw edges on top
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.6, 
                          edge_color='gray', width=2, zorder=20)
    
    # Draw nodes on top
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=300, 
                          node_color='lightblue', 
                          edgecolors='black', linewidths=2, zorder=30)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, 
                           font_weight='bold', zorder=40)
    
    # Add legend showing clique sizes
    legend_elements = []
    for size in sorted(cliques_by_size.keys()):
        cmap_name = clique_colors.get(size, 'gray')
        color = plt.cm.get_cmap(cmap_name)(0.7)
        legend_elements.append(
            mpatches.Patch(facecolor=color, edgecolor='black',
                          label=f'{size}-cliques (n={len(cliques_by_size[size])})')
        )
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    
    return ax


# Usage example
from correlation_network_animation import CorrelationFilter

# Create correlation matrix
corr_matrix = np.random.rand(20, 20)
corr_matrix = (corr_matrix + corr_matrix.T) / 2
np.fill_diagonal(corr_matrix, 1.0)

# Create PMFG
distance_matrix = np.sqrt(2 * (1 - corr_matrix))
pmfg = CorrelationFilter.planar_maximally_filtered_graph(distance_matrix)

# Create layout
pos = nx.spring_layout(pmfg, k=2/np.sqrt(len(pmfg.nodes())), iterations=100)

# Draw with all cliques shaded
fig, ax = plt.subplots(figsize=(12, 10))
draw_pmfg_with_all_cliques(pmfg, pos, ax)
plt.title('PMFG with All Cliques Shaded', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('pmfg_all_cliques.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Method 2: Advanced Clique Coloring Strategies

### Strategy 1: Size-Based Color Scheme

```python
def get_clique_color_by_size_and_strength(G, clique, size):
    """
    Color cliques by both size and correlation strength.
    Different color schemes for different clique sizes.
    """
    # Calculate average correlation
    edges = [(clique[i], clique[j]) 
            for i in range(len(clique)) 
            for j in range(i+1, len(clique))]
    weights = [G[u][v]['weight'] for u, v in edges if G.has_edge(u, v)]
    
    if not weights:
        return (0.5, 0.5, 0.5, 0.3)
    
    avg_weight = np.mean(weights)
    avg_correlation = 1 - (avg_weight ** 2) / 2
    
    # Different color schemes by size
    color_schemes = {
        3: 'RdYlBu_r',   # Triangles: diverging
        4: 'viridis',    # 4-cliques: sequential
        5: 'plasma',     # 5-cliques: sequential
        6: 'inferno',    # 6-cliques: sequential
    }
    
    cmap_name = color_schemes.get(size, 'gray')
    cmap = plt.cm.get_cmap(cmap_name)
    
    # Normalize correlation to [0, 1]
    color_val = (avg_correlation + 1) / 2
    
    # Get RGBA color
    color = cmap(color_val)
    
    # Adjust alpha by size
    alpha = 0.5 / max(1, size - 2)
    
    return (*color[:3], alpha)


def draw_cliques_with_size_distinction(G, pos, ax=None):
    """
    Draw network with clear visual distinction between clique sizes.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 12))
    
    # Find all cliques
    all_cliques = list(nx.enumerate_all_cliques(G))
    cliques_by_size = {}
    
    for clique in all_cliques:
        size = len(clique)
        if size >= 3:
            if size not in cliques_by_size:
                cliques_by_size[size] = []
            cliques_by_size[size].append(clique)
    
    # Draw from largest to smallest
    for size in sorted(cliques_by_size.keys(), reverse=True):
        for clique in cliques_by_size[size]:
            vertices = np.array([pos[node] for node in clique])
            
            # Use convex hull for larger cliques
            if len(vertices) > 3:
                try:
                    hull = ConvexHull(vertices)
                    vertices = vertices[hull.vertices]
                except:
                    pass
            
            # Get color
            color = get_clique_color_by_size_and_strength(G, clique, size)
            
            # Draw polygon with edge
            polygon = mpatches.Polygon(
                vertices, closed=True,
                facecolor=color,
                edgecolor='black' if size > 3 else 'none',  # Outline larger cliques
                linewidth=0.5 if size > 3 else 0,
                alpha=color[3],
                zorder=10 - size
            )
            ax.add_patch(polygon)
    
    # Draw network
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.5, width=1.5, zorder=20)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=250, 
                          node_color='white', edgecolors='black',
                          linewidths=1.5, zorder=30)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, zorder=40)
    
    # Statistics in title
    stats = " | ".join([f"{size}-cliques: {len(cliques)}" 
                        for size, cliques in sorted(cliques_by_size.items())])
    ax.set_title(f'Network with All Cliques\n{stats}', 
                fontsize=12, fontweight='bold')
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    
    return ax
```

### Strategy 2: Hierarchical Clique Rendering

```python
def draw_cliques_hierarchically(G, pos, correlation_matrix, ax=None):
    """
    Render cliques with visual hierarchy:
    - Largest cliques as background (most transparent)
    - Smaller cliques progressively more opaque
    - Creates depth perception
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 12))
    
    # Find all maximal cliques (not contained in larger cliques)
    all_cliques = list(nx.find_cliques(G))  # Maximal cliques
    
    # Also get all cliques for completeness
    all_subcliques = list(nx.enumerate_all_cliques(G))
    cliques_by_size = {}
    
    for clique in all_subcliques:
        size = len(clique)
        if size >= 3:
            if size not in cliques_by_size:
                cliques_by_size[size] = []
            cliques_by_size[size].append(clique)
    
    print(f"Maximal cliques: {len(all_cliques)}")
    print(f"Total cliques (size ≥ 3): {sum(len(v) for v in cliques_by_size.values())}")
    
    # Define rendering layers (largest first = background)
    for size in sorted(cliques_by_size.keys(), reverse=True):
        cliques = cliques_by_size[size]
        
        # Alpha: larger cliques more transparent
        base_alpha = 0.15 + (0.25 / size)  
        
        for clique in cliques:
            vertices = np.array([pos[node] for node in clique])
            
            # Convex hull for rendering
            if len(vertices) > 3:
                try:
                    hull = ConvexHull(vertices)
                    vertices = vertices[hull.vertices]
                except:
                    pass
            
            # Calculate correlation
            corr_vals = []
            for i in range(len(clique)):
                for j in range(i+1, len(clique)):
                    if clique[i] < len(correlation_matrix) and \
                       clique[j] < len(correlation_matrix):
                        corr_vals.append(correlation_matrix[clique[i], clique[j]])
            
            if corr_vals:
                avg_corr = np.mean(corr_vals)
                
                # Color intensity by correlation
                if avg_corr > 0.5:
                    color = plt.cm.Reds((avg_corr - 0.5) * 2)
                elif avg_corr > 0:
                    color = plt.cm.YlOrRd(avg_corr * 2)
                else:
                    color = plt.cm.Blues(abs(avg_corr))
                
                # Draw polygon
                polygon = mpatches.Polygon(
                    vertices, closed=True,
                    facecolor=color[:3],
                    edgecolor='gray' if size > 4 else 'none',
                    linewidth=0.3,
                    alpha=base_alpha,
                    zorder=1 + (10 - size)
                )
                ax.add_patch(polygon)
    
    # Draw network structure
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.6, 
                          edge_color='#444444', width=1.8, zorder=20)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=300,
                          node_color='white', edgecolors='black',
                          linewidths=2, zorder=30)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8,
                           font_weight='bold', zorder=40)
    
    # Create legend
    legend_elements = []
    for size in sorted(cliques_by_size.keys()):
        count = len(cliques_by_size[size])
        legend_elements.append(
            mpatches.Patch(facecolor=plt.cm.Reds(0.6),
                          alpha=0.15 + (0.25 / size),
                          edgecolor='black' if size > 4 else 'none',
                          label=f'{size}-cliques: {count}')
        )
    ax.legend(handles=legend_elements, loc='upper right',
             fontsize=9, framealpha=0.9)
    
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.axis('off')
    
    return ax
```

---

## Method 3: Animated All-Clique Visualization

### Extending Animation Framework

```python
class NetworkAnimatorWithAllCliques:
    """
    Extended animator that shades ALL cliques, not just triangles.
    """
    
    def __init__(self, figsize=(14, 12), max_clique_size=6):
        self.figsize = figsize
        self.max_clique_size = max_clique_size
        self.fig = None
        self.ax = None
    
    def draw_all_cliques_frame(self, G, pos, correlation_matrix=None):
        """
        Draw single frame with all cliques shaded.
        """
        # Find all cliques
        all_cliques = list(nx.enumerate_all_cliques(G))
        cliques_by_size = {}
        
        for clique in all_cliques:
            size = len(clique)
            if 3 <= size <= self.max_clique_size:
                if size not in cliques_by_size:
                    cliques_by_size[size] = []
                cliques_by_size[size].append(clique)
        
        # Clear previous
        self.ax.clear()
        
        # Draw cliques (largest first)
        for size in sorted(cliques_by_size.keys(), reverse=True):
            for clique in cliques_by_size[size]:
                vertices = np.array([pos[node] for node in clique])
                
                # Convex hull for larger cliques
                if len(vertices) > 3:
                    try:
                        hull = ConvexHull(vertices)
                        vertices = vertices[hull.vertices]
                    except:
                        pass
                
                # Calculate correlation
                if correlation_matrix is not None:
                    corr_vals = [correlation_matrix[clique[i], clique[j]]
                                for i in range(len(clique))
                                for j in range(i+1, len(clique))
                                if clique[i] < len(correlation_matrix) and
                                   clique[j] < len(correlation_matrix)]
                    avg_corr = np.mean(corr_vals) if corr_vals else 0
                else:
                    # Use edge weights
                    edges = [(clique[i], clique[j]) 
                            for i in range(len(clique)) 
                            for j in range(i+1, len(clique))]
                    weights = [G[u][v]['weight'] for u, v in edges 
                              if G.has_edge(u, v)]
                    avg_weight = np.mean(weights) if weights else 1.0
                    avg_corr = 1 - (avg_weight ** 2) / 2
                
                # Color by size and strength
                color_val = (avg_corr + 1) / 2
                
                # Different colormaps by size
                if size == 3:
                    color = plt.cm.coolwarm(color_val)
                elif size == 4:
                    color = plt.cm.viridis(color_val)
                elif size == 5:
                    color = plt.cm.plasma(color_val)
                else:
                    color = plt.cm.inferno(color_val)
                
                alpha = 0.4 / (size - 2)
                
                polygon = mpatches.Polygon(
                    vertices, closed=True,
                    facecolor=color,
                    edgecolor='black' if size > 3 else 'none',
                    linewidth=0.5 if size > 3 else 0,
                    alpha=alpha,
                    zorder=10 - size
                )
                self.ax.add_patch(polygon)
        
        # Draw network
        nx.draw_networkx_edges(G, pos, ax=self.ax, alpha=0.5,
                              width=1.5, edge_color='gray', zorder=20)
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_size=200,
                              node_color='white', edgecolors='black',
                              linewidths=1.5, zorder=30)
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=7, zorder=40)
        
        # Statistics
        stats = " | ".join([f"{size}-cliques: {len(cs)}"
                           for size, cs in sorted(cliques_by_size.items())])
        self.ax.set_title(f'All Cliques: {stats}', fontsize=10)
        
        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.axis('off')
    
    def animate_all_cliques(self, correlation_estimates, 
                           output_file='all_cliques_animation.mp4',
                           fps=10):
        """
        Create animation showing evolution of all cliques.
        """
        from matplotlib.animation import FuncAnimation, FFMpegWriter
        
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        
        # Pre-compute graphs
        graphs = []
        positions = []
        
        for est in correlation_estimates:
            corr = est['correlation']
            dist = np.sqrt(2 * (1 - corr))
            
            # Create PMFG
            from correlation_network_animation import CorrelationFilter
            G = CorrelationFilter.planar_maximally_filtered_graph(dist)
            
            # Layout
            pos = nx.spring_layout(G, k=2/np.sqrt(len(G.nodes())),
                                  iterations=50, seed=42)
            
            graphs.append(G)
            positions.append(pos)
        
        # Animation function
        def update(frame):
            G = graphs[frame]
            pos = positions[frame]
            corr = correlation_estimates[frame]['correlation']
            
            self.draw_all_cliques_frame(G, pos, corr)
            
            date = correlation_estimates[frame].get('date', f'Frame {frame}')
            self.ax.text(0.02, 0.98, f'Date: {date}',
                        transform=self.ax.transAxes,
                        fontsize=10, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Create animation
        anim = FuncAnimation(self.fig, update, frames=len(graphs),
                            interval=1000/fps, repeat=True)
        
        # Save
        writer = FFMpegWriter(fps=fps, bitrate=1800)
        anim.save(output_file, writer=writer)
        
        print(f"Animation saved: {output_file}")
        
        return anim
```

---

## Method 4: 3D Visualization of All Cliques

### Extrude Cliques by Size

```python
def visualize_cliques_3d_by_size(G, pos, correlation_matrix):
    """
    3D visualization where cliques are extruded with height = clique size.
    Larger cliques appear taller, making hierarchy visible.
    """
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Get all cliques
    all_cliques = list(nx.enumerate_all_cliques(G))
    cliques_by_size = {}
    
    for clique in all_cliques:
        size = len(clique)
        if size >= 3:
            if size not in cliques_by_size:
                cliques_by_size[size] = []
            cliques_by_size[size].append(clique)
    
    # Draw each clique as 3D prism
    for size in sorted(cliques_by_size.keys()):
        for clique in cliques_by_size[size]:
            vertices_2d = np.array([pos[node] for node in clique])
            
            # Convex hull for rendering
            if len(vertices_2d) > 3:
                try:
                    hull = ConvexHull(vertices_2d)
                    vertices_2d = vertices_2d[hull.vertices]
                except:
                    pass
            
            # Calculate correlation
            corr_vals = [correlation_matrix[clique[i], clique[j]]
                        for i in range(len(clique))
                        for j in range(i+1, len(clique))]
            avg_corr = np.mean(corr_vals)
            
            # Height proportional to clique size
            height = size * 0.1  # Larger cliques are taller
            
            # Base and top vertices
            vertices_base = np.column_stack([vertices_2d, np.zeros(len(vertices_2d))])
            vertices_top = np.column_stack([vertices_2d, np.full(len(vertices_2d), height)])
            
            # Color by correlation
            color = plt.cm.coolwarm((avg_corr + 1) / 2)
            
            # Draw base face
            poly_base = [vertices_base]
            ax.add_collection3d(Poly3DCollection(poly_base, alpha=0.3,
                                                facecolor=color, edgecolor='black'))
            
            # Draw top face
            poly_top = [vertices_top]
            ax.add_collection3d(Poly3DCollection(poly_top, alpha=0.7,
                                                facecolor=color, edgecolor='black'))
            
            # Draw side faces
            for i in range(len(vertices_2d)):
                j = (i + 1) % len(vertices_2d)
                side = [vertices_base[i], vertices_base[j],
                       vertices_top[j], vertices_top[i]]
                poly_side = [[side]]
                ax.add_collection3d(Poly3DCollection(poly_side, alpha=0.5,
                                                    facecolor=color,
                                                    edgecolor='black'))
    
    # Axis labels
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Clique Size', fontsize=12)
    ax.set_title('3D Clique Hierarchy\n(Height = Clique Size)', 
                fontsize=14, fontweight='bold')
    
    # Set view angle
    ax.view_init(elev=20, azim=45)
    
    return fig, ax
```

---

## Key Differences: Triangles vs. All Cliques

### Conceptual Differences

| Aspect | Triangles Only | All Cliques |
|--------|----------------|-------------|
| **Enumeration** | `len(clique) == 3` | `len(clique) >= 3` |
| **Count** | O(N²) typical | Exponential in worst case |
| **Rendering** | Always convex | May need convex hull |
| **Overlaps** | Moderate | Can be extensive |
| **Interpretation** | Local structure | Hierarchical structure |
| **Performance** | Fast | Can be slow for large graphs |
| **Colors** | Single scheme | Multiple schemes by size |

### Code Differences

**Triangle-only:**
```python
triangles = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]
for triangle in triangles:
    # Simple polygon rendering
    vertices = [pos[node] for node in triangle]
    polygon = mpatches.Polygon(vertices, ...)
```

**All cliques:**
```python
all_cliques = list(nx.enumerate_all_cliques(G))
cliques_by_size = group_by_size(all_cliques)  # Group first

for size in sorted(cliques_by_size.keys(), reverse=True):  # Largest first
    for clique in cliques_by_size[size]:
        vertices = [pos[node] for node in clique]
        
        # Need convex hull for larger cliques
        if len(vertices) > 3:
            hull = ConvexHull(vertices)
            vertices = vertices[hull.vertices]
        
        # Different color scheme per size
        cmap = get_cmap_for_size(size)
        
        # Adjust alpha by size
        alpha = compute_alpha(size)
        
        polygon = mpatches.Polygon(vertices, alpha=alpha, ...)
```

---

## Performance Optimization

### For Large Graphs with Many Cliques

```python
def draw_cliques_optimized(G, pos, max_clique_size=5, sample_rate=1.0):
    """
    Optimized rendering for graphs with many cliques.
    
    Parameters:
    -----------
    max_clique_size : int
        Don't render cliques larger than this
    sample_rate : float [0, 1]
        Randomly sample this fraction of cliques (for speed)
    """
    import random
    
    # Find cliques with size limit
    cliques = []
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) >= 3 and len(clique) <= max_clique_size:
            cliques.append(clique)
    
    # Sample if too many
    if sample_rate < 1.0:
        sample_size = int(len(cliques) * sample_rate)
        cliques = random.sample(cliques, sample_size)
    
    print(f"Rendering {len(cliques)} cliques (sampled at {sample_rate*100}%)")
    
    # ... rest of rendering code
```

### Caching Convex Hulls

```python
def precompute_clique_hulls(G, pos):
    """
    Pre-compute convex hulls for all cliques.
    Useful for animations to avoid recomputing.
    """
    clique_hulls = {}
    
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) >= 3:
            vertices = np.array([pos[node] for node in clique])
            
            if len(vertices) > 3:
                try:
                    hull = ConvexHull(vertices)
                    hull_vertices = vertices[hull.vertices]
                    clique_hulls[tuple(sorted(clique))] = hull_vertices
                except:
                    clique_hulls[tuple(sorted(clique))] = vertices
            else:
                clique_hulls[tuple(sorted(clique))] = vertices
    
    return clique_hulls
```

---

## Best Practices for All-Clique Visualization

### 1. Size-Based Layering
```python
# Render largest cliques first (background)
for size in range(max_size, 2, -1):
    render_cliques_of_size(size)

# This creates natural depth ordering
```

### 2. Alpha Scaling
```python
# Transparency decreases with size
alpha = base_alpha / (size - 2)

# Prevents saturation from overlapping large cliques
```

### 3. Color Scheme Selection
```python
color_schemes = {
    3: 'coolwarm',    # Diverging for triangles
    4: 'viridis',     # Sequential for 4-cliques
    5: 'plasma',      # Different sequential for 5-cliques
    6: 'inferno',     # Yet another for 6-cliques
}

# Distinct colors help distinguish clique sizes
```

### 4. Edge Outlining
```python
# Outline larger cliques for clarity
edgecolor = 'black' if size > 3 else 'none'
linewidth = 0.5 if size > 3 else 0

# Makes non-triangular faces stand out
```

### 5. Legend with Counts
```python
# Show clique distribution
for size, cliques in cliques_by_size.items():
    legend_entry = f"{size}-cliques: {len(cliques)}"
    # Add to legend

# Helps interpret visual
```

### 6. Performance Limits
```python
# Set reasonable limits
MAX_CLIQUE_SIZE = 6  # Rarely need larger
MAX_CLIQUES_TO_RENDER = 1000  # Sample if more

# Prevents performance issues
```

---

## Interpretation Guide for All Cliques

### What Different Clique Sizes Mean:

**Triangles (3-cliques)**:
- Basic correlation structure
- Local clustering
- Common in all networks

**4-cliques (Tetrahedra)**:
- Four mutually correlated assets
- Strong local structure
- Moderately common in PMFG

**5+ cliques**:
- Highly integrated groups
- Rare but significant
- Indicate strong cohesion
- Potential systemic risk

### Visual Patterns:

**Many Small Cliques**:
- Fragmented structure
- Low systemic risk
- Good diversification

**Few Large Cliques**:
- Concentrated risk
- High correlation clusters
- Potential contagion paths

**Hierarchical Structure**:
- Nested cliques of increasing size
- Core-periphery organization
- Natural market sectors

### Temporal Analysis:

**Clique Growth**:
- Size increasing → Higher correlation
- Count increasing → More clustering
- Concern for systemic risk

**Clique Shrinkage**:
- Size decreasing → Diversification
- Count decreasing → Less clustering
- Opportunity for risk management

---

## Complete Production Example

```python
def create_comprehensive_clique_visualization(correlation_matrix,
                                             asset_names=None,
                                             max_clique_size=6,
                                             output_prefix='clique_viz'):
    """
    Create publication-quality visualization with all cliques.
    Generates multiple views for comprehensive analysis.
    """
    # Create PMFG
    from correlation_network_animation import CorrelationFilter
    distance_matrix = np.sqrt(2 * (1 - correlation_matrix))
    pmfg = CorrelationFilter.planar_maximally_filtered_graph(distance_matrix)
    
    # Layout
    pos = nx.spring_layout(pmfg, k=2/np.sqrt(len(pmfg.nodes())),
                          iterations=200, seed=42)
    
    # === View 1: All cliques with size distinction ===
    fig1, ax1 = plt.subplots(figsize=(16, 14))
    draw_cliques_with_size_distinction(pmfg, pos, ax1)
    ax1.set_title('PMFG: All Cliques by Size', fontsize=16, fontweight='bold')
    plt.savefig(f'{output_prefix}_by_size.png', dpi=300, bbox_inches='tight')
    
    # === View 2: Hierarchical rendering ===
    fig2, ax2 = plt.subplots(figsize=(16, 14))
    draw_cliques_hierarchically(pmfg, pos, correlation_matrix, ax2)
    ax2.set_title('PMFG: Hierarchical Clique Structure',
                 fontsize=16, fontweight='bold')
    plt.savefig(f'{output_prefix}_hierarchical.png', dpi=300, bbox_inches='tight')
    
    # === View 3: 3D extrusion ===
    fig3, ax3 = visualize_cliques_3d_by_size(pmfg, pos, correlation_matrix)
    plt.savefig(f'{output_prefix}_3d.png', dpi=300, bbox_inches='tight')
    
    # === View 4: Comparison (triangles vs. all cliques) ===
    fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Left: triangles only
    draw_pmfg_with_shaded_triangles(pmfg, pos, ax4a)  # Original function
    ax4a.set_title('Triangles Only', fontsize=14, fontweight='bold')
    
    # Right: all cliques
    draw_pmfg_with_all_cliques(pmfg, pos, ax4b)
    ax4b.set_title('All Cliques', fontsize=14, fontweight='bold')
    
    plt.suptitle('Comparison: Triangles vs. All Cliques',
                fontsize=16, fontweight='bold')
    plt.savefig(f'{output_prefix}_comparison.png', dpi=300, bbox_inches='tight')
    
    # Print statistics
    all_cliques = list(nx.enumerate_all_cliques(pmfg))
    clique_counts = {}
    for clique in all_cliques:
        size = len(clique)
        clique_counts[size] = clique_counts.get(size, 0) + 1
    
    print("\n=== Clique Statistics ===")
    for size in sorted(clique_counts.keys()):
        if size >= 3:
            print(f"{size}-cliques: {clique_counts[size]}")
    
    total_cliques = sum(c for s, c in clique_counts.items() if s >= 3)
    triangles = clique_counts.get(3, 0)
    print(f"\nTotal cliques (size ≥ 3): {total_cliques}")
    print(f"Triangles: {triangles} ({100*triangles/total_cliques:.1f}%)")
    
    return {
        'graph': pmfg,
        'positions': pos,
        'clique_counts': clique_counts,
        'figures': [fig1, fig2, fig3, fig4]
    }


# Usage
result = create_comprehensive_clique_visualization(
    correlation_matrix,
    asset_names=asset_names,
    output_prefix='market_cliques'
)
```

---

## Summary of Changes from Triangle-Only Guide

### 1. **Clique Enumeration**
- **Before**: `[c for c in nx.enumerate_all_cliques(G) if len(c) == 3]`
- **After**: `list(nx.enumerate_all_cliques(G))` with size grouping

### 2. **Polygon Rendering**
- **Before**: Direct polygon creation
- **After**: Convex hull computation for k > 3

### 3. **Color Schemes**
- **Before**: Single colormap
- **After**: Multiple colormaps per clique size

### 4. **Alpha Values**
- **Before**: Fixed alpha (0.3-0.4)
- **After**: Size-dependent alpha (`0.4 / (size - 2)`)

### 5. **Z-ordering**
- **Before**: All triangles at same level
- **After**: Larger cliques rendered first (background)

### 6. **Legends**
- **Before**: Simple or none
- **After**: Size-based with counts

### 7. **Performance**
- **Before**: Fast for all triangle counts
- **After**: Need sampling/limits for many cliques

### 8. **Interpretation**
- **Before**: Local correlation strength
- **After**: Hierarchical structure + size significance

---

This comprehensive guide provides everything needed to extend triangle shading to all cliques, with careful attention to the additional complexity and interpretability challenges!
