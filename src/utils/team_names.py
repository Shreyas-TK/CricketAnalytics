TEAM_MAPPING = {
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
    'Kings XI Punjab' : 'Punjab Kings',
    'Delhi Daredevils' : 'Delhi Capitals',
    'Rising Pune Supergiants' : 'Rising Pune Supergiant',
    'Pune Warriors' : 'Rising Pune Supergiant'

}

def standardize_team_names(matches):
    
    matches = matches.copy()
    
    cols = [
        'team1',
        'team2',
        'winner',
        'toss_winner'
    ]

    for col in cols:
        matches[col] = matches[col].replace(TEAM_MAPPING)
    
    return matches