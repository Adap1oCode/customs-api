def get_data():
    import requests
    from base64 import b64encode
    from base64 import b64encode
    import xml.etree.ElementTree as ET
    import re
    # OAuth2 client credentials
    client_id = '8Qi98qGZqFS5cdaH6kgX0r6XWRBg'
    client_secret = '32caa4ed-79d7-420f-89d6-636932c91d98'

    # Base URL for HMRC API
    base_url = 'https://test-api.service.hmrc.gov.uk/'

    # Token URL
    token_url = base_url + 'oauth/token'

    # API endpoint
    url = base_url + 'notifications/unpulled'

    # Construct the Authorization header with HTTP Basic Authentication
    auth_header = {
        'Authorization': 'Basic ' + b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }

    # Fetch the access token
    token_response = requests.post(token_url, headers=auth_header, data={'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret})

    # Extract access token from response
    access_token = token_response.json().get('access_token')

    # Make a GET request to the API endpoint with the access token
    if access_token:
        response = requests.get(url, headers={'Authorization': 'Bearer ' + access_token,'Accept':'application/vnd.hmrc.1.0+xml'})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            root = ET.fromstring(response.text)

            # Get all href attributes from links within resource
            href_list = [link.attrib['href'] for link in root.findall('.//link')]
            
            for href in href_list:
                href_replaced = href.replace('/notifications/unpulled/', '')
                print(href_replaced)
                print(response.text)
        else:
            print(f"API call failed with status code {response.status_code}")
            print("Response:")
            print(response.text)  # Print the response content for further investigation
    else:
        print("Access token retrieval failed. No access token received.")
        