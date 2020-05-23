#!/usr/bin/env python
import wiotp.sdk.application
myConfig = {
    "auth": {
        "key": "a-209kxe-4ezhm1f9dv",
        "token": "kQW!(tzSoo(cG+&Jgb"
    }
}
client = wiotp.sdk.application.ApplicationClient(config=myConfig)
serviceBinding = {
    "name": "cloudant_binding_service",
    "description": "",
    "type": "cloudant",
    "credentials": {
  "apikey": "lFO6j_KYUMk_ngYuSgOkkzx_1GKI8mfLky3te5kuovLJ",
  "host": "359a45c8-b6b2-4ae4-9131-a0c4bca6883f-bluemix.cloudantnosqldb.appdomain.cloud",
  "iam_apikey_description": "Auto-generated for key b2150be0-27c2-4a42-b42c-146864e011bd",
  "iam_apikey_name": "authent",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/727ba2cf3b164e39a4661655f216e743::serviceid:ServiceId-b779b6ac-32e8-4fe4-aab0-0e49fc27d158",
  "password": "e4c5e82781526f6eda3826d9d044d2961da4d1989b41b560a26ddbb9aae0d29f",
  "port": 443,
  "url": "https://359a45c8-b6b2-4ae4-9131-a0c4bca6883f-bluemix:e4c5e82781526f6eda3826d9d044d2961da4d1989b41b560a26ddbb9aae0d29f@359a45c8-b6b2-4ae4-9131-a0c4bca6883f-bluemix.cloudantnosqldb.appdomain.cloud",
  "username": "359a45c8-b6b2-4ae4-9131-a0c4bca6883f-bluemix"
}
}
cloudantService = client.serviceBindings.create(serviceBinding)
# Create the connector
connector = client.dsc.create(
    name="connector1", serviceId=cloudantService.id, type='cloudant', timezone="UTC", description="A test connector", enabled=True
)
# Create a destination under the connector
destination1 = connector.destinations.create(name="all-data", bucketInterval="DAY")
# Create a rule under the connector, that routes all events to the destination
rule1 = connector.rules.createEventRule(
    name="allevents", destinationName=destination1.name, description="Send all events", enabled=True, typeId="*", eventId="*"
)
# Create a second rule under the connector, that routes all state to the same destination
rule2 = connector.rules.createStateRule(
    name="allstate", destinationName=destination1.name, description="Send all state", enabled=True, logicalInterfaceId="*"
)
