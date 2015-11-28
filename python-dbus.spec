#
# Conditional build:
%bcond_without  python2         # Python 2.x module
%bcond_without  python3         # Python 3.x module
#
%define		rname		dbus-python
#
Summary:	Python library for using D-BUS
Summary(pl.UTF-8):	Biblioteka do używania D-BUS oparta o Pythona
Name:		python-dbus
Version:	1.2.0
Release:	9
License:	MIT
Group:		Libraries/Python
Source0:	http://dbus.freedesktop.org/releases/dbus-python/%{rname}-%{version}.tar.gz
# Source0-md5:	b09cd2d1a057cc432ce944de3fc06bf7
Patch0:		epydoc.patch
URL:		http://www.freedesktop.org/Software/DBusBindings
BuildRequires:	autoconf >= 2.59c
BuildRequires:	automake >= 1:1.9
BuildRequires:	cpp
BuildRequires:	dbus-devel >= 1.6
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	epydoc
BuildRequires:	libtool
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-devel >= 1:2.6}
%{?with_python3:BuildRequires:	python3-devel >= 3.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
%pyrequires_eq	python-modules
Requires:	dbus-glib >= 0.73
Requires:	dbus-libs >= 1.6
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
Requires:	dbus-devel >= 1.6
#R: python-dbus = %{version}-%{release}  or  python3-dbus = %{version}-%{release}
#R: python-devel >= 1:2.5  or  python3-devel

%description devel
C API for _dbus_bindings module.

%description devel -l pl.UTF-8
API C dla modułu _dbus_bindings.

%package -n python3-dbus
Summary:	Python 3 library for using D-BUS
Summary(pl.UTF-8):	Biblioteka do używania D-BUS oparta o Pythona 3
Group:		Libraries/Python
Requires:	dbus-glib >= 0.73
Requires:	dbus-libs >= 1.6

%description -n python3-dbus
D-BUS add-on library to integrate the standard D-BUS library with
Python 3.

%description -n python3-dbus -l pl.UTF-8
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z Pythonem 3.

%prep
%setup -qn %{rname}-%{version}
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%if %{with python3}
mkdir py3
cd py3
../%configure \
	PYTHON=%{__python3} \
	PYTHON_LIBS=-lpython3
%{__make}
cd ..
%endif

%if %{with python2}
mkdir py2
cd py2
../%configure \
	PYTHON=%{__python} \
	PYTHON_LIBS=-lpython
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

# use sitedir instead of sitescriptdir to match PyQt4 dbus/mainloop dir
%if %{with python2}
%{__make} -C py2 install \
	pythondir=%{py_sitedir} \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_dbus*.la
%endif

%if %{with python3}
%{__make} -C py3 install \
	pythondir=%{py3_sitedir} \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/_dbus*.la
%endif

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/dbus-python

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/*.txt
%dir %{py_sitedir}/dbus
%{py_sitedir}/dbus/*.py[co]
%dir %{py_sitedir}/dbus/mainloop
%{py_sitedir}/dbus/mainloop/*.py[co]
%attr(755,root,root) %{py_sitedir}/_dbus_bindings.so
%attr(755,root,root) %{py_sitedir}/_dbus_glib_bindings.so
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/dbus-1.0/dbus/dbus-python.h
%{_pkgconfigdir}/dbus-python.pc

%if %{with python3}
%files -n python3-dbus
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/*.txt
%dir %{py3_sitedir}/dbus
%{py3_sitedir}/dbus/__pycache__
%{py3_sitedir}/dbus/*.py
%dir %{py3_sitedir}/dbus/mainloop
%{py3_sitedir}/dbus/mainloop/__pycache__
%{py3_sitedir}/dbus/mainloop/*.py
%attr(755,root,root) %{py3_sitedir}/_dbus_bindings.so
%attr(755,root,root) %{py3_sitedir}/_dbus_glib_bindings.so
%endif
