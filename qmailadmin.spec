%define vuser vpopmail
%define vgroup vchkpw
%define vhome /home/%{vuser}

Summary:	CGI admin interface to vpopmail
Summary(pl):	Interfejs CGI do administrowania vpopmailem
Name:		qmailadmin
Version:	1.0.1
Release:	1
License:	GPL
Group:		Networking/Mail
Source0:	%{name}-%{version}.tar.gz
#Source1:	README.hooks.bz2
#Source2:	%{name}.png
URL:		http://inter7.com/qmailadmin/
Requires:	qmail autorespond webserver ezmlm-idx vpopmail
BuildRequires:	autoconf
BuildRequires:	vpopmail-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
qmailadmin is a CGI software for administering vpopmail domains.

Every e-mail domain owner can manage its users, forwards,
autoresponders and mailinglists without nagging the system owner at
all.

Hooks are included to run external software when the domain owner adds
or deletes users, forwards, autoresponders and mailinglists. The main
reason you might want this is for billing purposes or just plain
logging.

%description -l pl
qmailadmin to program CGI do administrowania domenami vpopmaila.

Ka¿dy w³a¶ciciel domeny pocztowej mo¿e zarz±dzaæ swoimi u¿ytkownikami,
przekierowaniami, automatycznymi odpowiedziami i listami dyskusyjnymi
bez udzia³u administratora systemu.

qmailadmin ma mo¿liwo¶æ uruchamiania zewnêtrznych programów kiedy
w³a¶ciciel domeny dodaje lub usuwa u¿ytkowników, przekierowania,
automatyczne odpowiedzi i listy dyskusyjne. Mo¿e to s³u¿yæ do
wystawiania rachunków lub zwyk³ego logowania.

%prep
%setup -q

%build
autoconf
%configure \
--enable-cgibindir=/home/httpd/cgi-bin \
--with-htmllibdir=%{_datadir}/%{name} \
--enable-htmldir=/images/%{name} \
--enable-cgipath=/cgi-bin/%{name}.cgi \
--enable-autoresponder-bin=%{_bindir}/autorespond \
--enable-vpopuser=%{vuser} \
--enable-vpopgroup=%{vgroup} \
--enable-qmaildir=/var/qmail \
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
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name}/html,%{_libdir}/%{name}/scripts} \
	$RPM_BUILD_ROOT/home/httpd/{cgi-bin,html/images/%{name}} \
	$RPM_BUILD_ROOT{%{_menudir},%{_pixmapsdir}/hicolor/16x16/apps}

install %{name} $RPM_BUILD_ROOT/home/httpd/cgi-bin/%{name}.cgi

# install the templates and the language files.
install html/* $RPM_BUILD_ROOT%{_datadir}/%{name}/html

# install the images.
#install images/*.png %{buildroot}/var/www/html/images/%{name}/

# install the hooks documentation.
#bzcat %{SOURCE1} > README.hooks

#install %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/

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

# install menu entry.
cat <<EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): needs=X11 \
section=Configuration/Networking \
title="%{name} tool" \
longtitle="Web-based administration tool for qmail+vpopmail, works with every browser. Set the $BROWSER environment variable to choose your preferred browser." \
command="%{_libdir}/%{name}/scripts/%{name} 1>/dev/null 2>/dev/null" \
icon="%{_pixmapsdir}/hicolor/16x16/apps/%{name}.png"
EOF

gzip -9nf AUTHORS ChangeLog FAQ INSTALL NEWS README* themes/README.default

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.gz ChangeLog.gz FAQ.gz INSTALL.gz NEWS.gz README*.gz themes/README.default.gz
%attr(6755,%{vuser},%{vgroup}) /home/httpd/cgi-bin/%{name}.cgi
%config(noreplace) %{_datadir}/%{name}/html/*
%config(noreplace) /home/httpd/html/images/%{name}/*
%{_libdir}/menu/%{name}
%attr(755,root,root) %{_libdir}/%{name}/scripts/%{name}
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
