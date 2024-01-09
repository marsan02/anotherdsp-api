# Flask OpenRTB Bid Response Application

This application is a basic demonstration of handling OpenRTB bid requests and responses using Flask, a lightweight WSGI web application framework in Python. It's designed to provide a simple example of how a Demand-Side Platform (DSP) might interact with bid requests in the OpenRTB format.

## Features

- **Bid Request Handling:** The application listens for POST requests at the `/bid` route, expecting OpenRTB bid request data in JSON format.
- **Bid Calculation Logic:** A `calculate_bid` function is implemented, which is where the logic for calculating the bid price based on the request data should be placed. Currently, it returns a fixed bid price for demonstration purposes.
- **Bid Response Construction:** The application constructs a bid response in the OpenRTB format, echoing back the request ID and including essential details like the bid price, ad markup, and identifiers for reporting.

## Getting Started

To get the application running on your local machine, follow these steps:

### Prerequisites

Ensure you have Python installed on your system. This application was developed using Python 3.8.

### Installation

1. Clone the repository to your local machine.
2. Navigate to the cloned directory.
3. It's recommended to create a virtual environment:

To launch bidbus: python bidbus.py
To test bidbus.py: 
curl -X POST http://localhost:3000/bid -H "Content-Type: application/json" -d @example_request.json | tee response.json
curl http://localhost:5000/campaigns


geolocation dbs available: https://www.maxmind.com/en/accounts/957659/geoip/downloads

bidbus structure:
/DSP
    /bidbus
        __init__.py
        app.py
        routes.py
    /services
        __init__.py
        campaign_selection_service.py
        geoip_service.py
        bid_calculation_service.py
        parse_request_service.py
    /database
        __init__.py
        db.py
    /utils
        __init__.py
        logger.py
    .env
    main.py