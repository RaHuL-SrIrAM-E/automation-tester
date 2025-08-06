#!/usr/bin/env python3
"""
Test script for the Postman to Karate converter API
"""

import requests
import json
import os

# Sample Postman collection for testing
SAMPLE_POSTMAN_COLLECTION = {
    "info": {
        "name": "Sample API Collection",
        "description": "A sample collection for testing the converter",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Get Users",
            "request": {
                "method": "GET",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "url": {
                    "raw": "{{baseUrl}}/api/users",
                    "host": ["{{baseUrl}}"],
                    "path": ["api", "users"]
                },
                "description": "Get all users"
            },
            "response": []
        },
        {
            "name": "Create User",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n  \"name\": \"John Doe\",\n  \"email\": \"john@example.com\"\n}"
                },
                "url": {
                    "raw": "{{baseUrl}}/api/users",
                    "host": ["{{baseUrl}}"],
                    "path": ["api", "users"]
                },
                "description": "Create a new user"
            },
            "response": []
        }
    ],
    "variable": [
        {
            "key": "baseUrl",
            "value": "https://jsonplaceholder.typicode.com"
        }
    ]
}

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:5001/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running.")
        return False
    return True

def test_convert_endpoint():
    """Test the convert endpoint with sample data"""
    print("\nTesting convert endpoint...")
    try:
        # Test with JSON data
        response = requests.post(
            "http://localhost:5001/convert",
            json=SAMPLE_POSTMAN_COLLECTION,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Convert endpoint working")
            
            # Save the ZIP file
            filename = "test-karate-suite.zip"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ ZIP file saved as {filename}")
            
            # Check file size
            file_size = os.path.getsize(filename)
            print(f"📦 ZIP file size: {file_size} bytes")
            
        else:
            print(f"❌ Convert endpoint failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"❌ Error testing convert endpoint: {str(e)}")
        return False
    
    return True

def test_file_upload():
    """Test the convert endpoint with file upload"""
    print("\nTesting file upload...")
    try:
        # Create a temporary JSON file
        temp_file = "temp_postman_collection.json"
        with open(temp_file, "w") as f:
            json.dump(SAMPLE_POSTMAN_COLLECTION, f)
        
        # Test file upload
        with open(temp_file, "rb") as f:
            files = {"file": (temp_file, f, "application/json")}
            response = requests.post("http://localhost:5001/convert", files=files)
        
        # Clean up temp file
        os.remove(temp_file)
        
        if response.status_code == 200:
            print("✅ File upload working")
            
            # Save the ZIP file
            filename = "test-karate-suite-upload.zip"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ ZIP file saved as {filename}")
            
        else:
            print(f"❌ File upload failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing file upload: {str(e)}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Postman to Karate Converter API")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("\n❌ Health check failed. Please start the server first.")
        return
    
    # Test convert endpoint with JSON
    test_convert_endpoint()
    
    # Test file upload
    test_file_upload()
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    main() 