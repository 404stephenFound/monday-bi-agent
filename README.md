# Skylark Drones - Monday.com BI Agent

## Overview
An AI agent that interprets business queries across Monday.com 'Deals' and 'Work Orders' boards. Built with Python, Streamlit, and Google Gemini.

## Setup
1. Create a `.env` file with your `MONDAY_API_TOKEN` and `GEMINI_API_KEY`.
2. Add your `DEALS_BOARD_ID` and `WORK_ORDERS_BOARD_ID`.
3. Run `pip install -r requirements.txt`.
4. Launch with `streamlit run app.py`.

## Key Features
- **Data Resilience**: Gracefully handles null values and inconsistent date formats.
- **Cross-Board Intelligence**: Connects sales pipeline to project execution.
- **Executive Reporting**: One-click leadership briefing generation.