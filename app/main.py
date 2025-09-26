from fastapi import FastAPI
from .routers import auth, users, expenses, categories, reports

app = FastAPI(title="Expense Tracker API", version="0.1.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"]) 
app.include_router(users.router, prefix="/users", tags=["users"]) 
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"]) 
app.include_router(categories.router, prefix="/categories", tags=["categories"]) 
app.include_router(reports.router, prefix="/reports", tags=["reports"]) 


@app.get("/")
def root():
    return {"status": "ok", "service": "expense-tracker-api"}
