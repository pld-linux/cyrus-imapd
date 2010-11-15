# Conditional build:
%bcond_without	perl		# build with perl
%bcond_without	shared		# build with shared patch (not updated)

%{?with_perl:%include	/usr/lib/rpm/macros.perl}
Summary:	High-performance mail store with IMAP and POP3
Summary(pl.UTF-8):	Wysoko wydajny serwer IMAP i POP3
Summary(pt_BR.UTF-8):	Um servidor de mail de alto desempenho que suporta IMAP e POP3
Name:		cyrus-imapd
Version:	2.3.16
Release:	6
License:	BSD-like
Group:		Networking/Daemons/POP3
Source0:	ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{name}-%{version}.tar.gz
# Source0-md5:	6a37feb1985974eee8a4a4b2932dd54c
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
# https://bugzilla.andrew.cmu.edu/show_bug.cgi?id=3095
Patch1:		%{name}-shared.patch
# https://bugzilla.andrew.cmu.edu/show_bug.cgi?id=3094
Patch2:		%{name}-verifydbver.patch
Patch3:		gcc44.patch
Patch4:		glibc.patch
Patch5:		asneeded.patch
URL:		http://cyrusimap.web.cmu.edu/imapd/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 1.5.27
BuildRequires:	db-devel >= 4.1.25
BuildRequires:	flex
BuildRequires:	libcom_err-devel >= 1.21
BuildRequires:	libtool
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel >= 0.9.7d
%{?with_perl:BuildRequires:	perl-devel >= 1:5.8.0}
%{?with_perl:BuildRequires:	rpm-perlprov}
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
%{?with_shared:Requires:	%{name}-libs = %{version}-%{release}}
Requires:	rc-scripts >= 0.4.0.18
%{!?with_shared:Obsoletes:	%{name}-libs}
# needed by scripts from %{_bindir}
Requires:	pam >= 0.79.0
%{?with_perl:Requires:	perl-%{name} = %{version}-%{release}}
Provides:	imapdaemon
Provides:	pop3daemon
Provides:	user(cyrus)
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

%define		_libexecdir	%{_libdir}/cyrus

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

%description libs
Shared cyrus-imapd libraries.

%description libs -l pl.UTF-8
Współdzielone biblioteki cyrus-imapd.

%package devel
Summary:	Header files for developing with cyrus-imapd libraries
Summary(pl.UTF-8):	Pliki nagłówkowe do programowania z użyciem bibliotek cyrus-imapd
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

rm -rf autom4te.cache

%build
cd makedepend
%{__libtoolize}
%{__aclocal}
%{__autoconf}
cp -f %{_datadir}/automake/config.* .
%configure
%{__make}
PATH=$PATH:$(pwd); export PATH
cd ..
%{__libtoolize}
%{__aclocal} -I cmulocal
%{__autoheader}
%{__autoconf}
cp -f %{_datadir}/automake/config.* .
cp -f %{_datadir}/automake/install-sh .
%configure \
	--with-cyrus-prefix=%{_libexecdir} \
	--with-service-path=%{_libexecdir} \
	--with-com_err=/usr \
	--%{!?with_perl:without-perl}%{?with_perl:with-perl=%{__perl}} \
	--without-libwrap \
	--enable-nntp \
	--enable-replication
%{__make} -j1 \
	INSTALLDIRS=vendor \
	VERSION=%{version}

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
	$RPM_BUILD_ROOT/etc/security/blacklist.pop3

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	CYRUS_USER=%(id -u) \
	CYRUS_GROUP=%(id -g) \
	INSTALLDIRS=vendor

install deliver-wrapper $RPM_BUILD_ROOT%{_libexecdir}/deliver-wrapper

install %{SOURCE1}	%{SOURCE2} %{SOURCE4} %{SOURCE5} .
install %{SOURCE6}	$RPM_BUILD_ROOT/etc/logrotate.d/cyrus-imapd
install %{SOURCE7}	$RPM_BUILD_ROOT%{_sysconfdir}/imapd.conf
install %{SOURCE9}	$RPM_BUILD_ROOT/etc/pam.d/imap
install %{SOURCE10}	$RPM_BUILD_ROOT/etc/pam.d/pop
sed -e 's,/''usr/lib/cyrus,%{_libexecdir},' %{SOURCE11} > $RPM_BUILD_ROOT/etc/rc.d/init.d/cyrus-imapd
sed -e 's,/''usr/lib/cyrus,%{_libexecdir},' %{SOURCE13} > $RPM_BUILD_ROOT/etc/rc.d/init.d/cyrus-sync
install %{SOURCE12}	$RPM_BUILD_ROOT%{_sysconfdir}/cyrus.conf

