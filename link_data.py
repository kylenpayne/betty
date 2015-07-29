'''
link_data.py
'''
import pandas as pd
def link_data(fighters):
    '''
    link_data takes a list of fighters and 
    starts by looking at the records of fighters in the
    list of fighter objects.
    
    At each row of the record, it will check to see if the opponent
    is in the list of fighters. 
    
    The search is going to be prototyped as serial currently, as the 
    list of fighters is currently not sorted alphabetically.
    
    
    '''
    
    for fighter in fighters:
        record = fighter.attr['record']
        for index, row in record.iterrows():
            '''
            take the opponent name and strip the extra shit off of 
            it so you can place it into a string and then search using the list 
            comprehension for the name of the opponent.
            
            '''
            opponent_name = row['opponent'].to_string()
            opponent_name = " ".join(re.findall("[a-zA-Z]+", opponent_name))
            
            
    opponent = [fighter for fighter in fighters if fighter.attr['name'] == opponent_name]