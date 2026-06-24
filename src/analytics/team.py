import pandas as pd 

# Each team winning percentage
def team_win_percentage(matches):
    #Each team win counts
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

#Total matches played
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
# Joining played and wins 
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

    result = result[result['matches_played'] >= 100]

    return (
        result
        .sort_values('win_pct',ascending = False)
    )

# Toss imapct 
def toss_impact(matches):

    #Both toss and match winner 
    toss_match_win = (
        matches[matches['toss_winner'] == matches['winner']
        ].shape[0]
    )

    #total matches 
    total_matches = matches.shape[0]

    #percentage of match toss winner
    pct = (
        toss_match_win / total_matches 
    )* 100

    return pct

# Venue analysis 
def highest_scoring_venues(matches, deliveries, top_n = 10):
    #innings score
    innings_score = (
        deliveries
        .groupby(['matchId','inning']) 
        .agg (
        {
            'batsman_runs': 'sum',
            'extras': 'sum'
        }).reset_index()
    )

# Innings total score 
    innings_score['total_score'] = (
        innings_score['batsman_runs'] + innings_score['extras']
    )

# rusn in venues 
    venue_score  = (
        innings_score.merge(
            matches[['matchId','venue']]
            ,on = 'matchId'
        ).groupby('venue')
        .agg(
            avg_score = ('total_score', 'mean'),
            innings_count = ('total_score', 'count')
        )
        .reset_index()
    )
    venue_score = venue_score[venue_score['innings_count'] >= 20]

    return (venue_score
    .sort_values('avg_score', ascending = False)
    .head(top_n)
    )

# Toss imapct 
def toss_impact(matches):
    toss_wins =(
        matches['toss_winner'] == matches['winner']
    ).sum()

    total_matches = (
        matches['winner'].notna().sum()
    )

    return round(
        toss_wins / total_matches * 100 ,2
    )

# venue toss impact 
def venue_toss_impact(matches, top_n = 10):

    temp = matches.copy()

    temp['toss_match_win'] = (
        temp['toss_winner'] == temp['winner']
    )

    venue_stats = (
        temp
        .groupby('venue')
        .agg(
            matches = ('matchId','count'),
            toss_match_win_pct = ('toss_match_win', 'mean')
        ).reset_index()
    )

    venue_stats['toss_match_win_pct'] = (
    venue_stats['toss_match_win_pct'] * 100
    ).round(2)

    venue_stats =(
        venue_stats[venue_stats['matches'] >= 10]
    )

    return (
        venue_stats.sort_values('toss_match_win_pct', ascending = False)
    ).head(top_n)