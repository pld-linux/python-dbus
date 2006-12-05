#
%define		dbus_version	0.91
%define		expat_version	1:1.95.5
%define		glib2_version	1:2.12.1
%define		rname		dbus-python
#
Summary:	Python library for using D-BUS
Summary(pl):	Biblioteka do u¿ywania D-BUS oparta o Pythona
Name:		python-dbus
Version:	0.71
Release:	5
License:	AFL v2.1 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/%{rname}-%{version}.tar.gz
# Source0-md5:	ee893bc87b784a8c2285f5041b5e7033
Patch0:		dbus-python_fixes.patch
URL:		http://www.freedesktop.org/Software/DBusBindings
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	cpp
BuildRequires:	dbus-glib-devel >= 0.71
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-Pyrex >= 0.9.4.2
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
Requires:	dbus-glib >= 0.71
Requires:	python-libxml2 >= 1:2.6.26
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-BUS add-on library to integrate the standard D-BUS library with
Python.

%description -l pl
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z Pythonem.

%prep
%setup -qn %{rname}-%{version}
%patch0 -p1

%build
python setup.py build
	
%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
	
rm -f $RPM_BUILD_ROOT%{py_sitedir}/dbus/*.{py,la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# AFL not in common-licenses, so COPYING included
%doc AUTHORS COPYING ChangeLog NEWS
%dir %{py_sitedir}/dbus
%attr(755,root,root) %{py_sitedir}/dbus/*.so
%{py_sitedir}/dbus/*.py[co]
%{py_sitedir}/dbus_python-*.egg-info
