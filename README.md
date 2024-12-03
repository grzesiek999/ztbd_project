# ztbd_project

## MongoDB
### 1) Setup
1. Run docker-compose up
2. Run in terminal
<br>a) Enter mongosh:
    ```
    docker exec -it [CONTAINER_ID] mongosh
    ```
    b) Create the user with credentials from `.env` file`:
    ```
    use admin
    ```
    ```
    db.createUser({
      user: "[username]",
      pwd: "[password]",
      roles: [{ role: "root", db: "admin" }]
    })
    ```
    c) Set profiler:<br>
    ```
    db.auth("[username]", "[password]")
    ```
    ```
    db.setProfilingLevel(1, { slowms: 0, filter: { "command.comment": "backend_query" } })
    ```
   
### 2) Run fastapi