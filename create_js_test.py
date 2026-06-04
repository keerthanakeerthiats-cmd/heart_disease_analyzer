"""
JavaScript Error Checker - Creates a test HTML file to verify JavaScript functionality
"""

test_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JavaScript Error Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .test-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; }
        .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #0056b3; }
        #result { margin-top: 20px; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>JavaScript Error Test</h1>
    
    <div class="test-container">
        <h2>Test 1: Basic Object Handling</h2>
        <button onclick="testObjectHandling()">Run Test</button>
        <div id="test1-result"></div>
    </div>
    
    <div class="test-container">
        <h2>Test 2: Object.entries() Function</h2>
        <button onclick="testObjectEntries()">Run Test</button>
        <div id="test2-result"></div>
    </div>
    
    <div class="test-container">
        <h2>Test 3: JSON Parsing</h2>
        <button onclick="testJsonParsing()">Run Test</button>
        <div id="test3-result"></div>
    </div>
    
    <div class="test-container">
        <h2>Test 4: Fetch API</h2>
        <button onclick="testFetchApi()">Run Test</button>
        <div id="test4-result"></div>
    </div>

    <script>
        function displayResult(testId, success, message) {
            const resultDiv = document.getElementById(testId + '-result');
            resultDiv.className = success ? 'success' : 'error';
            resultDiv.innerHTML = success ? '✅ PASS: ' + message : '❌ FAIL: ' + message;
        }
        
        function testObjectHandling() {
            try {
                // Test with valid object
                const validData = {
                    prediction: 'Normal',
                    confidence: 95.5,
                    probabilities: {
                        'Normal': 95.5,
                        'Abnormal': 4.5
                    }
                };
                
                // Test the problematic code
                if (!validData || typeof validData !== 'object') {
                    throw new Error('Data validation failed');
                }
                
                const prediction = validData.prediction || 'Unknown';
                const confidence = validData.confidence || 0;
                const probabilities = validData.probabilities || {};
                
                if (probabilities && typeof probabilities === 'object' && Object.keys(probabilities).length > 0) {
                    const sortedProbs = Object.entries(probabilities).sort((a, b) => b[1] - a[1]);
                    displayResult('test1', true, `Object handling works correctly. Prediction: ${prediction}, Confidence: ${confidence}%, Probabilities: ${sortedProbs.length}`);
                } else {
                    displayResult('test1', true, `Object handling works. No probabilities data.`);
                }
            } catch (error) {
                displayResult('test1', false, `Error: ${error.message}`);
            }
        }
        
        function testObjectEntries() {
            try {
                const testData = {
                    'Normal': 95.5,
                    'Abnormal': 4.5
                };
                
                const sortedProbs = Object.entries(testData).sort((a, b) => b[1] - a[1]);
                displayResult('test2', true, `Object.entries() works correctly. Sorted: ${JSON.stringify(sortedProbs)}`);
            } catch (error) {
                displayResult('test2', false, `Error: ${error.message}`);
            }
        }
        
        function testJsonParsing() {
            try {
                const jsonString = '{"prediction": "Normal", "confidence": 95.5}';
                const parsed = JSON.parse(jsonString);
                displayResult('test3', true, `JSON parsing works. Parsed: ${parsed.prediction} (${parsed.confidence}%)`);
            } catch (error) {
                displayResult('test3', false, `Error: ${error.message}`);
            }
        }
        
        function testFetchApi() {
            try {
                // Check if fetch is available
                if (typeof fetch === 'function') {
                    displayResult('test4', true, 'Fetch API is available');
                } else {
                    displayResult('test4', false, 'Fetch API is not available');
                }
            } catch (error) {
                displayResult('test4', false, `Error: ${error.message}`);
            }
        }
        
        // Run all tests automatically when page loads
        window.addEventListener('load', function() {
            setTimeout(() => {
                testObjectHandling();
                testObjectEntries();
                testJsonParsing();
                testFetchApi();
            }, 1000);
        });
    </script>
</body>
</html>
"""

# Write the test file
with open("js_error_test.html", "w") as f:
    f.write(test_html)

print("JavaScript Error Test file created successfully!")
print("Open js_error_test.html in your browser to run the tests.")