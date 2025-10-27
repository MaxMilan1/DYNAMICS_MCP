"""Account-related tools for Dynamics 365"""

from typing import List, Dict, Any
from utils.dynamics_client import dynamics_client

def search_accounts(search_term: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for accounts in Dynamics 365 using partial name matching
    
    Args:
        search_term: Search term for account names (partial match)
        max_results: Maximum number of results to return
        
    Returns:
        List of matching accounts with details
    """
    print(f"Searching accounts for: '{search_term}'")
    
    endpoint = "accounts"
    params = {
        "$filter": f"contains(name, '{search_term}')",
        "$select": "accountid,name,emailaddress1,telephone1,address1_city,address1_country",
        "$orderby": "name",
        "$top": str(max_results)
    }
    
    result = dynamics_client.api_get(endpoint, params)
    accounts = result.get('value', []) if result else []
    
    # Format results
    formatted_results = []
    for account in accounts:
        formatted_results.append({
            "account_id": account['accountid'],
            "name": account['name'],
            "email": account.get('emailaddress1'),
            "phone": account.get('telephone1'),
            "city": account.get('address1_city'),
            "country": account.get('address1_country'),
            "type": "account"
        })
    
    print(f"Found {len(accounts)} matching accounts")
    return formatted_results

def format_accounts_output(accounts: List[Dict[str, Any]]) -> str:
    """Format account search results as readable string"""
    if not accounts:
        return "No accounts found matching your search criteria."
    
    output = [f"Found {len(accounts)} accounts:"]
    for account in accounts:
        email_info = f" |{account['email']}" if account.get('email') else ""
        phone_info = f" | {account['phone']}" if account.get('phone') else ""
        location_info = ""
        if account.get('city') or account.get('country'):
            location = f"{account.get('city', '')} {account.get('country', '')}".strip()
            location_info = f" | {location}" if location else ""
        
        output.append(f"  • {account['name']} (ID: {account['account_id']}){email_info}{phone_info}{location_info}")
    
    return "\n".join(output)

def search_accounts_tool(search_term: str, max_results: int = 5) -> str:
    """
    Tool function for MCP: Search accounts and return formatted results
    
    Args:
        search_term: Search term for account names
        max_results: Maximum results to return
        
    Returns:
        Formatted string with search results
    """
    accounts = search_accounts(search_term, max_results)
    return format_accounts_output(accounts)