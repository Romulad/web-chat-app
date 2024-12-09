IN_PRODUCTION = True
TESTING = False

if IN_PRODUCTION:
    OROGINS = [
        "http://ec2-35-180-138-45.eu-west-3.compute.amazonaws.com",
    ]
else:
    OROGINS = [
        "http://localhost:5173",
        "http://localhost:4173",
        "https://chat-ro.onrender.com",
    ]
