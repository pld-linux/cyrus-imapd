Summary:	high-performance mail store with imap and pop3
Name:		cyrus-imapd
Version:	1.6.22
Release:	0.2
Copyright:	academic/research
Group:		Networking/Daemons
Source0:	ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{name}-%{version}.tar.gz
Source1:	cyrus-README
Source2:	cyrus-procmailrc
Source3:	cyrus-deliver-wrapper.c
Source4:	cyrus-user-procmailrc.template
Source5:	cyrus-imapd-procmail+cyrus.mc
Source6:	cyrus-imapd.logrotate
Source7:	cyrus-imapd.conf
Source8:	cyrus-imapd.cron
Source9:	cyrus-imapd.inetd
Source10:	cyrus-imapd-pop3.inetd
Source11:	cyrus-imapd.pamd
Source12:	cyrus-imapd-pop.pamd
URL:		http://andrew2.andrew.cmu.edu/cyrus/imapd/
#Icon:		cyrus.gif
BuildRequires:	cyrus-sasl-devel
BuildRequires:	tcl-devel >= 8.0
BuildRequires:	openssl-devel
Obsoletes:	imapd
Obsoletes:	pop3daemon
Obsoletes:	imapdaemon
Conflicts:	qpopper
Conflicts:	solid-pop3d
Conflicts:	qpopper6
Provides:	imapdaemon
Provides:	pop3daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_prefix}/lib/cyrus

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

%description -l pl
Serwer Cyrus IMAP jest skalowalnym systemem e-mail dla przedsiêbiorstwa,
zaprojektowanym dla ma³ych i du¿ych firm i wykorzystuj±cym oparte na
standardach technologie.

Pe³na implementacja Cyrus IMAP pozwala na bezproblemowe ustawienie
¶rodowiska poczty i elektronicznej tablicy og³oszeniowej na kilku serwerach.
Tym siê ró¿ni od innych implementacji serwerów IMAP, ¿e jest uruchamiany
na "opieczêtowanych" serwerach, na które w normalnych waunkach u¿ytkownicy
nie mog± siê zalogowaæ. Baza danych skrzynek pocztowych jest pzrechowywana 
w tych czê¶ciach systemu plików, które s± dostêpne jedynie dla systemu
IMAP Cyrus. Wszelki dostêp do poczty ma miejsce poprzez oprogramowanie
wykorzystuj±ce protoko³y IMAP, POP3 oraz KPOP.

Nale¿y zwróciæ uwagê na fakt, ¿e pakiet ten mo¿e byæ wykorzystywany przez ISP,
nie mo¿e byæ jednak rozpowszechniany jako czê¶æ komercyjnego produktu.

%define version %{PACKAGE_VERSION}

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q 

%build

# prepare a makedepend
cd makedepend
autoconf
%configure 
make
export PATH=$PATH:`pwd`
cd ..
autoconf
%configure \
	--with-auth=unix
make

