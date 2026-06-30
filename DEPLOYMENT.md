# ILMORA – Production Deployment Guide (Single-Origin Monorepo)

This document provides a step-by-step guide to deploying **ILMORA – AI Career Platform** in production as a unified web service on Render, integrating both the React + Vite frontend and the FastAPI backend.

By serving both the frontend and backend from the same origin, all cross-origin resource sharing (CORS) preflight requests and protocol configuration issues are eliminated.

---

## 1. Firebase Authentication Setup

Ensure Firebase Auth is prepared for production and only accepts authentication requests from your custom domain or Render URL.

### Production Environment Settings
1. Go to the [Firebase Console](https://console.firebase.google.com/) and select your project.
2. Under **Build** > **Authentication** > **Settings** tab:
   - **Authorized Domains**: Add your production Render URL (e.g., `ilmora.onrender.com` or custom domain `ilmora-ai.com`).
   - *Remove `localhost` and `127.0.0.1` in the production-specific Firebase project* to lock down authentication and prevent cross-environment sign-ins.
3. Under **Project Settings** > **General**:
   - Verify your Web App Config credentials match the variables in the frontend environment setup.

---

## 2. Supabase Database Configuration

Ensure Supabase is configured with proper connections, pooling, and security settings.

### Connection & Pooling
- **Direct Database URL**: Use for running migrations or when low latency is required. Direct connections connect on port `5432` of your Supabase host.
- **Connection Pooler URL (Session/Transaction mode)**: Always use the connection pooler URL for serverless/hosted backend deployments (FastAPI on Render) to prevent exceeding database connection limits. The pooler connects on port `6543`.
  - Format: `postgresql://postgres:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require&supa=tx`

### Row Level Security (RLS) & Policies
- Ensure all public schemas and user-related tables have RLS enabled:
  ```sql
  ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
  ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
  ```
- Verify the standard security policies are active so users can only access their own records:
  ```sql
  CREATE POLICY "Users can manage own profile" ON public.user_profiles
    FOR ALL USING (auth.uid() = user_id);
  ```

---

## 3. Unified Web Service Deployment (Render)

ILMORA is built as a single, multi-stage Docker container. The build process installs Node dependencies, compiles the React SPA, and copies the static assets into FastAPI's directory before serving the Python app.

### Prerequisites
The project root contains:
- `Dockerfile`: Multi-stage build recipe.
- `render.yaml`: Blueprint definition.
- `backend/requirements.txt`: Python backend dependencies.
- `frontend/package.json`: Javascript build commands.

### Render Blueprint Deployment Steps
1. Push your repository to GitHub.
2. Go to the [Render Dashboard](https://dashboard.render.com/).
3. Click **New** > **Blueprint**.
4. Select your `AI-Career-Assistant` repository.
5. Render will automatically parse the `render.yaml` file and prompt you to enter the environment values:

| Environment Variable | Description |
| :--- | :--- |
| `DATABASE_URL` | Your Supabase pooler URL (port 6543 connection string) |
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_ANON_KEY` | Your Supabase public anonymous key |
| `SUPABASE_JWT_SECRET` | Your Supabase JWT Secret |
| `FIREBASE_PROJECT_ID` | Your Firebase Project ID |
| `VITE_SUPABASE_URL` | Frontend Supabase URL (same as `SUPABASE_URL`) |
| `VITE_SUPABASE_ANON_KEY` | Frontend Supabase Anon Key (same as `SUPABASE_ANON_KEY`) |
| `VITE_FIREBASE_API_KEY` | Your Firebase web API key |
| `VITE_FIREBASE_AUTH_DOMAIN` | Your Firebase auth domain (`xxx.firebaseapp.com`) |
| `VITE_FIREBASE_PROJECT_ID` | Your Firebase project ID (same as `FIREBASE_PROJECT_ID`) |
| `VITE_FIREBASE_STORAGE_BUCKET`| Your Firebase storage bucket |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Your Firebase messaging sender ID |
| `VITE_FIREBASE_APP_ID` | Your Firebase app ID |
| `VITE_FIREBASE_MEASUREMENT_ID` | Your Firebase analytics measurement ID |
| `VITE_API_URL` | Set to `/api/v1` (Relative URL ensures zero-CORS communication) |

6. Click **Approve**. Render will build the Docker container and deploy the service.

### Alternative (Manual Docker Deploy)
If you prefer not to use the Blueprint:
1. Click **New** > **Web Service**.
2. Connect your GitHub repository.
3. Configure the service:
   - **Root Directory**: (Leave blank - build from project root)
   - **Language**: `Docker`
4. Add all environment variables listed in the table above to the Web Service settings.
5. Deploy.

---

## 4. Custom Domain & HTTPS Configuration

To premium-brand your application, configure custom domains on Render.

### Render Web Service Domain
1. In your Render service, go to **Settings** > **Custom Domains**.
2. Enter your custom domain (e.g., `ilmora.com` or `app.ilmora.com`).
3. Render will provide DNS records:
   - For Apex Domain (`ilmora.com`): Set an **A Record** pointing to Render's IP address.
   - For Subdomain (`app.ilmora.com`): Set a **CNAME Record** pointing to your Render hostname (e.g., `ilmora.onrender.com`).
4. Render automatically provisions a free Let's Encrypt SSL certificate and enforces HTTPS redirects globally once the DNS resolves.

---

## 5. Google Search Console Verification

Verifying ownership of your domain in Google Search Console helps index the page and monitor traffic.

1. Go to the [Google Search Console](https://search.google.com/search-console).
2. Choose **Domain** verification (covers apex + subdomains) or **URL prefix** verification.
3. **Verification Method 1 (Recommended - DNS TXT Record)**:
   - Copy the TXT value provided by Google.
   - Go to your DNS hosting provider (e.g., GoDaddy, Cloudflare, Namecheap) and add a **TXT Record** with name `@` and the value copied.
4. **Verification Method 2 (HTML File)**:
   - Download the verification HTML file from Google.
   - Place this file in `frontend/public/` folder of the repository. It will automatically build into the public root path on deploy (accessible at `https://ilmora.com/google-verification-id.html`).
5. Click **Verify** in Search Console.

---

## 6. Complete Production Environment Checklist

Before declaring the deployment live, verify the following:

- [ ] **Secure Variables**: No passwords, private keys, or API tokens are checked into git. `.env` and local secrets are added to `.gitignore`.
- [ ] **Prod Database**: Supabase connection string uses the connection pooler (port 6543) and is running on a transaction pool mode.
- [ ] **Auth Domains**: Localhost is deactivated or restricted from Firebase Authentication domains in production console settings.
- [ ] **Health Endpoint**: Render service shows green and the `/health` endpoint is actively monitored.
- [ ] **HTTPS Enforced**: All requests redirect HTTP traffic to HTTPS securely.
- [ ] **Zero Dev Simulation**: The browser local storage contains no `sim_token` or dev flags, forcing standard Firebase login flows.
