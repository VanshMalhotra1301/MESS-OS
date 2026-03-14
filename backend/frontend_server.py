import os
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# --- CONFIGURATION ---
# We assume your HTML files are located in the 'frontend' folder based on your image
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# --- CREDENTIALS ---
USERS = {
    "mess_admin": {
        "email": "admin@bennett.edu.in",
        "password": "admin123", # Password for Mess Admin
        "redirect": "/admin/dashboard"
    },
    "ngo_admin": {
        "email": "ngo@feedingindia.org",
        "password": "ngo123",   # Password for NGO Admin
        "redirect": "/ngo/dashboard"
    }
}

# --- ROUTES ---

@app.get("/")
async def login_page():
    """Serves the Login Page"""
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))

@app.post("/login")
async def perform_login(email: str = Form(...), password: str = Form(...)):
    """Handles Login Logic"""
    
    # Check Mess Admin
    if email == USERS["mess_admin"]["email"] and password == USERS["mess_admin"]["password"]:
        return RedirectResponse(url=USERS["mess_admin"]["redirect"], status_code=303)
    
    # Check NGO Admin
    elif email == USERS["ngo_admin"]["email"] and password == USERS["ngo_admin"]["password"]:
        return RedirectResponse(url=USERS["ngo_admin"]["redirect"], status_code=303)
    
    # Invalid Credentials -> Redirect back to login
    else:
        return RedirectResponse(url="/?error=invalid_credentials", status_code=303)

@app.get("/admin/dashboard")
async def get_admin_dashboard():
    """Serves the Mess Admin Dashboard"""
    return FileResponse(os.path.join(FRONTEND_DIR, "admin_dashboard.html"))

@app.get("/ngo/dashboard")
async def get_ngo_dashboard():
    """Serves the NGO Admin Dashboard"""
    return FileResponse(os.path.join(FRONTEND_DIR, "ngo_dashboard.html"))

# --- RUN SERVER ---
if __name__ == "__main__":
    print("🚀 Frontend Server Running at http://127.0.0.1:8000")
    print(f"👉 Mess Admin Login: {USERS['mess_admin']['email']} / {USERS['mess_admin']['password']}")
    print(f"👉 NGO Admin Login:  {USERS['ngo_admin']['email']} / {USERS['ngo_admin']['password']}")
    uvicorn.run(app, host="127.0.0.1", port=8000)