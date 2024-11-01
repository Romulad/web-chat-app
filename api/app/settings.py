IN_PRODUCTION = False
TESTING = True

if IN_PRODUCTION:
    OROGINS = [
        "https://chat-ro.onrender.com",
    ]
else:
    OROGINS = [
        "http://localhost:5173",
        "http://localhost:4173",
        "https://chat-ro.onrender.com",
    ]
