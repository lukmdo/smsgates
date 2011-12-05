First:

    pip install -r requirements.txt
    python setup.py install
    
Use **smsgate** script with some alias sugar:

    alias sms_bob='smsgate.py -g GATE -l LOGIN -p PASSWORD -n BOB_PHONE_NUMBER $*'

Where *GATE* can be on of:

* vodafone.ie
* orange.pl
* ...yours?!

Then:

    echo "fun time!" | sms_bob
    sms_bob "fun time!"
    sms_bob It also works:)

Or build your code using **smsgates**:

    from smsgates import MySMSGate

    with MySMSGate(login=l, password=p) as gate:
        gate.send(some_text)

Ideas:
======
* reading from vCard (Mac Address Book, Google Contacts) 
* bash completion
* listing gates
* listing contacts
* storing some metadata (when/what send to who) ? configurable default off