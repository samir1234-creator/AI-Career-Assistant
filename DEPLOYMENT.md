# ILMORA – Production Deployment Guide

This document provides a step-by-step guide to deploying **ILMORA – AI Career Platform** in production using Vercel (Frontend), Render (Backend), Supabase (Database), and Firebase (Authentication).

---

## 1. Firebase Authentication Setup

Ensure Firebase Auth is prepared for production and only accepts authentication requests from authorized domains.

### Production Environment Settings
1. Go to the [Firebase Console](https://console.firebase.google.com/) and select your project.
2. Under **Build** > **Authentication** > **Settings** tab:
   - **Authorized Domains**: Add your production Vercel frontend domain (e.g., `ilmora.vercel.app` or your custom domain `ilmora.com`).
   - *Remove `localhost` and `127.0.0.1` in the production-specific Firebase project* to lock down authentication and prevent cross-environment sign-ins.
3. Under **Project Settings** > **General**:
   - Double check your Web App Config credentials match the variables in the frontend environment setup.

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

## 3. Backend Deployment (Render)

The FastAPI backend is configured for deployment on Render.

### Prerequisites
The backend folder contains:
- `requirements.txt`: Python dependencies.
- `/health` endpoint: Monitoring endpoint that returns `{"status": "ok", "version": "9.0.0"}`.

### Render Deployment Steps
1. Create a new **Web Service** on [Render](https://render.com/).
2. Connect your GitHub repository containing the codebase.
3. Configure the Web Service Settings:
   - **Name**: `ilmora-backend`
   - **Environment**: `Python 3`
   - **Root Directory**: `backend` (Important: Set this to `backend` so Render looks for requirements in the subfolder)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Configure the following environment variables in Render's settings:

| Environment Variable | Value/Description |
| :--- | :--- |
| `PROJECT_NAME` | `ILMORA API` |
| `API_V1_STR` | `/api/v1` |
| `BACKEND_CORS_ORIGINS` | Comma-separated list of allowed origins (e.g., `https://ilmora.vercel.app,https://ilmora.com`) |
| `MAX_UPLOAD_SIZE` | `5242880` (5 MB in bytes) |
| `SUPABASE_URL` | Your Supabase project URL (`https://xxx.supabase.co`) |
| `SUPABASE_ANON_KEY` | Your Supabase public anonymous key |
| `SUPABASE_JWT_SECRET` | Your Supabase JWT Secret (from project settings) |
| `DATABASE_URL` | Your Supabase pooler URL (port 6543 connection string) |
| `FIREBASE_PROJECT_ID` | Your Firebase Project ID (required for ID token validation) |

5. Render will automatically deploy the service and provide a public URL (e.g., `https://ilmora-backend-hzsb.onrender.com`).
6. Under **Advanced** > **Health Check Path**:
   - Path: `/health`
   - Render will monitor this path to perform zero-downtime rolling deploys.

---

## 4. Frontend Deployment (Vercel)

The React + Vite frontend is configured for deployment on Vercel as a Single Page Application (SPA).

### Prerequisites
The frontend folder contains:
- `vercel.json`: Rewrites all routing fallback to `index.html` to support React Router HTML5 History mode.
- `package.json`: Installation and build commands.

### Vercel Deployment Steps
1. In the [Vercel Dashboard](https://vercel.com/), click **Add New** > **Project**.
2. Import the GitHub repository containing the codebase.
3. Configure the Project Settings:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
4. Add the following Environment Variables:

| Environment Variable | Value/Description |
| :--- | :--- |
| `VITE_API_URL` | The Render backend API URL (e.g., `https://ilmora-backend-hzsb.onrender.com/api/v1`) |
| `VITE_SUPABASE_URL` | Your Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Your Supabase public anonymous key |
| `VITE_FIREBASE_API_KEY` | Your Firebase web api key |
| `VITE_FIREBASE_AUTH_DOMAIN` | Your Firebase auth domain (`xxx.firebaseapp.com`) |
| `VITE_FIREBASE_PROJECT_ID` | Your Firebase project ID |
| `VITE_FIREBASE_STORAGE_BUCKET`| Your Firebase storage bucket |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Your Firebase messaging sender ID |
| `VITE_FIREBASE_APP_ID` | Your Firebase app ID |
| `VITE_FIREBASE_MEASUREMENT_ID` | Your Firebase analytics measurement ID |

5. Click **Deploy**. Vercel will build the frontend and provide a staging/production deployment URL.

---

## 5. Custom Domain & HTTPS Configuration

To premium-brand your application, configure custom domains.

### Vercel (Frontend Domain)
1. In the Vercel project, go to **Settings** > **Domains**.
2. Enter your custom domain (e.g., `ilmora.com` or `app.ilmora.com`).
3. Vercel will provide DNS records:
   - For Apex Domain (`ilmora.com`): Set an **A Record** pointing to `76.76.21.21`.
   - For Subdomain (`app.ilmora.com`): Set a **CNAME Record** pointing to `cname.vercel-dns.com`.
4. Vercel automatically provisions a free Let's Encrypt SSL certificate and enforces HTTPS redirects globally once the DNS resolves.

### Render (Backend Domain)
If you wish to map a custom API subdomain (e.g., `api.ilmora.com`):
1. In the Render service, go to **Settings** > **Custom Domains**.
2. Enter `api.ilmora.com`.
3. Set the **CNAME Record** on your DNS provider pointing to Render's target domain (e.g., `ilmora-backend.onrender.com`).
4. Render automatically manages the Let's Encrypt SSL certificate and HTTPS encryption.

---

## 6. Google Search Console Verification

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

## 7. Complete Production Environment Checklist

Before declaring the deployment live, verify the following:

- [ ] **Secure Variables**: No passwords, private keys, or API tokens are checked into git. `.env` and local secrets are added to `.gitignore`.
- [ ] **Prod Database**: Supabase connection string uses the connection pooler (port 6543) and is running on a transaction pool mode.
- [ ] **Production CORS**: `BACKEND_CORS_ORIGINS` in Render environment settings lists only the secure production domains.
- [ ] **Auth Domains**: Localhost is deactivated or restricted from Firebase Authentication domains in production console settings.
- [ ] **Health Endpoint**: Render service shows green and the `/health` endpoint is actively monitored.
- [ ] **HTTPS Enforced**: Both frontend and backend requests redirect all HTTP traffic to HTTPS securely.
- [ ] **Zero Dev Simulation**: The browser local storage contains no `sim_token` or dev flags, forcing standard Firebase login flows.
