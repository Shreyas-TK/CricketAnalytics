import pandas as pd 

def team_win_percentage(matches):
    wins = (
        matches["winner"]
        .value_counts()
        .reset_index()
    )

    wins.columns =[
        'team',
        'wins'
    ]

    team1 = matches['team1'].value_counts()
    team2 = matches['team2'].value_counts()

    played = (
        team1.add(
            team2,
            fill_value=0
        )
        .reset_index()
    )

    played.columns =[
        'team',
        'matches_played'
    ]

    result = played.merge(
        wins,
        on = 'team',
        how = 'left'
    )

    result['wins'] = (
        result['wins'].fillna(0)
    )

    result['win_pct'] = (
        result['wins']/
        result['matches_played']
    )*100

    return (
        result
        .sort_values('win_pct',ascending = False)
    )


