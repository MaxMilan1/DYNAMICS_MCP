from fastmcp import FastMCP
from typing import Annotated
from annotated_types import MaxLen
from tools.accounts import search_accounts_tool
from tools.contacts import search_contacts_tool
from tools.opportunities import create_opportunity_tool, get_opportunity_tool, get_opportunities_tool, search_opportunities_by_name_tool, search_opportunities_by_date_tool, update_opportunity_tool
from tools.leads import search_leads_tool, create_lead_tool, search_leads_by_date_tool

mcp = FastMCP("Dynamics 365")

# Opportunity Tools
@mcp.tool()
def create_opportunity(
    name: str,
    account_search_term: str,
    contact_search_term: str,
    contract_verlengingen: bool,
    description: Annotated[str | None, MaxLen(40)] = None,
    estimated_close_date: str = None,
    xylos_contractverlenging: bool = None,
    sca_alreadyplanned: bool = None,
    xylos_bidoffice: bool = None,
    identifycustomercontacts: bool = None,
    opportunityratingcode: int = None,
    budgetstatus: int = None,
    xylos_opportunitytype: int = None,
    xylos_quotelanguage: int = None,
    xylos_opportunitysource: int = None,
    xylos_approach: int = None,
    need: int = None,
    purchaseprocess: int = None,
    xylos_salesdossierteams: str = None,
    xylos_effectivefrom: str = None,
    xylos_effectiveto: str = None
) -> str:
    """Create a new opportunity in Dynamics 365 with flexible account/contact lookup"""
    return create_opportunity_tool(
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

@mcp.tool()
def get_opportunity(opportunity_id: str) -> str:
    """Retrieve an opportunity by ID from Dynamics 365"""
    return get_opportunity_tool(opportunity_id)

@mcp.tool()
def get_opportunities(top: int = 100) -> str:
    """List recent opportunities from Dynamics 365"""
    return get_opportunities_tool(top)

@mcp.tool()
def search_opportunities_by_name(search_term: str, max_results: int = 20) -> str:
    """Search for opportunities in Dynamics 365 using partial name matching"""
    return search_opportunities_by_name_tool(search_term, max_results)

@mcp.tool()
def search_opportunities_by_date(start_date: str, end_date: str, max_results: int = 20) -> str:
    """Search for opportunities in Dynamics 365 within a date range"""
    return search_opportunities_by_date_tool(start_date, end_date, max_results)

@mcp.tool()
def update_opportunity(opportunity_id: str, updates: dict) -> str:
    """Update an existing opportunity in Dynamics 365"""
    return update_opportunity_tool(opportunity_id, updates)

# Contact Tools
@mcp.tool()
def search_contacts(search_term: str, max_results: int = 20) -> str:
    """Search for contacts in Dynamics 365 using partial name matching"""
    return search_contacts_tool(search_term, max_results)

# Account Tools
@mcp.tool()
def search_accounts(search_term: str, max_results: int = 20) -> str:
    """Search for accounts in Dynamics 365 using partial name matching"""
    return search_accounts_tool(search_term, max_results)

# Lead Tools
@mcp.tool()
def search_leads(search_term: str, max_results: int = 20) -> str:
    """Search for leads in Dynamics 365 using partial name matching"""
    return search_leads_tool(search_term, max_results)

@mcp.tool()
def search_leads_by_date(start_date: str, end_date: str, max_results: int = 20) -> str:
    """Search for leads in Dynamics 365 within a date range"""
    return search_leads_by_date_tool(start_date, end_date, max_results)

@mcp.tool()
def create_lead(
    subject: str,
    firstname: str,
    lastname: str,
    companyname: str,
    email: str = None,
    phone: str = None,
    mobilephone: str = None,
    jobtitle: str = None,
    websiteurl: str = None,
    description: Annotated[str | None, MaxLen(40)] = None,
    estimatedclosedate: str = None,
    xylos_leadsource: int = None,
    xylos_leadratingcode: int = None,
    parentaccountname: str = None,
    parentcontactname: str = None,
    xylos_gender: int = None,
    xylos_language: int = None,
    xylos_jobdescriptionid: str = None,
    address1_line1: str = None,
    address1_postalcode: str = None,
    address1_city: str = None,
    address1_stateorprovince: str = None,
    address1_country: str = None
) -> str:
    """Create a new lead in Dynamics 365"""
    return create_lead_tool(
        subject=subject,
        firstname=firstname,
        lastname=lastname,
        companyname=companyname,
        email=email,
        phone=phone,
        mobilephone=mobilephone,
        jobtitle=jobtitle,
        websiteurl=websiteurl,
        description=description,
        estimatedclosedate=estimatedclosedate,
        xylos_leadsource=xylos_leadsource,
        xylos_leadratingcode=xylos_leadratingcode,
        parentaccountname=parentaccountname,
        parentcontactname=parentcontactname,
        xylos_gender=xylos_gender,
        xylos_language=xylos_language,
        xylos_jobdescriptionid=xylos_jobdescriptionid,
        address1_line1=address1_line1,
        address1_postalcode=address1_postalcode,
        address1_city=address1_city,
        address1_stateorprovince=address1_stateorprovince,
        address1_country=address1_country
    )

if __name__ == "__main__":
    mcp.run()
