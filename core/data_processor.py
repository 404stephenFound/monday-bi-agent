import pandas as pd

class DataProcessor:
    @staticmethod
    def simplify_data(raw_board_data):
        """
        Transforms messy Monday.com GraphQL response into clean, AI-ready dictionaries.
        Addresses the 'Data Resilience' requirement by flagging missing/incomplete data.
        """
        # 1. Check if the raw data exists
        if not raw_board_data or 'items_page' not in raw_board_data:
            return []
        
        items = raw_board_data['items_page'].get('items', [])
        if not items:
            return []

        simplified = []
        data_quality_issues = 0

        for item in items:
            # Start with the Item Name
            row = {"Item Name": item.get('name', "Unnamed Item")}
            
            # 2. Iterate through column values
            column_values = item.get('column_values', [])
            for cv in column_values:
                title = cv.get('column', {}).get('title', 'Unknown Column')
                text_value = cv.get('text', '')

                # 3. DATA RESILIENCE: Handle nulls, empty strings, or 'None' strings
                if text_value is None or text_value.strip() == "" or text_value.lower() == "none":
                    text_value = "MISSING_DATA"
                    data_quality_issues += 1
                
                row[title] = text_value
            
            simplified.append(row)
        
        # 4. Optional: If the data is massive, we convert to a simplified list 
        # but keep it in a format the LLM likes (JSON-like list of dicts)
        return simplified

    @staticmethod
    def get_data_quality_report(simplified_data):
        """
        Analyzes the simplified data to provide a 'caveat' for the AI agent.
        Part of the 'Communicate data quality issues' requirement.
        """
        if not simplified_data or isinstance(simplified_data, str):
            return "No data available to analyze."

        total_rows = len(simplified_data)
        rows_with_missing = sum(1 for row in simplified_data if "MISSING_DATA" in row.values())
        
        quality_score = int(((total_rows - rows_with_missing) / total_rows) * 100) if total_rows > 0 else 0
        
        return {
            "total_records": total_rows,
            "incomplete_records": rows_with_missing,
            "quality_score": f"{quality_score}%",
            "caveat": f"Note: {rows_with_missing} out of {total_rows} records have incomplete fields."
        }