<center>
<h1>RDBSync</h1>

<img src="https://cdn-icons-png.flaticon.com/512/2587/2587247.png" width="128px" alt="Image from https://www.flaticon.com/free-icons/data-transfer">

<b><i>
A utility supports synchronizing SQL databases between two SQL database servers.
</i></b>

</center>

<hr>

# Project Roadmap 🛣️

1. Establish the connection between two database servers.
    1. Confirm the database flavor match(Ex. Both are MySQL)
    2. Confirm the user permission adequacy for perform sync operation.
        * **Document the required user privileges for database required to perform operation with this tool**.
        * Can be evaluate by user permission inspection. In MySQL use the below command.<br>
        ```MySQL
        SHOW GRANTS FOR database_user;
        ```
        * Provide warning if the provided user is more privileged user than required. Further, **do not proceed in
          operation if root user is provided**.

2. Identity all inconsistencies in the database table structure.
    * Before the operation we need to lock the two database form there operation.(Hold database reads and writes)
    * In MySQL below command will be used for that.<br>
    ```MySQL
    // block writes
    LOCK TABLES table_name  WRITE;
    // block reads
    LOCK TABLES table_name  READ;
    ```
    1. Database level inconsistencies
        * Just table in source and target will be compared.
    2. Table level inconsistencies
        * For each table field will be compared and make sure there names datatype and other constraints are identical.
        * Special forces need to be put into key constraint integrity.
    3. Other database elements such as view also need to consider. (may later)

3. Identify all data inconsistencies.
    * In this stage without any structural changes applied to the database, we may identify some inconsistencies of the
      data. But, after respective structural fixes there may have more data level inconsistencies.
    * Hence in this stage just showcase/list out available data inconsistencies.
    * In this process, by taking each and every table row by row and comparison should conduct.
    * Make sure to unlock the database tables after this process using the bellow command(for MySQL).
    ```MySQL
    // unlock all tables
    UNLOCK TABLES;
    ```
4. Treat for structural inconsistencies.
5. Treat for data inconsistencies.