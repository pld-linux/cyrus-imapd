%include	/usr/lib/rpm/macros.perl
Summary:	high-performance mail store with imap and pop3
Name:		cyrus-imapd
Version:	2.0.9
Release:	0.2
Copyright:	academic/research
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{name}-%{version}.tar.gz
Source1:	cyrus-README
Source2:	cyrus-procmailrc
Source3:	cyrus-deliver-wrapper.c
Source4:	cyrus-user-procmailrc.template
Source5:	%{name}-procmail+cyrus.mc
Source6:	%{name}.logrotate
Source7:	%{name}.conf
Source8:	%{name}.cron
Source9:	%{name}.pamd
Source10:	%{name}-pop.pamd
Source11:	%{name}.init
Source12:	cyrus.conf
Patch0:		%{name}-snmp.patch
Patch1:		%{name}-mandir.patch
URL:		http://andrew2.andrew.cmu.edu/cyrus/imapd/
#Icon:		cyrus.gif
BuildRequires:	cyrus-sasl-devel
#BuildRequires:	tcl-devel >= 8.0
BuildRequires:	openssl-devel
BuildRequires:	perl >= 5.6.0
BuildRequires:	db3-devel >= 3.1.17
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
The Cyrus IMAP server is a scaleable enterprise mail system designed
for use from small to large enterprise environments using
standards-based technologies.

A full Cyrus IMAP implementation allows a seamless mail and bulletin
board environment to be set up across multiple servers. It differs
from other IMAP server implementations in that it is run on "sealed"
servers, where users are not normally permitted to log in. The mailbox
database is stored in parts of the filesystem that are private to the
Cyrus IMAP system. All user access to mail is through software using
the IMAP, POP3, or KPOP protocols.

Note that this package can be used by ISPs and other to provide mail
services, but it may not be distributed as part of a commercial
product.

%description -l pl
Serwer Cyrus IMAP jest skalowalnym systemem e-mail dla
przedsiêbiorstwa, zaprojektowanym dla ma³ych i du¿ych firm i
wykorzystuj±cym oparte na standardach technologie.

Pe³na implementacja Cyrus IMAP pozwala na bezproblemowe ustawienie
¶rodowiska poczty i elektronicznej tablicy og³oszeniowej na kilku
serwerach. Tym siê ró¿ni od innych implementacji serwerów IMAP, ¿e
jest uruchamiany na "opieczêtowanych" serwerach, na które w normalnych
waunkach u¿ytkownicy nie mog± siê zalogowaæ. Baza danych skrzynek
pocztowych jest pzrechowywana w tych czê¶ciach systemu plików, które
s± dostêpne jedynie dla systemu IMAP Cyrus. Wszelki dostêp do poczty
ma miejsce poprzez oprogramowanie wykorzystuj±ce protoko³y IMAP, POP3
oraz KPOP.

Nale¿y zwróciæ uwagê na fakt, ¿e pakiet ten mo¿e byæ wykorzystywany
przez ISP, nie mo¿e byæ jednak rozpowszechniany jako czê¶æ
komercyjnego produktu.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1
%build
cd makedepend
autoconf
%configure 
%{__make}
export PATH=$PATH:`pwd`
cd ..
autoheader
autoconf
%configure \
	--with-auth=unix \
	--without-libwrap
%{__make}

