# Traveling Salesperson Problem Solver with Genetic Algorithm

This project demonstrates solving the **Traveling Salesperson Problem (TSP)** using **genetic algorithms** and visualizing the optimal route on a map. Real-world distances are retrieved using the **2GIS API**, and the route is displayed using Folium.

---

## Features

1. **Genetic Algorithm**:
   - Population-based optimization approach.
   - Includes random initialization, crossover, mutation, and selection.
   - Iterative improvements over generations to find the optimal route.

2. **Distance Data from 2GIS**:
   - Fetches real-world road distances between cities via the 2GIS API.
   - Ensures accurate representation of travel paths.

3. **Visualization**:
   - Displays the optimal path on an interactive map.
   - Saves the route as an HTML file (`tsp_route.html`).

4. **Customizable**:
   - Supports dynamic input of locations (latitude and longitude).
   - Adjustable genetic algorithm parameters.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/tsp-genetic-algorithm.git
   cd tsp-genetic-algorithm
   ```

2. Install the required libraries:
   ```bash
   pip install requests folium
   ```

3. Set up your 2GIS API key:
   - Replace the placeholder in the `API_KEY` variable with your 2GIS API key.
   - You can obtain the API key [here](https://dev.2gis.com/).

---

## Usage

1. Define the points:
   - Update the `points` variable in the script with the desired locations (latitude and longitude).

2. Run the script:
   ```bash
   python ga.py
   ```

3. View the results:
   - The best route and its cost will be displayed in the console.
   - The route will be saved in `tsp_route.html`.

---

## Example

For the points:
- Kazan Kremlin
- Tukay Square
- Ak Bars Arena
- National Library of the Republic of Tatarstan
- Kazan Family Center
- Kamal Theater Square

The program will:
1. Fetch distances between these points from the 2GIS API.
2. Use a genetic algorithm to compute the shortest route.
3. Display the route on an interactive map.

---

## Parameters

- `population_size`: Number of routes in each generation.
- `mutation_rate`: Probability of mutation for each route.
- `max_generations`: Number of generations to evolve.
- `API_KEY`: Your 2GIS API key.

---

## Output

1. Console:
   - The best route as a sequence of indices.
   - Total cost of the route.

2. Map:
   - Interactive visualization of the optimal route in `tsp_route.html`.


