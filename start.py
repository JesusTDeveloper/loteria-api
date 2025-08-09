#!/usr/bin/env python3
import os
import sys
import uvicorn

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"Starting server on port {port}")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
