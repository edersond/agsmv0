import os

__all__ = ["APP_GLOBALS"]

class APP_GLOBALS:
    """
    APP GLOBALS
    """
    APP_NAME = "AGIOTA SIMULATOR"
    APP_VERSION = "0.0.0"
    APP_DESCRIPTION = "AGIOTA SIMULATOR"
    
    class APP_DIRS:
        LIBS = os.path.join(os.getcwd(), "libs")
        LOGS = os.path.join(os.getcwd(), "logs")
        MEDIA = os.path.join(os.getcwd(), "media")
        MIDDLEWARE = os.path.join(os.getcwd(), "middleware")
        ROUTES = os.path.join(os.getcwd(), "routes")
        SRC = os.path.join(os.getcwd(), "src")
        STATIC = os.path.join(os.getcwd(), "static")
        TEMPLATES = os.path.join(os.getcwd(), "templates")
        TMP = os.path.join(os.getcwd(), "tmp")