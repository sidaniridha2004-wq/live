from app.core.normalize import normalize_text

def test_normalize():
    assert normalize_text('PSG') == 'paris saint-germain'
    assert normalize_text('  man utd ') == 'manchester united'
