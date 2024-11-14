from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

client = OpenAI()

def fetch_webpage_text(url):
    """Fetches and extracts text content from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return ' '.join([p.get_text() for p in soup.find_all('p')])
    except requests.RequestException as e:
        return str(e)

def check_compliance(page_text, policy_text):
    prompt = (
        "Use clear examples to help guide your analysis.\n\n"
        "### Compliance Policy:\n"
        f"{policy_text}\n\n"
        "### Webpage Content:\n"
        f"{page_text}\n\n"
        "### Instructions and Examples:\n"
        "1. Carefully read each statement in the Webpage Content.\n"
        "2. For any statement that appears non-compliant, include:\n"
        "   - The original statement.\n"
        "   - The specific policy rule or guideline it violates.\n"
        "   - An explanation of why it violates the policy.\n\n"
        "#### Example Finding:\n"
        "- Statement: 'This service guarantees 100% uptime.'\n"
        "- Policy Violation: Compliance Policy, Section 2 (Advertising Accuracy)\n"
        "- Explanation: The policy prohibits absolute guarantees, as they can be misleading.\n\n"
        "If not even a single non-compliance is found, then only respond with 'All content is compliant.'"
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "As a compliance-checking assistant, your job is to identify any content on a webpage that violates the compliance policy provided."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            temperature=0.7,
            seed=421
        )
        findings = response.choices[0].message.content.strip().split("\n")
        return findings
    except Exception as e:
        return [f"An error occurred: {str(e)}"]

@app.route('/check_compliance', methods=['POST'])
def check_compliance_endpoint():
    data = request.json
    page_url = data.get("page_url")
    policy_url = data.get("policy_url")
    if not page_url or not policy_url:
        return jsonify({"error": "Both page_url and policy_url are required"}), 400

    page_text = fetch_webpage_text(page_url)
    policy_text = fetch_webpage_text(policy_url)

    if "Error" in page_text or "Error" in policy_text:
        return jsonify({"error": "Failed to fetch webpage or policy text"}), 500

    findings = check_compliance(page_text, policy_text)

    if "An error occurred" in findings[0]:
        return jsonify({"error": findings[0]}), 500

    return jsonify({"non_compliant_findings": findings})

if __name__ == '__main__':
    app.run(debug=True)