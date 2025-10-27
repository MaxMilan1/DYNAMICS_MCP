"""Lead-related tools for Dynamics 365"""

from typing import List, Dict, Any, Optional
from utils.dynamics_client import dynamics_client
from tools.accounts import search_accounts
from tools.contacts import search_contacts

def search_leads(search_term: str, max_results: int) -> List[Dict[str, Any]]:
    """
    Search for leads in Dynamics 365 using partial name matching
    
    Args:
        search_term: Search term for lead names (partial match)
        max_results: Maximum number of results to return
        
    Returns:
        List of matching leads with details
    """
    print(f"Searching leads for: '{search_term}'")
    
    endpoint = "leads"
    params = {
        "$filter": f"contains(subject, '{search_term}') or contains(firstname, '{search_term}') or contains(lastname, '{search_term}')",
        "$select": "leadid,subject,firstname,lastname,emailaddress1,telephone1,companyname,statuscode",
        "$orderby": "createdon desc",
        "$top": str(max_results)
    }
    
    result = dynamics_client.api_get(endpoint, params)
    leads = result.get('value', []) if result else []
    
    # Format results
    formatted_results = []
    for lead in leads:
        full_name = f"{lead.get('firstname', '')} {lead.get('lastname', '')}".strip()
        formatted_results.append({
            "lead_id": lead['leadid'],
            "subject": lead.get('subject', ''),
            "full_name": full_name,
            "company_name": lead.get('companyname', ''),
            "email": lead.get('emailaddress1'),
            "phone": lead.get('telephone1'),
            "status": lead.get('statuscode'),
            "type": "lead"
        })
    
    print(f"Found {len(leads)} matching leads")
    return formatted_results

def search_leads_by_date(start_date: str, end_date: str, max_results: int) -> List[Dict[str, Any]]:
    """
    Search for leads created within a specific date range in Dynamics 365
    
    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        max_results: Maximum number of results to return
        
    Returns:
        List of matching leads with details
    """
    print(f"Searching leads from '{start_date}' to '{end_date}'")
    
    endpoint = "leads"
    params = {
        "$filter": f"createdon ge {start_date}T00:00:00Z and createdon le {end_date}T23:59:59Z",
        "$select": "leadid,subject,firstname,lastname,emailaddress1,telephone1,companyname,statuscode",
        "$orderby": "createdon desc",
        "$top": str(max_results)
    }
    
    result = dynamics_client.api_get(endpoint, params)
    leads = result.get('value', []) if result else []
    
    # Format results
    formatted_results = []
    for lead in leads:
        full_name = f"{lead.get('firstname', '')} {lead.get('lastname', '')}".strip()
        formatted_results.append({
            "lead_id": lead['leadid'],
            "subject": lead.get('subject', ''),
            "full_name": full_name,
            "company_name": lead.get('companyname', ''),
            "email": lead.get('emailaddress1'),
            "phone": lead.get('telephone1'),
            "status": lead.get('statuscode'),
            "type": "lead"
        })
    
    print(f"Found {len(leads)} matching leads")
    return formatted_results

