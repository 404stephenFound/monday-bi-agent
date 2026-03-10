import requests

class MondayIntegrator:
    def __init__(self, api_token):
        self.url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": api_token, 
            "API-Version": "2023-10",
            "Content-Type": "application/json"
        }

    def get_board_items(self, board_id):
        """
        Queries Monday.com GraphQL API. 
        Ensures 'Read-only' access to board data.
        """
        if not board_id:
            return None

        # Enhanced query to get board name and item details
        query = """
        {
          boards(ids: [%s]) {
            name
            items_page (limit: 100) {
              items {
                name
                column_values {
                  column { title }
                  text
                }
              }
            }
          }
        }
        """ % board_id
        
        try:
            response = requests.post(
                self.url, 
                json={'query': query}, 
                headers=self.headers,
                timeout=10 # Added timeout for resilience
            )
            
            # Standard HTTP check
            response.raise_for_status()
            
            result = response.json()

            # 1. CRITICAL: Monday returns 200 OK even for API errors
            # We must check the 'errors' key specifically.
            if "errors" in result:
                error_msg = result["errors"][0].get("message", "Unknown Monday API Error")
                print(f"❌ Monday API Error: {error_msg}")
                return None

            # 2. Check if the board exists/is accessible
            if not result.get('data') or not result['data'].get('boards'):
                print(f"❌ Board {board_id} not found or access denied.")
                return None
            
            # 3. Return the specific board object
            return result['data']['boards'][0]

        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected Integration Error: {str(e)}")
            return None