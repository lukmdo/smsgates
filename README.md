# smsgates project [![status](http://stillmaintained.com/ssspiochld/smsgates.png)](http://stillmaintained.com/ssspiochld/smsgates)

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

### Ideas:

- speedup vCard contacts parsing ?
- listing gates
- storing some metadata (when/what send to who) ? configurable default off
- support contact groups
- automate grabbing google contacts ?
- [twilio support](http://www.twilio.com/)