
# some helper-Classes

class PolySelection(object):
    def __init__(self,name,selectinIndexe):
        self.name=name
        self.selectionIndexe=selectinIndexe
		
class AWDerrorObject(object):
    def __init__(self, errorID=None,errorData=None):
        self.errorID=errorID
        self.errorData=errorData

class objectSettings(object):
    def __init__(self):
        pass                            