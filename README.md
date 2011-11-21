First:

    pip install -r requirements.txt

Then use smsgates/smsgate script:

    python smsgates/smsgate -l LOGIN -p PASSWORD MESSAGE_OR_STDIN

Or build your code using **smsgates**:

    from smsgates import MySMSGate

    with MySMSGate(login=l, password=p) as gate:
        gate.send(some_text)


List of supported gates:
- vodavone.ie
- ...yours?!
