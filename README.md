# Postman to Karate Test Suite Converter

A Flask API that converts Postman collections into Apache Karate test suites using Google's Gemini LLM.

## Features

- Accepts Postman collection JSON files
- Uses Gemini LLM to generate Karate test files
- Creates complete test suite with:
  - Feature files (`.feature`)
  - Karate configuration (`karate-config.js`)
  - Test runner (Java)
  - Supporting files
- Returns a downloadable ZIP file

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Gemini API:**
   - Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

3. **Run the application:**
   ```bash
   python app.py
   ```

## API Endpoints

### Health Check
```
GET /health
```
Returns the health status of the service.

### Convert Postman Collection
```
POST /convert
```
Converts a Postman collection to Karate test suite.

**Request:**
- Send a Postman collection JSON file in the request body
- Or send JSON data directly in the request body

**Response:**
- Returns a ZIP file containing the generated Karate test suite

## Usage Examples

### Using curl with file upload:
```bash
curl -X POST -F "file=@your-postman-collection.json" http://localhost:5001/convert -o karate-test-suite.zip
```

### Using curl with JSON data:
```bash
curl -X POST -H "Content-Type: application/json" -d @your-postman-collection.json http://localhost:5001/convert -o karate-test-suite.zip
```

## Project Structure

```
automation-tester/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .env               # Environment variables (create this)
```

## TODO

- [ ] Integrate Gemini LLM for intelligent test generation
- [ ] Add more comprehensive Postman collection parsing
- [ ] Implement better error handling and validation
- [ ] Add support for environment variables from Postman
- [ ] Create a simple web UI
- [ ] Add unit tests 