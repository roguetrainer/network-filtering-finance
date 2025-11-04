"""
Animated Correlation Network Filtering
=======================================

This script creates animations of filtered correlation networks over time using:
1. Synthetic time series with time-varying correlations
2. Rolling window correlation estimation
3. Network filtering methods (MST, PMFG, TMFG)
4. Graph layout and animation

Based on the work of Tomaso Aste and colleagues on geometric filtering methods.
"""

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from scipy.spatial.distance import squareform, pdist
from scipy.linalg import cholesky
import warnings
warnings.filterwarnings('ignore')


class SyntheticCorrelationGenerator:
    """
    Generate synthetic time series with time-varying correlation structure.
    
    Uses a diffusion process for correlation matrix parameters that evolves
    smoothly over time, allowing for realistic changing correlation structures.
    """
    
    def __init__(self, n_assets, seed=42):
        """
        Parameters:
        -----------
        n_assets : int
            Number of assets (time series)
        seed : int
            Random seed for reproducibility
        """
        self.n_assets = n_assets
        self.rng = np.random.RandomState(seed)
        
    def generate_base_correlation_matrix(self, block_structure=True):
        """
        Generate a base correlation matrix with optional block structure.
        
        Parameters:
        -----------
        block_structure : bool
            If True, create blocks of highly correlated assets (sectors)
            
        Returns:
        --------
        corr_matrix : np.ndarray
            Valid correlation matrix (positive semi-definite)
        """
        if block_structure:
            # Create sector-based correlation structure
            n_sectors = max(3, self.n_assets // 5)
            sector_assignments = np.random.choice(n_sectors, self.n_assets)
            
            # Base correlation matrix
            corr = np.eye(self.n_assets)
            
            for i in range(self.n_assets):
                for j in range(i+1, self.n_assets):
                    if sector_assignments[i] == sector_assignments[j]:
                        # Within sector: higher correlation
                        corr[i, j] = corr[j, i] = self.rng.uniform(0.4, 0.8)
                    else:
                        # Between sectors: lower correlation
                        corr[i, j] = corr[j, i] = self.rng.uniform(-0.1, 0.3)
        else:
            # Random correlation matrix
            A = self.rng.randn(self.n_assets, self.n_assets)
            corr = np.dot(A, A.T)
            
        # Ensure positive definite
        corr = self._ensure_positive_definite(corr)
        
        # Normalize to correlation matrix
        D = np.diag(1.0 / np.sqrt(np.diag(corr)))
        corr = D @ corr @ D
        
        return corr
    
    def _ensure_positive_definite(self, matrix, epsilon=1e-6):
        """Make matrix positive definite by adjusting eigenvalues."""
        eigvals, eigvecs = np.linalg.eigh(matrix)
        eigvals[eigvals < epsilon] = epsilon
        return eigvecs @ np.diag(eigvals) @ eigvecs.T
    
    def evolve_correlation_parameters(self, base_corr, n_steps, volatility=0.1):
        """
        Evolve correlation matrix parameters using a diffusion process.
        
        Parameters:
        -----------
        base_corr : np.ndarray
            Starting correlation matrix
        n_steps : int
            Number of time steps
        volatility : float
            Volatility of the diffusion process (controls rate of change)
            
        Returns:
        --------
        corr_sequence : list of np.ndarray
            Sequence of correlation matrices over time
        """
        corr_sequence = [base_corr.copy()]
        current_corr = base_corr.copy()
        
        for t in range(1, n_steps):
            # Ornstein-Uhlenbeck type process for mean reversion
            mean_reversion = 0.95
            
            # Extract off-diagonal correlations
            n = self.n_assets
            tril_idx = np.tril_indices(n, k=-1)
            correlations = current_corr[tril_idx]
            
            # Add noise and mean reversion
            noise = self.rng.randn(len(correlations)) * volatility
            correlations = mean_reversion * correlations + noise
            
            # Clip to valid correlation range
            correlations = np.clip(correlations, -0.95, 0.95)
            
            # Reconstruct symmetric matrix
            new_corr = np.eye(n)
            new_corr[tril_idx] = correlations
            new_corr = new_corr + new_corr.T - np.eye(n)
            
            # Ensure positive definite
            new_corr = self._ensure_positive_definite(new_corr)
            
            # Normalize
            D = np.diag(1.0 / np.sqrt(np.diag(new_corr)))
            new_corr = D @ new_corr @ D
            
            corr_sequence.append(new_corr)
            current_corr = new_corr
            
        return corr_sequence
    
    def generate_returns(self, corr_matrix, n_observations, mean_return=0.0, volatility=0.02):
        """
        Generate multivariate normal returns with given correlation structure.
        
        Parameters:
        -----------
        corr_matrix : np.ndarray
            Correlation matrix
        n_observations : int
            Number of return observations
        mean_return : float
            Mean return for all assets
        volatility : float
            Volatility for all assets
            
        Returns:
        --------
        returns : np.ndarray
            Shape (n_observations, n_assets)
        """
        mean = np.ones(self.n_assets) * mean_return
        cov = corr_matrix * (volatility ** 2)
        
        returns = self.rng.multivariate_normal(mean, cov, size=n_observations)
        return returns
    
    def generate_time_series(self, total_days=1000, window_size=252, 
                           volatility_process=0.05, returns_per_day=1):
        """
        Generate complete synthetic time series with evolving correlations.
        
        Parameters:
        -----------
        total_days : int
            Total number of days to generate
        window_size : int
            Size of rolling window for correlation estimation
        volatility_process : float
            Volatility of correlation evolution process
        returns_per_day : int
            Number of return observations per day
            
        Returns:
        --------
        returns_df : pd.DataFrame
            Daily returns with DatetimeIndex
        true_correlations : list of np.ndarray
            True correlation matrix for each day
        """
        # Generate evolving correlation structure
        n_correlation_states = total_days
        base_corr = self.generate_base_correlation_matrix(block_structure=True)
        correlation_sequence = self.evolve_correlation_parameters(
            base_corr, n_correlation_states, volatility=volatility_process
        )
        
        # Generate returns for each day
        all_returns = []
        dates = pd.date_range(start='2020-01-01', periods=total_days, freq='D')
        
        for day_idx, corr_matrix in enumerate(correlation_sequence):
            day_returns = self.generate_returns(
                corr_matrix, 
                n_observations=returns_per_day,
                volatility=0.02
            )
            # Aggregate to daily if multiple observations per day
            daily_return = day_returns.mean(axis=0)
            all_returns.append(daily_return)
        
        # Create DataFrame
        returns_df = pd.DataFrame(
            all_returns,
            index=dates,
            columns=[f'Asset_{i:02d}' for i in range(self.n_assets)]
        )
        
        return returns_df, correlation_sequence


class CorrelationFilter:
    """
    Apply network filtering methods to correlation matrices.
    """
    
    @staticmethod
    def correlation_to_distance(corr_matrix):
        """
        Convert correlation matrix to distance matrix using the metric:
        d_ij = sqrt(2(1 - C_ij))
        
        This satisfies triangle inequality and maps:
        - Perfect correlation (1) -> distance 0
        - No correlation (0) -> distance sqrt(2)
        - Perfect anti-correlation (-1) -> distance 2
        """
        distance = np.sqrt(2 * (1 - corr_matrix))
        np.fill_diagonal(distance, 0)
        return distance
    
    @staticmethod
    def minimum_spanning_tree(distance_matrix):
        """
        Construct Minimum Spanning Tree using Kruskal's algorithm.
        
        Returns:
        --------
        G : networkx.Graph
            MST with n-1 edges
        """
        n = distance_matrix.shape[0]
        
        # Create complete graph
        G_complete = nx.Graph()
        for i in range(n):
            for j in range(i+1, n):
                G_complete.add_edge(i, j, weight=distance_matrix[i, j])
        
        # Compute MST
        mst = nx.minimum_spanning_tree(G_complete, weight='weight')
        
        return mst
    
    @staticmethod
    def planar_maximally_filtered_graph(distance_matrix, max_iterations=None):
        """
        Construct PMFG by iteratively adding edges while maintaining planarity.
        
        Algorithm from Tumminello et al. (2005) PNAS.
        
        Returns:
        --------
        G : networkx.Graph
            PMFG with 3(n-2) edges (planar graph)
        """
        n = distance_matrix.shape[0]
        
        # Create complete graph
        G_complete = nx.Graph()
        for i in range(n):
            for j in range(i+1, n):
                G_complete.add_edge(i, j, weight=distance_matrix[i, j])
        
        # Sort edges by weight (smallest distance = highest correlation first)
        edges_sorted = sorted(G_complete.edges(data=True), 
                            key=lambda x: x[2]['weight'])
        
        # Build PMFG
        G_pmfg = nx.Graph()
        G_pmfg.add_nodes_from(range(n))
        max_edges = 3 * (n - 2)
        
        if max_iterations is None:
            max_iterations = len(edges_sorted)
        
        iterations = 0
        for source, dest, data in edges_sorted:
            if iterations >= max_iterations:
                break
            iterations += 1
            
            # Try adding edge
            G_pmfg.add_edge(source, dest, weight=data['weight'])
            
            # Check planarity
            is_planar, _ = nx.check_planarity(G_pmfg)
            if not is_planar:
                G_pmfg.remove_edge(source, dest)
            
            # Stop when we have enough edges
            if G_pmfg.number_of_edges() >= max_edges:
                break
        
        return G_pmfg
    
    @staticmethod
    def triangulated_maximally_filtered_graph(distance_matrix):
        """
        Construct TMFG using greedy triangle insertion (simplified version).
        
        Note: This is a simplified approximation. Full TMFG algorithm from
        Massara et al. (2016) involves more sophisticated geometric operations.
        
        Returns:
        --------
        G : networkx.Graph
            Approximate TMFG with 3(n-2) edges
        """
        n = distance_matrix.shape[0]
        
        # For small n, use PMFG
        if n <= 20:
            return CorrelationFilter.planar_maximally_filtered_graph(distance_matrix)
        
        # Start with 4 nodes forming tetrahedron (complete graph K4)
        G = nx.complete_graph(4)
        
        # Add weights to initial edges
        for i in range(4):
            for j in range(i+1, 4):
                G[i][j]['weight'] = distance_matrix[i, j]
        
        # Remaining nodes to insert
        remaining_nodes = list(range(4, n))
        
        # Insert nodes one by one
        while remaining_nodes and G.number_of_edges() < 3 * (n - 2):
            # Find best node to insert
            best_node = None
            best_triangle = None
            best_score = float('inf')
            
            for node in remaining_nodes[:min(5, len(remaining_nodes))]:  # Check first 5 for speed
                # Find best triangle to insert into
                for triangle in nx.enumerate_all_cliques(G):
                    if len(triangle) == 3:
                        # Score based on sum of distances to triangle vertices
                        score = sum(distance_matrix[node, v] for v in triangle)
                        if score < best_score:
                            best_score = score
                            best_node = node
                            best_triangle = triangle
            
            if best_node is None:
                break
            
            # Insert node into triangle
            for v in best_triangle:
                G.add_edge(best_node, v, weight=distance_matrix[best_node, v])
            
            remaining_nodes.remove(best_node)
        
        # Add remaining nodes with nearest neighbors if needed
        for node in remaining_nodes:
            neighbors = sorted(G.nodes(), 
                             key=lambda x: distance_matrix[node, x])[:3]
            for neighbor in neighbors:
                if G.number_of_edges() < 3 * (n - 2):
                    G.add_edge(node, neighbor, weight=distance_matrix[node, neighbor])
        
        return G


class RollingCorrelationEstimator:
    """
    Estimate correlation matrices using rolling windows.
    """
    
    def __init__(self, window_size=252):
        """
        Parameters:
        -----------
        window_size : int
            Number of observations in rolling window (e.g., 252 for 1 year of daily data)
        """
        self.window_size = window_size
    
    def estimate_correlations(self, returns_df):
        """
        Compute rolling correlation matrices.
        
        Parameters:
        -----------
        returns_df : pd.DataFrame
            Returns with DatetimeIndex
            
        Returns:
        --------
        correlation_estimates : list of dict
            Each dict contains:
            - 'date': end date of window
            - 'correlation': correlation matrix
            - 'n_obs': number of observations
        """
        correlation_estimates = []
        n_obs = len(returns_df)
        
        for end_idx in range(self.window_size, n_obs):
            start_idx = end_idx - self.window_size
            window_returns = returns_df.iloc[start_idx:end_idx]
            
            corr_matrix = window_returns.corr().values
            
            correlation_estimates.append({
                'date': returns_df.index[end_idx],
                'correlation': corr_matrix,
                'n_obs': self.window_size
            })
        
        return correlation_estimates


class NetworkAnimator:
    """
    Create animations of filtered correlation networks over time with dynamic layouts.
    """
    
    def __init__(self, figsize=(12, 10), dynamic_layout=True, shade_triangles=False):
        """
        Parameters:
        -----------
        figsize : tuple
            Figure size (width, height)
        dynamic_layout : bool
            If True, nodes move according to force-directed layout based on current edges
            If False, use static layout (old behavior)
        shade_triangles : bool
            If True, shade triangular faces (3-cliques) based on correlation strength
        """
        self.figsize = figsize
        self.dynamic_layout = dynamic_layout
        self.shade_triangles = shade_triangles
        self.node_colors = None
        self.node_labels = None
        
    def create_stable_layout(self, graphs, method='spring'):
        """
        Create a stable layout that works across all time steps.
        (Used only when dynamic_layout=False)
        
        Parameters:
        -----------
        graphs : list of networkx.Graph
            Sequence of graphs over time
        method : str
            Layout method: 'spring', 'circular', 'kamada_kawai'
            
        Returns:
        --------
        pos : dict
            Node positions {node: (x, y)}
        """
        # Use first graph to establish layout
        G_first = graphs[0]
        
        if method == 'spring':
            # Use first graph with many iterations for stability
            pos = nx.spring_layout(G_first, k=2/np.sqrt(len(G_first.nodes())), 
                                  iterations=100, seed=42)
        elif method == 'circular':
            pos = nx.circular_layout(G_first)
        elif method == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G_first)
        else:
            pos = nx.spring_layout(G_first, seed=42)
        
        return pos
    
    def compute_dynamic_layouts(self, graphs, smoothing_factor=0.3, 
                               k_factor=2.0, iterations_per_frame=10):
        """
        Compute dynamic force-directed layouts that evolve smoothly over time.
        
        Parameters:
        -----------
        graphs : list of networkx.Graph
            Sequence of graphs over time
        smoothing_factor : float (0 to 1)
            Higher values = smoother transitions, less responsive to changes
            0 = fully responsive to current graph structure
            1 = no movement (fully stable)
        k_factor : float
            Optimal distance between nodes (larger = more spread out)
        iterations_per_frame : int
            Number of spring layout iterations per frame
            
        Returns:
        --------
        layouts : list of dict
            Node positions for each time step
        """
        print(f"Computing dynamic layouts with smoothing={smoothing_factor}...")
        
        n_nodes = len(graphs[0].nodes())
        layouts = []
        
        # Initialize with spring layout of first graph
        current_pos = nx.spring_layout(
            graphs[0], 
            k=k_factor/np.sqrt(n_nodes),
            iterations=50,
            seed=42
        )
        layouts.append(current_pos.copy())
        
        # Evolve positions frame by frame
        for frame_idx, G in enumerate(graphs[1:], start=1):
            if frame_idx % 20 == 0:
                print(f"  Computing layout {frame_idx}/{len(graphs)}")
            
            # Compute new layout based on current graph structure
            # Using current_pos as starting point for smoother transitions
            new_pos = nx.spring_layout(
                G,
                pos=current_pos,  # Start from previous positions
                k=k_factor/np.sqrt(n_nodes),
                iterations=iterations_per_frame,
                seed=None  # Don't reset
            )
            
            # Smooth transition: blend old and new positions
            smoothed_pos = {}
            for node in new_pos:
                old_x, old_y = current_pos[node]
                new_x, new_y = new_pos[node]
                
                # Weighted average (smoothing)
                smoothed_x = smoothing_factor * old_x + (1 - smoothing_factor) * new_x
                smoothed_y = smoothing_factor * old_y + (1 - smoothing_factor) * new_y
                
                smoothed_pos[node] = np.array([smoothed_x, smoothed_y])
            
            current_pos = smoothed_pos
            layouts.append(current_pos.copy())
        
        print("  Dynamic layouts computed!")
        return layouts
    
    def setup_node_colors(self, n_nodes, n_clusters=None):
        """
        Set up node colors for visualization.
        
        Parameters:
        -----------
        n_nodes : int
            Number of nodes
        n_clusters : int, optional
            Number of clusters/sectors for coloring
        """
        if n_clusters is None:
            n_clusters = max(3, n_nodes // 5)
        
        # Assign random clusters
        cluster_assignments = np.random.choice(n_clusters, n_nodes)
        
        # Create color map
        cmap = plt.cm.Set3
        self.node_colors = [cmap(cluster / n_clusters) for cluster in cluster_assignments]
        self.node_labels = {i: f'{i}' for i in range(n_nodes)}
    
    def draw_shaded_triangles(self, G, pos, ax, correlation_matrix=None, alpha=0.3, cmap='RdYlBu_r'):
        """
        Draw shaded triangular faces (3-cliques) on the network.
        
        Parameters:
        -----------
        G : networkx.Graph
            Network with edges
        pos : dict
            Node positions {node: (x, y)}
        ax : matplotlib axis
            Axis to draw on
        correlation_matrix : np.ndarray, optional
            Correlation matrix to compute face colors. If None, use edge weights.
        alpha : float
            Transparency of triangular faces (0 to 1)
        cmap : str
            Colormap name for coloring triangles by correlation strength
        """
        # Find all triangles (3-cliques)
        triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]
        
        if len(triangles) == 0:
            return  # No triangles to draw
        
        # Shade each triangle
        for triangle in triangles:
            # Get positions of triangle vertices
            vertices = np.array([pos[node] for node in triangle])
            
            # Calculate average correlation for this triangle
            if correlation_matrix is not None:
                # Use provided correlation matrix
                corr_vals = [correlation_matrix[triangle[i], triangle[j]]
                            for i in range(3) for j in range(i+1, 3)]
                avg_correlation = np.mean(corr_vals)
            else:
                # Calculate from edge weights in graph
                edges = [(triangle[i], triangle[j]) for i in range(3) for j in range(i+1, 3)]
                weights = [G[u][v]['weight'] for u, v in edges if G.has_edge(u, v)]
                
                if weights:
                    avg_weight = np.mean(weights)
                    # Convert distance back to correlation: rho = 1 - d²/2
                    avg_correlation = 1 - (avg_weight ** 2) / 2
                else:
                    avg_correlation = 0.0
            
            # Map correlation to color
            # Normalize correlation from [-1, 1] to [0, 1] for colormap
            color_val = (avg_correlation + 1) / 2
            color = plt.cm.get_cmap(cmap)(color_val)
            
            # Create polygon patch for the triangle
            polygon = mpatches.Polygon(
                vertices, 
                closed=True,
                facecolor=color,
                edgecolor='none',
                alpha=alpha,
                zorder=1  # Draw triangles behind edges and nodes
            )
            ax.add_patch(polygon)
    
    def animate_filtered_networks(self, correlation_estimates, filter_method='pmfg',
                                  output_file='network_animation.mp4', 
                                  fps=10, interval=100,
                                  smoothing_factor=0.3, k_factor=2.0,
                                  triangle_alpha=0.3, triangle_cmap='RdYlBu_r'):
        """
        Create animation of filtered networks over time.
        
        Parameters:
        -----------
        correlation_estimates : list of dict
            Output from RollingCorrelationEstimator
        filter_method : str
            'mst', 'pmfg', or 'tmfg'
        output_file : str
            Output filename for animation
        fps : int
            Frames per second
        interval : int
            Milliseconds between frames
        smoothing_factor : float (0 to 1)
            Only used if dynamic_layout=True. Controls transition smoothness.
            Higher = smoother but less responsive. Default 0.3.
        k_factor : float
            Only used if dynamic_layout=True. Controls node spacing.
            Higher = more spread out. Default 2.0.
        triangle_alpha : float
            Transparency of triangular faces (0 to 1). Only used if shade_triangles=True.
        triangle_cmap : str
            Colormap for triangle shading. Only used if shade_triangles=True.
            
        Returns:
        --------
        anim : matplotlib.animation.FuncAnimation
        """
        # Create filtered graphs for all time steps
        print(f"Creating filtered graphs using {filter_method.upper()}...")
        graphs = []
        dates = []
        correlation_matrices = []  # Store for triangle shading
        
        for i, est in enumerate(correlation_estimates):
            if i % 20 == 0:
                print(f"  Processing {i+1}/{len(correlation_estimates)}")
            
            corr = est['correlation']
            correlation_matrices.append(corr)  # Store correlation matrix
            dist = CorrelationFilter.correlation_to_distance(corr)
            
            if filter_method == 'mst':
                G = CorrelationFilter.minimum_spanning_tree(dist)
            elif filter_method == 'pmfg':
                G = CorrelationFilter.planar_maximally_filtered_graph(dist)
            elif filter_method == 'tmfg':
                G = CorrelationFilter.triangulated_maximally_filtered_graph(dist)
            else:
                raise ValueError(f"Unknown filter method: {filter_method}")
            
            graphs.append(G)
            dates.append(est['date'])
        
        # Compute layouts (static or dynamic)
        if self.dynamic_layout:
            print("Computing dynamic force-directed layouts...")
            layouts = self.compute_dynamic_layouts(
                graphs, 
                smoothing_factor=smoothing_factor,
                k_factor=k_factor
            )
        else:
            print("Computing static layout...")
            static_pos = self.create_stable_layout(graphs, method='spring')
            layouts = [static_pos] * len(graphs)  # Same layout for all frames
        
        # Setup node colors
        n_nodes = len(graphs[0].nodes())
        self.setup_node_colors(n_nodes)
        
        # Create figure
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
            date = dates[frame]
            pos = layouts[frame]  # Use dynamic or static layout for this frame
            corr_matrix = correlation_matrices[frame]  # Get correlation matrix
            
            # Draw shaded triangles if enabled (drawn first, behind everything)
            if self.shade_triangles:
                self.draw_shaded_triangles(G, pos, ax, corr_matrix, 
                                          alpha=triangle_alpha, 
                                          cmap=triangle_cmap)
            
            # Draw edges with varying thickness based on weight
            edges = G.edges(data=True)
            if len(edges) > 0:
                weights = [1.0 / (1.0 + e[2].get('weight', 1.0)) for e in edges]
                max_weight = max(weights) if weights else 1.0
                edge_widths = [3 * w / max_weight for w in weights]
                
                nx.draw_networkx_edges(G, pos, width=edge_widths, 
                                      alpha=0.4, edge_color='gray', ax=ax)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_color=self.node_colors,
                                  node_size=300, alpha=0.9, ax=ax)
            
            # Draw labels
            nx.draw_networkx_labels(G, pos, self.node_labels, 
                                   font_size=8, font_weight='bold', ax=ax)
            
            # Add title with date and metrics
            n_edges = G.number_of_edges()
            avg_degree = 2 * n_edges / n_nodes
            
            # Count triangles if shading is enabled
            if self.shade_triangles:
                n_triangles = sum(1 for c in nx.enumerate_all_cliques(G) if len(c) == 3)
                title = f'{filter_method.upper()} Network (Triangles: {n_triangles})\n'
            else:
                title = f'{filter_method.upper()} Network\n'
            
            title += f'Date: {date.strftime("%Y-%m-%d")}\n'
            title += f'Edges: {n_edges}, Avg Degree: {avg_degree:.1f}'
            
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            
            # Add frame counter
            ax.text(0.02, 0.98, f'Frame {frame+1}/{len(graphs)}',
                   transform=ax.transAxes, fontsize=10,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            return []
        
        # Create animation
        print("Creating animation...")
        anim = animation.FuncAnimation(fig, update, init_func=init,
                                      frames=len(graphs), interval=interval,
                                      blit=True, repeat=True)
        
        # Save animation
        print(f"Saving animation to {output_file}...")
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, bitrate=1800)
        anim.save(output_file, writer=writer)
        print(f"Animation saved successfully!")
        
        plt.close()
        return anim
    
    def create_comparison_animation(self, correlation_estimates,
                                   output_file='network_comparison.mp4',
                                   fps=10, smoothing_factor=0.3):
        """
        Create side-by-side comparison of MST, PMFG, and TMFG.
        
        Parameters:
        -----------
        correlation_estimates : list of dict
            Output from RollingCorrelationEstimator
        output_file : str
            Output filename
        fps : int
            Frames per second
        smoothing_factor : float (0 to 1)
            Only used if dynamic_layout=True. Controls transition smoothness.
        """
        print("Creating filtered graphs for all methods...")
        
        all_graphs = {'MST': [], 'PMFG': [], 'TMFG': []}
        dates = []
        
        for i, est in enumerate(correlation_estimates):
            if i % 20 == 0:
                print(f"  Processing {i+1}/{len(correlation_estimates)}")
            
            corr = est['correlation']
            dist = CorrelationFilter.correlation_to_distance(corr)
            
            all_graphs['MST'].append(CorrelationFilter.minimum_spanning_tree(dist))
            all_graphs['PMFG'].append(
                CorrelationFilter.planar_maximally_filtered_graph(dist)
            )
            all_graphs['TMFG'].append(
                CorrelationFilter.triangulated_maximally_filtered_graph(dist)
            )
            dates.append(est['date'])
        
        # Create layouts for each method (dynamic or static)
        print("Computing layouts for each method...")
        all_layouts = {}
        for method in ['MST', 'PMFG', 'TMFG']:
            if self.dynamic_layout:
                print(f"  Computing dynamic layouts for {method}...")
                all_layouts[method] = self.compute_dynamic_layouts(
                    all_graphs[method], 
                    smoothing_factor=smoothing_factor
                )
            else:
                print(f"  Computing static layout for {method}...")
                static_pos = self.create_stable_layout(all_graphs[method], method='spring')
                all_layouts[method] = [static_pos] * len(dates)
        
        # Setup node colors
        n_nodes = len(all_graphs['MST'][0].nodes())
        self.setup_node_colors(n_nodes)
        
        # Create figure with subplots
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        def init():
            for ax in axes:
                ax.clear()
                ax.set_xlim(-1.5, 1.5)
                ax.set_ylim(-1.5, 1.5)
                ax.axis('off')
            return []
        
        def update(frame):
            date = dates[frame]
            
            for idx, (method, ax) in enumerate(zip(['MST', 'PMFG', 'TMFG'], axes)):
                ax.clear()
                ax.set_xlim(-1.5, 1.5)
                ax.set_ylim(-1.5, 1.5)
                ax.axis('off')
                
                G = all_graphs[method][frame]
                pos = all_layouts[method][frame]  # Use dynamic layout for this frame
                
                # Draw edges
                edges = G.edges(data=True)
                if len(edges) > 0:
                    weights = [1.0 / (1.0 + e[2].get('weight', 1.0)) for e in edges]
                    max_weight = max(weights) if weights else 1.0
                    edge_widths = [3 * w / max_weight for w in weights]
                    
                    nx.draw_networkx_edges(G, pos, width=edge_widths,
                                          alpha=0.4, edge_color='gray', ax=ax)
                
                # Draw nodes
                nx.draw_networkx_nodes(G, pos, node_color=self.node_colors,
                                      node_size=200, alpha=0.9, ax=ax)
                
                # Add title
                n_edges = G.number_of_edges()
                title = f'{method}\n{n_edges} edges'
                ax.set_title(title, fontsize=12, fontweight='bold')
            
            # Add overall title
            layout_type = "Dynamic" if self.dynamic_layout else "Static"
            fig.suptitle(f'Network Comparison ({layout_type} Layout) - {date.strftime("%Y-%m-%d")}',
                        fontsize=14, fontweight='bold')
            
            return []
        
        # Create animation
        print("Creating comparison animation...")
        anim = animation.FuncAnimation(fig, update, init_func=init,
                                      frames=len(dates), interval=100,
                                      blit=True, repeat=True)
        
        # Save
        print(f"Saving animation to {output_file}...")
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, bitrate=1800)
        anim.save(output_file, writer=writer)
        print(f"Animation saved successfully!")
        
        plt.close()
        return anim
    
    def visualize_network_with_triangles(self, correlation_matrix, filter_method='pmfg',
                                        output_file='network_triangles.png',
                                        title=None, figsize=None,
                                        triangle_alpha=0.35, triangle_cmap='RdYlBu_r'):
        """
        Create a static visualization of a network with shaded triangular faces.
        
        Parameters:
        -----------
        correlation_matrix : np.ndarray
            Correlation matrix
        filter_method : str
            'mst', 'pmfg', or 'tmfg'
        output_file : str
            Output filename for the image
        title : str, optional
            Custom title for the plot
        figsize : tuple, optional
            Figure size (width, height). Uses self.figsize if None.
        triangle_alpha : float
            Transparency of triangular faces (0 to 1)
        triangle_cmap : str
            Colormap for triangle shading
            
        Returns:
        --------
        fig, ax : matplotlib figure and axis
        """
        # Create filtered graph
        print(f"Creating {filter_method.upper()} network...")
        dist = CorrelationFilter.correlation_to_distance(correlation_matrix)
        
        if filter_method == 'mst':
            G = CorrelationFilter.minimum_spanning_tree(dist)
        elif filter_method == 'pmfg':
            G = CorrelationFilter.planar_maximally_filtered_graph(dist)
        elif filter_method == 'tmfg':
            G = CorrelationFilter.triangulated_maximally_filtered_graph(dist)
        else:
            raise ValueError(f"Unknown filter method: {filter_method}")
        
        # Create layout
        print("Computing layout...")
        n_nodes = len(G.nodes())
        pos = nx.spring_layout(G, k=2/np.sqrt(n_nodes), iterations=200, seed=42)
        
        # Setup colors
        self.setup_node_colors(n_nodes)
        
        # Create figure
        fig_size = figsize if figsize else self.figsize
        fig, ax = plt.subplots(figsize=fig_size)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
        
        # Draw shaded triangles
        print("Drawing triangular faces...")
        self.draw_shaded_triangles(G, pos, ax, correlation_matrix, 
                                   alpha=triangle_alpha, cmap=triangle_cmap)
        
        # Draw edges
        edges = G.edges(data=True)
        if len(edges) > 0:
            weights = [1.0 / (1.0 + e[2].get('weight', 1.0)) for e in edges]
            max_weight = max(weights) if weights else 1.0
            edge_widths = [3 * w / max_weight for w in weights]
            
            nx.draw_networkx_edges(G, pos, width=edge_widths, 
                                  alpha=0.5, edge_color='gray', ax=ax, zorder=2)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=self.node_colors,
                              node_size=400, alpha=0.9, 
                              edgecolors='black', linewidths=2,
                              ax=ax, zorder=3)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, self.node_labels, 
                               font_size=9, font_weight='bold', ax=ax, zorder=4)
        
        # Count triangles
        triangles = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]
        n_triangles = len(triangles)
        n_edges = G.number_of_edges()
        avg_degree = 2 * n_edges / n_nodes
        
        # Add title
        if title is None:
            title = f'{filter_method.upper()} Network with Shaded Triangular Faces\n'
            title += f'Nodes: {n_nodes} | Edges: {n_edges} | Triangles: {n_triangles} | '
            title += f'Avg Degree: {avg_degree:.1f}'
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Add colorbar
        sm = plt.cm.ScalarMappable(cmap=triangle_cmap, 
                                   norm=plt.Normalize(vmin=-1, vmax=1))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Triangle Avg Correlation', rotation=270, labelpad=20, fontsize=11)
        
        # Save
        print(f"Saving visualization to {output_file}...")
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Visualization saved!")
        
        return fig, ax


