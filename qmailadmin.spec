Summary:	CGI admin interface to vpopmail
Summary(pl.UTF-8):   Interfejs CGI do administrowania vpopmailem
Name:		qmailadmin
Version:	1.0.6
Release:	0.1
License:	GPL
Group:		Networking/Mail
Source0:	http://dl.sourceforge.net/qmailadmin/%{name}-%{version}.tar.gz
# Source0-md5:	7a6a4acb4f8a04b4cf5170778713020b
#Source1:	README.hooks.bz2
#Source2:	%{name}.png
URL:		http://inter7.com/qmailadmin.html
BuildRequires:	mysql-devel
BuildRequires:	vpopmail-devel >= 5.3.3-0.2
Requires:	autorespond
Requires:	ezmlm-idx
Requires:	qmail
Requires:	vpopmail
Requires:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vuser		vpopmail
%define		vgroup		vchkpw
%define		vhome		/var/lib/%{vuser}
%define		varqmail	/var/qmail
%define		httpdir		/home/services/httpd
%define		cgidir		/home/services/httpd/cgi-bin
%define		htmldir		/home/services/httpd/html

%description
qmailadmin is a CGI software for administering vpopmail domains.

Every e-mail domain owner can manage its users, forwards,
autoresponders and mailinglists without nagging the system owner at
all.

Hooks are included to run external software when the domain owner adds
or deletes users, forwards, autoresponders and mailinglists. The main
reason you might want this is for billing purposes or just plain
logging.

%description -l pl.UTF-8
qmailadmin to program CGI do administrowania domenami vpopmaila.

Każdy właściciel domeny pocztowej może zarządzać swoimi użytkownikami,
przekierowaniami, automatycznymi odpowiedziami i listami dyskusyjnymi
bez udziału administratora systemu.

qmailadmin ma możliwość uruchamiania zewnętrznych programów kiedy
właściciel domeny dodaje lub usuwa użytkowników, przekierowania,
automatyczne odpowiedzi i listy dyskusyjne. Może to służyć do
wystawiania rachunków lub zwykłego logowania.

%prep
%setup -q

%build
#%{__autoconf}

CFLAGS="%{rpmcflags} -I/usr/include/vpopmail"
LIBS="/usr/%{_lib}/libvpopmail.a -lmysqlclient"; export LIBS
# don't use -lnsl
export ac_cv_lib_nsl_gethostbyaddr=no
# don't regenerate, configure has been modified
%configure2_13 \
	--enable-cgibindir=%{cgidir} \
	--with-htmllibdir=%{_datadir}/%{name} \
	--enable-htmldir=/images/%{name} \
	--enable-cgipath=/cgi-bin/%{name}.cgi \
	--enable-autoresponder-bin=%{_bindir}/autorespond \
	--enable-vpopuser=%{vuser} \
	--enable-vpopgroup=%{vgroup} \
	--enable-qmaildir=%{varqmail} \
	--enable-ezmlmdir=%{_bindir} \
	--enable-vpopmaildir=%{vhome} \
	--enable-maxpopusers=-1 \
	--enable-maxaliases=-1 \
	--enable-maxforwards=-1 \
	--enable-maxautoresponders=-1 \
	--enable-maxmailinglists=-1 \
	--enable-maxusersperpage=15 \
	--enable-maxaliasesperpage=25 \
	--enable-ezmlmidx=y \
	--enable-defaultquota=-1 \
	--enable-no-cache=y

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{htmldir}/images/%{name},%{cgidir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/html \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/scripts

install %{name} $RPM_BUILD_ROOT%{cgidir}/%{name}.cgi

# install the templates and the language files.
install html/* $RPM_BUILD_ROOT%{_datadir}/%{name}/html

# install the images.
install images/* $RPM_BUILD_ROOT%{htmldir}/images/%{name}
cp $RPM_BUILD_ROOT%{_datadir}/%{name}/html/en $RPM_BUILD_ROOT%{_datadir}/%{name}/html/en-us

# install script to call the web interface from the menu.
cat <<EOF > $RPM_BUILD_ROOT%{_libdir}/%{name}/scripts/%{name}
#!/bin/sh
url='http://localhost/cgi-bin/%{name}.cgi'
if ! [ -z "\$BROWSER" ] && ( which \$BROWSER ); then
  browser=\`which \$BROWSER\`
elif [ -x %{_bindir}/netscape ]; then
  browser=%{_bindir}/netscape
elif [ -x %{_bindir}/konqueror ]; then
  browser=%{_bindir}/konqueror
elif [ -x %{_bindir}/lynx ]; then
  browser='xterm -bg black -fg white -e lynx'
elif [ -x %{_bindir}/links ]; then
  browser='xterm -bg black -fg white -e links'
else
  xmessage "No web browser found, install one or set the BROWSER environment variable!"
  exit 1
fi
\$browser \$url
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ INSTALL NEWS README*
%attr(6755,%{vuser},%{vgroup}) %{cgidir}/%{name}.cgi
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/html
# XXX: files in _datadir cannot be config
%config(noreplace) %{_datadir}/%{name}/html/*
%dir %{htmldir}/images
%dir %{htmldir}/images/%{name}
%config(noreplace) %{htmldir}/images/%{name}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/scripts
%attr(755,root,root) %{_libdir}/%{name}/scripts/%{name}
