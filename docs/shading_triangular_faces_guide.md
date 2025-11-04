# Shading Triangular Faces in Geometric Correlation Networks

## Overview

Visualizing the **triangular faces** (3-cliques) of PMFG and TMFG networks can dramatically enhance interpretation by:
- Revealing local correlation strength clusters
- Making the planar structure more apparent
- Showing "correlation density" regions
- Creating more intuitive 3D-like depth perception
- Highlighting structural changes over time

This guide covers multiple approaches using matplotlib, plotly, and other libraries.

---

## Method 1: Matplotlib with Polygon Patches (2D)

### Basic Implementation

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

def draw_pmfg_with_shaded_triangles(G, pos, ax=None):
    """
    Draw PMFG with shaded triangular faces.
    
    Parameters:
    -----------
    G : networkx.Graph
        PMFG network with edge weights
    pos : dict
        Node positions {node: (x, y)}
    ax : matplotlib axis
        Axis to draw on (creates new if None)
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 10))
    
    # Find all triangles (3-cliques)
    triangles = [clique for clique in nx.enumerate_all_cliques(G) 
                 if len(clique) == 3]
    
    print(f"Found {len(triangles)} triangular faces")
    
    # Shade triangles based on internal correlation strength
    for triangle in triangles:
        # Get positions of triangle vertices
        vertices = np.array([pos[node] for node in triangle])
        
        # Calculate average edge weight (correlation) for this triangle
        edges = [(triangle[i], triangle[j]) 
                for i in range(3) for j in range(i+1, 3)]
        weights = [G[u][v]['weight'] for u, v in edges if G.has_edge(u, v)]
        
        if weights:
            avg_weight = np.mean(weights)
            # Convert distance back to correlation: d = sqrt(2(1-rho))
            # Therefore: rho = 1 - d²/2
            avg_correlation = 1 - (avg_weight ** 2) / 2
            
            # Map correlation to color
            # High correlation (close to 1) -> Red
            # Low correlation (close to 0) -> Blue
            # Negative correlation -> Purple
            if avg_correlation > 0:
                color = plt.cm.RdYlBu_r(avg_correlation)  # Red for high correlation
            else:
                color = plt.cm.PuOr((avg_correlation + 1) / 2)  # Purple for negative
            
            # Create polygon patch
            polygon = mpatches.Polygon(
                vertices, 
                closed=True,
                facecolor=color,
                edgecolor='none',
                alpha=0.3,  # Semi-transparent
                zorder=1  # Behind nodes and edges
            )
            ax.add_patch(polygon)
    
    # Draw edges on top
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.6, 
                          edge_color='gray', width=2, zorder=2)
    
    # Draw nodes on top
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=300, 
                          node_color='lightblue', 
                          edgecolors='black', linewidths=2, zorder=3)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, 
                           font_weight='bold', zorder=4)
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    
    return ax


# Usage example
from correlation_network_animation import CorrelationFilter

# Assume you have a correlation matrix
corr_matrix = np.random.rand(20, 20)
corr_matrix = (corr_matrix + corr_matrix.T) / 2  # Make symmetric
np.fill_diagonal(corr_matrix, 1.0)

# Create PMFG
distance_matrix = np.sqrt(2 * (1 - corr_matrix))
pmfg = CorrelationFilter.planar_maximally_filtered_graph(distance_matrix)

# Create layout
pos = nx.spring_layout(pmfg, k=2/np.sqrt(len(pmfg.nodes())), iterations=100)

# Draw with shaded triangles
fig, ax = plt.subplots(figsize=(12, 10))
draw_pmfg_with_shaded_triangles(pmfg, pos, ax)
plt.title('PMFG with Shaded Triangular Faces', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('pmfg_shaded_triangles.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Advanced: Color by Different Metrics

```python
def get_triangle_color_by_metric(G, triangle, metric='correlation'):
    """
    Get color for triangle based on different metrics.
    
    Parameters:
    -----------
    metric : str
        'correlation' - average correlation
        'volatility' - variance of correlations
        'centrality' - average betweenness centrality
        'cluster' - clustering coefficient
    """
    edges = [(triangle[i], triangle[j]) 
            for i in range(3) for j in range(i+1, 3)]
    
    if metric == 'correlation':
        weights = [G[u][v]['weight'] for u, v in edges if G.has_edge(u, v)]
        avg_weight = np.mean(weights)
        avg_correlation = 1 - (avg_weight ** 2) / 2
        # Normalize to [0, 1]
        return (avg_correlation + 1) / 2
    
    elif metric == 'volatility':
        weights = [G[u][v]['weight'] for u, v in edges if G.has_edge(u, v)]
        return np.std(weights) if len(weights) > 1 else 0
    
    elif metric == 'centrality':
        centrality = nx.betweenness_centrality(G)
        return np.mean([centrality[node] for node in triangle])
    
    elif metric == 'cluster':
        clustering = nx.clustering(G)
        return np.mean([clustering[node] for node in triangle])
    
    return 0.5  # Default


def draw_pmfg_with_metric_shading(G, pos, metric='correlation', cmap='RdYlBu_r'):
    """
    Draw PMFG with triangles shaded by various metrics.
    """
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Find all triangles
    triangles = [clique for clique in nx.enumerate_all_cliques(G) 
                 if len(clique) == 3]
    
    # Get color values for all triangles
    color_values = [get_triangle_color_by_metric(G, tri, metric) 
                   for tri in triangles]
    
    # Normalize colors
    vmin, vmax = min(color_values), max(color_values)
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    
    # Draw triangles
    for triangle, color_val in zip(triangles, color_values):
        vertices = np.array([pos[node] for node in triangle])
        color = plt.cm.get_cmap(cmap)(norm(color_val))
        
        polygon = mpatches.Polygon(
            vertices, closed=True,
            facecolor=color, edgecolor='none',
            alpha=0.4, zorder=1
        )
        ax.add_patch(polygon)
    
    # Draw network
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.5, width=1.5, zorder=2)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=200, 
                          node_color='white', edgecolors='black', 
                          linewidths=1.5, zorder=3)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, zorder=4)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(f'{metric.title()}', rotation=270, labelpad=20)
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    
    plt.title(f'PMFG: Triangles Shaded by {metric.title()}', 
             fontsize=14, fontweight='bold')
    
    return fig, ax
```

---

## Method 2: Animated Shaded Triangles

### Integrate into Animation Framework

```python
class NetworkAnimatorWithShading(NetworkAnimator):
    """
    Extended animator that shades triangular faces.
    """
    
    def draw_shaded_triangles(self, G, pos, ax, alpha=0.3):
        """
        Draw shaded triangular faces for a single frame.
        """
        # Find triangles
        triangles = [clique for clique in nx.enumerate_all_cliques(G) 
                     if len(clique) == 3]
        
        # Shade each triangle
        for triangle in triangles:
            vertices = np.array([pos[node] for node in triangle])
            
            # Calculate triangle "strength"
            edges = [(triangle[i], triangle[j]) 
                    for i in range(3) for j in range(i+1, 3)]
            weights = [G[u][v]['weight'] for u, v in edges if G.has_edge(u, v)]
            
            if weights:
                avg_weight = np.mean(weights)
                avg_correlation = 1 - (avg_weight ** 2) / 2
                
                # Color based on correlation
                color = plt.cm.RdYlBu_r((avg_correlation + 1) / 2)
                
                polygon = mpatches.Polygon(
                    vertices, closed=True,
                    facecolor=color, edgecolor='none',
                    alpha=alpha, zorder=1
                )
                ax.add_patch(polygon)
    
    def animate_with_shaded_faces(self, correlation_estimates, 
                                  filter_method='pmfg',
                                  output_file='animation_shaded.mp4',
                                  fps=10, triangle_alpha=0.3):
        """
        Create animation with shaded triangular faces.
        """
        print(f"Creating filtered graphs with shaded faces...")
        
        # Create graphs
        graphs = []
        dates = []
        for i, est in enumerate(correlation_estimates):
            if i % 20 == 0:
                print(f"  Processing {i+1}/{len(correlation_estimates)}")
            
            corr = est['correlation']
            dist = CorrelationFilter.correlation_to_distance(corr)
            
            if filter_method == 'pmfg':
                G = CorrelationFilter.planar_maximally_filtered_graph(dist)
            elif filter_method == 'tmfg':
                G = CorrelationFilter.triangulated_maximally_filtered_graph(dist)
            else:
                raise ValueError("Shading only works for PMFG/TMFG")
            
            graphs.append(G)
            dates.append(est['date'])
        
        # Compute layouts
        if self.dynamic_layout:
            layouts = self.compute_dynamic_layouts(graphs, smoothing_factor=0.3)
        else:
            static_pos = self.create_stable_layout(graphs)
            layouts = [static_pos] * len(graphs)
        
        # Setup
        n_nodes = len(graphs[0].nodes())
        self.setup_node_colors(n_nodes)
        
        # Create animation
        fig, ax = plt.subplots(figsize=self.figsize)
        
        def init():
            ax.clear()
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.axis('off')
            return []
        
        def update(frame):
            ax.clear()
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.axis('off')
            
            G = graphs[frame]
            pos = layouts[frame]
            date = dates[frame]
            
            # Draw shaded triangles FIRST (background)
            self.draw_shaded_triangles(G, pos, ax, alpha=triangle_alpha)
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.4, 
                                  edge_color='gray', width=2, zorder=2)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, ax=ax, 
                                  node_color=self.node_colors,
                                  node_size=300, alpha=0.9, zorder=3)
            
            # Labels
            nx.draw_networkx_labels(G, pos, ax=ax, 
                                   labels=self.node_labels,
                                   font_size=8, font_weight='bold', zorder=4)
            
            # Title
            n_triangles = sum(1 for c in nx.enumerate_all_cliques(G) if len(c) == 3)
            title = f'{filter_method.upper()} with Shaded Faces\n'
            title += f'Date: {date.strftime("%Y-%m-%d")}\n'
            title += f'Triangles: {n_triangles}'
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            
            return []
        
        # Create and save animation
        print("Creating animation with shaded faces...")
        anim = animation.FuncAnimation(fig, update, init_func=init,
                                      frames=len(graphs), interval=100,
                                      blit=True, repeat=True)
        
        print(f"Saving to {output_file}...")
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, bitrate=1800)
        anim.save(output_file, writer=writer)
        print("Done!")
        
        plt.close()
        return anim
```

---

## Method 3: Plotly for Interactive 3D with Shaded Faces

```python
import plotly.graph_objects as go
from scipy.spatial import Delaunay

def create_interactive_3d_pmfg(G, correlation_matrix):
    """
    Create interactive 3D visualization with shaded triangular faces.
    
    Uses spring layout in 3D and shades triangles based on correlation.
    """
    # 3D spring layout
    pos_3d = nx.spring_layout(G, dim=3, k=2/np.sqrt(len(G.nodes())), 
                             iterations=100, seed=42)
    
    # Extract positions
    nodes = list(G.nodes())
    x_nodes = [pos_3d[node][0] for node in nodes]
    y_nodes = [pos_3d[node][1] for node in nodes]
    z_nodes = [pos_3d[node][2] for node in nodes]
    
    # Find all triangles
    triangles = [clique for clique in nx.enumerate_all_cliques(G) 
                 if len(clique) == 3]
    
    # Create mesh for triangular faces
    x_tri = []
    y_tri = []
    z_tri = []
    intensities = []
    
    for triangle in triangles:
        # Get triangle vertices
        for node in triangle:
            idx = nodes.index(node)
            x_tri.append(x_nodes[idx])
            y_tri.append(y_nodes[idx])
            z_tri.append(z_nodes[idx])
        
        # Calculate average correlation for coloring
        corr_vals = [correlation_matrix[triangle[i], triangle[j]]
                    for i in range(3) for j in range(i+1, 3)]
        avg_corr = np.mean(corr_vals)
        intensities.extend([avg_corr] * 3)  # One value per vertex
    
    # Create triangular faces
    n_triangles = len(triangles)
    i_indices = list(range(0, 3*n_triangles, 3))
    j_indices = list(range(1, 3*n_triangles, 3))
    k_indices = list(range(2, 3*n_triangles, 3))
    
    # Create mesh3d for shaded faces
    mesh = go.Mesh3d(
        x=x_tri, y=y_tri, z=z_tri,
        i=i_indices, j=j_indices, k=k_indices,
        intensity=intensities,
        colorscale='RdYlBu_r',
        opacity=0.5,
        name='Triangular Faces',
        hoverinfo='skip',
        colorbar=dict(title="Correlation", x=1.1)
    )
    
    # Create edges
    edge_trace = []
    for edge in G.edges():
        x0, y0, z0 = pos_3d[edge[0]]
        x1, y1, z1 = pos_3d[edge[1]]
        edge_trace.append(go.Scatter3d(
            x=[x0, x1, None], y=[y0, y1, None], z=[z0, z1, None],
            mode='lines',
            line=dict(color='gray', width=2),
            hoverinfo='none',
            showlegend=False
        ))
    
    # Create nodes
    node_trace = go.Scatter3d(
        x=x_nodes, y=y_nodes, z=z_nodes,
        mode='markers+text',
        marker=dict(
            size=10,
            color='lightblue',
            line=dict(color='black', width=2)
        ),
        text=[str(node) for node in nodes],
        textposition='top center',
        name='Nodes',
        hovertemplate='Node: %{text}<extra></extra>'
    )
    
    # Create figure
    fig = go.Figure(data=[mesh] + edge_trace + [node_trace])
    
    fig.update_layout(
        title='Interactive 3D PMFG with Shaded Triangular Faces',
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title=''),
            aspectmode='cube'
        ),
        showlegend=True,
        hovermode='closest'
    )
    
    return fig


# Usage
fig = create_interactive_3d_pmfg(pmfg, corr_matrix)
fig.show()
# Or save
fig.write_html('pmfg_3d_interactive.html')
```

---

## Method 4: Mayavi for High-Quality 3D Rendering

```python
from mayavi import mlab
import networkx as nx

def visualize_pmfg_mayavi_3d(G, correlation_matrix):
    """
    Create high-quality 3D visualization with mayavi.
    """
    # 3D layout
    pos_3d = nx.spring_layout(G, dim=3, iterations=100, seed=42)
    
    # Extract coordinates
    nodes = list(G.nodes())
    x = np.array([pos_3d[n][0] for n in nodes])
    y = np.array([pos_3d[n][1] for n in nodes])
    z = np.array([pos_3d[n][2] for n in nodes])
    
    # Start mayavi
    mlab.figure(bgcolor=(1, 1, 1), size=(1200, 1000))
    
    # Draw triangular faces
    triangles = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    
    for triangle in triangles:
        # Get triangle coordinates
        tri_x = [pos_3d[n][0] for n in triangle]
        tri_y = [pos_3d[n][1] for n in triangle]
        tri_z = [pos_3d[n][2] for n in triangle]
        
        # Calculate average correlation
        corr_vals = [correlation_matrix[triangle[i], triangle[j]]
                    for i in range(3) for j in range(i+1, 3)]
        avg_corr = np.mean(corr_vals)
        
        # Map correlation to color (red = high, blue = low)
        color = (1.0, 1.0 - avg_corr, 1.0 - avg_corr)  # RGB
        
        # Draw triangle as mesh
        mlab.triangular_mesh(
            tri_x, tri_y, tri_z,
            [[0, 1, 2]],  # Single triangle
            color=color,
            opacity=0.4
        )
    
    # Draw edges
    for edge in G.edges():
        x_edge = [pos_3d[edge[0]][0], pos_3d[edge[1]][0]]
        y_edge = [pos_3d[edge[0]][1], pos_3d[edge[1]][1]]
        z_edge = [pos_3d[edge[0]][2], pos_3d[edge[1]][2]]
        mlab.plot3d(x_edge, y_edge, z_edge, 
                   tube_radius=0.01, color=(0.5, 0.5, 0.5))
    
    # Draw nodes
    mlab.points3d(x, y, z, scale_factor=0.1, color=(0.3, 0.5, 0.8))
    
    # Labels
    for i, node in enumerate(nodes):
        mlab.text3d(x[i], y[i], z[i], str(node), scale=0.05)
    
    mlab.title('PMFG with Shaded Triangular Faces (3D)')
    mlab.show()
```

---

## Method 5: Custom Shader for Real-time WebGL

```python
def export_pmfg_to_threejs(G, correlation_matrix, output_file='pmfg_3d.html'):
    """
    Export PMFG to Three.js visualization with shaded faces.
    """
    # 3D layout
    pos_3d = nx.spring_layout(G, dim=3, iterations=100, seed=42)
    
    # Find triangles
    triangles = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    
    # Generate Three.js code
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>PMFG 3D Visualization</title>
    <style>
        body {{ margin: 0; overflow: hidden; }}
        canvas {{ display: block; }}
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff);
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5;
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        
        // Add lights
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(1, 1, 1);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));
        
        // Node positions
        const positions = {json.dumps({str(n): list(pos_3d[n]) for n in G.nodes()})};
        
        // Draw triangular faces
        const triangles = {json.dumps([[str(n) for n in tri] for tri in triangles])};
        const correlations = {json.dumps([[correlation_matrix[tri[i], tri[j]] 
                                          for i in range(3) for j in range(i+1, 3)] 
                                         for tri in triangles])};
        
        triangles.forEach((tri, idx) => {{
            const geom = new THREE.BufferGeometry();
            const vertices = new Float32Array([
                ...positions[tri[0]],
                ...positions[tri[1]],
                ...positions[tri[2]]
            ]);
            geom.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
            geom.setIndex([0, 1, 2]);
            geom.computeVertexNormals();
            
            // Color based on average correlation
            const avgCorr = correlations[idx].reduce((a,b) => a+b) / correlations[idx].length;
            const color = new THREE.Color();
            color.setHSL((1 - avgCorr) * 0.7, 1.0, 0.5); // Red to blue
            
            const material = new THREE.MeshPhongMaterial({{
                color: color,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.6,
                shininess: 30
            }});
            
            const mesh = new THREE.Mesh(geom, material);
            scene.add(mesh);
        }});
        
        // Draw nodes
        Object.entries(positions).forEach(([node, pos]) => {{
            const geometry = new THREE.SphereGeometry(0.05, 32, 32);
            const material = new THREE.MeshPhongMaterial({{ color: 0x4080ff }});
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.set(...pos);
            scene.add(sphere);
            
            // Label
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = 64;
            canvas.height = 64;
            context.fillStyle = 'white';
            context.fillRect(0, 0, 64, 64);
            context.fillStyle = 'black';
            context.font = '32px Arial';
            context.textAlign = 'center';
            context.fillText(node, 32, 40);
            
            const texture = new THREE.CanvasTexture(canvas);
            const spriteMaterial = new THREE.SpriteMaterial({{ map: texture }});
            const sprite = new THREE.Sprite(spriteMaterial);
            sprite.position.set(...pos);
            sprite.scale.set(0.2, 0.2, 1);
            scene.add(sprite);
        }});
        
        // Draw edges
        const edges = {json.dumps([[str(e[0]), str(e[1])] for e in G.edges()])};
        edges.forEach(edge => {{
            const points = [
                new THREE.Vector3(...positions[edge[0]]),
                new THREE.Vector3(...positions[edge[1]])
            ];
            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            const material = new THREE.LineBasicMaterial({{ color: 0x888888 }});
            const line = new THREE.Line(geometry, material);
            scene.add(line);
        }});
        
        // Animation loop
        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();
        
        // Handle resize
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>
</body>
</html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Exported to {output_file}")
    print("Open in browser to view interactive 3D visualization")
```

---

## Method 6: Advanced Techniques

### A. Time-Varying Triangle Opacity

```python
def animate_with_pulsing_triangles(animator, correlation_estimates):
    """
    Triangles pulse based on how their correlation is changing.
    """
    # Track correlation changes
    triangle_histories = {}
    
    for frame, est in enumerate(correlation_estimates):
        corr = est['correlation']
        G = create_filtered_graph(corr)
        
        triangles = get_all_triangles(G)
        
        for tri in triangles:
            tri_id = tuple(sorted(tri))
            avg_corr = compute_triangle_correlation(G, tri)
            
            if tri_id not in triangle_histories:
                triangle_histories[tri_id] = []
            triangle_histories[tri_id].append(avg_corr)
        
        # Alpha based on rate of change
        for tri, history in triangle_histories.items():
            if len(history) > 1:
                rate_of_change = abs(history[-1] - history[-2])
                alpha = 0.2 + 0.6 * rate_of_change  # Pulse when changing
                # Draw with this alpha
```

### B. Gradient Shading Within Triangles

```python
def create_gradient_triangle(vertices, correlations):
    """
    Create triangle with gradient based on vertex correlations.
    
    Each vertex can have different color intensity.
    """
    # Use matplotlib's triangular mesh for gradient
    from matplotlib.tri import Triangulation
    
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = correlations  # One value per vertex
    
    triangulation = Triangulation(x, y)
    
    # This creates smooth gradient across triangle
    return triangulation, z
```

### C. 3D Extrusion Based on Correlation

```python
def extrude_triangles_by_correlation(G, pos, correlation_matrix):
    """
    Extrude triangles in Z-direction based on correlation strength.
    High correlation = higher elevation.
    """
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    triangles = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    
    for triangle in triangles:
        # Base triangle at z=0
        vertices_base = np.array([pos[node] for node in triangle])
        
        # Calculate height from correlation
        corr_vals = [correlation_matrix[triangle[i], triangle[j]]
                    for i in range(3) for j in range(i+1, 3)]
        avg_corr = np.mean(corr_vals)
        height = avg_corr * 0.5  # Scale height
        
        # Top triangle at z=height
        vertices_top = vertices_base.copy()
        
        # Create 3D polygon (base + top + sides)
        vertices_3d_base = np.column_stack([vertices_base, 
                                           np.zeros(3)])
        vertices_3d_top = np.column_stack([vertices_base, 
                                          np.full(3, height)])
        
        # Draw base
        poly_base = [[vertices_3d_base[0], vertices_3d_base[1], 
                     vertices_3d_base[2]]]
        ax.add_collection3d(Poly3DCollection(poly_base, alpha=0.3, 
                                            facecolor='blue', 
                                            edgecolor='black'))
        
        # Draw top
        poly_top = [[vertices_3d_top[0], vertices_3d_top[1], 
                    vertices_3d_top[2]]]
        ax.add_collection3d(Poly3DCollection(poly_top, alpha=0.7,
                                            facecolor=plt.cm.RdYlBu_r(avg_corr),
                                            edgecolor='black'))
        
        # Draw sides (3 rectangles)
        for i in range(3):
            j = (i + 1) % 3
            side = [[vertices_3d_base[i], vertices_3d_base[j],
                    vertices_3d_top[j], vertices_3d_top[i]]]
            ax.add_collection3d(Poly3DCollection(side, alpha=0.5,
                                                facecolor='gray',
                                                edgecolor='black'))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Correlation')
    ax.set_title('PMFG with Extruded Triangular Faces')
    
    return fig, ax
```

---

## Comparison of Methods

| Method | Dimensionality | Interactivity | Quality | Complexity |
|--------|---------------|---------------|---------|------------|
| Matplotlib Patches | 2D | None | Good | Low |
| Matplotlib Animation | 2D | Time | Good | Medium |
| Plotly 3D | 3D | Full | Very Good | Medium |
| Mayavi | 3D | Medium | Excellent | High |
| Three.js/WebGL | 3D | Full | Excellent | High |
| 3D Extrusion | 3D | None | Very Good | Medium |

---

## Best Practices

1. **Color Choice**:
   - Use diverging colormaps (RdYlBu_r) for correlations
   - Red = high correlation (strong)
   - Blue = low/negative correlation (weak)
   - Makes intuition immediate

2. **Alpha/Transparency**:
   - Keep alpha ≤ 0.5 to see overlapping triangles
   - Lower alpha for many triangles
   - Can vary alpha by importance

3. **Z-ordering**:
   - Triangles behind everything (zorder=1)
   - Edges middle (zorder=2)
   - Nodes in front (zorder=3)
   - Labels on top (zorder=4)

4. **Performance**:
   - For >100 triangles, use simplified rendering
   - Consider LOD (level of detail) for animations
   - Pre-compute colors to save time

5. **Interpretation**:
   - Add colorbar showing correlation scale
   - Annotate what colors mean
   - Show triangle count in title
   - Explain in caption

---

## Interpretation Guide

### What Shaded Triangles Reveal:

**Dense Red Regions**:
- High local correlation clusters
- Assets moving together
- Potential sector groupings
- Systemic risk areas

**Sparse Blue Regions**:
- Low correlation areas
- Diversification opportunities
- Independent asset groups
- Potential hedges

**Mixed Color Patterns**:
- Heterogeneous correlation structure
- Complex dependencies
- Transition regions

**Temporal Changes** (in animations):
- Red spreading → Increasing systemic risk
- Blue appearing → Diversification improving
- Color intensifying → Stronger correlations
- Flickering → Unstable relationships

---

## Complete Example: Production-Ready

```python
def create_publication_quality_pmfg(correlation_matrix, 
                                   asset_names=None,
                                   title="PMFG with Shaded Triangular Faces"):
    """
    Create publication-quality PMFG visualization with shaded faces.
    """
    # Create PMFG
    distance_matrix = np.sqrt(2 * (1 - correlation_matrix))
    pmfg = CorrelationFilter.planar_maximally_filtered_graph(distance_matrix)
    
    # Layout
    pos = nx.spring_layout(pmfg, k=2/np.sqrt(len(pmfg.nodes())), 
                          iterations=200, seed=42)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 14))
    
    # Get triangles
    triangles = [c for c in nx.enumerate_all_cliques(pmfg) if len(c) == 3]
    print(f"Network has {len(triangles)} triangular faces")
    
    # Shade triangles
    color_values = []
    for triangle in triangles:
        vertices = np.array([pos[node] for node in triangle])
        
        # Calculate average correlation
        corr_vals = [correlation_matrix[triangle[i], triangle[j]]
                    for i in range(3) for j in range(i+1, 3)]
        avg_corr = np.mean(corr_vals)
        color_values.append(avg_corr)
        
        # Color
        color = plt.cm.RdYlBu_r(avg_corr)
        
        # Draw
        polygon = mpatches.Polygon(vertices, closed=True,
                                  facecolor=color, edgecolor='none',
                                  alpha=0.4, zorder=1)
        ax.add_patch(polygon)
    
    # Draw network
    edges = pmfg.edges(data=True)
    edge_weights = [1.0/(1.0 + e[2]['weight']) for e in edges]
    max_weight = max(edge_weights)
    edge_widths = [3 * w / max_weight for w in edge_weights]
    
    nx.draw_networkx_edges(pmfg, pos, ax=ax, width=edge_widths,
                          alpha=0.6, edge_color='#333333', zorder=2)
    
    # Draw nodes
    nx.draw_networkx_nodes(pmfg, pos, ax=ax, node_size=400,
                          node_color='white', edgecolors='black',
                          linewidths=2, zorder=3)
    
    # Labels
    if asset_names:
        labels = {i: asset_names[i] for i in range(len(asset_names))}
    else:
        labels = {i: f"A{i}" for i in pmfg.nodes()}
    
    nx.draw_networkx_labels(pmfg, pos, labels, ax=ax,
                           font_size=9, font_weight='bold',
                           font_family='sans-serif', zorder=4)
    
    # Colorbar
    norm = plt.Normalize(vmin=min(color_values), vmax=max(color_values))
    sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Average Triangle Correlation', 
                  rotation=270, labelpad=25, fontsize=12)
    
    # Formatting
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.axis('off')
    ax.set_aspect('equal')
    
    # Title with statistics
    n_edges = pmfg.number_of_edges()
    avg_degree = 2 * n_edges / len(pmfg.nodes())
    
    title_full = f"{title}\n"
    title_full += f"Edges: {n_edges} | Triangles: {len(triangles)} | "
    title_full += f"Avg Degree: {avg_degree:.1f}"
    
    ax.set_title(title_full, fontsize=16, fontweight='bold', pad=20)
    
    # Save
    plt.tight_layout()
    plt.savefig('pmfg_shaded_publication.png', dpi=300, 
               bbox_inches='tight', facecolor='white')
    plt.savefig('pmfg_shaded_publication.pdf', 
               bbox_inches='tight', facecolor='white')
    
    return fig, ax
```

---

This comprehensive guide provides multiple approaches for shading triangular faces in PMFG/TMFG visualizations, from simple 2D matplotlib to advanced 3D interactive visualizations!
