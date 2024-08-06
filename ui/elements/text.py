from .uielement import UIElement
from ..common.defs import DEFAULT_TEXT

class Text(UIElement, UIName='Text'):
    def __init__(self, content):
        raise RuntimeError("Use Text.new() to create a text object")
    
    def __add__(self, other):
        if isinstance(other, str) and isinstance(self, Text):
                r = self.content + other
        return r

    #To enforce the creation of a correct Text (as it must be a string)
    @classmethod
    def _priv_init(cls, content, **kargs) -> None:
        instance = super().__new__(cls)
        instance.properties = {'end':kargs['end'], 'prefix':kargs['prefix'], 'indent':kargs['indent'], 'align':kargs['align']}
        super().__init__(instance, content)
        return instance

    @classmethod
    def new(cls, content, **kargs):
        if not isinstance(content, str):
            print('text: text type not str')
            return None
        test = cls.validate(**kargs)
        if not test:
            print('text: incomplete kargs - setting missing to defaults')
            for key in DEFAULT_TEXT.keys():
                if not kargs.get(key):
                    kargs[key] = DEFAULT_TEXT[key]
        return cls._priv_init(content, **kargs)

    @staticmethod
    def validate(**test:dict) -> bool:
        for key in DEFAULT_TEXT.keys():
            if key not in test:
                return False
        return True

    def render(self)-> str:
        return self.content.center(self.dimensions[0])





