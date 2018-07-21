## Introduction
This is a RESTful API build with `python flask`, `mysql`, `docker-compose`, based on the requirements 
[here](https://github.com/lalamove/challenge-2018/blob/master/backend.md)

## How To Run The Project
1. navigate to top level folder and run `start.sh`, the `start.sh` will build the docker containers, `tech_challenge` , and `mysql` respectively.

2. The app is listening on port `8080`, you can make a call such as 
`localhost:8080/order`

## Api interface example

#### Place order

  - Method: `POST`
  - URL path: `/order`
  - Request body:

    ```
    {
        "origin": ["START_LATITUDE", "START_LONGTITUDE"],
        "destination": ["END_LATITUDE", "END_LONGTITUDE"]
    }
    ```
  - Sample Curl:

    ```
        curl -X POST \
        http://localhost:8080/order \
        -H 'Cache-Control: no-cache' \
        -H 'Content-Type: application/json'
        -d '{
            "origin": [32.048104, -116.543285],
            "destination": [45.264057, -122.763736]
        }
        '
    ```

  - Response:

    Header: `HTTP 200`
    Body:
      ```
      {
          "id": <order_id>,
          "distance": <total_distance>,
          "status": "UNASSIGN"
      }
      ```
    or 
    
    Header: `HTTP 500`
    Body:
      ```json
      {
          "error": "ERROR_DESCRIPTION"
      }
      ```

#### Take order

  - Method: `PUT`
  - URL path: `/order/:id`
  - Request body:
    ```
    {
        "status":"taken"
    }
    ```
  - Sample Curl:

    ```
    curl -X PUT \
    http://localhost:8080/order/2 \
    -H 'Cache-Control: no-cache' \
    -H 'Content-Type: application/json'
    -d '{
        "status":"taken"
    }'
    ```

  - Response:
    Header: `HTTP 200`
    Body:
      ```
      {
          "status": "SUCCESS"
      }
      ```
    or
    
    Header: `HTTP 409`
    Body:
      ```
      {
          "error": "ORDER_ALREADY_BEEN_TAKEN"
      }
      ```

#### Order list

  - Method: `GET`
  - Url path: `/orders?page=:page&limit=:limit`
  - Response:

    ```
    [
        {
            "id": <order_id>,
            "distance": <total_distance>,
            "status": <ORDER_STATUS>
        },
        ...
    ]
    ```

  - Sample Curl:

    ```
        curl -X GET \
        'http://localhost:8080/orders?page=1&limit=3' \
        -H 'Cache-Control: no-cache'
    ```


### If More Time To Do List
- Need another table for storing who is taking the order.
- Need table for the different statuses, currently stored as varchar
- Prevent sql injection by using SQLAlchemy
- Some unit test with mocked databases
 

