from app import create_app

# Create the Flask app instance
app = create_app()

if __name__ == "__main__":
    # Run the app on port 800 and bind to all interfaces
    app.run(debug=True, host='0.0.0.0', port=8000)
