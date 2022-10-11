<center>
<h1>RDBSync</h1>

<img src="https://www.flaticon.com/download/icon/2587247?icon_id=2587247&author=422&team=422&keyword=Data+transfer&pack=2587128&style=0&style_id=1056&format=png&color=%23000000&colored=2&size=128&selection=1&premium=0&type=standard&token=03AIIukzjJXo35tbADu_o74uA3GpW1TemWKQm614305nqv05ZrbUlb1YxQCujYrwpi9r1oxTEaKTtVm560lXuJeYYvnvqrsqUXZyglyQufTyupEfHpj2bIAG7z-3F7JrmgywiAVEfgKS0nyFk8gDJw5kke86KSFHeqdC5Vq-yYdyeFMRuH-lO2vQlRnIclDT5sf01C15xX2GJrlH3XOqZD11_YGsMAzrVWuuCTLxHomEPWvwgL7AkQfoGLsM10F8Ultn3Tk3H-uvx3pekgTnWtTUhEixbfquYfpf4beN5-O7-QAdRbFHQqA91YihT24ELemv-cMmVxozyqvA9qmJlHauZlH1VQkheHkzuGkx2naOjiTuwb70OecJCpsMzexm9x5xJFRYCFRdggzH-rv5EiuLWLC4T9Vu6o-r83wIq5ISxM10vhq0Hi8-IlKFRjZsyvo1zR2YRaCe6567_zWZ-qCoxeE2J-8QtoN1X1OLEDfreN9WjOrWGN2O-fnhh5uA_cqXfUlHigXQtOGf0yctWaWjonfYIkeB5Foc5nVZ4EorG8Ge-cAfYynhqE9glErHUxkKVjlqFDisQupPscWJFTWc2meiEU_rzsBuoIzthJTKwL2MoMZ9y7cF7Yh5PyhBfvkb25_YPhd6tArfJR4wK-WTUjfJPb0CszIUsSRoC-wU9QF3U0f2gJ2clxz5iBJ_ci0fxvXB-uaxAfp2L_TL-LSuw4B7guVGHaG5UcpjaCnVQcFVE6W2z93aeRTSGP8ApA8XASqJ9ss8KaeNMho9KUqIR7JGSPPnFiR-gKCDz0_DeRhzG4sZkzhi0-nG1vV2hdhOhRrD12eqhtV0O8krSC9PMnxZwVbOZBZzXDlkbSc8frui2VjJShSPuAIy6sUzAAQuHVbsekToENYNZGkMtK2GN9VZebqPOg1b71pihfRyEvBwEZOit3j2UZvm8BUVXQG9twynv356gqa3LPwQQ_4vMZVpT8_w2ghapkJ6d3aqtFp1H1FC2CfpErW52Lv0hKqdrA7e0MkOgLfbIGPFlX-z8XIiHTGYKxRbVU9b6NjzFGNofF3GNch3X-aMTFzdiTA79osRQghWSGi29hIL6XyDjggLA54Brpp7lwJdpZpkUwGq9czEw7dDWlj0Lu8a6NHSACxGjxJQkEd1QV-f-yl-6UqAtK963Hh5F1T9GOeRi7ndWT9WKDH6wKPwFEqJ2jJ70HxOsD1fXDkUEfa1bCdcdTzZzGO90yliQPLN03HOsLegh6Sq3gOR0Xq175ZqD6Qhgc-FOmDT9lkCoZBRzu_ZbWmfdVCNYwad2tTodETl4wYce7CmloUFLDHTAqZ49d5LhfWCu4UWb8mvgoH_UIAHvuXaeJphYx3w" alt="Image from https://www.flaticon.com/free-icons/data-transfer">

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
        * Provide warning if the provided user is more privileged user than required. Further, **do not proceed in operation if root user is provided**.

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
    * In this stage without any structural changes applied to the database, we may identify some inconsistencies of the data. But, after respective structural fixes there may have more data level inconsistencies.
    * Hence in this stage just showcase/list out available data inconsistencies.
    * In this process, by taking each and every table row by row and comparison should conduct.
    * Make sure to unlock the database tables after this process using the bellow command(for MySQL).
    ```MySQL
    // unlock all tables
    UNLOCK TABLES;
    ```
4. Treat for structural inconsistencies.
5. Treat for data inconsistencies.