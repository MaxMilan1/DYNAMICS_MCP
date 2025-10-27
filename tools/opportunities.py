"""Opportunity-related tools for Dynamics 365"""

from typing import Dict, Any, Optional, List
from utils.dynamics_client import dynamics_client
from tools.contacts import search_contacts
from tools.accounts import search_accounts

def create_opportunity(name: str,
                     contract_verlengingen: bool,
                     account_search_term: str,
                     contact_search_term: str,
                     description: Optional[str] = None,
                     estimated_close_date: Optional[str] = None,
                     # New optional fields
                     xylos_contractverlenging: Optional[bool] = None,
                     sca_alreadyplanned: Optional[bool] = None,
                     xylos_bidoffice: Optional[bool] = None,
                     identifycustomercontacts: Optional[bool] = None,
                     opportunityratingcode: Optional[int] = None,
                     budgetstatus: Optional[int] = None,
                     xylos_opportunitytype: Optional[int] = None,
                     xylos_quotelanguage: Optional[int] = None,
                     xylos_opportunitysource: Optional[int] = None,
                     xylos_approach: Optional[int] = None,
                     need: Optional[int] = None,
                     purchaseprocess: Optional[int] = None,
                     xylos_salesdossierteams: Optional[str] = None,
                     xylos_effectivefrom: Optional[str] = None,
                     xylos_effectiveto: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new opportunity in Dynamics 365 with flexible lookup resolution
    
    Args:
        # Required fields
        name: Name of the opportunity (required)
        contract_verlengingen: Contract verlengingen boolean (required)
        account_search_term: Search term to find related account (required)
        contact_search_term: Search term to find related contact (required)

        # Optional fields
        description: A brief description of the opportunity (max 40 characters)
        estimated_close_date: Estimated close date (YYYY-MM-DD)        
        xylos_contractverlenging: Boolean field for contract extension
        sca_alreadyplanned: Boolean field for already planned
        xylos_bidoffice: Boolean field for bid office
        identifycustomercontacts: Boolean field for customer contacts identification
        opportunityratingcode: Optionset for opportunity rating (integer)
        budgetstatus: Optionset for budget status (integer)
        xylos_opportunitytype: Optionset for opportunity type (integer)
        xylos_quotelanguage: Optionset for quote language (integer)
        xylos_opportunitysource: Optionset for opportunity source (integer)
        xylos_approach: Optionset for approach (integer)
        need: Integer field for need
        purchaseprocess: Integer field for purchase process
        xylos_salesdossierteams: String field for sales dossier teams
        xylos_effectivefrom: Effective from date (YYYY-MM-DD)
        xylos_effectiveto: Effective to date (YYYY-MM-DD)
        
    Returns:
        Dictionary with operation results
    """

    if len(description) > 40:
        return {
            "success": False,
            "message": f"Subject must be 40 characters or less. Current length: {len(description)}"
        }
    
    print(f"Creating opportunity: {name}")
    
    # Prepare opportunity data with default values
    
    data = {
        "name": name,
        "description": description,
        "xylos_contractverlenging": contract_verlengingen 
    }
    
    # Handle date fields
    if estimated_close_date:
        data["estimatedclosedate"] = estimated_close_date
    if xylos_effectivefrom:
        data["xylos_effectivefrom"] = xylos_effectivefrom
    if xylos_effectiveto:
        data["xylos_effectiveto"] = xylos_effectiveto
    
    # Handle boolean fields - only update if provided
    if xylos_contractverlenging is not None:
        data["xylos_contractverlenging"] = xylos_contractverlenging
    if sca_alreadyplanned is not None:
        data["sca_alreadyplanned"] = sca_alreadyplanned
    if xylos_bidoffice is not None:
        data["xylos_bidoffice"] = xylos_bidoffice
    if identifycustomercontacts is not None:
        data["identifycustomercontacts"] = identifycustomercontacts
    
    # Handle optionset fields (integers)
    if opportunityratingcode is not None:
        data["opportunityratingcode"] = opportunityratingcode
    if budgetstatus is not None:
        data["budgetstatus"] = budgetstatus
    if xylos_opportunitytype is not None:
        data["xylos_opportunitytype"] = xylos_opportunitytype
    if xylos_quotelanguage is not None:
        data["xylos_quotelanguage"] = xylos_quotelanguage
    if xylos_opportunitysource is not None:
        data["xylos_opportunitysource"] = xylos_opportunitysource
    if xylos_approach is not None:
        data["xylos_approach"] = xylos_approach
    
    # Handle integer fields
    if need is not None:
        data["need"] = need
    if purchaseprocess is not None:
        data["purchaseprocess"] = purchaseprocess
    
    # Handle string fields
    if xylos_salesdossierteams is not None:
        data["xylos_salesdossierteams"] = xylos_salesdossierteams
    
    # Resolve account lookup
    resolved_account_id = None
    accounts = search_accounts(account_search_term, max_results=1)
    if accounts:
        resolved_account_id = accounts[0]['account_id']
        print(f"Linked account: {accounts[0]['name']}")
    else:
        print(f"No accounts found for search term: {account_search_term}")
    
    if resolved_account_id:
        data["customerid_account@odata.bind"] = f"/accounts({resolved_account_id})"
    
    # Resolve contact lookup
    resolved_contact_id = None
    contacts = search_contacts(contact_search_term, max_results=1)
    if contacts:
        resolved_contact_id = contacts[0]['contact_id']
        print(f"Linked contact: {contacts[0]['fullname']}")
    else:
        print(f"No contacts found for search term: {contact_search_term}")
    
    if resolved_contact_id:
        data["parentcontactid@odata.bind"] = f"/contacts({resolved_contact_id})"
    
    # Create the opportunity
    opportunity_id = dynamics_client.api_post("opportunities", data, "xylos_opportunityid")
    
    if opportunity_id:
        return {
            "success": True,
            "opportunity_id": opportunity_id,
            "message": f"Opportunity '{name}' created successfully",
            "linked_account_id": resolved_account_id,
            "linked_contact_id": resolved_contact_id
        }
    else:
        return {
            "success": False,
            "message": f"Failed to create opportunity '{name}'"
        }

def get_opportunity(opportunity_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve an opportunity by ID from Dynamics 365
    
    Args:
        opportunity_id: The ID of the opportunity to retrieve
        
    Returns:
        Dictionary with opportunity details or None if not found
    """

    print(f"Retrieving opportunity: {opportunity_id}")
    
    endpoint = f"opportunities({opportunity_id})"
    result = dynamics_client.api_get(endpoint)
    
    if result:
        print(f"Retrieved opportunity: {result.get('name', 'Unknown')}")
    else:
        print(f"Opportunity not found: {opportunity_id}")
    
    return result

def search_opportunities_by_name(search_term: str, max_results: int) -> List[Dict[str, Any]]:
    """
    Search opportunities by name containing the search term
    
    Args:
        search_term: Term to search in opportunity names
        max_results: Maximum number of results to return
        
    Returns:
        List of opportunity dictionaries
    """
    print(f"Searching opportunities with term: {search_term}")
    
    filter_query = f"contains(name, '{search_term}')"
    params = {
        "$filter": filter_query,
        "$top": max_results
    }
    
    result = dynamics_client.api_get("opportunities", params)
    opportunities = result.get('value', []) if result else []
    
    return opportunities

def search_opportunities_by_date(start_date: str, end_date: str, max_results: int) -> List[Dict[str, Any]]:
    """
    Search opportunities created within a date range
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        max_results: Maximum number of results to return
        
    Returns:
        List of opportunity dictionaries
    """
    print(f"Searching opportunities from {start_date} to {end_date}")
    
    filter_query = f"createdon ge {start_date} and createdon le {end_date}"
    params = {
        "$filter": filter_query,
        "$top": max_results
    }
    
    result = dynamics_client.api_get("opportunities", params)
    opportunities = result.get('value', []) if result else []
    
    return opportunities

def get_opportunities(top: int = 100) -> List[Dict[str, Any]]:
    """
    List recent opportunities from Dynamics 365
    
    Args:
        top: Number of recent opportunities to retrieve
        
    Returns:
        List of opportunity dictionaries
    """
    print(f"Listing top {top} recent opportunities")
    
    endpoint = "opportunities"
    params = {
        "$top": top,
        "$orderby": "createdon desc"
    }
    
    result = dynamics_client.api_get(endpoint, params)
    opportunities = result.get('value', []) if result else []
    
    print(f"Retrieved {len(opportunities)} opportunities")
    return opportunities

def update_opportunity(opportunity_id: str, updates: Dict[str, Any]) -> bool:
    """
    Update an existing opportunity in Dynamics 365
    
    Args:
        opportunity_id: The ID of the opportunity to update
        updates: Dictionary of fields to update
        
    Returns:
        True if update was successful, False otherwise
    """
    print(f"Updating opportunity: {opportunity_id} with {updates}")
    
    endpoint = f"opportunities({opportunity_id})"
    success = dynamics_client.api_patch(endpoint, updates)
    
    if success:
        print(f"Opportunity '{opportunity_id}' updated successfully")
    else:
        print(f"Failed to update opportunity '{opportunity_id}'")
    
    return success

## TOOLS FOR MCP

def create_opportunity_tool(name: str,
                          account_search_term: str,
                          contact_search_term: str,
                          contract_verlengingen: bool,
                          # Optional fields
                          description: Optional[str] = None,
                          estimated_close_date: Optional[str] = None,
                          xylos_contractverlenging: Optional[bool] = None,
                          sca_alreadyplanned: Optional[bool] = None,
                          xylos_bidoffice: Optional[bool] = None,
                          identifycustomercontacts: Optional[bool] = None,
                          opportunityratingcode: Optional[int] = None,
                          budgetstatus: Optional[int] = None,
                          xylos_opportunitytype: Optional[int] = None,
                          xylos_quotelanguage: Optional[int] = None,
                          xylos_opportunitysource: Optional[int] = None,
                          xylos_approach: Optional[int] = None,
                          need: Optional[int] = None,
                          purchaseprocess: Optional[int] = None,
                          xylos_salesdossierteams: Optional[str] = None,
                          xylos_effectivefrom: Optional[str] = None,
                          xylos_effectiveto: Optional[str] = None) -> str:
    """
    Tool function for MCP: Create opportunity and return formatted results
    
    Args:
        # Required fields
        name: Name of the opportunity (required)
        contract_verlengingen: Contract verlengingen boolean (required)
        account_search_term: Search term to find related account (required)
        contact_search_term: Search term to find related contact (required)

        # Optional fields
        description: Description of the opportunity
        estimated_close_date: Estimated close date (YYYY-MM-DD)        
        xylos_contractverlenging: Boolean field for contract extension
        sca_alreadyplanned: Boolean field for already planned
        xylos_bidoffice: Boolean field for bid office
        identifycustomercontacts: Boolean field for customer contacts identification
        opportunityratingcode: Optionset for opportunity rating (integer)
        budgetstatus: Optionset for budget status (integer)
        xylos_opportunitytype: Optionset for opportunity type (integer)
        xylos_quotelanguage: Optionset for quote language (integer)
        xylos_opportunitysource: Optionset for opportunity source (integer)
        xylos_approach: Optionset for approach (integer)
        need: Integer field for need
        purchaseprocess: Integer field for purchase process
        xylos_salesdossierteams: String field for sales dossier teams
        xylos_effectivefrom: Effective from date (YYYY-MM-DD)
        xylos_effectiveto: Effective to date (YYYY-MM-DD)
        
    Returns:
        Formatted string with operation results
    """
    result = create_opportunity(
        name=name,
        account_search_term=account_search_term,
        contact_search_term=contact_search_term,
        contract_verlengingen=contract_verlengingen,
        description=description,
        estimated_close_date=estimated_close_date,
        xylos_contractverlenging=xylos_contractverlenging,
        sca_alreadyplanned=sca_alreadyplanned,
        xylos_bidoffice=xylos_bidoffice,
        identifycustomercontacts=identifycustomercontacts,
        opportunityratingcode=opportunityratingcode,
        budgetstatus=budgetstatus,
        xylos_opportunitytype=xylos_opportunitytype,
        xylos_quotelanguage=xylos_quotelanguage,
        xylos_opportunitysource=xylos_opportunitysource,
        xylos_approach=xylos_approach,
        need=need,
        purchaseprocess=purchaseprocess,
        xylos_salesdossierteams=xylos_salesdossierteams,
        xylos_effectivefrom=xylos_effectivefrom,
        xylos_effectiveto=xylos_effectiveto
    )
    
    if result["success"]:
        output = [f"{result['message']}", f"Opportunity ID: {result['opportunity_id']}"]
        if result.get('linked_account_id'):
            output.append(f"Linked Account ID: {result['linked_account_id']}")
        if result.get('linked_contact_id'):
            output.append(f"Linked Contact ID: {result['linked_contact_id']}")
        return "\n".join(output)
    else:
        return f"{result['message']}"

def get_opportunity_tool(opportunity_id: str) -> str:
    """
    Tool function for MCP: Get opportunity details and return formatted results
    
    Args:
        opportunity_id: The ID of the opportunity to retrieve
        
    Returns:
        Formatted string with opportunity details
    """
    opportunity = get_opportunity(opportunity_id)
    
    if not opportunity:
        return f"Opportunity with ID '{opportunity_id}' not found"
    
    # Format the opportunity data
    output = [f"Opportunity Details (ID: {opportunity_id}):"]
    output.append(f"  • Name: {opportunity.get('name', 'N/A')}")
    output.append(f"  • Description: {opportunity.get('description', 'N/A')}")
    output.append(f"  • Estimated Close Date: {opportunity.get('estimatedclosedate', 'N/A')}")
    output.append(f"  • Status: {opportunity.get('statuscode', 'N/A')}")
    output.append(f"  • Created On: {opportunity.get('createdon', 'N/A')}")
    
    return "\n".join(output)

def get_opportunities_tool(top: int) -> str:
    """
    Tool function for MCP: List recent opportunities and return formatted results
    
    Args:
        top: Number of recent opportunities to retrieve
        
    Returns:
        Formatted string with list of opportunities
    """
    opportunities = get_opportunities(top)
    
    if not opportunities:
        return "No opportunities found."
    
    output = [f"Top {len(opportunities)} Recent Opportunities:"]
    for opp in opportunities:
        output.append(f"  • {opp.get('name', 'N/A')} (ID: {opp.get('opportunityid', 'N/A')}) - Created On: {opp.get('createdon', 'N/A')}")
    
    return "\n".join(output)

def search_opportunities_by_name_tool(search_term: str, max_results: int = 50) -> str:
    """
    Tool function for MCP: Search opportunities and return formatted results
    
    Args:
        search_term: Term to search in opportunity names
        max_results: Maximum number of results to return
    Returns:
        Formatted string with search results
    """
    opportunities = search_opportunities_by_name(search_term, max_results)
    
    if not opportunities:
        return f"No opportunities found matching '{search_term}'."
    
    output = [f"Found {len(opportunities)} opportunities matching '{search_term}':"]   
    for opp in opportunities:
        output.append(f"  • {opp.get('name', 'N/A')} (ID: {opp.get('opportunityid', 'N/A')}) - Created On: {opp.get('createdon', 'N/A')}")

    return "\n".join(output)

def search_opportunities_by_date_tool(start_date: str, end_date: str, max_results: int = 50) -> str:
    """
    Tool function for MCP: Search opportunities by date range and return formatted results
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        max_results: Maximum number of results to return
        
    Returns:
        Formatted string with search results
    """
    opportunities = search_opportunities_by_date(start_date, end_date, max_results)
    
    if not opportunities:
        return f"No opportunities found between {start_date} and {end_date}."
    
    output = [f"Found {len(opportunities)} opportunities between {start_date} and {end_date}:"]
    for opp in opportunities:
        output.append(f"  • {opp.get('name', 'N/A')} (ID: {opp.get('opportunityid', 'N/A')}) - Created On: {opp.get('createdon', 'N/A')}")
    
    return "\n".join(output)

def update_opportunity_tool(opportunity_id: str, updates: Dict[str, Any]) -> str:
    """
    Tool function for MCP: Update opportunity and return formatted results
    
    Args:
        opportunity_id: The ID of the opportunity to update
        updates: Dictionary of fields to update
        
    Returns:
        Formatted string with operation results
    """
    success = update_opportunity(opportunity_id, updates)
    
    if success:
        return f"Opportunity '{opportunity_id}' updated successfully."
    else:
        return f"Failed to update opportunity '{opportunity_id}'."