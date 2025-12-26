# Custom TLS Certificates

Telebugs automatically creates and installs a Let's Encrypt TLS certificate for
you. If you already have your own certificate, you can use it instead.

## TLS Termination with Nginx

[Nginx][1] is the recommended way to use a custom certificate. It works as a reverse
proxy and handles TLS termination.

During the `telebugs setup` command, leave the domain prompt empty and press
Enter. This runs Telebugs on `http://localhost:5555` without TLS.

1. Install Nginx.

   ```sh
   apt-get update
   apt-get install nginx
   ```

2. Create a config file at `/etc/nginx/sites-available/telebugs`.

   ```nginx
   server {
      listen 443 ssl;
      server_name <YOUR_DOMAIN>;

      ssl_certificate /path/to/your/fullchain.pem;
      ssl_certificate_key /path/to/your/privkey.pem;

      location / {
          proxy_pass http://localhost:5555;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
    }

    server {
      listen 80;
      server_name <YOUR_DOMAIN>;
      return 301 https://$host$request_uri;
    }
   ```

3. Enable the config.

   ```sh
   ln -s /etc/nginx/sites-available/telebugs /etc/nginx/sites-enabled/
   ```

4. Test and restart Nginx.

   ```sh
   nginx -t
   systemctl restart nginx
   ```

Nginx now handles your certificate and forwards traffic securely to Telebugs.

## TLS Termination with HAProxy

[HAProxy][2] is another solid option for custom certificates.

Leave the domain prompt empty during setup, just like with Nginx.

1. Install HAProxy.

   ```sh
   apt-get update
   apt-get install haproxy
   ```

2. Add this to `/etc/haproxy/haproxy.cfg`.

   ```
   frontend https_frontend
     bind *:443 ssl crt /path/to/your/certificate.pem
     mode http
     option httplog
     default_backend telebugs_backend

   backend telebugs_backend
     mode http
     server telebugs_server localhost:5555 check
     option http-server-close
     http-request set-header X-Forwarded-Proto https
     http-request set-header X-Forwarded-For %[src]
     http-request set-header X-Forwarded-Host %[req.hdr(Host)]
     http-request set-header X-Real-IP %[src]
   ```

   **Note:** The `certificate.pem` file must contain both the certificate and
   private key concatenated.

   For Let's Encrypt:

   ```sh
   cat fullchain.pem privkey.pem > /etc/ssl/private/certificate.pem
   ```

3. Test and restart HAProxy.

   ```sh
   haproxy -c -f /etc/haproxy/haproxy.cfg
   systemctl restart haproxy
   ```

HAProxy now handles your certificate and forwards traffic to Telebugs.

[1]: https://nginx.org/
[2]: https://www.haproxy.org/
