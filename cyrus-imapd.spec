Summary:	high-performance mail store with imap and pop3
Name:		cyrus-imapd
Version:	1.5.19
Release:	2
Copyright:	academic/research
Group:		Networking/Daemons
Source0:	ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{name}-v%{version}.tar.gz
Source1:	cyrus-README
Source2:	cyrus-procmailrc
Source3:	cyrus-deliver-wrapper.c
Source4:	cyrus-user-procmailrc.template
Source5:	cyrus-redhat-procmail+cyrus.mc
Source6:	cyrus-imapd.logrotate
URL:		http://andrew2.andrew.cmu.edu/cyrus/imapd/
Icon:		cyrus.gif
Buildroot:	/tmp/%{name}-%{version}-root

%description
The Cyrus IMAP server is a scaleable enterprise mail system
designed for use from small to large enterprise environments using
standards-based technologies.

A full Cyrus IMAP implementation allows a seamless mail and bulletin
board environment to be set up across multiple servers. It differs from
other IMAP server implementations in that it is run on "sealed"
servers, where users are not normally permitted to log in. The mailbox
database is stored in parts of the filesystem that are private to the
Cyrus IMAP system. All user access to mail is through software using
the IMAP, POP3, or KPOP protocols.

Note that this package can be used by ISPs and other to provide mail
services, but it may not be distributed as part of a commercial product.

%define version %{PACKAGE_VERSION}

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n cyrus-imapd-v%{version}

%build
if [ ! -d %{_libdir}/sendmail-cf/cf ] ; then
  echo Need full sendmail-cf installation
  exit -1
fi

# prepare a makedepend
cd makedepend
%configure 
make
export PATH=$PATH:`pwd`
cd ..
# now go ahead
# I hope one day there is --with-login=pam :-)
./configure %{_target_platform} \
	--with-tcl=/usr \
	--prefix=/usr \
	--with-login=unix
make

gcc -Wall -o deliver-wrapper $RPM_SOURCE_DIR/cyrus-deliver-wrapper.c

%install
# First create the 'cyrus' user if it doesn't exist
grep ^cyrus: /etc/passwd >/dev/null || {
  echo 'cyrus:*:76:12:cyrus:/var/imap:/bin/bash' >>/etc/passwd
}

cp -p $RPM_SOURCE_DIR/cyrus-README $RPM_BUILD_DIR/cyrus-imapd-v%{version}/README.RPM

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/cyrus/bin
install -g mail -m 2755 -s deliver-wrapper $RPM_BUILD_ROOT/usr/cyrus/bin/deliver-wrapper

mkdir -p $RPM_BUILD_ROOT/etc
cat <<END >$RPM_BUILD_ROOT/etc/imapd.conf
configdirectory: /var/imap
partition-default: /var/spool/imap
admins: root
allowanonymouslogin: no
END

cp -p $RPM_SOURCE_DIR/cyrus-procmailrc $RPM_BUILD_ROOT/etc/procmailrc.cyrus
mkdir -p $RPM_BUILD_ROOT/usr/cyrus/etc
cp -p $RPM_SOURCE_DIR/cyrus-user-procmailrc.template $RPM_BUILD_ROOT/usr/cyrus/etc/user-procmailrc.template

mkdir $RPM_BUILD_ROOT/etc/logrotate.d
install %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/cyrus-imapd

mkdir $RPM_BUILD_ROOT/etc/cron.daily
cat <<END >$RPM_BUILD_ROOT/etc/cron.daily/cyrus-imapd
#!/bin/bash
su cyrus -s /bin/bash -c '/usr/cyrus/bin/deliver -E 3'
END
chmod +x $RPM_BUILD_ROOT/etc/cron.daily/cyrus-imapd

mkdir -p $RPM_BUILD_ROOT/var
cd $RPM_BUILD_ROOT/var
mkdir -p imap
chown cyrus:mail imap
chmod 750 imap

cd imap
true >> mailboxes
mkdir user quota proc log msg deliverdb
chown cyrus:mail *

mkdir -p $RPM_BUILD_ROOT/var/spool
cd $RPM_BUILD_ROOT/var/spool
mkdir -p imap
chown cyrus:mail imap
chmod 750 imap

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
ln -s ../cyrus/bin/imapd $RPM_BUILD_ROOT%{_sbindir}/imapd
ln -s ../cyrus/bin/pop3d $RPM_BUILD_ROOT%{_sbindir}/ipop3d

