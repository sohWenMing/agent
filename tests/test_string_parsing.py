from string_parsing import join_with_space

def  test_join_with_space():
    words = [
        "this",
        "is",
        "a",
        "test",
    ]

    assert(join_with_space(words)) == "this is a test"