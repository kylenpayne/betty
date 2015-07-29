 #!/usr/bin/env
'''
class declaration for a fighter in the ufc.
'''
class fighter:
    
    def __init__(self, attr):
        self.attr = attr
    
class attr:
    # order of the attributes
    # height, reach, record, division, name, nationality, 
    # camp, tenure
    
    
    '''
    class for attributes assigned to fighters
    '''
    def __init__(self, attrs):
        self.height = attrs['height']
        self.record = attrs['record']
        self.division = attrs['division']
        self.name = attrs['name']
        self.nation = attrs['nationality']
        self.team = attrs['team']
        self.tenure = attrs['tenure']
        self.style = attrs['style']
        self.age = attrs['age']

        
    