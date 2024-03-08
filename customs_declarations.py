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
    url = base_url + 'customs/declarations/amend'

    # Define header parameters including the access token
    headers = {
        'Accept': 'application/vnd.hmrc.2.0+xml',
        'Content-Type': 'application/xml; charset=UTF-8',
        #'X-Badge-Identifier': 'ABC123',  # Replace with your badge identifier
        'X-Submitter-Identifier': 'GB450948607016',  # Replace with your submitter identifier
        'Authorization': 'Bearer ' + access_token  # Use the obtained access token
    }
    print(headers)

    # Define request body (as an example XML)
    request_body = """
    <md:MetaData xmlns="urn:wco:datamodel:WCO:DEC-DMS:2"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:clm63055="urn:un:unece:uncefact:codelist:standard:UNECE:AgencyIdentificationCode:D12B"
                xmlns:ds="urn:wco:datamodel:WCO:MetaData_DS-DMS:2"
                xmlns:md="urn:wco:datamodel:WCO:DocumentMetaData-DMS:2"
                xsi:schemaLocation="urn:wco:datamodel:WCO:DocumentMetaData-DMS:2 ../DocumentMetaData_2_DMS.xsd ">
        <md:WCODataModelVersionCode>3.6</md:WCODataModelVersionCode>
        <md:WCOTypeName>DEC</md:WCOTypeName>
        <md:ResponsibleCountryCode>GB</md:ResponsibleCountryCode>
        <md:ResponsibleAgencyName>HMRC</md:ResponsibleAgencyName>
        <md:AgencyAssignedCustomizationVersionCode>v2.1</md:AgencyAssignedCustomizationVersionCode>
        <Declaration xmlns="urn:wco:datamodel:WCO:DEC-DMS:2"
                    xmlns:clm5ISO42173A="urn:un:unece:uncefact:codelist:standard:ISO:ISO3AlphaCurrencyCode:2012-08-31"
                    xmlns:clm63055="urn:un:unece:uncefact:codelist:standard:UNECE:AgencyIdentificationCode:D12B"
                    xmlns:p1="urn:wco:datamodel:WCO:Declaration_DS:DMS:2"
                    xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:6"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="urn:wco:datamodel:WCO:DEC-DMS:2 ../WCO_DEC_2_DMS.xsd ">
            
            <!--
                SCENARIO
                A trader submits an Exports Type J (C21E) declaration, exporting goods from GB to ROW.

                The trader enters the following information on the declaration:
                -Procedure Code '0014' at item level in DE 1/10
                -Additional Procedure Code '19Z' at item level in DE 1/11
                -Additional Information Code 'FZPER' in DE 2/2.
                
                An EAL and EDL are submitted to arrive and then depart the goods at DUCR level. 
            -->
            <FunctionCode>9</FunctionCode>
            <!--DE 2/5: LRN. 
                The trader assigned reference to the declaration. -->
            <FunctionalReferenceID>New_Consgn_030823</FunctionalReferenceID>
            <!-- The IssueDateTime element is not required for any declarations. This was included for internal testing.-->
            <!-- <IssueDateTime>
                <p1:DateTimeString formatCode="304">20220608125200+01</p1:DateTimeString>
            </IssueDateTime> -->
            <!--DE 1/1: Declaration Type.
                EX to represent an Export declaration. -->
            <!--DE 1/2: Additional Declaration Type.
                K to represent a Pre lodged declaration. -->
            <TypeCode>EXJ</TypeCode>
            <!--DE 1/9: Total Number of Items.
                Total number of goods items on the declaration. -->
            <GoodsItemQuantity>1</GoodsItemQuantity>
            <DeclarationOfficeID>GBLBA001</DeclarationOfficeID>
            <!--DE 3/20: Representative Identification Number.
                EORI number of the Representative.
                DE 3/21: Representative Status Code.
                '2' Indicating direct representation. -->
            <Agent>
                <ID>GB150454489082</ID>
                <FunctionCode>2</FunctionCode>
            </Agent>
            <AuthorisationHolder>
                <ID>GB150454489082</ID>
                <CategoryCode>FZ</CategoryCode>
            </AuthorisationHolder>
            <!--DE 7/4: 4 Mode of Transport at the Border.
                Code 4 indicating that the mode of transport used to arrive at the UK external border is by Air Transport. -->
            <BorderTransportMeans>
                <ModeCode>4</ModeCode>
            </BorderTransportMeans>
            <Consignment>
                <Consignor>
                <!--DE 3/7: Consignor Name and Address. -->
                    <Name>Mr.ConsignorKR00400</Name>
                    <Address>
                        <CityName>Compact City</CityName>
                        <CountryCode>KR</CountryCode>
                        <Line>Seoul</Line>
                        <PostcodeID>145-2345</PostcodeID>
                    </Address>
                </Consignor>
            </Consignment>
            <!--DE 3/18: Declarant Identification Number.
                EORI number of the Declarant. -->
            <Declarant>
                <ID>GB150454489082</ID>
            </Declarant>
            <!-- 5/12: 'GB000085' Code indicating Gatwick. -->
            <ExitOffice>
                <ID>GB000085</ID>
            </ExitOffice>
            <!--DE 3/2: Exporter Identification Number. 
                EORI number of the Exporter. -->
            <Exporter>
                <ID>GB427168118378</ID>
            </Exporter>
            <GoodsShipment>
                <!--DE 3/9: Consignee Name and Address. -->
                <Consignee>
                    <Name>Mr Consignee</Name>
                    <Address>
                        <CityName>Ota City</CityName>
                        <CountryCode>JP</CountryCode>
                        <Line>Tokyo</Line>
                        <PostcodeID>144-0041</PostcodeID>
                    </Address>
                </Consignee>
                <Consignment>
                    <!--DE 7/2: Container.
                        '0' Indicating goods not arriving in container. -->
                    <ContainerCode>0</ContainerCode>
                    <!--DE 7/7: Identity of the means of transport at departure. 
                        Type 40 to indicate an IATA flight number. -->
                    <DepartureTransportMeans>
                        <ID>98765</ID>
                        <IdentificationTypeCode>40</IdentificationTypeCode>
                    </DepartureTransportMeans>
                    <GoodsLocation>
                        <!--DE 5/23: Location of Goods - Identification of location. 
                            ID to give a unique position of the location. 
                            LGWLGWLGW - Indicating London Gatwick Airport. -->
                        <Name>LGWLGWLGW</Name>
                        <!--DE 5/23: Location of Goods - Type of location. 
                            A in this scenario to represent that it is a designated location. -->
                        <TypeCode>A</TypeCode>
                        <Address>
                            <!--DE 5/23: Location of Goods - Qualifier of the identification. 
                                Type of ID of the Location - U in this scenario for UN/LOCODE. -->
                            <TypeCode>U</TypeCode>
                            <!--DE 5/23: Location of Goods - Country. 
                                'GB' Country code of the country where the goods may be examined, GB in this scenario. -->
                            <CountryCode>GB</CountryCode>
                        </Address>
                    </GoodsLocation>
                </Consignment>
                <!--DE 5/8: Country of Destination Code.
                    JP Indicating Japan. -->
                <Destination>
                    <CountryCode>JP</CountryCode>
                </Destination>
                <GovernmentAgencyGoodsItem>
                    <!--DE 1/6: Goods Item Number.
                        Sequential number of the goods item. -->
                    <SequenceNumeric>1</SequenceNumeric>
                    <!--DE 2/3: Documents produced, certificates and authorisations, additional references.
                        Document code C600 for authorisation to operate a Free Zone. -->
                    <AdditionalDocument>
                        <CategoryCode>C</CategoryCode>
                        <ID>GBFZ42716811837820220201100011</ID>
                        <TypeCode>600</TypeCode>
                    </AdditionalDocument>
                    <!--DE 2/2: Additional Information.
                        Statement code '00400' to indicate the Exporter. -->
                    <AdditionalInformation>
                        <StatementCode>00400</StatementCode>
                        <StatementDescription>Exporter</StatementDescription>
                    </AdditionalInformation>
                    <!--DE 2/2: Additional Information.
                        Statement code 'FZPER' to indicate the number of days the goods have been held in the Free Zone. -->
                    <AdditionalInformation>
                        <StatementCode>FZPER</StatementCode>
                        <StatementDescription>12 days</StatementDescription>
                    </AdditionalInformation>
                    <Commodity>
                        <!--DE 6/8: Description of Goods.
                            Description specific enough to enable classification - without repeating the CN code description in the Tariff for this scenario. -->
                        <Description>Paper Envelopes</Description>
                    </Commodity>
                    <!--DE 1/10: Procedure.
                        0014 to indicate the goods are being removed from a Temporary Storage or Free Zone, where they are re-exported direct from the UK. -->
                    <GovernmentProcedure>
                        <CurrentCode>00</CurrentCode>
                        <PreviousCode>14</PreviousCode>
                    </GovernmentProcedure>
                    <!--DE 1/11: Additional Procedure Code. 
                        19Z to indicate the goods are being entered to or removed from a Free Port/Free Zone using a C21 Customs Clearance Request.
                        When used on export declarations, the additional information code FZPER must also be declared. -->
                    <GovernmentProcedure>
                        <CurrentCode>19Z</CurrentCode>
                    </GovernmentProcedure>
                    <!--DE 6/10: Number of Packages. 
                        In this case 1. -->
                    <Packaging>
                        <SequenceNumeric>1</SequenceNumeric>
                        <MarksNumbersID>2379261ETT</MarksNumbersID>
                        <QuantityQuantity>1</QuantityQuantity>
                        <TypeCode>PK</TypeCode>
                    </Packaging>
                </GovernmentAgencyGoodsItem>
                <!--DE 2/1: Simplified Declaration/ Previous Documents.
                    Previous document to show the DUCR assigned to the consignment.
                    This is a mandatory field. -->
                <PreviousDocument>
                    <CategoryCode>Z</CategoryCode>
                    <ID>3GB427168118378-0308A2</ID>
                    <TypeCode>DCR</TypeCode>
                </PreviousDocument>
            </GoodsShipment>
        </Declaration>
    </md:MetaData>
    """
    # Make the POST request with headers and request body
    response = requests.post(url, headers=headers, data=request_body)

    if response.status_code == 202:
        print("Declaration submission successful!")
        print("Response:")
        print(response.text)  
    else:
        print(f"Declaration submission failed with status code {response.status_code}")
        print("Response:")
        print(response.text)  # Print the response content for further investigation
        
        print("Error details:")
        print(response.headers)  # Print response headers
