# QuLab: Central Clearing Impact Simulator

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Title and Description

**QuLab: Central Clearing Impact Simulator** is a Streamlit-powered educational application designed as a laboratory project to explore the profound impact of central clearing on derivatives markets. This application specifically focuses on how daily margin requirements and settlement processes for centrally cleared Over-The-Counter (OTC) contracts significantly reduce the cash flow and price differences observed between Exchange-Traded Derivatives (ETDs) like futures and traditional OTC forwards.

Through an interactive interface, users can simulate various market conditions and clearing scenarios, visualizing the effects of clearing on cash flows, margin balances, and credit risk. This tool serves as a practical demonstration of key concepts in derivatives pricing, risk management, and market infrastructure.

## Features

This application provides a comprehensive suite of functionalities to analyze derivatives clearing:

*   **Synthetic Market Data Generation**: Dynamically generate realistic, albeit synthetic, time-series data for asset prices, allowing for controlled simulation environments.
*   **Robust Data Validation**: Implement strict data validation and pre-processing steps to ensure the integrity and quality of all input data, preventing erroneous calculations.
*   **Summary Statistics**: Display key descriptive statistics for generated data, offering quick insights into data distribution and potential outliers.
*   **Theoretical Futures Price Calculation**: Compute the fair theoretical price of a futures contract at inception using the cost of carry model, providing a benchmark for analysis.
*   **Multi-Scenario Cash Flow & Margin Simulation**:
    *   **Exchange-Traded Futures**: Simulate daily mark-to-market (MTM), margin adjustments, and cash flows for typical futures contracts.
    *   **Non-Centrally Cleared OTC (Forwards)**: Model the MTM value and single cash flow at maturity for traditional forward contracts, highlighting the lack of interim settlements.
    *   **Centrally Cleared OTC**: Demonstrate how central clearing introduces futures-like margining and daily settlement to OTC derivatives, reducing counterparty risk.
*   **Qualitative Credit Risk Assessment**: Provide a high-level qualitative assessment of credit risk associated with each clearing scenario, emphasizing the risk mitigation benefits of central clearing.
*   **Price Difference Heatmap (Conceptual)**: Generate and visualize a heatmap demonstrating how factors like correlation and volatility *could* impact residual price differences between futures and forwards, even with clearing (currently uses dummy data for illustration).
*   **Interactive User Interface**: A user-friendly sidebar allows for easy adjustment of simulation parameters, providing immediate visual feedback on the impact of changes.

## Getting Started

Follow these instructions to get the application up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/qucrete-qu-lab-central-clearing.git
    cd qucrete-qu-lab-central-clearing
    ```
    *(Note: Replace `https://github.com/your-username/qucrete-qu-lab-central-clearing.git` with the actual repository URL if available)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file in your project root with the following content:
    ```
    streamlit
    pandas
    numpy
    altair
    ```
    Then, install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Streamlit application:**
    From the root directory of your project (where `app.py` is located), execute:
    ```bash
    streamlit run app.py
    ```

2.  **Access the Application:**
    Your web browser should automatically open to the Streamlit application (usually `http://localhost:8501`). If not, copy and paste the URL from your terminal into your browser.

3.  **Interact with the Simulator:**
    *   Use the **sidebar** on the left to adjust **Simulation Parameters** such as Initial Spot Price, Volatility, Days to Maturity, Margins, and Contract Size.
    *   Select the **Derivative Scenario** (Exchange-Traded Futures, Centrally Cleared OTC, or Non-Centrally Cleared OTC) to see the different cash flow and margin dynamics.
    *   Adjust **Price Difference Heatmap Parameters** to explore the conceptual impact of correlation and volatility.
    *   Observe the generated spot prices, cash flow charts, margin balance graphs, data tables, and credit risk assessments in the main panel.

## Project Structure

The project is organized into a modular structure for clarity and maintainability:

```
.
├── app.py                            # Main Streamlit entry point and navigation
├── application_pages/                # Directory for individual application modules/pages
│   └── central_clearing_simulator.py # Core logic and UI for the Central Clearing Impact Simulator
└── requirements.txt                  # List of Python dependencies
```

## Technology Stack

*   **Python**: The core programming language.
*   **Streamlit**: For building the interactive web application interface.
*   **Pandas**: For data manipulation and analysis, especially with DataFrames.
*   **NumPy**: For numerical operations, particularly in synthetic data generation.
*   **Altair**: For creating interactive and publication-quality statistical visualizations (e.g., heatmaps).

## Contributing

This project is primarily intended as a lab demonstration. However, if you are interested in contributing to similar educational projects:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and ensure they adhere to existing code style.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your contributions align with the educational goals and quality standards.

## License

© 2025 QuantUniversity. All Rights Reserved.

**Important Notice:**
This application was created for **educational purposes only** and is **not intended for commercial use**.
*   You **may not copy, share, or redistribute** this application or its code **without explicit prior written consent** from QuantUniversity.
*   You **may not delete or modify this license information** without authorization.
*   This application was generated using **QuCreate**, an AI-powered assistant.
*   Content generated by AI models may contain **hallucinated or incorrect information**. Please **verify all information and calculations before relying on them**.

For permissions or commercial licensing inquiries, please contact QuantUniversity.

## Contact

For any questions, feedback, or commercial licensing requests, please contact:

Email: [info@quantuniversity.com](mailto:info@quantuniversity.com)
Website: [QuantUniversity](https://www.quantuniversity.com)