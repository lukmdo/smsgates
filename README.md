First:

    pip install -r requirements.txt
    python setup.py install
    
Use **smsgate** script with some alias sugar:

    alias sms_bob="smsgate -l LOGIN -p PASSWORD -n BOB_PHONE_NUMBER $*"

Then:

    echo "fun time!" | sms_bob


Or build your code using **smsgates**:

    from smsgates import MySMSGate

    with MySMSGate(login=l, password=p) as gate:
        gate.send(some_text)


List of supported gates:
- vodavone.ie
- ...yours?!