gcc $RPM_OPT_FLAGS -DLIBEXECDIR=\"%{_libexecdir}\" -s -Wall -o deliver-wrapper %{SOURCE3}

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT/usr/cyrus/etc 
install -d \
	$RPM_BUILD_ROOT{%{_sbindir},%{_libexecdir},%{_mandir}} \
	$RPM_BUILD_ROOT/etc/{logrotate.d,cron.daily,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/var/spool/imap/stage. \
	$RPM_BUILD_ROOT/var/lib/imap/{user,quota,proc,log,msg,deliverdb,sieve} \
	$RPM_BUILD_ROOT%{_libdir}/sendmail-cf/cf 
touch $RPM_BUILD_ROOT/var/lib/imap/mailboxes \
	$RPM_BUILD_ROOT/var/lib/imap/faillog \
	$RPM_BUILD_ROOT/etc/security/blacklist.imap \
	$RPM_BUILD_ROOT/etc/security/blacklist.pop

make install DESTDIR=$RPM_BUILD_ROOT CYRUS_USER="`id -u`" CYRUS_GROUP="`id -g`"

#mkdir -p $RPM_BUILD_ROOT/usr/cyrus/bin
#install -g mail -m 2755 -s deliver-wrapper $RPM_BUILD_ROOT/usr/cyrus/bin/deliver-wrapper
install deliver-wrapper $RPM_BUILD_ROOT/usr/cyrus/bin/deliver-wrapper

install %{SOURCE1} .
install %{SOURCE2} $RPM_BUILD_ROOT/etc/procmailrc.cyrus
#install %{SOURCE4} $RPM_BUILD_ROOT/usr/cyrus/etc/user-procmailrc.template
install %{SOURCE5} $RPM_BUILD_ROOT%{_libdir}/sendmail-cf/cf/procmail+cyrus.mc
install %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/cyrus-imapd
install %{SOURCE7} $RPM_BUILD_ROOT/etc/imapd.conf
install %{SOURCE8} $RPM_BUILD_ROOT/etc/cron.daily/cyrus-imapd
install %{SOURCE9} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/imapd
install %{SOURCE10} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/pop3d
install %{SOURCE11} $RPM_BUILD_ROOT/etc/pam.d/imap
install %{SOURCE12} $RPM_BUILD_ROOT/etc/pam.d/pop

mv $RPM_BUILD_ROOT/usr/cyrus/bin/* 	$RPM_BUILD_ROOT%{_libexecdir}
mv $RPM_BUILD_ROOT/usr/man/*		$RPM_BUILD_ROOT%{_mandir}

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man*/* \
	cyrus-README

# make hashed dirs
cd $RPM_BUILD_ROOT/var
/usr/bin/perl <<EOF
foreach \$i ("a".."z") 
{
  mkdir "lib/imap/user/\$i", 0755;
  mkdir "lib/imap/quota/\$i", 0755;
  mkdir "lib/imap/sieve/\$i", 0755;
  mkdir "spool/imap/\$i", 0755;
}
EOF

%pre
if [ -z "`id -u cyrus 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 76 -r -d /var/spool/imap -s /bin/false -c "Cyrus User" -g mail cyrus 1>&2
	if [ -f /var/db/passwd.db ]; then
		/usr/bin/update-db 1>&2
	fi
fi

%post
touch /var/lib/imap/faillog
chown cyrus.mail /var/lib/imap/faillog
chmod 640 /var/lib/imap/faillog
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

# force synchronous updates
cd /var/lib/imap
chattr +S . user quota user/* quota/* 2>/dev/null
chattr +S /var/spool/imap /var/spool/imap/* 2>/dev/null

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi
if [ "$1" = "0" ]; then
	if [ -n "`id -u cyrus 2>/dev/null`" ]; then
		/usr/sbin/userdel cyrus 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#doc README README.RPM doc
%doc doc/html/*.html

%config /etc/imapd.conf
%config /etc/procmailrc.cyrus
%config(noreplace) %verify(not size md5 mtime) /etc/logrotate.d/cyrus-imapd
%attr( 640, root,root) %config(noreplace) %verify(not size md5 mtime) /etc/sysconfig/rc-inetd/*
%attr( 440, cyrus,root) %config(noreplace) %verify(not size md5 mtime) /etc/pam.d/*
%attr( 640, cyrus,mail) %ghost /var/lib/imap/faillog
%attr( 755, root,root) /etc/cron.daily/cyrus-imapd
%attr( 755, root,root) %{_bindir}/*
%attr(4750,cyrus,mail) %{_libexecdir}/deliver
%attr(2755,cyrus,mail) %{_libexecdir}/deliver-wrapper
%attr( 755, root,root) %{_libexecdir}/arbitron
%attr( 755, root,root) %{_libexecdir}/collectnews
%attr( 755, root,root) %{_libexecdir}/dump_deliverdb
%attr( 755, root,root) %{_libexecdir}/feedcyrus
%attr( 755, root,root) %{_libexecdir}/fud
%attr( 755, root,root) %{_libexecdir}/mbpath
%attr( 755, root,root) %{_libexecdir}/quota
%attr( 755, root,root) %{_libexecdir}/reconstruct
%attr( 755, root,root) %{_libexecdir}/syncnews
%attr( 755, root,root) %{_libexecdir}/timsieved
%attr( 755, root,root) %{_libexecdir}/pop3d
%attr( 755, root,root) %{_libexecdir}/imapd

#%attr(0755,root,root) %{_sbindir}/imapd
#%attr(0755,root,root) %{_sbindir}/ipop3d

%defattr(640,cyrus,mail,750)
/var/spool/imap
%dir /var/lib/imap
/var/lib/imap/deliverdb
/var/lib/imap/quota
/var/lib/imap/user
/var/lib/imap/sieve
/var/lib/imap/log
/var/lib/imap/msg
/var/lib/imap/proc
%config(noreplace) %verify(not size md5 mtime) /var/lib/imap/mailboxes
%defattr(644,root,root,755)

%{_mandir}/man*/*

%{_includedir}/cyrus
%{_libdir}/lib*.a
