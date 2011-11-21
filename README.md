First:
    pip install -r requirements.txt
Then use smsgates/smsgate script:
    python smsgates/smsgate -l LOGIN -p PASSWORD MESSAGE_OR_STDIN
Add alias sugar:
    export sms_bob="python smsgates/smsgate -l LOGIN -p PASSWORD -n BOB_PHONE_NUMBER MESSAGE_OR_STDIN"
Then:
    echo "fun time!" | sms_bob


Or build your code using **smsgates**:

    from smsgates import MySMSGate

    with MySMSGate(login=l, password=p) as gate:
        gate.send(some_text)


List of supported gates:
- vodavone.ie
- ...yours?!


