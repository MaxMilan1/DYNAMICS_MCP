"""Contact-related tools for Dynamics 365"""

from typing import List, Dict, Any
from utils.dynamics_client import dynamics_client

def search_contacts(search_term: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for contacts in Dynamics 365 using partial name matching
    
    Args:
        search_term: Search term for contact names (partial match)
        max_results: Maximum number of results to return
        
    Returns:
        List of matching contacts with details
    """
    print(f"Searching contacts for: '{search_term}'")
    
    endpoint = "contacts"
    params = {
        "$filter": f"contains(fullname, '{search_term}')",
        "$select": "contactid,fullname,emailaddress1,telephone1,jobtitle,_parentcustomerid_value",
        "$orderby": "fullname",
        "$top": str(max_results)
    }
    
    result = dynamics_client.api_get(endpoint, params)
    contacts = result.get('value', []) if result else []
    
    # Format results
    formatted_results = []
    for contact in contacts:
        formatted_results.append({
            "contact_id": contact['contactid'],
            "fullname": contact['fullname'],
            "email": contact.get('emailaddress1'),
            "phone": contact.get('telephone1'),
            "job_title": contact.get('jobtitle'),
            "parent_customer_id": contact.get('_parentcustomerid_value'),
            "type": "contact"
        })
    
    print(f"Found {len(contacts)} matching contacts")
    return formatted_results

def format_contacts_output(contacts: List[Dict[str, Any]]) -> str:
    """Format contact search results as readable string"""
    if not contacts:
        return "No contacts found matching your search criteria."
    
    output = [f"Found {len(contacts)} contacts:"]
    for contact in contacts:
        email_info = f" | {contact['email']}" if contact.get('email') else ""
        phone_info = f" | {contact['phone']}" if contact.get('phone') else ""
        job_info = f" | {contact['job_title']}" if contact.get('job_title') else ""
        
        output.append(f"  • {contact['fullname']} (ID: {contact['contact_id']}){job_info}{email_info}{phone_info}")
    
    return "\n".join(output)

def search_contacts_tool(search_term: str, max_results: int = 5) -> str:
    """
    Tool function for MCP: Search contacts and return formatted results
    
    Args:
        search_term: Search term for contact names
        max_results: Maximum results to return
        
    Returns:
        Formatted string with search results
    """
    contacts = search_contacts(search_term, max_results)
    return format_contacts_output(contacts)