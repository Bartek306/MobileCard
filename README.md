# MobileCard 
Generate vcard, scraping panoramafirm.pl search result.

## Structure of vcard
### name
name of service provider
### address
address of service provider
### phone
phone number of service provider


## Resource URL
http://127.0.0.1:8000

## Endpoints:
/vcard

#/vcard
Return generated html code
#### Response format: html code
#### Request parameters
location(required) - location where we want find service
service(required) - type of service 
#### Example of request
{
    "service": "hydraulik",
    "location": "Warszawa"
}
