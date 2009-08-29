#
# TODO:
# - package documentation
#
%define		rname		dbus-python
#
Summary:	Python library for using D-BUS
Summary(pl.UTF-8):	Biblioteka do używania D-BUS oparta o Pythona
Name:		python-dbus
Version:	0.83.0
Release:	3
License:	MIT
Group:		Libraries/Python
Source0:	http://dbus.freedesktop.org/releases/dbus-python/%{rname}-%{version}.tar.gz
# Source0-md5:	562c78876219bf458d79a041af18293d
URL:		http://www.freedesktop.org/Software/DBusBindings
BuildRequires:	autoconf >= 2.59c
BuildRequires:	automake
BuildRequires:	cpp
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
Requires:	dbus-glib >= 0.73
Requires:	dbus-libs >= 1.0
Requires:	python-libxml2 >= 1:2.6.26
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-BUS add-on library to integrate the standard D-BUS library with
Python.

%description -l pl.UTF-8
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z Pythonem.

%package devel
Summary:	C API for _dbus_bindings module
Summary(pl.UTF-8):	API C dla modułu _dbus_bindings
License:	AFL v2.1 or LGPL v2.1
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel >= 0.93
Requires:	python-devel >= 1:2.5

%description devel
C API for _dbus_bindings module.

%description devel -l pl.UTF-8
API C dla modułu _dbus_bindings.

%prep
%setup -qn %{rname}-%{version}

%build
%configure
%{__make}
	
%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{py_sitedir}/dbus/mainloop

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT%{py_sitedir}/dbus/__init__.py
touch $RPM_BUILD_ROOT%{py_sitedir}/dbus/mainloop/__init__.py

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

rm -f $RPM_BUILD_ROOT%{py_sitedir}/_dbus*.la	

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%dir %{py_sitescriptdir}/dbus
%dir %{py_sitescriptdir}/dbus/mainloop
%{py_sitescriptdir}/*.py[co]
%{py_sitescriptdir}/dbus/*.py[co]
%{py_sitescriptdir}/dbus/mainloop/*.py[co]
%attr(755,root,root) %{py_sitedir}/_dbus*.so
%dir %{py_sitedir}/dbus
%dir %{py_sitedir}/dbus/mainloop
%{py_sitedir}/dbus/*.py[co]
%{py_sitedir}/dbus/mainloop/*.py[co]
#%{py_sitescriptdir}/dbus_python-*.egg-info

%files devel
%defattr(644,root,root,755)
%{_includedir}/dbus-1.0/dbus/dbus-python.h
%{_pkgconfigdir}/dbus-python.pc