mkdir -p $RPM_BUILD_ROOT%{_libdir}/sendmail-cf/cf
cp -p $RPM_SOURCE_DIR/cyrus-redhat-procmail+cyrus.mc $RPM_BUILD_ROOT%{_libdir}/sendmail-cf/cf/redhat-procmail+cyrus.mc
cd %{_libdir}/sendmail-cf/cf
mkdir -p $RPM_BUILD_ROOT/usr/cyrus/etc
m4 < $RPM_SOURCE_DIR/cyrus-redhat-procmail+cyrus.mc > $RPM_BUILD_ROOT%{_libdir}/sendmail-cf/cf/redhat-procmail+cyrus.cf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# create the 'cyrus' user if it doesn't exist
grep ^cyrus: /etc/passwd >/dev/null || {
  echo 'cyrus:*:76:12:cyrus:/var/imap:/bin/bash' >>/etc/passwd
}

%post
# update syslog
grep ^local6 /etc/syslog.conf >/dev/null || {
  echo "local6.debug						/var/log/imapd.log" >>/etc/syslog.conf
  killall -1 syslogd 2>/dev/null
}
touch /var/log/imapd.log
chmod 640 /var/log/imapd.log

# update inetd to run as user 'cyrus'
sed '/^imap/s/root/cyrus/;/^pop-3/s/root/cyrus/' </etc/inetd.conf >/etc/inetd.conf.tmp &&
mv /etc/inetd.conf.tmp /etc/inetd.conf &&
killall -1 inetd 2>/dev/null

# force synchronous updates
cd /var/imap
chattr +S . user quota 2>/dev/null
chattr +S /var/spool/imap 2>/dev/null

cd /etc
# make backup copy of sendmail.cf if we've got a pre-cyrus cf file
if grep -q cyrus /etc/sendmail.cf ; then
  echo not updating cyrus-aware sendmail.cf
else
  cp sendmail.cf mail/sendmail-pre-cyrus-backup.cf
  echo made backup of sendmail.cf in mail/sendmail-pre-cyrus-backup.cf
  cp %{_libdir}/sendmail-cf/cf/redhat-procmail+cyrus.cf /etc/sendmail.cf
  echo installed cyrus-aware sendmail.cf
  # signal sendmail
  if [ -f /var/run/sendmail.pid ]; then
    /etc/rc.d/init.d/sendmail restart
  fi
fi

%preun
# try to revert to pre-cyrus sendmail.cf
if [ -f /etc/mail/sendmail-pre-cyrus-backup.cf ] ; then
  cd /etc
  cp sendmail.cf mail/sendmail-post-cyrus-backup.cf
  echo made backup of sendmail.cf in mail/sendmail-post-cyrus-backup.cf
  mv mail/sendmail-pre-cyrus-backup.cf sendmail.cf
  echo reverted to pre-cyrus sendmail.cf
  grep -q ^cyrus: /etc/passwd >/dev/null && \
    grep -v ^cyrus: /etc/passwd >/etc/passwd.tmp && \
      mv /etc/passwd.tmp /etc/passwd
  # signal sendmail
  if [ -f /var/run/sendmail.pid ]; then
    /etc/rc.d/init.d/sendmail restart
  fi
else
  echo No pre-cyrus sendmail.cf backup available.
  echo You will have to install a new sendmail.cf and
  echo remove the cyrus-user manually.
fi

# put the inetd config file back to normal
sed '/^imap/s/cyrus/root/;/^pop-3/s/cyrus/root/' </etc/inetd.conf >/etc/inetd.conf.tmp &&
mv /etc/inetd.conf.tmp /etc/inetd.conf &&
killall -1 inetd 2>/dev/null

%files

%doc README README.RPM doc

# build roots are your friend - if only they would exclude /usr/doc!
%config /etc/imapd.conf
%config /etc/procmailrc.cyrus
/etc/logrotate.d
/etc/cron.daily/*
%{_bindir}/*
/usr/cyrus
%{_includedir}
%{_libdir}
%{_mandir}/man*/*
%{_sbindir}/*
/var
