# smsgates project 

## First:

```bash
pip install -r requirements.pip
python setup.py install
python setup.py test
```

## Then make most from **sendsms** script:

For most flexibility export your contacts (from [Google Contacts](https://www.google.com/contacts) or [Apple Adress Book](http://support.apple.com/kb/HT2486)
in _vCard_ to ```$HOMEDIR/Documents/contacts.vcf```). Then add that to your ```.bashrc```:

```bash
SMSGATES_BOOTSTRAP=`which smsgates_bootstrap.sh`
if [ "$?" -eq "0" ]; then
  export SMSGATES_SENDSMS_GATE="GATENAME"
  export SMSGATES_SENDSMS_LOGIN="LOGIN"
  export SMSGATES_SENDSMS_PASSWORD="PASSWORD"
  source "$SMSGATES_BOOTSTRAP"
fi
```

Send __bob__ sms with name TAB completion:

```bash
sms b+TAB
sms bob MSG
echo "fun time!" |sms bob
```

For more see ```sendsms.py -h```

## Or build your code using **smsgates**:

```python
from smsgates.contrib import MySMSGate

with MySMSGate(login=l, password=p) as gate:
    gate.send(some_text, number)
```

## Your mobile provider has poor/None sms gate ...maybe [twilio.com](http://www.twilio.com) is for you

[Twilio](https://www.twilio.com) looks as nice option [if you don't mind paying few $](https://www.twilio.com/sms/pricing).
Just [create an account](https://www.twilio.com/login) and kick:

```
pip install -r provider_requirements/twilio_requirements.pip
```

An then pass:
- ```--gate_name``` as __twilio.com__
- ```--sender``` as your number
- ```--login``` as your account sid
- ```--password``` as your account token

### Ideas:

- speedup vCard contacts parsing ?
- listing gates
- storing some metadata (when/what send to who) ? configurable default off
- support contact groups
- automate grabbing google contacts ?