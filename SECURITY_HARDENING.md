# Production Security Hardening Guide

## 🔒 Security Features Implemented

### 1. **JWT Authentication**
- Token-based authentication with HS256 algorithm
- Configurable token expiration (default: 60 minutes)
- Token refresh mechanism
- Secure claims validation

### 2. **API Key Management**
- Programmatic API key generation
- Key rotation support
- Configurable permissions per key
- Key expiration and revocation
- Last-used tracking

### 3. **Rate Limiting**
- Token bucket algorithm
- Per-client rate limiting
- Configurable rate limits (default: 60 req/min)
- Remaining quota tracking

### 4. **Role-Based Access Control (RBAC)**
- Pre-defined roles: admin, user, viewer, api_client
- Fine-grained permissions
- Custom role creation
- Permission inheritance

### 5. **SSL/TLS Support**
- HTTPS support with certificate configuration
- Client certificate verification (optional)
- Secure communication channel

### 6. **Data Encryption**
- Encryption manager for sensitive data
- Supports custom encryption implementations
- Key management through environment variables

### 7. **Audit Logging**
- All access events logged
- Security event tracking
- Audit trail for compliance
- Detailed event logging with severity levels

---

## 🚀 Deployment Configuration

### Environment Variables

```bash
# JWT Configuration
export JWT_SECRET_KEY="your-secret-key-here-min-32-chars"
export JWT_EXPIRE_MINUTES=60

# API Key Configuration
export API_KEY_EXPIRE_DAYS=365

# SSL/TLS Configuration
export SSL_CERT_FILE="/path/to/cert.pem"
export SSL_KEY_FILE="/path/to/key.pem"

# Encryption Configuration
export ENCRYPTION_KEY="your-encryption-key-here"

# Database
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/hyper_registry"

# Redis
export REDIS_URL="redis://localhost:6379"

# Rate Limiting
export RATE_LIMIT_PER_MINUTE=100

# Logging
export LOG_LEVEL="INFO"
```

### Production Checklist

- [ ] Generate strong JWT secret key (min 32 characters)
- [ ] Generate SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Enable HTTPS only
- [ ] Setup authentication for all endpoints
- [ ] Configure rate limiting thresholds
- [ ] Enable audit logging
- [ ] Setup log aggregation
- [ ] Configure backup and recovery
- [ ] Document API keys and secrets
- [ ] Setup monitoring and alerts
- [ ] Enable CORS restrictions
- [ ] Configure database encryption
- [ ] Setup VPN for admin access
- [ ] Enable multi-factor authentication (if applicable)

---

## 🔐 Security Best Practices

### 1. **Key Management**

```bash
# Generate strong JWT secret
openssl rand -base64 32

# Generate SSL certificate (self-signed)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

### 2. **Rate Limiting Configuration**

```python
# Adjust based on expected traffic
rate_limiter = RateLimiter(requests_per_minute=100)

# For public API: 10-30 req/min
# For internal API: 100-1000 req/min
# For high-volume: 1000+ req/min
```

### 3. **RBAC Configuration**

```python
# Create custom role
rbac_manager.create_role("data_analyst", [
    "read",
    "search",
    "analytics:read"
])

# Assign to user
user.roles = ["data_analyst"]
```

### 4. **API Key Rotation**

```bash
# Generate new key
new_key = api_key_manager.generate_key(
    user_id="user_123",
    name="production_key_v2",
    expires_in_days=90
)

# Revoke old key
api_key_manager.revoke_key("old_key_id")
```

### 5. **Audit Log Monitoring**

```python
# Get recent security events
logs = audit_logger.get_logs(limit=100)

# Monitor for suspicious activity
for log in logs:
    if log.get("severity") == "critical":
        send_alert(log)
```

---

## 🛡️ SSL/TLS Setup

### Using Let's Encrypt (Recommended)

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Generate certificate
certbot certonly --standalone -d your-domain.com

# Configure in environment
export SSL_CERT_FILE="/etc/letsencrypt/live/your-domain.com/fullchain.pem"
export SSL_KEY_FILE="/etc/letsencrypt/live/your-domain.com/privkey.pem"
```

### Manual Self-Signed Certificate

```bash
# Generate private key and certificate
openssl req -x509 -newkey rsa:4096 \
  -keyout ./ssl/key.pem \
  -out ./ssl/cert.pem \
  -days 365 -nodes \
  -subj "/C=US/ST=State/L=City/O=Org/CN=localhost"

# Set permissions
chmod 600 ./ssl/key.pem
chmod 644 ./ssl/cert.pem
```

---

## 🔑 Authentication Examples

### JWT Token Creation and Usage

```bash
# Get JWT token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "secure_password"
  }'

# Use token in API requests
curl http://localhost:8000/api/v1/registry/entries \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### API Key Usage

```bash
# Generate API key
api_key = api_key_manager.generate_key(
    user_id="user_123",
    name="integration_key",
    permissions=["read", "write"]
)

# Use in API requests
curl http://localhost:8000/api/v1/registry/entries \
  -H "X-API-Key: generated_api_key_here"
```

---

## 📊 Security Monitoring

### Setup Monitoring Alerts

```python
# Monitor failed authentication attempts
if log.get("status") == "failed" and "auth" in log.get("action", ""):
    send_alert("Failed authentication attempt", log)

# Monitor rate limit violations
if "rate_limit" in log.get("description", ""):
    send_alert("Rate limit violation", log)

# Monitor permission denied events
if "denied" in log.get("status", ""):
    send_alert("Permission denied", log)
```

### Audit Log Analysis

```bash
# Find all access by user
grep '"user_id": "user_123"' audit.log

# Find failed operations
grep '"status": "failed"' audit.log

# Find recent security events
grep '"severity": "critical"' audit.log | tail -20
```

---

## 🔄 Incident Response

### If API Key is Compromised

1. **Immediately revoke the key**
   ```python
   api_key_manager.revoke_key(compromised_key_id)
   ```

2. **Generate new key**
   ```python
   new_key, _ = api_key_manager.generate_key(
       user_id=user_id,
       name="replacement_key"
   )
   ```

3. **Audit trail**
   ```python
   audit_logger.log_security_event(
       event_type="key_revoked",
       severity="high",
       description="API key revoked due to compromise",
       user_id=user_id
   )
   ```

### If Unauthorized Access Detected

1. **Enable detailed logging**
2. **Activate emergency rate limiting** (1 req/min)
3. **Temporarily disable affected user account**
4. **Review audit logs**
5. **Enable multi-factor authentication**

---

## ✅ Security Testing Checklist

- [ ] Test JWT token expiration
- [ ] Test API key revocation
- [ ] Test rate limiting
- [ ] Test permission denial
- [ ] Test SSL/TLS connection
- [ ] Test encryption/decryption
- [ ] Test audit logging
- [ ] Test failed authentication attempts
- [ ] Test invalid API keys
- [ ] Test privilege escalation protection
- [ ] Test SQL injection prevention
- [ ] Test XSS prevention
- [ ] Test CSRF protection
- [ ] Test unauthorized access detection

---

## 📚 Additional Resources

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8949)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/sql-security.html)
