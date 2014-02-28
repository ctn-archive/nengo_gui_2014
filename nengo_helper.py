import nengo
import traceback

class ModelHelper(nengo.Model):
    def add(self, obj):
        super(ModelHelper, nengo.Model).add(self, obj)
        
        for fn, line, function, code in reversed(traceback.extract_stack()):
            if fn == '<editor>':
                obj._created_line_number = line
        
nengo.Model = ModelHelper        
