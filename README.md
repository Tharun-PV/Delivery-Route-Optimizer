# Delivery Route Optimizer

## Concept

The Delivery Route Optimizer is a web application built with Flask that allows users to optimize delivery routes for a fleet of electric vehicles. Users can input coordinates manually or upload a CSV file containing the coordinates of a central dispatch hub and multiple delivery locations. The application calculates the most efficient routes using the Clarke-Wright savings algorithm and displays the routes on a map. It also provides key metrics such as distance and estimated time for each route.

## Explanation

### Backend (Flask)

#### 1. Initialization and Setup:

- **Flask application is initialized.**
- `read_csv` function reads CSV data and returns it as a list of dictionaries.
- `calculate_distances` function calculates distances between all pairs of locations using the geodesic distance and creates a directed graph (DiGraph) using NetworkX.
- `clarke_wright_savings` function implements the Clarke-Wright savings algorithm to determine the optimized delivery routes.
- `calculate_metrics` function calculates the total distance and estimated time for each route.

#### 2. Routing:

- The `/` route handles both GET and POST requests.
- For POST requests, the application processes either the uploaded CSV file or the manually entered coordinates to compute and display optimized routes.

#### 3. CSV and Form Handling:

- Handles CSV file uploads and processes them to extract coordinates.
- Manages manual input of coordinates through form fields.
- Computes routes and metrics based on input data.

### Frontend (HTML/CSS/JavaScript)

#### 1. HTML Structure:

- Form for inputting hub and delivery location coordinates.
- Map container to display the routes using Leaflet.
- Metrics container to display route metrics.

#### 2. JavaScript Functionality:

- Dynamically adds new input fields for delivery locations.
- Handles form submission via AJAX to avoid page reloads.
- Displays routes and markers on the map using Leaflet.
- Animates the rider's movement along the routes.

#### 3. Map and Routing:

- Initializes a Leaflet map centered on a default location.
- Uses custom icons for the hub, delivery locations, and rider.
- Displays routes using the Leaflet Routing Machine.
- Animates the rider's movement along the routes when the play button is clicked.

## Summary

The Delivery Route Optimizer is a comprehensive solution for optimizing delivery routes based on user-provided coordinates. It leverages Flask for the backend, handling data processing and route optimization. The frontend utilizes Leaflet for map visualization and provides an interactive interface for users to input data and view optimized routes. Key metrics are calculated and displayed to help users understand the efficiency of the routes.

## Use Case

- **Logistics and Delivery Services:** Optimize delivery routes to minimize travel distance and time, leading to cost savings and improved efficiency.
- **Fleet Management:** Manage and optimize routes for a fleet of electric vehicles to ensure timely deliveries.
- **Urban Planning:** Plan efficient routes for various municipal services like waste collection or postal delivery.

## Packages and Tools Used

### Backend (Python):

- **Flask:** A lightweight web framework for building the application.
- **csv:** For reading and writing CSV files.
- **os:** For file path operations.
- **networkx:** For creating and manipulating complex networks and graphs.
- **geopy:** For calculating geodesic distances between coordinates.

### Frontend (HTML/CSS/JavaScript):

- **Leaflet:** An open-source JavaScript library for interactive maps.
- **Leaflet Routing Machine:** A plugin for Leaflet to handle route visualization and animations.
- **Bootstrap:** For responsive design and styling.
- **Custom CSS:** For additional styling and layout customization.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- NetworkX
- Geopy

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/delivery-route-optimizer.git
   ```
2. Navigate to the project directory:
   ```
   cd delivery-route-optimizer
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```
   flask run
   ```
5. Open your browser and navigate to http://localhost:5000 to use the application.
