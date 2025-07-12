# TODO: zephyr notification?

#
# Conditional build:
%bcond_without	doc		# documentation regeneration
%bcond_without	http		# HTTP support
%bcond_without	ldap		# LDAP support
%bcond_without	lmdb		# LMDB backend support
%bcond_without	mysql		# MySQL backend support
%bcond_without	perl		# Perl support
%bcond_without	pgsql		# PostgreSQL backend support
%bcond_with	sphinx		# Sphinx search engine support (broken)
%bcond_without	xapian		# Xapian search engine support
#
#
Summary:	High-performance mail store with IMAP and POP3
Summary(pl.UTF-8):	Wysoko wydajny serwer IMAP i POP3
Summary(pt_BR.UTF-8):	Um servidor de mail de alto desempenho que suporta IMAP e POP3
Name:		cyrus-imapd
Version:	3.8.5
Release:	2
License:	BSD-like
Group:		Networking/Daemons/POP3
#Source0Download: https://github.com/cyrusimap/cyrus-imapd/releases
Source0:	https://github.com/cyrusimap/cyrus-imapd/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3eca3a7253d5a960fedc874e47996c98
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
Source13:	cyrus-sync.init
Patch0:		%{name}-et.patch
Patch1:		libxml2.patch
Patch2:		%{name}-clamav-0.101.patch
URL:		http://www.cyrusimap.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 2.1.7
BuildRequires:	db-devel >= 4.1.25
BuildRequires:	flex
BuildRequires:	jansson-devel >= 2.3
%{?with_http:BuildRequires:	libbrotli-devel}
BuildRequires:	libcap-devel
BuildRequires:	libcom_err-devel >= 1.21
%{?with_http:BuildRequires:	libical-devel >= 2.0}
BuildRequires:	libicu-devel
BuildRequires:	libtool >= 2:2.2.6
%{?with_http:BuildRequires:	libxml2-devel >= 1:2.7.3}
%{?with_lmdb:BuildRequires:	lmdb-devel}
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	net-snmp-devel
%{?with_http:BuildRequires:	nghttp2-devel >= 1.5}
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	patchutils
%{?with_doc:BuildRequires:	perl-Pod-POM-View-Restructured}
%{?with_perl:BuildRequires:	perl-devel >= 1:5.8.0}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_perl:BuildRequires:	rpm-perlprov}
BuildRequires:	rpmbuild(macros) >= 1.527
%{?with_http:BuildRequires:	shapelib-devel >= 1.4.1}
%{?with_http:BuildRequires:	sqlite3-devel >= 3}
%{?with_doc:BuildRequires:	sphinx-pdg-3}
%{?with_xapian:BuildRequires:	xapian-core-devel}
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts >= 0.4.0.18
# needed by scripts from %{_bindir}
Requires:	pam >= 0.79.0
%{?with_perl:Requires:	perl-%{name} = %{version}-%{release}}
Provides:	imapdaemon
Provides:	pop3daemon
Provides:	user(cyrus)
Obsoletes:	cyrus-imapd-doc < 3
Obsoletes:	imap
Obsoletes:	imapd
Obsoletes:	imapdaemon
Obsoletes:	pop3daemon
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pkglibexecdir	%{_libexecdir}/cyrus

%define		skip_post_check_so	libcyrus(|_min|_imap|_sieve).so.*

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

%description -l pl.UTF-8
Serwer Cyrus IMAP jest skalowalnym systemem e-mail dla
przedsiębiorstwa, zaprojektowanym dla małych i dużych firm i
wykorzystującym oparte na standardach technologie.

Pełna implementacja Cyrus IMAP pozwala na bezproblemowe ustawienie
środowiska poczty i elektronicznej tablicy ogłoszeniowej na kilku
serwerach. Tym się różni od innych implementacji serwerów IMAP, że
jest uruchamiany na "opieczętowanych" serwerach, na które w normalnych
warunkach użytkownicy nie mogą się zalogować. Baza danych skrzynek
pocztowych jest przechowywana w tych częściach systemu plików, które
są dostępne jedynie dla systemu IMAP Cyrus. Wszelki dostęp do poczty
ma miejsce poprzez oprogramowanie wykorzystujące protokoły IMAP, POP3
oraz KPOP.

%description -l pt_BR.UTF-8
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

%package libs
Summary:	Shared cyrus-imapd libraries
Summary(pl.UTF-8):	Współdzielone biblioteki cyrus-imapd
Group:		Libraries
Requires:	cyrus-sasl-libs >= 2.1.7
Requires:	jansson >= 2.3

%description libs
Shared cyrus-imapd libraries.

%description libs -l pl.UTF-8
Współdzielone biblioteki cyrus-imapd.