def main():
    """
    Main execution function demonstrating the complete pipeline.
    """
    print("="*70)
    print("Animated Correlation Network Filtering")
    print("="*70)
    
    # Parameters
    n_assets = 20  # Number of assets
    total_days = 500  # Total days of data
    window_size = 100  # Rolling window size
    
    print(f"\nParameters:")
    print(f"  Number of assets: {n_assets}")
    print(f"  Total days: {total_days}")
    print(f"  Window size: {window_size}")
    
    # Step 1: Generate synthetic data
    print("\n" + "="*70)
    print("Step 1: Generating synthetic time series with evolving correlations")
    print("="*70)
    
    generator = SyntheticCorrelationGenerator(n_assets=n_assets, seed=42)
    returns_df, true_correlations = generator.generate_time_series(
        total_days=total_days,
        window_size=window_size,
        volatility_process=0.05
    )
    
    print(f"\nGenerated returns shape: {returns_df.shape}")
    print(f"Date range: {returns_df.index[0]} to {returns_df.index[-1]}")
    
    # Step 2: Estimate rolling correlations
    print("\n" + "="*70)
    print("Step 2: Estimating rolling correlation matrices")
    print("="*70)
    
    estimator = RollingCorrelationEstimator(window_size=window_size)
    correlation_estimates = estimator.estimate_correlations(returns_df)
    
    print(f"\nEstimated {len(correlation_estimates)} correlation matrices")
    
    # Step 3: Create animations
    print("\n" + "="*70)
    print("Step 3: Creating network animations")
    print("="*70)
    
    # Create animations with DYNAMIC layouts (nodes move with force-directed layout)
    print("\n*** Creating DYNAMIC layout animations ***")
    print("(Nodes will move according to evolving correlation structure)\n")
    
    animator_dynamic = NetworkAnimator(figsize=(12, 10), dynamic_layout=True)
    
    # Create individual animations for each method
    for method in ['mst', 'pmfg', 'tmfg']:
        print(f"\n--- Creating {method.upper()} animation (DYNAMIC) ---")
        animator_dynamic.animate_filtered_networks(
            correlation_estimates,
            filter_method=method,
            output_file=f'{method}_network_animation_dynamic.mp4',
            fps=10,
            interval=100,
            smoothing_factor=0.3,  # Controls smoothness (0=very responsive, 1=static)
            k_factor=2.0  # Controls node spacing
        )
    
    # Create comparison animation with dynamic layout
    print("\n--- Creating comparison animation (DYNAMIC) ---")
    animator_dynamic.create_comparison_animation(
        correlation_estimates,
        output_file='network_comparison_dynamic.mp4',
        fps=10,
        smoothing_factor=0.3
    )
    
    # Optional: Also create STATIC layout versions for comparison
    print("\n\n*** Creating STATIC layout animations for comparison ***")
    print("(Nodes stay in fixed positions)\n")
    
    animator_static = NetworkAnimator(figsize=(12, 10), dynamic_layout=False)
    
    # Just create comparison for static version
    print("\n--- Creating comparison animation (STATIC) ---")
    animator_static.create_comparison_animation(
        correlation_estimates,
        output_file='network_comparison_static.mp4',
        fps=10
    )
    
    # Step 4: Create visualizations with shaded triangles
    print("\n" + "="*70)
    print("Step 4: Creating static visualizations with shaded triangular faces")
    print("="*70)
    
    # Create visualizations with triangle shading for each method
    print("\n*** Creating static images with triangle shading ***\n")
    
    animator_triangles = NetworkAnimator(figsize=(14, 12), shade_triangles=True)
    
    # Use the last correlation matrix for static visualization
    last_corr = correlation_estimates[-1]['correlation']
    
    for method in ['pmfg', 'tmfg']:  # MST has no triangles, only trees
        print(f"\n--- Creating {method.upper()} visualization with triangles ---")
        animator_triangles.visualize_network_with_triangles(
            last_corr,
            filter_method=method,
            output_file=f'{method}_triangles.png',
            triangle_alpha=0.35,
            triangle_cmap='RdYlBu_r'  # Red=high correlation, Blue=low
        )
    
    # Step 5: Create animations WITH triangle shading
    print("\n" + "="*70)
    print("Step 5: Creating animated networks with shaded triangular faces")
    print("="*70)
    
    print("\n*** Creating animations with triangle shading (PMFG only) ***")
    print("(This may take longer due to triangle rendering)\n")
    
    animator_shaded = NetworkAnimator(figsize=(14, 12), dynamic_layout=True, 
                                     shade_triangles=True)
    
    print("\n--- Creating PMFG animation with shaded triangles ---")
    animator_shaded.animate_filtered_networks(
        correlation_estimates,
        filter_method='pmfg',
        output_file='pmfg_network_triangles_animation.mp4',
        fps=10,
        interval=100,
        smoothing_factor=0.3,
        triangle_alpha=0.35,
        triangle_cmap='RdYlBu_r'
    )
    
    print("\n" + "="*70)
    print("All animations completed successfully!")
    print("="*70)
    print("\nOutput files:")
    print("  Dynamic layouts:")
    print("    - mst_network_animation_dynamic.mp4")
    print("    - pmfg_network_animation_dynamic.mp4")
    print("    - tmfg_network_animation_dynamic.mp4")
    print("    - network_comparison_dynamic.mp4")
    print("  Static layout:")
    print("    - network_comparison_static.mp4")
    print("  Static images with triangle shading:")
    print("    - pmfg_triangles.png")
    print("    - tmfg_triangles.png")
    print("  Animated with triangle shading:")
    print("    - pmfg_network_triangles_animation.mp4")
    print("\nNote: Dynamic layouts show how node positions evolve with correlations!")
    print("Triangle colors: Red=high correlation, Blue=low correlation")
    print("="*70)
    
    return returns_df, correlation_estimates


if __name__ == "__main__":
    returns_df, correlation_estimates = main()