mv -f $RPM_BUILD_ROOT%{_libexecdir}/master	$RPM_BUILD_ROOT%{_libexecdir}/cyrus-master
mv -f $RPM_BUILD_ROOT%{_mandir}/man8/master.8	$RPM_BUILD_ROOT%{_mandir}/man8/cyrus-master.8
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/idled.8

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
rm -f $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
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
%doc cyrus-imapd-procmail+cyrus.mc COPYRIGHT doc/*.html tools
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/cyrus-imapd
%attr(440,cyrus,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.*
%attr(754,root,root) /etc/rc.d/init.d/cyrus-imapd
%attr(754,root,root) /etc/rc.d/init.d/cyrus-sync
%attr(640,cyrus,mail) %ghost /var/lib/imap/faillog
%attr(755,root,root) %{_bindir}/*
%dir %{_libexecdir}
%attr(4754,cyrus,mail) %{_libexecdir}/deliver
%attr(2755,cyrus,mail) %{_libexecdir}/deliver-wrapper
%attr(755,root,root) %{_libexecdir}/arbitron
%attr(755,root,root) %{_libexecdir}/chk_cyrus
%attr(755,root,root) %{_libexecdir}/ctl_cyrusdb
%attr(755,root,root) %{_libexecdir}/ctl_deliver
%attr(755,root,root) %{_libexecdir}/ctl_mboxlist
%attr(755,root,root) %{_libexecdir}/cvt_cyrusdb
%attr(755,root,root) %{_libexecdir}/cyr_dbtool
%attr(755,root,root) %{_libexecdir}/cyr_df
%attr(755,root,root) %{_libexecdir}/cyr_expire
%attr(755,root,root) %{_libexecdir}/cyr_synclog
%attr(755,root,root) %{_libexecdir}/cyrdump
%attr(755,root,root) %{_libexecdir}/cyrus-master
%attr(755,root,root) %{_libexecdir}/fetchnews
%attr(755,root,root) %{_libexecdir}/fud
%attr(755,root,root) %{_libexecdir}/imapd
%attr(755,root,root) %{_libexecdir}/ipurge
%attr(755,root,root) %{_libexecdir}/lmtpd
%attr(755,root,root) %{_libexecdir}/lmtpproxyd
%attr(755,root,root) %{_libexecdir}/make_md5
%attr(755,root,root) %{_libexecdir}/make_sha1
%attr(755,root,root) %{_libexecdir}/mbexamine
%attr(755,root,root) %{_libexecdir}/mbpath
%attr(755,root,root) %{_libexecdir}/nntpd
%attr(755,root,root) %{_libexecdir}/notifyd
%attr(755,root,root) %{_libexecdir}/pop3d
%attr(755,root,root) %{_libexecdir}/pop3proxyd
%attr(755,root,root) %{_libexecdir}/proxyd
%attr(755,root,root) %{_libexecdir}/quota
%attr(755,root,root) %{_libexecdir}/reconstruct
%attr(755,root,root) %{_libexecdir}/sievec
%attr(755,root,root) %{_libexecdir}/sieved
%attr(755,root,root) %{_libexecdir}/smmapd
%attr(755,root,root) %{_libexecdir}/squatter
%attr(755,root,root) %{_libexecdir}/sync_client
%attr(755,root,root) %{_libexecdir}/sync_reset
%attr(755,root,root) %{_libexecdir}/sync_server
%attr(755,root,root) %{_libexecdir}/timsieved
%attr(755,root,root) %{_libexecdir}/tls_prune
%attr(755,root,root) %{_libexecdir}/unexpunge


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

%if %{with shared}
%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcyrus-%{version}.so
%attr(755,root,root) %{_libdir}/libcyrus_min-%{version}.so
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/cyrus
%if %{with shared}
%attr(755,root,root) %{_libdir}/libcyrus.so
%attr(755,root,root) %{_libdir}/libcyrus_min.so
%{_libdir}/libcyrus.la
%{_libdir}/libcyrus_min.la

%files static
%defattr(644,root,root,755)
%endif
%{_libdir}/libcyrus.a
%{_libdir}/libcyrus_min.a

%if %{with perl}
%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/Cyrus
%dir %{perl_vendorarch}/auto/Cyrus
%dir %{perl_vendorarch}/auto/Cyrus/IMAP
%attr(755,root,root) %{perl_vendorarch}/auto/Cyrus/IMAP/IMAP.so
%{perl_vendorarch}/auto/Cyrus/IMAP/IMAP.bs
%dir %{perl_vendorarch}/auto/Cyrus/SIEVE
%dir %{perl_vendorarch}/auto/Cyrus/SIEVE/managesieve
%attr(755,root,root) %{perl_vendorarch}/auto/Cyrus/SIEVE/managesieve/managesieve.so
%{perl_vendorarch}/auto/Cyrus/SIEVE/managesieve/managesieve.bs
%endif
