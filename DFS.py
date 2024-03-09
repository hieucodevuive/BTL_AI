import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Canvas, Button, StringVar, Label, Entry, messagebox
from tkinter import ttk
import random


class State:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def add_neighbor(self, neighbor_state):
        self.neighbors.append(neighbor_state)


class GraphSearchDFS:
    def __init__(self):
        self.visited = set()
        self.path = []

    def depth_first_search(self, current_state, target_state):
        self.visited.add(current_state)

        if current_state == target_state:
            self.path.append(current_state)
            return True

        for neighbor_state in current_state.neighbors:
            if neighbor_state not in self.visited:
                if self.depth_first_search(neighbor_state, target_state):
                    self.path.insert(0, current_state)
                    return True

        return False

    def search(self, start_state, target_state):
        self.visited = set()
        self.path = []

        if self.depth_first_search(start_state, target_state):
            return self.path
        else:
            return None


class GraphSearchApp:
    def __init__(self, master, states):
        self.master = master
        self.master.title("Graph Search App")

        # Create states dynamically
        self.states = {state_name: State(state_name) for state_name in states}

        # Define state transitions (edges)
        for state_name, state in self.states.items():
            if state_name != "H":  # Adjust as needed based on your graph structure
                neighbor_name = chr(ord(state_name) + 1)
                state.add_neighbor(self.states[neighbor_name])

        # Initialize graph
        self.G = nx.Graph()
        self.G.add_edges_from(
            [
                (state_name, chr(ord(state_name) + 1))
                for state_name in states
                if state_name != "H"
            ]
        )

        # Initialize graph search
        self.graph_search = GraphSearchDFS()

        # Create GUI components
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(self.frame, text="Start State:").grid(row=0, column=0, padx=5, pady=5)
        self.start_var = StringVar()
        self.entry_start = Entry(
            self.frame, textvariable=self.start_var, font=("Helvetica", 12)
        )
        self.entry_start.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Target State:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.target_var = StringVar()
        self.entry_target = Entry(
            self.frame, textvariable=self.target_var, font=("Helvetica", 12)
        )
        self.entry_target.grid(row=1, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(
            self.frame, text="Search", command=self.perform_search
        )
        self.search_button.grid(row=2, columnspan=2, pady=10)

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=1, column=0)

        self.path = None

    def perform_search(self):
        start_state_name = self.start_var.get().upper()
        target_state_name = self.target_var.get().upper()

        # In giá trị để kiểm tra
        print("Start State:", start_state_name)
        print("Target State:", target_state_name)

        try:
            start_state = self.states[start_state_name]
            target_state = self.states[target_state_name]

            # Lấy đường dẫn từ GraphSearchDFS
            self.graph_search.search(start_state, target_state)

            if self.graph_search.path:
                messagebox.showinfo(
                    "Search Result",
                    f"Path found: {[state.name for state in self.graph_search.path]}",
                )
                self.plot_searched_graph()  # Không truyền đối số path
            else:
                messagebox.showinfo("Search Result", "No path found.")
        except KeyError:
            messagebox.showerror(
                "Error", "Invalid state names. Please use A, B, C, ..., H."
            )

    def plot_searched_graph(self):
        pos = nx.spring_layout(self.G)
        self.ax.clear()

        # Draw graph with random node colors
        nx.draw(
            self.G,
            pos,
            with_labels=True,
            font_weight="bold",
            node_size=700,
            font_size=8,
            font_color="black",
            edge_color="gray",
            linewidths=0.5,
            cmap=plt.cm.Blues,
            node_color=[
                random.choice(["blue", "green", "yellow", "orange", "red"])
                for _ in self.G.nodes
            ],
            ax=self.ax,
        )

        # Highlight path
        if self.graph_search.path:
            path_edges = [
                (self.graph_search.path[i - 1].name, self.graph_search.path[i].name)
                for i in range(1, len(self.graph_search.path))
            ]
            nx.draw_networkx_edges(
                self.G,
                pos,
                edgelist=path_edges,
                edge_color="red",
                width=2,
                ax=self.ax,
            )

            # Draw nodes in the path with a different color
            path_nodes = [state.name for state in self.graph_search.path]
            nx.draw_networkx_nodes(
                self.G,
                pos,
                nodelist=path_nodes,
                node_color="blue",
                node_size=700,
                ax=self.ax,
            )

        self.canvas.draw()


if __name__ == "__main__":
    root = Tk()
    app = GraphSearchApp(root, ["A", "B", "C", "D", "E", "F", "G", "H"])
    root.mainloop()
