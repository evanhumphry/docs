# Web Server Configuration

A checklist for setting up and verifying an Nginx web server with SSL.

---

## 1. Nginx Status

```bash
# Check if nginx is running
sudo systemctl status nginx

# Enable nginx to start on boot
sudo systemctl enable nginx

# Test nginx configuration
sudo nginx -t
```

## 2. Port Configuration

```bash
# Verify nginx is listening on 443
sudo ss -tulpn | grep :443
```

## 3. SSL Certificates

Required files (typically in `/etc/nginx/ssl/` or `/etc/ssl/` or `/etc/pki/`):

- `fullchain.pem` — domain + intermediate certificates
- `privkey.pem` — private key

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;
}
```

## 4. Firewall

```bash
# firewalld (Fedora/RHEL)
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload

# UFW (Ubuntu/Debian)
sudo ufw allow https
sudo ufw allow 443/tcp
```

## 5. Testing

```bash
# Test SSL configuration
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Test port accessibility
nc -zv yourdomain.com 443
```

## 6. Restart

```bash
sudo systemctl restart nginx
```
