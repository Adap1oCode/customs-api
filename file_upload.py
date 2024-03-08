def get_data():
    from requests_oauthlib import OAuth2Session
    from oauthlib.oauth2 import BackendApplicationClient
    import requests

    import os 
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    my_client_id  = '8Qi98qGZqFS5cdaH6kgX0r6XWRBg'
    client_secret = '32caa4ed-79d7-420f-89d6-636932c91d98'

    base_url = 'https://test-api.service.hmrc.gov.uk/'

    authorization_url = 'https://test-api.service.hmrc.gov.uk/oauth/authorize'
    _token_url = 'https://test-api.service.hmrc.gov.uk/oauth/token'

    redirect_uri = 'https://d1.adaplo.io/web'

    scope = ['write:customs-declaration']

    oauth = OAuth2Session(client_id=my_client_id, scope=scope, redirect_uri=redirect_uri)

    # Redirect user to HMRC's authorization server for user authentication and authorization
    authorization_url, state = oauth.authorization_url(authorization_url)



    # Print the authorization URL and prompt the user to visit it in their browser
    print('Please go to %s and authorize access.' % authorization_url)

    # After user authorization, HMRC will redirect back to your application's redirect URI
    # with an authorization code as a query parameter

    # Extract the authorization code from the redirect URI
    authorization_response = input('Enter the full callback URL: ')

    from urllib.parse import urlparse, parse_qs

    # Parse the authorization response URL
    parsed_url = urlparse(authorization_response)

    # Extract the query parameters
    query_params = parse_qs(parsed_url.query)

    # Extract the authorization code and state from the query parameters
    authorization_code = query_params.get('code', [None])[0]
    state = query_params.get('state', [None])[0]

    if authorization_code and state:
        # If both authorization code and state are present, use them to fetch the token
        token = oauth.fetch_token(token_url=_token_url, authorization_response=authorization_response, client_id=my_client_id, client_secret=client_secret,include_client_id=True)
        
        access_token = token['access_token']
        print(f"\n{token}\n")
    else:
        print("Missing authorization code or state in the response URL.")
        
    # API endpoint for customs declarations
    url = base_url + 'customs/declarations/file-upload'

    request_body = """
    <FileUploadRequest xmlns="hmrc:fileupload" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <DeclarationID>DEC123</DeclarationID>
    <FileGroupSize>2</FileGroupSize>
    <Files>
    <File>
        <FileSequenceNo>1</FileSequenceNo>
        <DocumentType>Certificate of Origin</DocumentType>
        <SuccessRedirect>https://success-redirect.com</SuccessRedirect>
        <ErrorRedirect>https://error-redirect.com</ErrorRedirect>
    </File>
    <File>
        <FileSequenceNo>2</FileSequenceNo>
        <DocumentType>Licence</DocumentType>
    </File>
    </Files>
    </FileUploadRequest>


    """

    # Define header parameters including the access token
    headers = {
        'Accept': 'application/vnd.hmrc.2.0+xml',
        'Content-Type': 'application/xml; charset=UTF-8',
        #'X-Badge-Identifier': 'ABC123',  # Replace with your badge identifier
        'X-Eori-Identifier': 'GB450948607016',  # Replace with your submitter identifier
        'Authorization': 'Bearer ' + access_token  # Use the obtained access token
    }


    response = requests.post(url, headers=headers,data=request_body)

    if response.status_code == 200:
        print("Declaration submission successful!")
        print("Response:")
        print(response.text)  
    else:
        print(f"Declaration submission failed with status code {response.status_code}")
        print("Response:")
        print(response.text)  # Print the response content for further investigation
        
        print("Error details:")
        print(response.headers)  # Print response headers
