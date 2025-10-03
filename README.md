# ztbd_project

Teamwork project for a studies subject Advanced Database Technologies which goal is compare queries times in PostgreSQL vs MongoDB.
## 1) Setup
### MongoDB
1. Run docker-compose up
2. Set profiler:<br>
    a) Enter mongosh:
    ```
    docker exec -it [CONTAINER_ID] mongosh
    ```
    b) Set profiler:<br>
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

   a) Set SSH:
    ```
    docker exec -it [CONTAINER_ID] bin/bash
    ```
    ```
    service ssh start
    ```
    
   
### 2) Run Docker
1. Run docker-compose up<br>
   a) Development:
   ```
   docker-compose up -d mongo postgres fastapi_dev react-app
   ```
   b) Production:
   ```
   docker-compose up -d mongo postgres fastapi react-app
   ```
