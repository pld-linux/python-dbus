#
# Conditional build:
%bcond_without	python2		# Python 2.x module
%bcond_without	python3		# Python 3.x module
%bcond_without	apidocs		# Sphinx-based API documentation
#
%define		rname		dbus-python
#
Summary:	Python library for using D-BUS
Summary(pl.UTF-8):	Biblioteka do używania D-BUS oparta o Pythona
Name:		python-dbus
Version:	1.2.8
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://dbus.freedesktop.org/releases/dbus-python/%{rname}-%{version}.tar.gz
# Source0-md5:	7379db774c10904f27e7e2743d90fb43
URL:		https://www.freedesktop.org/wiki/Software/DBusBindings
BuildRequires:	autoconf >= 2.59c
BuildRequires:	autoconf-archive
BuildRequires:	automake >= 1:1.13
BuildRequires:	cpp
BuildRequires:	dbus-devel >= 1.8
BuildRequires:	glib2-devel >= 1:2.40
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
%if %{with apidocs}
BuildRequires:	python-Sphinx
BuildRequires:	python-sphinx_rtd_theme
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
%if %{with apidocs} && %{without python2}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-sphinx_rtd_theme
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	dbus-libs >= 1.8
Requires:	glib2 >= 1:2.40
Requires:	python-libxml2 >= 1:2.6.26
Requires:	python-modules >= 1:2.7
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
Requires:	dbus-devel >= 1.8
Requires:	glib2-devel >= 1:2.40
#R: python-dbus = %{version}-%{release}  or  python3-dbus = %{version}-%{release}
#R: python-devel >= 1:2.7  or  python3-devel >= 1:3.4

%description devel
C API for _dbus_bindings module.

%description devel -l pl.UTF-8
API C dla modułu _dbus_bindings.

%package apidocs
Summary:	API documentation for Python dbus module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona dbus
Group:		Documentation

%description apidocs
API documentation for Python dbus module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona dbus.

%package -n python3-dbus
Summary:	Python 3 library for using D-BUS
Summary(pl.UTF-8):	Biblioteka do używania D-BUS oparta o Pythona 3
Group:		Libraries/Python
Requires:	dbus-libs >= 1.8
Requires:	glib2 >= 1:2.40
Requires:	python3-modules >= 1:3.4

%description -n python3-dbus
D-BUS add-on library to integrate the standard D-BUS library with
Python 3.

%description -n python3-dbus -l pl.UTF-8
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z Pythonem 3.

%prep
%setup -qn %{rname}-%{version}

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%if %{with python3}
mkdir py3
cd py3
../%configure \
	PYTHON=%{__python3} \
	PYTHON_LIBS=-lpython3 \
	--enable-documentation%{?with_python2:=no}%{!?with_python2:%{!?with_apidocs:=no}}
%{__make}
cd ..
%endif

%if %{with python2}
mkdir py2
cd py2
../%configure \
	PYTHON=%{__python} \
	PYTHON_LIBS=-lpython \
	--enable-documentation%{!?with_apidocs:=no}
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

%if %{with apidocs}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/dbus-python/{_sources,objects.inv}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/{API_CHANGES,tutorial}.txt
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

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/dbus-python
%endif

%if %{with python3}
%files -n python3-dbus
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/{API_CHANGES,tutorial}.txt
%dir %{py3_sitedir}/dbus
%{py3_sitedir}/dbus/__pycache__
%{py3_sitedir}/dbus/*.py
%dir %{py3_sitedir}/dbus/mainloop
%{py3_sitedir}/dbus/mainloop/__pycache__
%{py3_sitedir}/dbus/mainloop/*.py
%attr(755,root,root) %{py3_sitedir}/_dbus_bindings.so
%attr(755,root,root) %{py3_sitedir}/_dbus_glib_bindings.so
%endif
