import google.generativeai as genai
import json
import logging
from config import Config

logger = logging.getLogger(__name__)

class GeminiService:
    """Service class for interacting with Gemini LLM"""
    
    def __init__(self):
        """Initialize Gemini service with API key"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_karate_test_suite(self, postman_collection):
        """
        Generate Karate test suite from Postman collection using Gemini LLM
        
        Args:
            postman_collection (dict): Parsed Postman collection JSON
            
        Returns:
            dict: Generated Karate files with their content
        """
        try:
            # Extract collection information
            collection_info = postman_collection.get('info', {})
            collection_name = collection_info.get('name', 'postman-collection')
            
            # Create prompt for Gemini
            prompt = self._create_generation_prompt(postman_collection)
            
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response and extract generated files
            karate_files = self._parse_gemini_response(response.text, collection_name)
            
            logger.info(f"Successfully generated Karate test suite for collection: {collection_name}")
            return karate_files
            
        except Exception as e:
            logger.error(f"Error generating Karate test suite: {str(e)}")
            raise
    
    def _create_generation_prompt(self, postman_collection):
        """Create a comprehensive prompt for Gemini to generate Karate test suite"""
        
        # Extract key information from Postman collection
        collection_info = postman_collection.get('info', {})
        items = postman_collection.get('item', [])
        
        # Create a summary of the collection
        collection_summary = {
            'name': collection_info.get('name', 'Unknown'),
            'description': collection_info.get('description', ''),
            'requests': []
        }
        
        # Extract request information
        for item in items:
            if 'request' in item:
                request_info = {
                    'name': item.get('name', 'Unknown'),
                    'method': item['request'].get('method', 'GET'),
                    'url': item['request'].get('url', {}),
                    'headers': item['request'].get('header', []),
                    'body': item['request'].get('body', {}),
                    'description': item.get('description', '')
                }
                collection_summary['requests'].append(request_info)
        
        prompt = f"""
You are an expert in Apache Karate testing framework. Your task is to convert a Postman collection into a complete Karate test suite.

Postman Collection Information:
{json.dumps(collection_summary, indent=2)}

Please generate a complete Karate test suite with the following structure:

1. **karate-config.js** - Configuration file with environment-specific settings
2. **TestRunner.java** - Java test runner class
3. **features/** directory containing:
   - Individual .feature files for each request/endpoint
   - Common utilities and shared steps

Requirements:
- Use proper Karate syntax and best practices
- Include appropriate assertions and validations
- Handle different HTTP methods (GET, POST, PUT, DELETE, etc.)
- Include proper error handling
- Use descriptive scenario names
- Add comments for clarity
- Handle request headers and body parameters
- Include response validation where appropriate

Please provide the complete file structure and content for each file. Format your response as a JSON object with the following structure:

{{
    "karate-config.js": "content of config file",
    "TestRunner.java": "content of test runner",
    "features": {{
        "feature1.feature": "content of feature file 1",
        "feature2.feature": "content of feature file 2",
        "common.feature": "content of common utilities"
    }}
}}

Make sure all generated code is syntactically correct and follows Karate conventions.
"""
        
        return prompt
    
    def _parse_gemini_response(self, response_text, collection_name):
        """
        Parse Gemini response and extract generated Karate files
        
        Args:
            response_text (str): Raw response from Gemini
            collection_name (str): Name of the Postman collection
            
        Returns:
            dict: Parsed Karate files
        """
        try:
            # Try to extract JSON from the response
            # Look for JSON block in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                parsed_files = json.loads(json_str)
                
                # Validate the structure
                if not isinstance(parsed_files, dict):
                    raise ValueError("Invalid response structure")
                
                return parsed_files
            else:
                # If no JSON found, create a fallback structure
                logger.warning("Could not parse JSON from Gemini response, using fallback")
                return self._create_fallback_structure(collection_name)
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {str(e)}")
            return self._create_fallback_structure(collection_name)
    
    def _create_fallback_structure(self, collection_name):
        """Create a fallback structure when Gemini response parsing fails"""
        return {
            'karate-config.js': self._generate_fallback_config(),
            'TestRunner.java': self._generate_fallback_runner(collection_name),
            'features': {
                'sample.feature': self._generate_fallback_feature()
            }
        }
    
    def _generate_fallback_config(self):
        """Generate a basic Karate configuration file"""
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
    
    def _generate_fallback_runner(self, collection_name):
        """Generate a basic test runner"""
        class_name = collection_name.replace('-', '').replace(' ', '') + 'TestRunner'
        return f'''import com.intuit.karate.junit5.Karate;

public class {class_name} {{
    
    @Karate.Test
    Karate testAll() {{
        return Karate.run().relativeTo(getClass());
    }}
}}'''
    
    def _generate_fallback_feature(self):
        """Generate a basic feature file"""
        return '''Feature: Sample API Test

Background:
    * url baseUrl

Scenario: Sample GET request
    Given path '/api/sample'
    When method GET
    Then status 200
    And match response contains { "message": "success" }''' 