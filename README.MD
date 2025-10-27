# Authentication Setup
## Development Mode (Interactive)

For development and testing, use interactive authentication:

```bash
DYNAMICS_AUTH_MODE=interactive
DYNAMICS_CLIENT_ID=client-secret
```

How it works:

- Opens browser for one-time authentication
- Caches tokens for subsequent requests
- Perfect for local development

## Production Mode (Service Account)
For production environments, use service account authentication:

```bash
DYNAMICS_AUTH_MODE=service_account
DYNAMICS_SERVICE_CLIENT_ID=your-production-app-id
DYNAMICS_SERVICE_CLIENT_SECRET=your-client-secret
DYNAMICS_SERVICE_TENANT_ID=your-tenant-id
```
Setup required:

- Create new App Registration in Azure
- Generate client secret
- Add app to Dynamics 365 security roles
- Set environment variables