from api_service import create_api_app

# Create Flask app using app factory
app = create_api_app()

if __name__ == "__main__":
    # Explicit host for CI compatibility
    app.run(host="127.0.0.1", port=5000, debug=True)