def create_lead(
    subject: str,
    firstname: str,
    lastname: str,
    companyname: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    mobilephone: Optional[str] = None,
    jobtitle: Optional[str] = None,
    websiteurl: Optional[str] = None,
    description: Optional[str] = None,
    estimatedclosedate: Optional[str] = None,
    xylos_leadsource: Optional[int] = None,
    xylos_leadratingcode: Optional[int] = None,
    parentaccountname: Optional[str] = None,
    parentcontactname: Optional[str] = None,
    xylos_gender: Optional[int] = None,
    xylos_language: Optional[int] = None,
    xylos_jobdescriptionid: Optional[str] = None,
    address1_line1: Optional[str] = None,
    address1_postalcode: Optional[str] = None,
    address1_city: Optional[str] = None,
    address1_stateorprovince: Optional[str] = None,
    address1_country: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new lead in Dynamics 365
    
    Args:
        subject: Lead subject/title (max 40 characters)
        firstname: First name
        lastname: Last name  
        companyname: Company name
        email: Email address
        phone: Phone number
        mobilephone: Mobile phone number
        jobtitle: Job title
        websiteurl: Website URL
        description: Lead description
        estimatedclosedate: Estimated close date
        xylos_leadsource: Lead source code
        xylos_leadratingcode: Lead rating code
        parentaccountname: Parent account name
        parentcontactname: Parent contact name
        xylos_gender: Gender code
        xylos_language: Language code
        xylos_jobdescriptionid: Job description ID
        address1_line1: Street address
        address1_postalcode: Postal code
        address1_city: City
        address1_stateorprovince: State/Province
        address1_country: Country
        
    Returns:
        Dictionary with operation results
    """

    if len(subject) > 40:
        return {
            "success": False,
            "message": f"Subject must be 40 characters or less. Current length: {len(subject)}"
        }
    
    print(f"Creating lead: {subject}")
    
    lead_data = {
        "subject": subject,
        "firstname": firstname,
        "lastname": lastname,
        "companyname": companyname
    }
    
    # Lookup account by name
    resolved_account_id = None
    if parentaccountname:
        accounts = search_accounts(parentaccountname, max_results=1)
        if accounts:
            resolved_account_id = accounts[0]['account_id']
            print(f"Linked account: {accounts[0]['name']}")
        else:
            print(f"No accounts found for search term: {parentaccountname}")
    
    if resolved_account_id:
        lead_data["_parentaccountid_value"] = resolved_account_id
    
    # Lookup contact by name
    resolved_contact_id = None
    if parentcontactname:
        contacts = search_contacts(parentcontactname, max_results=1)
        if contacts:
            resolved_contact_id = contacts[0]['contact_id']
            print(f"Linked contact: {contacts[0]['fullname']}")
        else:
            print(f"No contacts found for search term: {parentcontactname}")
    
    if resolved_contact_id:
        lead_data["_parentcontactid_value"] = resolved_contact_id

    # Optional fields
    if email:
        lead_data["emailaddress1"] = email
    if phone:
        lead_data["telephone1"] = phone
    if mobilephone:
        lead_data["mobilephone"] = mobilephone
    if jobtitle:
        lead_data["jobtitle"] = jobtitle
    if websiteurl:
        lead_data["websiteurl"] = websiteurl
    if description:
        lead_data["description"] = description
    if estimatedclosedate:
        lead_data["estimatedclosedate"] = estimatedclosedate
    if xylos_leadsource is not None:
        lead_data["xylos_leadsource"] = xylos_leadsource
    if xylos_leadratingcode is not None:
        lead_data["xylos_leadratingcode"] = xylos_leadratingcode
    if xylos_gender is not None:
        lead_data["xylos_gender"] = xylos_gender
    if xylos_language is not None:
        lead_data["xylos_language"] = xylos_language
    if xylos_jobdescriptionid:
        lead_data["_xylos_jobdescriptionid_value"] = xylos_jobdescriptionid
    if address1_line1:
        lead_data["address1_line1"] = address1_line1
    if address1_postalcode:
        lead_data["address1_postalcode"] = address1_postalcode
    if address1_city:
        lead_data["address1_city"] = address1_city
    if address1_stateorprovince:
        lead_data["address1_stateorprovince"] = address1_stateorprovince
    if address1_country:
        lead_data["address1_country"] = address1_country
    
    lead_id = dynamics_client.api_post("leads", lead_data, "xylos_leadidentifier")
    
    if lead_id:
        return {
            "success": True,
            "lead_id": lead_id,
            "message": f"Lead '{subject}' created successfully"
        }
    else:
        return {
            "success": False,
            "message": f"Failed to create lead '{subject}'"
        }

def format_leads_output(leads: List[Dict[str, Any]]) -> str:
    """Format lead search results as readable string"""
    if not leads:
        return "No leads found matching your search criteria."
    
    output = [f"Found {len(leads)} leads:"]
    for lead in leads:
        email_info = f" | {lead['email']}" if lead.get('email') else ""
        phone_info = f" | {lead['phone']}" if lead.get('phone') else ""
        company_info = f" | {lead['company_name']}" if lead.get('company_name') else ""
        
        output.append(f"  • {lead['subject']} ({lead['full_name']}){company_info}{email_info}{phone_info}")
        output.append(f"    ID: {lead['lead_id']}")
    
    return "\n".join(output)

# Tool functions for MCP
def search_leads_tool(search_term: str, max_results: int = 50) -> str:
    """
    Tool function for MCP: Search leads and return formatted results
    """
    leads = search_leads(search_term, max_results)
    return format_leads_output(leads)

def search_leads_by_date_tool(start_date: str, end_date: str, max_results: int = 50) -> str:
    """
    Tool function for MCP: Search leads by date and return formatted results
    """
    leads = search_leads_by_date(start_date, end_date, max_results)
    return format_leads_output(leads)

def create_lead_tool(
    subject: str,
    firstname: str,
    lastname: str,
    companyname: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    mobilephone: Optional[str] = None,
    jobtitle: Optional[str] = None,
    websiteurl: Optional[str] = None,
    description: Optional[str] = None,
    estimatedclosedate: Optional[str] = None,
    xylos_leadsource: Optional[int] = None,
    xylos_leadratingcode: Optional[int] = None,
    parentaccountname: Optional[str] = None,
    parentcontactname: Optional[str] = None,
    xylos_gender: Optional[int] = None,
    xylos_language: Optional[int] = None,
    xylos_jobdescriptionid: Optional[str] = None,
    address1_line1: Optional[str] = None,
    address1_postalcode: Optional[str] = None,
    address1_city: Optional[str] = None,
    address1_stateorprovince: Optional[str] = None,
    address1_country: Optional[str] = None
) -> str:
    """
    Tool function for MCP: Create a new lead
    """
    result = create_lead(
        subject,
        firstname,
        lastname,
        companyname,
        email,
        phone,
        mobilephone,
        jobtitle,
        websiteurl,
        description,
        estimatedclosedate,
        xylos_leadsource,
        xylos_leadratingcode,
        parentaccountname,
        parentcontactname,
        xylos_gender,
        xylos_language,
        xylos_jobdescriptionid,
        address1_line1,
        address1_postalcode,
        address1_city,
        address1_stateorprovince,
        address1_country
    )

    if result['success']:
        return f"Lead created successfully with ID: {result['lead_id']}"
    else:
        return f"Error creating lead: {result['message']}"


