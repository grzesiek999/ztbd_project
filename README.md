# ztbd_project

## 1) Setup
### MongoDB
1. Run docker-compose up
2. Run in terminal
<br>a) Enter mongosh:
    ```
    docker exec -it [CONTAINER_ID] mongosh
    ```
    c) Set profiler:<br>
    ```
    use admin
    ```
    ```
    db.auth("[username]", "[password]")
    ```
    ```
    use [db_name]
    ```
    ```
    db.setProfilingLevel(1, { slowms: 0, filter: { "command.comment": "backend_query" } })
    ```
   
### 2) Run Docker
1. Run docker-compose up<br>
   a) Development:
   ```
   docker-compose up -d mongo postgres fastapi_dev
   ```
   b) Production:
   ```
   docker-compose up -d mongo postgres fastapi
   ```