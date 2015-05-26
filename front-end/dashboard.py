#!/usr/bin/env python3

from Dashboard.Routes import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
