from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import tempfile
import zipfile
from datetime import datetime
import logging
from config import Config
from gemini_service import GeminiService

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini service
gemini_service = None
try:
    if Config.GEMINI_API_KEY:
        gemini_service = GeminiService()
        logger.info("Gemini service initialized successfully")
    else:
        logger.warning("GEMINI_API_KEY not found. Running in fallback mode without LLM integration.")
except Exception as e:
    logger.error(f"Failed to initialize Gemini service: {str(e)}")
    logger.warning("Running in fallback mode without LLM integration.")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Postman to Karate converter is running"})

@app.route('/convert', methods=['POST'])
def convert_postman_to_karate():
    """
    Convert Postman collection to Karate test suite
    Expects: JSON file in request body or JSON data directly
    Returns: ZIP file containing Karate test suite
    """
    try:
        # Check if file is uploaded or JSON is sent directly
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400
            
            # Read the uploaded file
            postman_data = json.loads(file.read())
            logger.info(f"Received file: {file.filename}")
        else:
            # Try to get JSON from request body
            postman_data = request.get_json()
            if not postman_data:
                return jsonify({"error": "No JSON data provided"}), 400
            logger.info("Received JSON data directly")

        # Validate that it's a Postman collection
        if not is_valid_postman_collection(postman_data):
            return jsonify({"error": "Invalid Postman collection format"}), 400

        # Process the collection and generate Karate files
        if gemini_service:
            karate_files = gemini_service.generate_karate_test_suite(postman_data)
        else:
            # Fallback to basic generation if Gemini service is not available
            karate_files = process_postman_collection(postman_data)
        
        # Create ZIP file
        zip_path = create_zip_file(karate_files)
        
        # Return the ZIP file
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"karate-test-suite-{datetime.now().strftime('%Y%m%d-%H%M%S')}.zip",
            mimetype='application/zip'
        )

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

def is_valid_postman_collection(data):
    """Validate if the data is a valid Postman collection"""
    try:
        # Basic validation - check for required Postman collection fields
        if not isinstance(data, dict):
            return False
        
        # Check for Postman collection structure
        if 'info' in data and 'item' in data:
            return True
        
        # Alternative: check for Postman collection v2.1 structure
        if 'info' in data and isinstance(data.get('item'), list):
            return True
            
        return False
    except:
        return False

def process_postman_collection(postman_data):
    """
    Process Postman collection and generate Karate files
    This is a placeholder - will be implemented with Gemini LLM integration
    """
    logger.info("Processing Postman collection...")
    
    # Extract collection info
    collection_info = postman_data.get('info', {})
    collection_name = collection_info.get('name', 'postman-collection')
    
    # For now, return a basic structure
    # TODO: Integrate with Gemini LLM to generate actual Karate files
    karate_files = {
        'karate-config.js': generate_karate_config(),
        'TestRunner.java': generate_test_runner(collection_name),
        'features/': {
            'sample.feature': generate_sample_feature()
        }
    }
    
    return karate_files

def generate_karate_config():
    """Generate basic Karate configuration file"""
    return '''function fn() {
    var env = karate.env || 'dev';
    var config = {
        baseUrl: 'http://localhost:8080',
        timeout: 10000
    };
    
    if (env === 'dev') {
        config.baseUrl = 'http://localhost:8080';
    } else if (env === 'staging') {
        config.baseUrl = 'https://staging-api.example.com';
    } else if (env === 'prod') {
        config.baseUrl = 'https://api.example.com';
    }
    
    return config;
}'''

def generate_test_runner(collection_name):
    """Generate Karate test runner Java file"""
    return f'''import com.intuit.karate.junit5.Karate;

public class {collection_name.replace('-', '').replace(' ', '')}TestRunner {{
    
    @Karate.Test
    Karate testAll() {{
        return Karate.run().relativeTo(getClass());
    }}
}}'''

def generate_sample_feature():
    """Generate a sample Karate feature file"""
    return '''Feature: Sample API Test

Background:
    * url baseUrl

Scenario: Sample GET request
    Given path '/api/sample'
    When method GET
    Then status 200
    And match response contains { "message": "success" }'''

def create_zip_file(karate_files):
    """Create a ZIP file containing the Karate test suite"""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, 'karate-test-suite.zip')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path, content in karate_files.items():
            if isinstance(content, dict):
                # Handle directory structure
                for sub_file, sub_content in content.items():
                    full_path = os.path.join(file_path, sub_file)
                    zipf.writestr(full_path, sub_content)
            else:
                # Handle single file
                zipf.writestr(file_path, content)
    
    logger.info(f"Created ZIP file: {zip_path}")
    return zip_path

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 