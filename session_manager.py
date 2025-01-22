class SessionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SessionManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.session_data = {}  # Initialize session data only once
        return cls._instance

    def set(self, key, value):
        self.session_data[key] = value

    def get(self, key, default=None):
        return self.session_data.get(key, default)

    def clear(self):
        self.session_data.clear()
