# QuLab: Central Clearing Impact Simulator

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Title and Description

**QuLab: Central Clearing Impact Simulator** is a Streamlit-based educational application designed to provide a practical understanding of the impact of central clearing on the pricing and valuation of financial derivative contracts. This interactive tool allows users, including risk managers, compliance officers, and institutional finance students, to explore the fundamental differences between Exchange-Traded Derivatives (ETDs) like futures and Over-The-Counter (OTC) derivatives (forwards).

The application focuses on demonstrating how margin requirements and daily settlement processes, key components of central clearing, effectively reduce cash flow and price differences between these contract types. By simulating various scenarios, users can gain insights into counterparty risk mitigation and market dynamics in cleared vs. non-cleared environments.

## Features

This application offers the following key functionalities:

*   **Interactive Simulation Parameters**: Adjust initial spot prices, days to maturity, volatility, risk-free rates, contract size, initial margin, and maintenance margin through an intuitive sidebar.
*   **Dynamic Scenario Selection**: Compare cash flow dynamics and risk profiles for:
    *   **Non-Centrally Cleared OTC**: Simulates traditional forward contracts with lump-sum settlement.
    *   **Centrally Cleared OTC**: Demonstrates OTC contracts with daily margining, mimicking central clearing benefits.
    *   **Exchange-Traded Futures**: Illustrates the standard daily settlement and margining process of futures.
*   **Simulated Spot Price Trend**: Visualize the underlying asset's price movement over time.
*   **Theoretical Futures Price Calculation**: Calculate the theoretical futures price at inception based on user-defined parameters.
*   **Detailed Cash Flow & Margin Visualization**: Plot daily PnL, cash flows, and margin account balances to understand the mechanics of daily settlement and margin calls.
*   **Credit Risk Assessment**: Provides a qualitative assessment of credit risk exposure for each selected derivative type.
*   **(Dummy) Price Difference Heatmap**: Explore the conceptual impact of interest rate correlation and volatility on residual price differences between derivative types (uses dummy data for illustration purposes, indicating a potential area for future enhancement).
*   **Clear Navigation**: Easy switching between "Introduction," "Simulator," and "References" pages.

## Getting Started

Follow these instructions to set up and run the QuLab application on your local machine.

### Prerequisites

*   Python 3.7 or higher
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd qu_lab_app # Assuming 'qu_lab_app' is the root directory name
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**
    Create a `requirements.txt` file in the root directory of your project with the following content:

    ```
    streamlit
    pandas
    numpy
    plotly
    ```

    Then, install the dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Streamlit application:**
    Ensure your virtual environment is active and you are in the root directory of the project (where `app.py` is located).
    ```bash
    streamlit run app.py
    ```

2.  **Access the application:**
    After running the command, your web browser will automatically open the application (usually at `http://localhost:8501`).

3.  **Navigate and Interact:**
    *   Use the **sidebar** on the left to navigate between "Introduction", "Simulator", and "References" pages.
    *   On the **"Simulator"** page, adjust the simulation parameters (Initial Spot Price, Days to Maturity, Volatility, etc.) in the sidebar.
    *   Select the desired **derivative type** (Non-Centrally Cleared OTC, Centrally Cleared OTC, Exchange-Traded Futures) to see the respective simulation results, cash flows, and credit risk assessment.
    *   Explore the visualizations and summary statistics provided.

## Project Structure

The project is organized into a clear and modular structure:

```
qu_lab_app/
├── app.py                      # Main Streamlit application entry point
├── application_pages/          # Directory containing individual application pages
│   ├── __init__.py             # Makes application_pages a Python package
│   ├── introduction.py         # Content for the 'Introduction' page
│   ├── simulator.py            # Core simulation logic and visualizations for the 'Simulator' page
│   └── references.py           # References and licensing information for the 'References' page
└── requirements.txt            # Lists all Python dependencies
```

## Technology Stack

*   **Python**: The core programming language for the application logic.
*   **Streamlit**: The framework used for building the interactive web application.
*   **Pandas**: For data manipulation and analysis, especially for tabular data.
*   **NumPy**: For numerical operations, particularly in generating synthetic data.
*   **Plotly**: For creating interactive and publication-quality visualizations (line charts, heatmaps).

## Contributing

This project is primarily a lab exercise. While direct contributions via pull requests might not be the primary mode for this specific educational context, general principles would apply:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

For specific educational feedback or inquiries regarding the lab content, please refer to the contact information below.

## License

This application is provided under a specific educational license by QuantUniversity.

```
© QuantUniversity 2025
This notebook (and associated application code) was created for **educational purposes only** and is **not intended for commercial use**.
- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.
- You **may not delete or modify this license cell** without authorization.
- This notebook was generated using **QuCreate**, an AI-powered assistant.
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.

All rights reserved.
```

For permissions or commercial licensing inquiries, please contact QuantUniversity.

## Contact

For any questions, feedback, or commercial licensing inquiries, please contact:

*   **Email**: [info@quantuniversity.com](mailto:info@quantuniversity.com)
*   **Website**: [QuantUniversity](https://www.quantuniversity.com)