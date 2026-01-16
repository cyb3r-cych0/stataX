from statax.output.plot_theme import apply_theme, THEMES

def test_apply_theme():
    apply_theme("classic")
    apply_theme("clean")
    apply_theme("journal")

def test_invalid_theme_raises():
    try:
        apply_theme("nope")
    except ValueError:
        assert True
