divert(-1)
include(`../m4/cf.m4')
define(`confDEF_USER_ID',``8:12'')
OSTYPE(`linux')
undefine(`UUCP_RELAY')
undefine(`BITNET_RELAY')
FEATURE(redirect)
FEATURE(always_add_domain)
FEATURE(use_cw_file)
FEATURE(local_procmail)
define(`CYRUS_MAILER_FLAGS',`Aw5:/|@o')
define(`confLOCAL_MAILER',`cyrus')
dnl # Note: CYUSER isn't needed, but must put $u in mailer args otherwise
dnl # it uses SMTP for delivery!
define(`CYRUS_MAILER_ARGS', `procmail -p /etc/procmailrc.cyrus CYUSER=$u')
define(`CYRUS_MAILER_PATH', `/usr/bin/procmail')
MAILER(cyrus)
MAILER(procmail)
MAILER(smtp)
HACK(check_mail3,`hash -a@JUNK /etc/mail/deny')
HACK(use_ip,`/etc/mail/ip_allow')
HACK(use_names,`/etc/mail/name_allow')
HACK(use_relayto,`/etc/mail/relay_allow')
HACK(check_rcpt4)
HACK(check_relay3)
dnl Not yet tested...
dnl LOCAL_RULE_0
dnl Rbb + $+ < @ $=w . >	$#cyrusbb $: $1
