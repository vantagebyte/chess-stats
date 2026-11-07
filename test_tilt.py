from tilt import split_sittings

def test_split_sittings():
    games = [
        (1000, 1200, 'win'),
        (1300, 1500, 'loss'),   
        (3000, 3200, 'win'),    
            ]
    assert split_sittings(games) == [['win', 'loss'], ['win']]