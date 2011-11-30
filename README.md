# smsgates project [![status](http://stillmaintained.com/ssspiochld/smsgates.png)](http://stillmaintained.com/ssspiochld/smsgates)

## First:

```bash
pip install -r requirements.pip
python setup.py install
python setup.py test
```

## Then make most of **sendsms** script:

For most flexibility export your :book: contacts (from Google Contacts or Adress Book
in **vCard** to ```$HOMEDIR/Documents/contacts.vcf```). Then add that to your ```.bashrc``` or ```.bash_profile```:

```bash
alias sms='sendsms.py -g GATE -l LOGIN -p PASSWORD -t $*'
```

Where **GATE** can be on of:

* vodafone.ie
* orange.pl
* ...yours?!

```bash
function _sendsms_complete {
    local IFS=$'\n'
    local cur="${COMP_WORDS[COMP_CWORD]}"
    if [ -z "$cur" ]; then
        COMPREPLY=( $(sendsms.py -s|awk -F, '{print $1; print $2}'|sort -u|sed -e 's/ /\\ /') )
    else
        local cur=`echo -n $cur|tr -d '\'`
        COMPREPLY=( $(sendsms.py -s|awk -F, '{print $1; print $2}'|sort -u|grep -i ${cur}|sed -e 's/ /\\ /') )
    fi
}
complete -o default -F _sendsms_complete sms
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

* speedup vCard contacts parsing ?
* listing gates
* storing some metadata (when/what send to who) ? configurable default off
* adding contact groups
