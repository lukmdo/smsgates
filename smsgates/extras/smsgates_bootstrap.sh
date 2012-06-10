alias sms='sendsms.py -g "$SMSGATES_SENDSMS_GATE" -l "$SMSGATES_SENDSMS_LOGIN" -p "$SMSGATES_SENDSMS_PASSWORD" -t $*';

function _sendsms_complete {
    local IFS=$'\n';
    local cur="${COMP_WORDS[COMP_CWORD]}";
    if [ -z "$cur" ]; then
        COMPREPLY=( $(sendsms.py -s|awk -F, '{print $1; print $2}'|sort -u|sed -e 's/ /\\ /') );
    else
        cur=$(echo -n "$cur"|tr -d '\\');
        COMPREPLY=( $(sendsms.py -s|awk -F, '{print $1; print $2}'|sort -u|grep -i "${cur}"|sed -e 's/ /\\ /') );
    fi
}

complete -o default -F _sendsms_complete sms;
