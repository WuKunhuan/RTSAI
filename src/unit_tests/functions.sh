
# An example of shell script unit test: 

# #!/usr/bin/expect -f
# spawn ./your_script.sh
# expect "Please enter your name:"
# send "John Doe\r"
# expect "Hello, John Doe! How are you today?"

# ————————————————————————

expect_equal() {
    actual_value=$1
    expected_value=$2
    testcase_name=$3
    if [[ "$expected_value" == "$actual_value" ]]; then
        return 0
    else
        echo "expect_equal: $testcase_name: FAILED"
        echo "-   actual:   '$actual_value'"
        echo "-   expected: '$expected_value'"
        return 1
    fi
}

expect_not_equal() {
    actual_value=$1
    expected_value=$2
    testcase_name=$3
    if [[ "$expected_value" != "$actual_value" ]]; then
        return 0
    else
        echo "expect_equal: $testcase_name: FAILED"
        echo "-   actual:   '$actual_value'"
        echo "-   expected: '$expected_value'"
        return 1
    fi
}

assert_equal() {
    expected_value=$1
    actual_value=$2
    testcase_name=$3
    if [[ "$expected_value" == "$actual_value" ]]; then
        return 0
    else
        echo "assert_equal: $testcase_name: FAILED"; 
        echo "-   actual:   '$actual_value'"
        echo "-   expected: '$expected_value'"
        echo ""
        echo "$test_name FAILED"
        exit 1
    fi
}

assert_not_equal() {
    expected_value=$1
    actual_value=$2
    testcase_name=$3
    if [[ "$expected_value" != "$actual_value" ]]; then
        return 0
    else
        echo "assert_equal: $testcase_name: FAILED"; 
        echo "-   actual:   '$actual_value'"
        echo "-   expected: '$expected_value'"
        echo ""
        echo "$test_name FAILED"
        exit 1
    fi
}

# ————————————————————————

