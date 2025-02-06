from assertpy import assert_that

def assert_status_code(response, expected_status):
    assert_that(response.status_code).is_equal_to(expected_status)

def assert_contains_key(json_response, key):
    assert_that(json_response).contains_key(key)

def assert_equal(actual, expected):
    assert_that(actual).is_equal_to(expected)

def assert_not_equal(actual, expected):
    assert_that(actual).is_not_equal_to(expected)

def assert_created_time(actual, expected, ignore_microseconds=True):
    actual = actual.replace(microsecond=0)
    expected = expected.replace(microsecond=0)

    assert_that(actual).is_equal_to(expected, ignore_microseconds=ignore_microseconds)