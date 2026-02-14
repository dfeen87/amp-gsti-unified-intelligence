"""
Standalone Runner for Global Observability Node
================================================

This script runs the observability node as an independent service.
It binds to port 8081 by default (configurable via OBS_NODE_PORT).
"""

import os
import sys


def main():
    """Run the observability node."""
    # Get port from environment or use default
    port = int(os.getenv("OBS_NODE_PORT", 8081))
    host = os.getenv("OBS_NODE_HOST", "0.0.0.0")
    
    print("=" * 70)
    print("AMP-GSTI Global Observability Node")
    print("=" * 70)
    print(f"Starting on {host}:{port}")
    print("Mode: Read-Only (all write operations disabled)")
    print("=" * 70)
    
    try:
        import uvicorn
        
        uvicorn.run(
            "observability_node.app:app",
            host=host,
            port=port,
            log_level="info",
            access_log=True,
        )
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting observability node: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
