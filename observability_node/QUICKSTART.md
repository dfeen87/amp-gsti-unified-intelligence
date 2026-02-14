# Global Observability Node - Quick Start Guide

## Overview

The Global Observability Node is a standalone, read-only FastAPI microservice that provides transparent access to the AMP-GSTI platform's internal state without exposing any control surfaces.

**Key Features:**
- ✅ Read-only (no state modifications)
- ✅ Independent service (runs separately from main API)
- ✅ Production-safe (graceful degradation)
- ✅ No authentication required (safe by design)
- ✅ All endpoints are GET-only

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL database (configured)
- Redis (optional, for cache metrics)

### Installation

1. **Install dependencies** (from project root):
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment** (optional):
   ```bash
   export OBS_NODE_PORT=8081      # Default: 8081
   export OBS_NODE_HOST=0.0.0.0   # Default: 0.0.0.0
   ```

3. **Run the observability node**:
   ```bash
   python -m observability_node.run
   ```

   Or directly:
   ```bash
   python observability_node/run.py
   ```

The service will start on `http://0.0.0.0:8081` by default.

## Accessing the Service

- **Root:** http://localhost:8081/
- **Health Check:** http://localhost:8081/health
- **API Docs:** http://localhost:8081/docs
- **ReDoc:** http://localhost:8081/redoc

## Available Endpoints

### 1. GET /health

Health check with connectivity status.

**Example Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": {
    "uptime_seconds": 3600.5,
    "uptime_human": "0d 1h 0m 0s",
    "started_at": "2024-01-15T10:00:00"
  },
  "connectivity": {
    "database": "connected",
    "redis": "connected"
  },
  "environment": "development",
  "timestamp": "2024-01-15T11:00:00"
}
```

### 2. GET /api/system_state

Comprehensive system resource metrics.

**Example Response:**
```json
{
  "status": "operational",
  "system_resources": {
    "cpu": {
      "percent": 23.5,
      "count": 8
    },
    "memory": {
      "percent": 45.2,
      "used_mb": 2048.5,
      "total_mb": 4096.0
    },
    "disk": {
      "percent": 60.0,
      "used_gb": 120.5,
      "total_gb": 200.0
    },
    "load_averages": {
      "1min": 1.5,
      "5min": 1.2,
      "15min": 1.0
    }
  },
  "database": {
    "status": "connected",
    "statistics": {
      "total_candidates": 150,
      "total_queries": 500,
      "active_users": 5
    }
  },
  "redis": {
    "status": "connected",
    "metrics": {
      "used_memory_mb": 50.2,
      "connected_clients": 3,
      "hit_rate": 85.5
    }
  }
}
```

### 3. GET /api/gsti_state

Current GSTI (Gold-Silver Trust Index) state.

**Example Response:**
```json
{
  "status": "available",
  "gold_silver_ratio": 82.5,
  "volatility_index": "N/A",
  "economic_regime": "bullish",
  "confidence_score": 0.15,
  "last_update": "2024-01-15T10:30:00",
  "timestamp": "2024-01-15T11:00:00"
}
```

### 4. GET /api/amp_state

Current AMP (Anonymous Merit Protocol) state.

**Example Response:**
```json
{
  "status": "available",
  "candidates_evaluated": 150,
  "merit_score_distribution": {
    "min": 45.0,
    "max": 98.5,
    "mean": 72.3,
    "median": 75.0,
    "std_dev": 12.5
  },
  "credential_weighting": {
    "total_credential_types": 25,
    "credentials_by_type": {
      "skill": 120,
      "character": 45,
      "loyalty": 30
    }
  },
  "last_evaluation": "N/A"
}
```

### 5. GET /api/forecast_state

Forecast engine state and hiring outlook.

**Example Response:**
```json
{
  "status": "available",
  "hiring_outlook": {
    "strategy": "aggressive_growth",
    "recommendation": "Accelerate hiring for growth roles",
    "risk_level": "moderate"
  },
  "talent_flow_indicators": {
    "signal": "balanced",
    "interpretation": "Balanced loyalty distribution",
    "loyalty_ratio": 0.45
  },
  "macroeconomic_signals": {
    "gold_silver_ratio": 82.5,
    "market_regime": "bullish",
    "goodwill_momentum": 0.05
  },
  "model_confidence": {
    "level": "high",
    "hours_since_update": 0.5,
    "reason": "Data is 0.5 hours old"
  }
}
```

### 6. GET /api/audit_summary

Audit log summaries (anonymized, no PII).

**Parameters:**
- `limit` (optional): Number of entries to return (default: 50, max: 200)

**Example Response:**
```json
{
  "status": "available",
  "total_entries": 50,
  "recent_entries": [
    {
      "action": "candidate_query",
      "timestamp": "2024-01-15T10:55:00",
      "user_role": "admin"
    },
    {
      "action": "gsti_update",
      "timestamp": "2024-01-15T10:30:00",
      "user_role": "admin"
    }
  ],
  "mutation_summary": {
    "candidate_register": 10,
    "gsti_update": 5,
    "system_reset": 0
  }
}
```

## Security Model

### Read-Only Enforcement

All non-GET requests (POST, PUT, PATCH, DELETE) are **automatically rejected** with HTTP 405:

```bash
curl -X POST http://localhost:8081/api/system_state
# Response: {"error": "Method not allowed", "message": "This is a read-only observability node..."}
```

### No State Modifications

The observability node **never**:
- Triggers scoring operations
- Executes candidate matching
- Updates GSTI metrics
- Modifies database state
- Exposes credentials or secrets

### Graceful Degradation

If database or Redis are unavailable, endpoints return informative error messages instead of failing:

```json
{
  "status": "error",
  "error": "Database connection failed",
  "timestamp": "2024-01-15T11:00:00"
}
```

## Docker Deployment

### Dockerfile Example

Create `Dockerfile.observability` in project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy observability node
COPY observability_node/ ./observability_node/
COPY app/ ./app/

# Expose port
EXPOSE 8081

# Run observability node
CMD ["python", "-m", "observability_node.run"]
```

