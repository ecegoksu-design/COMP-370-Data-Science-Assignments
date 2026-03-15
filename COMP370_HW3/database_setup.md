1) Install MariaDB
    sudo apt update
    sudo apt install mariadb-server -y
2) Edit MariaDB Configuration
    sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
    bind-address = 0.0.0.0
    port = 6002
3) Restart MariaDB
    sudo systemctl restart mariadb
4) Edit EC2 Configuration
    Edit inbound rules
    Add new rule (Type: Custom TCP, Port range: 6002, Source: 0.0.0.0/0)
5) Log into MariaDB
    sudo mysql -u root
6) Run SQL Commands Below
    CREATE DATABASE comp370_test;
    CREATE USER 'comp370'@'%' IDENTIFIED BY '$ungl@ss3s';
    GRANT ALL PRIVILEGES ON comp370_test.* TO 'comp370'@'%';
    FLUSH PRIVILEGES;
    EXIT;
7) Open DBeaver and try if connection is successful
    New DataBase Connection
    Database Type: MariaDB
    Host: EC2's Public IP 
    Port: 6002
    Database: comp370_test
    Username: comp370
    Password: $ungl@ss3s
    Test Connection