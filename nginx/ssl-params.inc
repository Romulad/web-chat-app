# secure nginx, see https://ssl-config.mozilla.org

ssl_protocols TLSv1.3
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off; # Requires nginx >= 1.5.9
ssl_stapling on; # Requires nginx >= 1.3.7
ssl_stapling_verify on; # Requires nginx => 1.3.7
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# https://hstspreload.org
add_header Strict-Transport-Security "max-age=63072000" always; 
# By default, HSTS header is not added to subdomain requests. If you have subdomains and want
# HSTS to apply to all of them, you should add the includeSubDomains variable like this:
#add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;

add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header X-Robots-Tag none;