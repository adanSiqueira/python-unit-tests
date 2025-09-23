class DataBase:
    """Simulate a basic user database"""
    def __init__(self):
        self.data = {}

    def add_user(self, user_id, name):
        if user_id in self.data:
            raise ValueError("User ID already exists")
        self.data[user_id] = name
    
    def __getitem__(self, user_id):
        return self.data.get(user_id, None)
    
    def __delitem__(self, user_id):
        if user_id in self.data:
            del self.data[user_id]
        else:
            raise KeyError("User ID not found")