### Build and Run

```bash
# Build
docker build -f Dockerfile.observability -t amp-gsti-obs:latest .

# Run
docker run -d \
  -p 8081:8081 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/amp_gsti \
  -e REDIS_URL=redis://redis:6379/0 \
  -e OBS_NODE_PORT=8081 \
  --name amp-gsti-observability \
  amp-gsti-obs:latest
```

## Kubernetes Deployment

### Deployment YAML

Create `k8s/observability-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: amp-gsti-observability
  labels:
    app: amp-gsti-observability
spec:
  replicas: 2
  selector:
    matchLabels:
      app: amp-gsti-observability
  template:
    metadata:
      labels:
        app: amp-gsti-observability
    spec:
      containers:
      - name: observability
        image: amp-gsti-obs:latest
        ports:
        - containerPort: 8081
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: amp-gsti-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: amp-gsti-secrets
              key: redis-url
        - name: OBS_NODE_PORT
          value: "8081"
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8081
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8081
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: amp-gsti-observability-service
spec:
  selector:
    app: amp-gsti-observability
  ports:
  - protocol: TCP
    port: 8081
    targetPort: 8081
  type: LoadBalancer
```

### Deploy

```bash
kubectl apply -f k8s/observability-deployment.yaml
kubectl get services amp-gsti-observability-service
```

## Monitoring and Alerting

### Prometheus Integration

The observability node exposes metrics that can be scraped by Prometheus:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'amp-gsti-observability'
    static_configs:
      - targets: ['localhost:8081']
    metrics_path: '/api/system_state'
    scrape_interval: 30s
```

### Health Check Monitoring

Use the `/health` endpoint for uptime monitoring:

```bash
# Check every 30 seconds
watch -n 30 'curl -s http://localhost:8081/health | jq .'
```

## Troubleshooting

### Port Already in Use

```bash
# Change port
export OBS_NODE_PORT=8082
python -m observability_node.run
```

### Database Connection Failed

Check that `DATABASE_URL` is correctly configured in your environment or `.env` file.

### Import Errors

Ensure you're running from the project root and all dependencies are installed:

```bash
cd /path/to/amp-gsti-unified-intelligence
pip install -r requirements.txt
python -m observability_node.run
```

## Production Considerations

1. **Run behind reverse proxy** (nginx, Traefik) for HTTPS termination
2. **Set resource limits** in container orchestration
3. **Monitor endpoint response times** for performance degradation
4. **Rate limit** at ingress to prevent abuse
5. **Log all access** for audit trail

## Support

For issues or questions, refer to the main project README or open an issue on GitHub.
