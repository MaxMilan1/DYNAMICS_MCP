"""Configuration for Dynamics 365 with Microsoft Agent Framework"""
import os
import dotenv

dotenv.load_dotenv()

AUTH_MODE = os.getenv("DYNAMICS_AUTH_MODE", "interactive")

if AUTH_MODE == "service_account":
    DYNAMICS_CONFIG = {
        "url": "https://xylos-sb.crm4.dynamics.com",
        "api_version": "v9.2",
        "authority": f"https://login.microsoftonline.com/{os.getenv('DYNAMICS_SERVICE_TENANT_ID')}",
        "scopes": ["https://xylos-sb.crm4.dynamics.com/.default"],
        "client_id": os.getenv("DYNAMICS_SERVICE_CLIENT_ID"),
        "client_secret": os.getenv("DYNAMICS_SERVICE_CLIENT_SECRET"),
    }
else:
    DYNAMICS_CONFIG = {
        "url": "https://xylos-sb.crm4.dynamics.com",
        "api_version": "v9.2",
        "authority": "https://login.microsoftonline.com/common",
        "scopes": ["https://xylos-sb.crm4.dynamics.com/user_impersonation"],
        "client_id": os.getenv("DYNAMICS_CLIENT_ID"),
        "client_secret": os.getenv("DYNAMICS_CLIENT_SECRET"),
    }