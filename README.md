## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/nerf2op/sei-ai-take-home-assigment.git
```
### 2. Create Virtual Environment
```
cd sei-ai-take-home-assigment
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
### 3. Install Required Libraries
```
pip install -r requirements.txt
```
### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following environment variables:
```
OPENAI_API_KEY=your_openai_api_key_here
```
## Usage
### 1. Running the Application
```
python app.py  
```
## API Endpoint
**Endpoint:** `/check_compliance`  
**Method:** `POST`  
**Content-Type:** `application/json`
**Request Body:**
```json
{
    "page_url": "https://example.com/webpage",
    "policy_url": "https://example.com/compliance-policy"
}
```
**Response:**
```json
{
    "non_compliant_findings": [
        "Violation details...",
        "Policy non-compliance..."
    ]
}
```