%{__cc} $RPM_OPT_FLAGS -DLIBEXECDIR=\"%{_libexecdir}\" -s -Wall -o deliver-wrapper %{SOURCE3}

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{%{_sbindir},%{_libexecdir},%{_mandir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{logrotate.d,cron.daily,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/var/spool/imap/stage. \
	$RPM_BUILD_ROOT/var/lib/imap/{user,quota,proc,log,msg,deliverdb/db,sieve,db,socket} \
	$RPM_BUILD_ROOT/etc/{security,pam.d,rc.d/init.d}

touch $RPM_BUILD_ROOT/var/lib/imap/mailboxes \
	$RPM_BUILD_ROOT/var/lib/imap/faillog \
	$RPM_BUILD_ROOT/etc/security/blacklist.imap \
	$RPM_BUILD_ROOT/etc/security/blacklist.pop

%{__make} install DESTDIR=$RPM_BUILD_ROOT CYRUS_USER="`id -u`" CYRUS_GROUP="`id -g`" mandir=%{_mandir}

install deliver-wrapper $RPM_BUILD_ROOT%{_prefix}/cyrus/bin/deliver-wrapper

install %{SOURCE1}	.
install %{SOURCE2}	.
install %{SOURCE4}	.
install %{SOURCE5}	.
install %{SOURCE6}	$RPM_BUILD_ROOT/etc/logrotate.d/cyrus-imapd
install %{SOURCE7}	$RPM_BUILD_ROOT%{_sysconfdir}/imapd.conf
install %{SOURCE8}	$RPM_BUILD_ROOT/etc/cron.daily/cyrus-imapd
install %{SOURCE9}	$RPM_BUILD_ROOT/etc/pam.d/imap
install %{SOURCE10}	$RPM_BUILD_ROOT/etc/pam.d/pop
install %{SOURCE11}	$RPM_BUILD_ROOT/etc/rc.d/init.d/cyrus-imapd
install %{SOURCE12}	$RPM_BUILD_ROOT%{_sysconfdir}/cyrus.conf

mv $RPM_BUILD_ROOT%{_prefix}/cyrus/bin/*	$RPM_BUILD_ROOT%{_libexecdir}
mv $RPM_BUILD_ROOT%{_libexecdir}/master		$RPM_BUILD_ROOT%{_libexecdir}/cyrus-master

gzip -9nf cyrus-README cyrus-procmailrc	cyrus-user-procmailrc.template \
	cyrus-imapd-procmail+cyrus.mc

# make hashed dirs
oldpwd=`pwd`
cd $RPM_BUILD_ROOT/var
perl <<EOF
foreach \$i ("a".."z") 
{
  mkdir "lib/imap/user/\$i", 0755;
  mkdir "lib/imap/quota/\$i", 0755;
  mkdir "lib/imap/sieve/\$i", 0755;
  mkdir "spool/imap/\$i", 0755;
}
EOF
cd ${oldpwd}

%pre
if [ -z "`id -u cyrus 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 76 -r -d /var/spool/imap -s /bin/false -c "Cyrus User" -g mail cyrus 1>&2
fi

%post
/sbin/chkconfig --add cyrus-imapd
touch /var/lib/imap/faillog
chown cyrus.mail /var/lib/imap/faillog
chmod 640 /var/lib/imap/faillog
cd /var/lib/imap
chattr +S . user quota user/* quota/* 2>/dev/null
chattr +S /var/spool/imap /var/spool/imap/* 2>/dev/null
if [ -f /var/lock/subsys/cyrus-imapd ]; then
	/etc/rc.d/init.d/cyrus-imapd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/cyrus-imapd start\" to start apache http daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/cyrus-imapd ]; then
		/etc/rc.d/init.d/cyrus-imapd stop 1>&2
	fi
	/sbin/chkconfig --del cyrus-imapd
fi

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel cyrus
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.html
%config %{_sysconfdir}/*.conf
%attr(640,root,root) %config(noreplace) /etc/logrotate.d/cyrus-imapd
%attr(440,cyrus,root) %config(noreplace) %verify(not size md5 mtime) /etc/pam.d/*
%attr(754,root,root) /etc/rc.d/init.d/cyrus-imapd
%attr(640,cyrus,mail) %ghost /var/lib/imap/faillog
%attr(755,root,root) /etc/cron.daily/cyrus-imapd
%attr(755,root,root) %{_bindir}/*
%attr(4750,cyrus,mail) %{_libexecdir}/deliver
%attr(2755,cyrus,mail) %{_libexecdir}/deliver-wrapper
%attr(755,root,root) %{_libexecdir}/ctl_deliver
%attr(755,root,root) %{_libexecdir}/ctl_mboxlist
%attr(755,root,root) %{_libexecdir}/feedcyrus
%attr(755,root,root) %{_libexecdir}/fud
%attr(755,root,root) %{_libexecdir}/imapd
%attr(755,root,root) %{_libexecdir}/ipurge
%attr(755,root,root) %{_libexecdir}/lmtpd
%attr(755,root,root) %{_libexecdir}/cyrus-master
%attr(755,root,root) %{_libexecdir}/mbpath
%attr(755,root,root) %{_libexecdir}/pop3d
%attr(755,root,root) %{_libexecdir}/quota
%attr(755,root,root) %{_libexecdir}/reconstruct
%attr(755,root,root) %{_libexecdir}/timsieved

%dir %{perl_sitearch}/Cyrus
%{perl_sitearch}/Cyrus/*.pm
%dir %{perl_sitearch}/Cyrus/IMAP
%{perl_sitearch}/Cyrus/IMAP/*.pm
%dir %{perl_sitearch}/Cyrus/SIEVE
%{perl_sitearch}/Cyrus/SIEVE/*.pm
%dir %{perl_sitearch}/auto/Cyrus
%dir %{perl_sitearch}/auto/Cyrus/IMAP
%{perl_sitearch}/auto/Cyrus/IMAP/*.so
%{perl_sitearch}/auto/Cyrus/IMAP/*.bs
%dir %{perl_sitearch}/auto/Cyrus/SIEVE
%dir %{perl_sitearch}/auto/Cyrus/SIEVE/acap
%{perl_sitearch}/auto/Cyrus/SIEVE/acap/*.so
%{perl_sitearch}/auto/Cyrus/SIEVE/acap/*.bs
%dir %{perl_sitearch}/auto/Cyrus/SIEVE/managesieve
%{perl_sitearch}/auto/Cyrus/SIEVE/managesieve/*.so
%{perl_sitearch}/auto/Cyrus/SIEVE/managesieve/*.bs

%attr(750,cyrus,mail) /var/spool/imap
%attr(750,cyrus,mail) %dir /var/lib/imap
%attr(750,cyrus,mail) %dir /var/lib/imap/deliverdb
%attr(750,cyrus,mail) /var/lib/imap/deliverdb/db
%attr(750,cyrus,mail) /var/lib/imap/quota
%attr(750,cyrus,mail) /var/lib/imap/user
%attr(750,cyrus,mail) /var/lib/imap/sieve
%attr(750,cyrus,mail) /var/lib/imap/log
%attr(750,cyrus,mail) /var/lib/imap/msg
%attr(750,cyrus,mail) /var/lib/imap/proc
%attr(750,cyrus,mail) /var/lib/imap/db
%attr(750,cyrus,mail) /var/lib/imap/socket
%attr(750,cyrus,mail) %config(noreplace) %verify(not size md5 mtime) /var/lib/imap/mailboxes

%{_mandir}/man*/*
%{_includedir}/cyrus
%{_libdir}/lib*.a
