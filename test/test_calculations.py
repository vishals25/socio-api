from app.calculations import add

def test_add():
    print("testing")
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2
    assert add(1, -1) == 0

test_add()