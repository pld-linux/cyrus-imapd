%include	/usr/lib/rpm/macros.perl
Summary:	High-performance mail store with imap and pop3
Summary(pl):	Wysoko wydajny serwer IMAP i POP3
Summary(pt_BR):	Um servidor de mail de alto desempenho que suporta IMAP e POP3
Name:		cyrus-imapd
Version:	2.0.17
Release:	3
License:	BSD-like
Group:		Networking/Daemons
Source0:	ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{name}-%{version}.tar.gz
# Source0-md5:	21a666e8bf41be5169ede375309f6e94
Source1:	cyrus-README
Source2:	cyrus-procmailrc
Source3:	cyrus-deliver-wrapper.c
Source4:	cyrus-user-procmailrc.template
Source5:	%{name}-procmail+cyrus.mc
Source6:	%{name}.logrotate
Source7:	%{name}.conf
Source9:	%{name}.pamd
Source10:	%{name}-pop.pamd
Source11:	%{name}.init
Source12:	cyrus.conf
Patch0:		%{name}-snmp.patch
Patch1:		%{name}-mandir.patch
Patch2:		%{name}-paths.patch
Patch3:		%{name}-overquota.patch
# http://www.imasy.or.jp/~ume/ipv6/cyrus-imapd-2.0.17-ipv6-20021205.diff.gz
Patch4:		%{name}-2.0.17-ipv6-20021205.diff.gz
Patch5:		%{name}-et.patch
Patch6:		%{name}-ac250.patch
Patch7:		%{name}-db3.patch
Patch8:		%{name}-ipv6.m4.patch
Patch9:		%{name}-ac25x.patch
Patch10:	%{name}-snprintf.patch
Patch11:	%{name}-CAN-2004-101x.patch
URL:		http://andrew2.andrew.cmu.edu/cyrus/imapd/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 1.5.27
BuildRequires:	db3-devel >= 3.1.17
BuildRequires:	e2fsprogs-devel >= 1.21
BuildRequires:	flex
BuildRequires:	openssl-devel >= 0.9.6m
BuildRequires:	perl-devel >= 5.6.1
BuildRequires:	ucd-snmp-devel >= 4.2.6
PreReq:		rc-scripts
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Provides:	imapdaemon
Provides:	pop3daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	courier-imap
Conflicts:	courier-imap-common
Conflicts:	courier-imap-pop3
Conflicts:	imap
Conflicts:	imap-common
Conflicts:	imap-pop2
Conflicts:	imap-pop3
Conflicts:	qpopper
Conflicts:	qpopper6
Conflicts:	solid-pop3d
Conflicts:	tpop3d
Obsoletes:	imapd
Obsoletes:	imap
Obsoletes:	pop3daemon
Obsoletes:	imapdaemon

%define		_libexecdir	%{_prefix}/lib/cyrus

%description
The Cyrus IMAP server is a scalable enterprise mail system designed
for use from small to large enterprise environments using
standards-based technologies.

A full Cyrus IMAP implementation allows a seamless mail and bulletin
board environment to be set up across multiple servers. It differs
from other IMAP server implementations in that it is run on "sealed"
servers, where users are not normally permitted to log in. The mailbox
database is stored in parts of the filesystem that are private to the
Cyrus IMAP system. All user access to mail is through software using
the IMAP, POP3, or KPOP protocols.

%description -l pl
Serwer Cyrus IMAP jest skalowalnym systemem e-mail dla
przedsiêbiorstwa, zaprojektowanym dla ma³ych i du¿ych firm i
wykorzystuj±cym oparte na standardach technologie.

Pe³na implementacja Cyrus IMAP pozwala na bezproblemowe ustawienie
¶rodowiska poczty i elektronicznej tablicy og³oszeniowej na kilku
serwerach. Tym siê ró¿ni od innych implementacji serwerów IMAP, ¿e
jest uruchamiany na "opieczêtowanych" serwerach, na które w normalnych
waunkach u¿ytkownicy nie mog± siê zalogowaæ. Baza danych skrzynek
pocztowych jest przechowywana w tych czê¶ciach systemu plików, które
s± dostêpne jedynie dla systemu IMAP Cyrus. Wszelki dostêp do poczty
ma miejsce poprzez oprogramowanie wykorzystuj±ce protoko³y IMAP, POP3
oraz KPOP.

%description -l pt_BR
O servidor IMAP Cyrus é um sistema de mail corporativo escalável
projetado para uso por pequenos a grandes ambientes corporativos
usando tecnologias baseadas em padrões abertos.

Uma implementação completa do Cyrus permite se configurar um ambiente
transparente de mail e bulletin board entre múltiplos servidores. Ele
difere de outros servidores IMAP por rodar em servidores "selados",
onde usuários não possuem normalmente a permissão de log in. O banco
de dados de caixas de mail é armazenado em partes do sistema de
arquivos que são privativos do sistema Cyrus. Todo o acesso de
usuários aos mails se dá através de software usando os protocolos
IMAP, POP3 ou KPOP.

%package devel
Summary:	Libraries and include files for developing with cyrus-imapd
Summary(pl):	Pliki potrzebne do programowania z u¿yciem cyrus-imapd
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with cyrus-imapd.

