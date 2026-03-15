1) SSH into your EC2 instance
    ssh -i .ssh/id.pem egoksu@X.Y.Z.W
2) Update packages and install Apache
    sudo apt update
    sudo apt install apache2 -y
3) Edit Apache port configuration
    sudo nano /etc/apache2/ports.conf
    Listen 8008
4) Edit site configuration
    sudo nano /etc/apache2/sites-available/000-default.conf
    <VirtualHost *:8008>
5) Restart Apache
    sudo systemctl restart apache2
6) EC2 Configuration
    Edit inbound rules
    Add new rule (Type: Custom TCP, Port range: 8008, Source: 0.0.0.0/0)
7) Create file
    sudo nano /var/www/html/comp370_hw3.txt
    "At first glance, Bojack Horseman seems to be a show that narrates the story of a horse
    who used to be famous in the 1990s. It offers insights into the entertainment sector in Hollywood
    and successfully satirizes the Hollywood lifestyle through anthropomorphic characters and
    absurd visuals. However, as the series progresses, it starts depicting the everyday human struggle
    and transforms into a more realistic show relatable on sociological and psychological levels. This
    new tone of the show is supported by subtle artistic references, symbolic meanings behind the
    visuals and psychological, philosophical, and sociological concepts behind the narration."
8) On a web server, type the command below to see if it works
    http://X.Y.Z.W:8008/comp370_hw3.txt