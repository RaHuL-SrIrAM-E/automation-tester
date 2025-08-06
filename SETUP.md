# Setup Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd automation-tester
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

## Gemini API Setup

To use the LLM-powered conversion feature, you need a Gemini API key:

1. **Get a Gemini API key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated API key

2. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```

   **Note:** Replace `your_actual_api_key_here` with your actual Gemini API key.

## Running the Application

1. **Start the server:**
   ```bash
   python3 app.py
   ```
   
   The server will start on `http://localhost:5001`

2. **Test the API:**
   ```bash
   python3 test_api.py
   ```

## API Endpoints

- **Health Check:** `GET http://localhost:5001/health`
- **Convert Collection:** `POST http://localhost:5001/convert`

## Usage Examples

### Convert a Postman collection file:
```bash
curl -X POST -F "file=@your-collection.json" http://localhost:5001/convert -o karate-suite.zip
```

### Convert with JSON data:
```bash
curl -X POST -H "Content-Type: application/json" -d @your-collection.json http://localhost:5001/convert -o karate-suite.zip
```

## Fallback Mode

If you don't set up the Gemini API key, the application will run in fallback mode and generate basic Karate test files without LLM enhancement.

## Troubleshooting

### Port 5000 already in use
On macOS, port 5000 is often used by AirPlay. The application is configured to use port 5001 by default.

### SSL Warnings
You may see SSL warnings related to LibreSSL. These are warnings and don't affect functionality.

### API Key Issues
If you see "GEMINI_API_KEY is required" errors, make sure your `.env` file is in the project root and contains the correct API key. 