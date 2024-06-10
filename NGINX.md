# Nginx: A Brief Overview for Cloud Software Engineers

Nginx is a high-performance web server that also functions as a reverse proxy, load balancer, and HTTP cache. It is widely used due to its efficiency, scalability, and ability to handle a large number of simultaneous connections.

## Key Components and Concepts

### Web Server

- **Static Content**: Nginx can serve static pages (HTML, CSS, JS, images) directly from the filesystem.
- **Resource Efficiency**: It is highly resource-efficient, making it a popular choice for high-performance web servers.

### Reverse Proxy

- **Intermediary**: Nginx can act as an intermediary between clients (web browsers) and backend servers.
- **Request Forwarding**: It receives client requests, forwards them to backend servers (e.g., Node.js, Python, PHP applications), and returns the responses to the client.
- **Benefits**: Helps protect the backend server, hides internal infrastructure details, and distributes the workload.

### Load Balancer

- **Request Distribution**: Nginx can distribute requests among multiple backend servers to improve scalability and redundancy.
- **Algorithms**: Supports various load-balancing algorithms, such as round-robin, least connections, and IP hash.

### Cache

- **Response Caching**: Nginx can cache responses from backend servers to reduce load and improve response times.

## Configuration Structure

Nginx configuration is based on configuration blocks written in text files (usually located in `/etc/nginx/nginx.conf` and `/etc/nginx/sites-available/`).

### Configuration Contexts

- **Main**: Global Nginx settings.
- **HTTP**: HTTP protocol-related settings.
- **Server**: Defines a virtual server with specific settings for a domain or set of domains.
- **Location**: Defines rules for URI matching and associated settings.

### Common Directives

- **listen**: Defines the port the server will listen on.
- **server_name**: Defines the server name (domain).
- **location**: Defines URI matching rules and associated settings.
- **proxy_pass**: Defines the backend to which the request will be forwarded.
- **root/alias**: Defines the document root directory for serving static files.

## Example Configurations

### Web Server Example

```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    location / {
        root /var/www/your_domain.com/html;
        index index.html index.htm;
    }

    location /css/ {
        alias /var/www/your_domain.com/css/;
    }

    location /scripts/ {
        alias /var/www/your_domain.com/scripts/;
    }

    error_log /var/log/nginx/your_domain.com_error.log;
    access_log /var/log/nginx/your_domain.com_access.log;
}
```

### Reverse Proxy Example

````nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
````

### Load Balancer Example

````nginx
upstream backend_servers {
    server backend1.example.com;
    server backend2.example.com;
}

server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
````

### Cache Example
````nginx
proxy_cache_path /data/nginx/cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m use_temp_path=off;

server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    location / {
        proxy_cache my_cache;
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        add_header X-Proxy-Cache $upstream_cache_status;
    }
}
````

## Key Commands

### Start/Restart Nginx:
```shell
sudo systemctl start nginx
sudo systemctl restart nginx
```
### Test Configuration:
```shell
sudo nginx -t
```
### Check Nginx Status:
```shell
sudo systemctl status nginx
```

## Comparison with Cloud Services

- **AWS Elastic Load Balancer (ELB) and GCP Cloud Load Balancing**: Similar to using Nginx as a load balancer to distribute traffic among backend servers.
- **AWS API Gateway and GCP API Gateway**: Comparable to using Nginx as a reverse proxy to route requests to different backend services.
- **AWS CloudFront and GCP Cloud CDN**: While not a complete replacement, Nginx can be used as a caching layer to improve performance.


https://nginx.org/en/docs/