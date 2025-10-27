"""Dynamics 365 API Client"""

import msal
import requests
import json
import os
from typing import Dict, Any, Optional
from config import DYNAMICS_CONFIG, AUTH_MODE
import time
import re

class Dynamics365Client:
    """Client for Dynamics 365 API operations"""
    
    def __init__(self):
        self.dynamics_url = DYNAMICS_CONFIG["url"]
        self.base_api_url = f"{self.dynamics_url}/api/data/{DYNAMICS_CONFIG['api_version']}"
        self.auth_mode = AUTH_MODE
        self.token_cache_file = "token_cache.json"
    
    def get_access_token(self) -> str:
        if self.auth_mode == "service_account":
            return self._get_service_account_token()
        else:
            return self._get_interactive_token()
    
    def _get_service_account_token(self) -> str:
        """Production: Client credentials flow"""
        app = msal.ConfidentialClientApplication(
            client_id=DYNAMICS_CONFIG["client_id"],
            client_credential=DYNAMICS_CONFIG["client_secret"],
            authority=DYNAMICS_CONFIG["authority"]
        )
        
        result = app.acquire_token_for_client(scopes=DYNAMICS_CONFIG["scopes"])
        
        if "access_token" in result:
            print("Service account token acquired")
            return result["access_token"]
        else:
            error_msg = result.get('error_description', 'Unknown error')
            raise Exception(f"Service auth failed: {error_msg}")
    
    def _get_interactive_token(self) -> str:
        """Development: Interactive flow with caching"""
        # Try cached token first
        cached_token = self._load_cached_token()
        if cached_token:
            print("Using cached interactive token")
            return cached_token
            
        app = msal.PublicClientApplication(
            client_id=DYNAMICS_CONFIG["client_id"],
            authority=DYNAMICS_CONFIG["authority"]
        )
        
        print("Getting interactive token...")
        result = app.acquire_token_interactive(scopes=DYNAMICS_CONFIG["scopes"])
        
        if "access_token" in result:
            self._save_token_cache(result)
            print("Interactive token acquired and cached")
            return result["access_token"]
        else:
            error_msg = result.get('error_description', 'Unknown error')
            raise Exception(f"Interactive auth failed: {error_msg}")
    
    def _load_cached_token(self) -> Optional[str]:
        if os.path.exists(self.token_cache_file):
            try:
                with open(self.token_cache_file, 'r') as f:
                    cache_data = json.load(f)
                if cache_data.get('expires_on', 0) > (time.time() + 300):
                    return cache_data['access_token']
            except:
                pass
        return None
    
    def _save_token_cache(self, token_result):
        expires_on = time.time() + token_result.get('expires_in', 3600) - 300
        cache_data = {
            'access_token': token_result['access_token'],
            'expires_on': expires_on
        }
        with open(self.token_cache_file, 'w') as f:
            json.dump(cache_data, f)
    
        
    def get_headers(self) -> Dict[str, str]:
        """Get standard headers for API requests"""
        access_token = self.get_access_token()
        return {
            'Authorization': f'Bearer {access_token}',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8'
        }
    
    def api_get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Make GET request to Dynamics API"""
        url = f"{self.base_api_url}/{endpoint}"
        headers = self.get_headers()
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API GET failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"API GET error: {e}")
            return None
    
    # def api_post(self, endpoint: str, data: Dict[str, Any]) -> Optional[str]:
    #     """Make POST request to Dynamics API"""
    #     url = f"{self.base_api_url}/{endpoint}"
    #     headers = self.get_headers()
        
    #     try:
    #         response = requests.post(url, headers=headers, json=data, timeout=30)
    #         if response.status_code == 204:
    #             entity_id = response.headers.get('OData-EntityId', '')
    #             if entity_id:
    #                 return entity_id.split('(')[-1].split(')')[0]
    #             return "success"
    #         else:
    #             print(f"API POST failed: {response.status_code} - {response.text}")
    #             return None
    #     except Exception as e:
    #         print(f"API POST error: {e}")
    #         return None

    def api_post(self, endpoint: str, data: Dict[str, Any], id_field: str) -> Optional[str]:
        """Make POST request to Dynamics API"""
        url = f"{self.base_api_url}/{endpoint}"
        headers = self.get_headers()
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=120)
            
            if response.status_code == 204:
                entity_id = response.headers.get('OData-EntityId', '')
                if entity_id:
                    # Extract GUID from format: /leads(guid)
                    guid_match = re.search(r'\(([^)]+)\)', entity_id)
                    if guid_match:
                        guid = guid_match.group(1)
                        # Now get the custom ID field for this entity
                        return self.get_custom_entity_id(endpoint, guid, id_field)
                
                return None
                
            else:
                print(f"API POST failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"API POST error: {e}")
            return None
        
    def get_custom_entity_id(self, endpoint: str, guid: str, id_field: str) -> Optional[str]:
        """Get the custom ID field for an entity using its GUID"""
        try:
            # Fetch the entity to get the custom ID
            url = f"{self.base_api_url}/{endpoint}({guid})?$select={id_field}"
            headers = self.get_headers()
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                custom_id = result.get(id_field)
                if custom_id:
                    print(f"Found custom ID: {custom_id}")
                    return custom_id
            
            print(f"Could not retrieve custom ID field '{id_field}' for {endpoint}")
            return None
        
        except Exception as e:
            print(f"Error getting custom entity ID: {e}")
            return None

    def api_patch(self, endpoint: str, data: Dict[str, Any]) -> bool:
        """Make PATCH request to Dynamics API"""
        url = f"{self.base_api_url}/{endpoint}"
        headers = self.get_headers()
        
        try:
            response = requests.patch(url, headers=headers, json=data, timeout=30)
            if response.status_code == 204:
                return True
            else:
                print(f"API PATCH failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"API PATCH error: {e}")
            return False

# Create global client instance
dynamics_client = Dynamics365Client()