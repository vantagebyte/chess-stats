from tilt import split_sittings, longest_streaks

def test_split_sittings():
    games = [
        (1000, 1200, 'win'),
        (1300, 1500, 'loss'),   
        (3000, 3200, 'win'),    
            ]
    assert split_sittings(games) == [['win', 'loss'], ['win']]
    
def test_longest_streaks():
    sittings = [['loss', 'loss', 'draw', 'loss', 'win']]
    assert longest_streaks(sittings) == {'win': 1, 'loss': 2, 'winless': 4}
    