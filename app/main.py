from fastapi import FastAPI
from routes import auth, products, cart, orders, address, admin
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ecommerce API", 
    version="1.0.0",
    description="A complete ecommerce API with orders and addresses"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(address.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Ecommerce API", 
        "docs": "/docs",
        "features": [
            "Phone authentication", 
            "Product management", 
            "Shopping cart",
            "Order management",
            "Address management"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ecommerce-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)