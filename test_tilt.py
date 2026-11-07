from tilt import split_sittings, longest_streaks, results_after, results_by_streak

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

def test_results_after():
    sittings = [['win', 'loss', 'loss', 'draw', 'win'], ['loss', 'win']]
    assert results_after(sittings) == {
        'win':  {'win': 0, 'loss': 1, 'draw': 0},
        'loss': {'win': 1, 'loss': 1, 'draw': 1},
        'draw': {'win': 1, 'loss': 0, 'draw': 0},
    }

def test_results_by_streak():
    sittings = [['win', 'loss', 'loss', 'loss', 'loss', 'win']]
    assert results_by_streak(sittings) == {
        ('win', 1):  {'win': 0, 'loss': 1, 'draw': 0},
        ('loss', 1): {'win': 0, 'loss': 1, 'draw': 0},
        ('loss', 2): {'win': 0, 'loss': 1, 'draw': 0},
        ('loss', 3): {'win': 1, 'loss': 1, 'draw': 0},
    }
