
class UIElement:
    def __init_subclass__(cls, UIName, **kargs) -> None:
        cls.UIName = UIName
        super().__init_subclass__(**kargs)

    def __init__(self, content) -> None:
        self.content = content

    def __call__(self):
        return self.render()
    
    def __repr__(self) -> str:
        return self.render()
    
    """    
    @classmethod
    def create(cls, UIName, name, content):
        return UIELEMENT_LOOKUP[UIName](name, content)
    """    

    def update(self, contents):
        while  isinstance(self.content, UIElement):
            self = self.content
        self.content = contents

    def render(self):
        raise NotImplementedError('uielement: render() method required by uielements')