%description devel -l pl
Ten pakiet zawiera biblioteki oraz pliki nag³ówkowe niezbêdne do
tworzenia oprogramowania z wykorzystaniem cyrus-imapd.

%package static
Summary:	Static cyrus-imapd libraries
Summary(pl):	Biblioteki statyczne cyrus-imapd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static cyrus-imapd libraries

%description static -l pl
Biblioteki statyczne cyrus-imapd

%package -n perl-%{name}
Summary:	Perl interface to cyrus-imapd library
Summary(pl):	Perlowy interfejs do biblioteki cyrus-imapd
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}

%description -n perl-%{name}
Perl interface to cyrus-imapd library.

%description -n perl-%{name} -l pl
Perlowy interfejs do biblioteki cyrus-imapd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%build
cd makedepend
rm -f aclocal.m4
%{__aclocal}
%{__autoconf}
%configure
%{__make}
PATH=$PATH:`pwd`; export PATH
cd ..
rm -f aclocal.m4
%{__aclocal} -I cmulocal
%{__autoheader}
%{__autoconf}
%configure \
	--with-auth=unix \
	--without-libwrap \
	--with-cyrus-prefix=%{_libexecdir} \
	--with-com_err=/usr
%{__make}

%{__cc} %{rpmcflags} \
	-DLIBEXECDIR="\"%{_libexecdir}\"" %{rpmldflags} -Wall -o deliver-wrapper %{SOURCE3}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_sbindir},%{_libexecdir},%{_mandir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{logrotate.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/var/spool/imap/stage. \
	$RPM_BUILD_ROOT/var/lib/imap/{user,quota,proc,log,msg,deliverdb/db,sieve,db,socket} \
	$RPM_BUILD_ROOT/etc/{security,pam.d,rc.d/init.d}

touch $RPM_BUILD_ROOT/var/lib/imap/mailboxes \
	$RPM_BUILD_ROOT/var/lib/imap/faillog \
	$RPM_BUILD_ROOT/etc/security/blacklist.imap \
	$RPM_BUILD_ROOT/etc/security/blacklist.pop

%{__make} install DESTDIR=$RPM_BUILD_ROOT CYRUS_USER="`id -u`" CYRUS_GROUP="`id -g`" mandir=%{_mandir}

install deliver-wrapper $RPM_BUILD_ROOT%{_libexecdir}/deliver-wrapper

install %{SOURCE1}	%{SOURCE2} %{SOURCE4} %{SOURCE5} .
install %{SOURCE6}	$RPM_BUILD_ROOT/etc/logrotate.d/cyrus-imapd
install %{SOURCE7}	$RPM_BUILD_ROOT%{_sysconfdir}/imapd.conf
install %{SOURCE9}	$RPM_BUILD_ROOT/etc/pam.d/imap
install %{SOURCE10}	$RPM_BUILD_ROOT/etc/pam.d/pop
install %{SOURCE11}	$RPM_BUILD_ROOT/etc/rc.d/init.d/cyrus-imapd
install %{SOURCE12}	$RPM_BUILD_ROOT%{_sysconfdir}/cyrus.conf

mv -f $RPM_BUILD_ROOT%{_libexecdir}/bin/*	$RPM_BUILD_ROOT%{_libexecdir}
mv -f $RPM_BUILD_ROOT%{_libexecdir}/master	$RPM_BUILD_ROOT%{_libexecdir}/cyrus-master
mv -f $RPM_BUILD_ROOT%{_mandir}/man8/master.8	$RPM_BUILD_ROOT%{_mandir}/man8/cyrus-master.8
rm -rf $RPM_BUILD_ROOT%{_libexecdir}/bin
rm -rf $RPM_BUILD_ROOT%{_mandir}/man8/idled.8

touch $RPM_BUILD_ROOT/etc/security/blacklist.{imap,pop}

find $RPM_BUILD_ROOT%{perl_sitearch} -name .packlist -exec rm {} \;

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
	echo "Run \"/etc/rc.d/init.d/cyrus-imapd start\" to start cyrus imap daemon."
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
%doc cyrus-README cyrus-procmailrc cyrus-user-procmailrc.template
%doc cyrus-imapd-procmail+cyrus.mc COPYRIGHT doc/*.html
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%attr(640,root,root) /etc/logrotate.d/cyrus-imapd
%attr(440,cyrus,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.*
%attr(754,root,root) /etc/rc.d/init.d/cyrus-imapd
%attr(640,cyrus,mail) %ghost /var/lib/imap/faillog
%attr(755,root,root) %{_bindir}/*
%attr(4754,cyrus,mail) %{_libexecdir}/deliver
%attr(2755,cyrus,mail) %{_libexecdir}/deliver-wrapper
%attr(755,root,root) %{_libexecdir}/ctl_deliver
%attr(755,root,root) %{_libexecdir}/ctl_mboxlist
%attr(755,root,root) %{_libexecdir}/cyrdump
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

%files devel
%defattr(644,root,root,755)
%{_includedir}/cyrus

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_sitearch}/Cyrus
%{perl_sitearch}/auto/Cyrus