%package devel
Summary:	Header files for developing with cyrus-imapd libraries
Summary(pl.UTF-8):	Pliki nagłówkowe do programowania z użyciem bibliotek cyrus-imapd
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	cyrus-sasl-devel >= 2.1.7
Requires:	jansson-devel >= 2.3

%description devel
This package provides the necessary header files files to allow you to
develop with cyrus-imapd libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe niezbędne do tworzenia
oprogramowania z wykorzystaniem bibliotek cyrus-imapd.

%package static
Summary:	Static cyrus-imapd libraries
Summary(pl.UTF-8):	Biblioteki statyczne cyrus-imapd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static cyrus-imapd libraries

%description static -l pl.UTF-8
Biblioteki statyczne cyrus-imapd

%package -n perl-%{name}
Summary:	Perl interface to cyrus-imapd library
Summary(pl.UTF-8):	Perlowy interfejs do biblioteki cyrus-imapd
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{version}-%{release}

%description -n perl-%{name}
Perl interface to cyrus-imapd library.

%description -n perl-%{name} -l pl.UTF-8
Perlowy interfejs do biblioteki cyrus-imapd.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE4} %{SOURCE5} .

find docsrc/ -name '*.pyc' -print0 | xargs --null %{__rm}

%build
%{__libtoolize}
%{__aclocal} -I cmulocal
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--libexecdir=%{pkglibexecdir} \
	--enable-autocreate \
	--enable-backup \
	--enable-calalarmd \
	%{__enable_disable http} \
	--enable-idled \
	--enable-murder \
	--enable-nntp \
	--enable-replication \
	%{__enable_disable sphinx} \
	--enable-static \
	%{__enable_disable xapian} \
	--with-com_err=/usr \
	%{__with_without ldap} \
	--with-libcap \
	--without-libwrap \
	%{__with_without lmdb} \
	%{__with_without mysql} \
	%{__with_without perl perl %{__perl}} \
	%{__with_without pgsql} \
	%{__with_without doc sphinx-build}

%{__make} -j1 \
	INSTALLDIRS=vendor \
	VERSION=%{version}

