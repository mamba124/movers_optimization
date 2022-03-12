

class MockedDriver:
    def __init__(self, page):
        self.page = page
        self.text = "blabla"
    
    def find_elements(self, name, attr):
        return [MockedDriverInstance(self.page)]

    def find_element(self, name, attr):
        return MockedDriverInstance(self.page)
    
    def get(self, link):
        pass

    def refresh(self):
        pass
    
class MockedDriverInstance(MockedDriver):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def get_attribute(self, attr):
        return self.page
    
    def send_keys(self, arg):
        print("sent keys")
    
    def click(self):
        print("clicked")

