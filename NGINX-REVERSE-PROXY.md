```
server {
    listen 80; # Port on which Nginx will listen
    server_name example.com; # Domain name

    # HTTP to HTTPS redirection
    listen 443 ssl;
    ssl_certificate /path/to/ssl_certificate.crt;
    ssl_certificate_key /path/to/ssl_certificate_key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # WWW or non-WWW redirection
    if ($host = www.example.com) {
        return 301 https://example.com$request_uri;
    }

    # Redirect to HTTPS
    if ($scheme = http) {
        return 301 https://$host$request_uri;
    }

    # Root and index configuration
    root /var/www/example.com/html;
    index index.html index.htm index.nginx-debian.html;

    # Log configuration
    access_log /var/log/nginx/example.com.access.log;
    error_log /var/log/nginx/example.com.error.log;

    # Static files configuration
    location /static/ {
        alias /var/www/example.com/static/;
        expires 30d;
    }

    # Reverse proxy configuration
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade; # Bypass cache for WebSocket connections
    }

    # WebSocket configuration
    location /ws/ {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Gzip compression configuration
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_proxied any;
    gzip_min_length 1000;

    # Access restriction configuration
    location /admin {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }

    # Rate limiting configuration
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
    location / {
        limit_req zone=one burst=5;
    }

    # Security headers configuration
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";

    # Content Security Policy configuration
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'";

    # HTTP Strict Transport Security (HSTS) configuration
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";

    # 404 error page configuration
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }

    # 500 error page configuration
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        internal;
    }

    # Load balancing configuration
    upstream backend {
        server backend1.example.com;
        server backend2.example.com;
    }
    location / {
        proxy_pass http://backend;
    }

    # Buffering configuration
    proxy_buffering on;
    proxy_buffers 16 4k;
    proxy_buffer_size 8k;

    # Client body size configuration
    client_max_body_size 10M;

    # Connection timeout configuration
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    # Custom error handling
    location = /50x.html {
        internal;
        root /var/www/errors;
    }

    # Cross-Origin Resource Sharing (CORS) configuration
    location /api/ {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Origin, X-Requested-With, Content-Type, Accept, Authorization';
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }

    # Custom 403 Forbidden page
    error_page 403 /403.html;
    location = /403.html {
        internal;
        root /var/www/errors;
    }

    # Limit rate per IP address
    limit_conn_zone $binary_remote_addr zone=addr:10m;
    limit_conn addr 5;

    # Enable SSL session caching
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Keep-alive timeout
    keepalive_timeout 65;

    # Logging format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    # Use the defined log format
    access_log /var/log/nginx/access.log main;
}

````
## Explanation of Configurations

### listen
Specifies the port on which Nginx will listen. The default is 80 for HTTP and 443 for HTTPS.

### server_name
The domain name for which the server is configured.

### ssl_certificate and ssl_certificate_key
Paths to the SSL certificate files.

### ssl_protocols and ssl_ciphers
Allowed SSL protocols and ciphers.

### root and index
Root directory and index files.

### access_log and error_log
Paths to the access and error log files.

### location /static/
Defines a directory for serving static files, with a 30-day cache expiration.

### proxy_pass
Address of the backend server to which requests will be forwarded.

### proxy_set_header
Configures HTTP headers that will be sent to the backend server.

### proxy_cache_bypass
Bypasses cache for specific conditions, such as WebSocket connections.

### proxy_http_version, proxy_set_header Upgrade, and proxy_set_header Connection
Specific configurations for WebSocket support.

### gzip
Enables gzip compression.

### gzip_types
Specifies the MIME types that should be compressed.

### gzip_proxied
Specifies the requests for which compression should be enabled.

### gzip_min_length
Minimum length of responses to be compressed.

### auth_basic and auth_basic_user_file
Configures basic authentication to restrict access to certain areas.

### limit_req_zone and limit_req
Rate limiting configuration to protect against DDoS attacks.

### add_header
Adds HTTP headers to enhance security.

### Content-Security-Policy
Configures Content Security Policy headers to prevent cross-site scripting (XSS) and other code injection attacks.

### Strict-Transport-Security
Configures HTTP Strict Transport Security (HSTS) headers to enforce secure connections.

### error_page
Defines custom error pages.

### upstream
Defines a group of backend servers for load balancing.

### proxy_buffering, proxy_buffers, and proxy_buffer_size
Configures buffering to optimize performance.

### client_max_body_size
Sets the maximum allowed size of the client request body.

### proxy_connect_timeout, proxy_send_timeout, and proxy_read_timeout
Configures timeouts for connections, sending, and reading data from the backend server.

### CORS configuration
Adds headers to enable Cross-Origin Resource Sharing (CORS), which allows resources to be requested from another domain.

### limit_conn_zone and limit_conn
Limits the number of simultaneous connections from a single IP address.

### ssl_session_cache and ssl_session_timeout
Configures SSL session caching and timeout settings to improve performance.

### keepalive_timeout
Sets the time a keep-alive connection can remain idle before being closed.

### log_format and access_log
Defines a custom logging format and applies it to the access log.