%{__cc} %{rpmcflags} \
	-DLIBEXECDIR="\"%{pkglibexecdir}\"" %{rpmldflags} -Wall -o deliver-wrapper %{SOURCE3}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_sbindir},%{pkglibexecdir},%{_mandir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{logrotate.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/var/spool/imap/stage. \
	$RPM_BUILD_ROOT/var/lib/imap/{user,quota,proc,log,msg,deliverdb/db,sieve,db,socket} \
	$RPM_BUILD_ROOT/etc/{security,pam.d,rc.d/init.d}

touch $RPM_BUILD_ROOT/var/lib/imap/mailboxes \
	$RPM_BUILD_ROOT/var/lib/imap/faillog \
	$RPM_BUILD_ROOT/etc/security/blacklist.imap \
	$RPM_BUILD_ROOT/etc/security/blacklist.pop3

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	CYRUS_USER=%(id -u) \
	CYRUS_GROUP=%(id -g) \
	INSTALLDIRS=vendor

# ensure +x bit for rpm autodeps
chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so*

install -p deliver-wrapper $RPM_BUILD_ROOT%{pkglibexecdir}/deliver-wrapper

cp -p %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/cyrus-imapd
cp -p %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/imapd.conf
cp -p %{SOURCE9} $RPM_BUILD_ROOT/etc/pam.d/imap
cp -p %{SOURCE10} $RPM_BUILD_ROOT/etc/pam.d/pop
sed -e 's,/''usr/lib/cyrus,%{pkglibexecdir},' %{SOURCE11} > $RPM_BUILD_ROOT/etc/rc.d/init.d/cyrus-imapd
sed -e 's,/''usr/lib/cyrus,%{pkglibexecdir},' %{SOURCE13} > $RPM_BUILD_ROOT/etc/rc.d/init.d/cyrus-sync
cp -p %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/cyrus.conf

# We rename some utils, so we need to sort out the manpages
for i in master reconstruct quota deliver; do
	mv $RPM_BUILD_ROOT%{_mandir}/man8/{,cyr}$i.8
done

%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/idled.8

touch $RPM_BUILD_ROOT/etc/security/blacklist.{imap,pop3}

# make hashed dirs
for i in $(%{__perl} -le 'print for "a".."z"'); do
	install -d $RPM_BUILD_ROOT%{_var}/lib/imap/user/$i
	install -d $RPM_BUILD_ROOT%{_var}/lib/imap/quota/$i
	install -d $RPM_BUILD_ROOT%{_var}/lib/imap/sieve/$i
	install -d $RPM_BUILD_ROOT%{_var}/spool/imap/$i
done

%if %{with perl}
find $RPM_BUILD_ROOT%{perl_vendorarch} -name .packlist | xargs rm -v
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 76 -d /var/spool/imap -s /bin/false -c "Cyrus User" -g mail cyrus

%post
touch /var/lib/imap/faillog
chown cyrus:mail /var/lib/imap/faillog
chmod 640 /var/lib/imap/faillog
cd /var/lib/imap
chattr +S . user quota user/* quota/* 2>/dev/null ||:
chattr +S /var/spool/imap /var/spool/imap/* 2>/dev/null ||:

/sbin/chkconfig --add cyrus-imapd
%service cyrus-imapd restart "cyrus imap daemon"
%service cyrus-sync restart "cyrus replication service"

%preun
if [ "$1" = "0" ]; then
	%service cyrus-imapd stop
	%service cyrus-sync stop
	/sbin/chkconfig --del cyrus-imapd
	/sbin/chkconfig --del cyrus-sync
fi

%postun
if [ "$1" = "0" ]; then
	%userremove cyrus
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc cyrus-README cyrus-procmailrc cyrus-user-procmailrc.template
%doc cyrus-imapd-procmail+cyrus.mc COPYING tools
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/cyrus-imapd
%attr(440,cyrus,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.*
%attr(754,root,root) /etc/rc.d/init.d/cyrus-imapd
%attr(754,root,root) /etc/rc.d/init.d/cyrus-sync
%attr(640,cyrus,mail) %ghost /var/lib/imap/faillog
%attr(755,root,root) %{_bindir}/cyradm
%attr(755,root,root) %{_bindir}/httptest
%attr(755,root,root) %{_bindir}/imtest
%attr(755,root,root) %{_bindir}/installsieve
%attr(755,root,root) %{_bindir}/lmtptest
%attr(755,root,root) %{_bindir}/mupdatetest
%attr(755,root,root) %{_bindir}/nntptest
%attr(755,root,root) %{_bindir}/pop3test
%attr(755,root,root) %{_bindir}/sieveshell
%attr(755,root,root) %{_bindir}/sivtest
%attr(755,root,root) %{_bindir}/smtptest
%attr(755,root,root) %{_bindir}/synctest

%dir %{pkglibexecdir}
%attr(2755,cyrus,mail) %{pkglibexecdir}/deliver-wrapper
%attr(755,root,root) %{pkglibexecdir}/backupd
%attr(755,root,root) %{pkglibexecdir}/calalarmd
%attr(755,root,root) %{pkglibexecdir}/fud
%{?with_http:%attr(755,root,root) %{pkglibexecdir}/httpd}
%attr(755,root,root) %{pkglibexecdir}/idled
%attr(755,root,root) %{pkglibexecdir}/imapd
%attr(755,root,root) %{pkglibexecdir}/lmtpd
%attr(755,root,root) %{pkglibexecdir}/lmtpproxyd
%attr(755,root,root) %{pkglibexecdir}/master
%attr(755,root,root) %{pkglibexecdir}/mupdate
%attr(755,root,root) %{pkglibexecdir}/nntpd
%attr(755,root,root) %{pkglibexecdir}/notifyd
%attr(755,root,root) %{pkglibexecdir}/ptloader
%attr(755,root,root) %{pkglibexecdir}/pop3d
%attr(755,root,root) %{pkglibexecdir}/pop3proxyd
%attr(755,root,root) %{pkglibexecdir}/promstatsd
%attr(755,root,root) %{pkglibexecdir}/proxyd
%attr(755,root,root) %{pkglibexecdir}/smmapd
%attr(755,root,root) %{pkglibexecdir}/sync_server
%attr(755,root,root) %{pkglibexecdir}/timsieved
%attr(755,root,root) %{_sbindir}/arbitron
%attr(755,root,root) %{_sbindir}/chk_cyrus
%attr(755,root,root) %{_sbindir}/ctl_backups
%attr(755,root,root) %{_sbindir}/ctl_conversationsdb
%attr(755,root,root) %{_sbindir}/ctl_cyrusdb
%attr(755,root,root) %{_sbindir}/ctl_deliver
%attr(755,root,root) %{_sbindir}/ctl_mboxlist
%{?with_http:%attr(755,root,root) %{_sbindir}/ctl_zoneinfo}
%attr(755,root,root) %{_sbindir}/cvt_cyrusdb
%attr(755,root,root) %{_sbindir}/cvt_xlist_specialuse
%attr(755,root,root) %{_sbindir}/cyr_buildinfo
%attr(755,root,root) %{_sbindir}/cyr_cd.sh
%attr(755,root,root) %{_sbindir}/cyr_dbtool
%attr(755,root,root) %{_sbindir}/cyr_deny
%attr(755,root,root) %{_sbindir}/cyr_df
%attr(755,root,root) %{_sbindir}/cyrdump
%attr(755,root,root) %{_sbindir}/cyr_backup
%attr(755,root,root) %{_sbindir}/cyr_expire
%attr(755,root,root) %{_sbindir}/cyr_info
%attr(755,root,root) %{_sbindir}/cyr_ls
%attr(755,root,root) %{_sbindir}/cyr_pwd
%attr(755,root,root) %{_sbindir}/cyr_synclog
%attr(755,root,root) %{_sbindir}/cyr_userseen
%attr(755,root,root) %{_sbindir}/cyr_virusscan
%{?with_http:%attr(755,root,root) %{_sbindir}/dav_reconstruct}
%attr(755,root,root) %{_sbindir}/deliver
%attr(755,root,root) %{_sbindir}/fetchnews
%attr(755,root,root) %{_sbindir}/ipurge
%attr(755,root,root) %{_sbindir}/mbexamine
%attr(755,root,root) %{_sbindir}/mbpath
%attr(755,root,root) %{_sbindir}/mbtool
%attr(755,root,root) %{_sbindir}/quota
%attr(755,root,root) %{_sbindir}/ptdump
%attr(755,root,root) %{_sbindir}/ptexpire
%attr(755,root,root) %{_sbindir}/reconstruct
%attr(755,root,root) %{_sbindir}/relocate_by_id
%attr(755,root,root) %{_sbindir}/restore
%attr(755,root,root) %{_sbindir}/sievec
%attr(755,root,root) %{_sbindir}/sieved
%attr(755,root,root) %{_sbindir}/squatter
%attr(755,root,root) %{_sbindir}/sync_client
%attr(755,root,root) %{_sbindir}/sync_reset
%attr(755,root,root) %{_sbindir}/tls_prune
%attr(755,root,root) %{_sbindir}/unexpunge

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
%attr(750,cyrus,mail) %config(noreplace) %verify(not md5 mtime size) /var/lib/imap/mailboxes

%{_mandir}/man*/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcyrus.so.0
%attr(755,root,root) %ghost %{_libdir}/libcyrus.so.*.*
%attr(755,root,root) %{_libdir}/libcyrus_min.so.0
%attr(755,root,root) %ghost %{_libdir}/libcyrus_min.so.*.*
%attr(755,root,root) %{_libdir}/libcyrus_imap.so.0
%attr(755,root,root) %ghost %{_libdir}/libcyrus_imap.so.*.*
%attr(755,root,root) %{_libdir}/libcyrus_sieve.so.0
%attr(755,root,root) %ghost %{_libdir}/libcyrus_sieve.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/cyrus
%attr(755,root,root) %{_libdir}/libcyrus.so
%attr(755,root,root) %{_libdir}/libcyrus_min.so
%attr(755,root,root) %{_libdir}/libcyrus_imap.so
%attr(755,root,root) %{_libdir}/libcyrus_sieve.so
%{_libdir}/libcyrus.la
%{_libdir}/libcyrus_min.la
%{_libdir}/libcyrus_imap.la
%{_libdir}/libcyrus_sieve.la
%{_pkgconfigdir}/libcyrus.pc
%{_pkgconfigdir}/libcyrus_imap.pc
%{_pkgconfigdir}/libcyrus_min.pc
%{_pkgconfigdir}/libcyrus_sieve.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcyrus.a
%{_libdir}/libcyrus_imap.a
%{_libdir}/libcyrus_min.a
%{_libdir}/libcyrus_sieve.a

%if %{with perl}
%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/Cyrus
%dir %{perl_vendorarch}/auto/Cyrus
%dir %{perl_vendorarch}/auto/Cyrus/IMAP
%attr(755,root,root) %{perl_vendorarch}/auto/Cyrus/IMAP/IMAP.so
%dir %{perl_vendorarch}/auto/Cyrus/SIEVE
%dir %{perl_vendorarch}/auto/Cyrus/SIEVE/managesieve
%attr(755,root,root) %{perl_vendorarch}/auto/Cyrus/SIEVE/managesieve/managesieve.so
%dir %{perl_vendorlib}/Cyrus
%dir %{perl_vendorlib}/Cyrus/Annotator
%{perl_vendorlib}/Cyrus/Annotator/AnnotateInlinedCIDs.pm
%{perl_vendorlib}/Cyrus/Annotator/Daemon.pm
%{perl_vendorlib}/Cyrus/Annotator/Message.pm
%endif
