date -u +%FT%TZ
grep '^user:' /etc/passwd
grep -E '^(wheel|netdev|users):' /etc/group
[ "$(grep '^user:' /etc/shadow | cut -d: -f2)" = '$6$cal1122$ZIs03fvnBPSkasZ1B2RLSUt5dtUPGWVefzUbzC/CFnMSXK4xzJO5MQW1e3hyUIucJpFf/YLlootGG36zQ6EqB0' ] && echo "password hash: equal to declared" || echo "password hash: different"
