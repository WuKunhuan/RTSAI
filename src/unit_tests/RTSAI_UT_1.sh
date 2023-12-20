
# ————————————————————————

source functions
test_name="RTSAI Unit Test 1"
test_status=0

# ————————————————————————

# Call RTSAI
output=$(RTSAI)
expected="Welcome to the world of RTSAI! "
expect_equal "$output" "$expected" "RTSAI hello world"
if [[ $? -eq 1 ]]; then
    test_status=1
fi

# ————————————————————————

if [[ $test_status -eq 0 ]]; then
    echo "$test_name SUCCESS"
else
    echo ""
    echo "$test_name FAILED"
fi

