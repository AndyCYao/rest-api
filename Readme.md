## Introduction
This is a RESTful API build with `python flask`, `mysql`, `docker`, based on the requirements 
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


### If More Time To Do List
- Need another table for storing who is taking the order.
- Need table for the different statuses, currently stored as varchar
- Prevent sql injection by using SQLAlchemy
- Some unit test with mocked databases
 

