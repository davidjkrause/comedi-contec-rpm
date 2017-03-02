%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:		comedilib
Version:	0.11.0
Release:	1%{?dist}
Summary:	Data Acquisition library for the Comedi driver
License:	LGPLv2
Group:		System Environment/Kernel
URL:		http://www.comedi.org/

%global commit0 5a5a46b4eec5c8112d1b54406287f9cf7368cda7
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
Source0:        https://github.com/Linux-Comedi/%{name}/archive/%{commit0}/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel
BuildRequires:	docbook-utils
BuildRequires:	swig
BuildRequires:	flex
BuildRequires:	autoconf automake libtool gcc make bison
Requires:	flex


%description
Comedilib is a user-space library that provides a developer-friendly
interface to Comedi devices. Included in the Comedilib distribution
is documentation, configuration and calibration utilities,
and demonstration programs.

%package devel
Summary:	Libraries/include files for Comedi
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
# pkgconfig deps are automatic in Fedora and EL>=6
%if 0%{?rhel} == 5
Requires:	pkgconfig
%endif

%description devel
Comedilib is a library for using Comedi, a driver interface for data
acquisition hardware.

%prep
%autosetup -n %{name}-%{commit0}

%build
./autogen.sh
# Ruby bindings don't build
%configure --disable-dependency-tracking --disable-static --disable-ruby-binding
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install 
chmod -x ${RPM_BUILD_ROOT}%{python_sitearch}/comedi.py
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/_comedi.la

# adding to installed docs in order to avoid using %%doc magic
for f in AUTHORS COPYING README ; do
    cp -p $f ${RPM_BUILD_ROOT}%{_docdir}/%{name}/${f}
done


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/comedi_*
%{_sbindir}/comedi_*
%{_sysconfdir}/pcmcia/comedi
%config(noreplace)%{_sysconfdir}/pcmcia/comedi.*
%{_libdir}/libcomedi.so.*
%{python_sitearch}/*
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/COPYING
%{_docdir}/%{name}/README
%{_docdir}/%{name}/*.conf

%files devel
%{_libdir}/libcomedi.so
%{_libdir}/pkgconfig/*
%{_includedir}/comedi*

%changelog
* Thu Mar 02 2017 David Krause <david.krause@gmail.com> - 0.11.0-1
- Update to v0.11.0 source release
- Use autoconf in build step
- Update man page paths for latest release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-18
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 14 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.1-13
- Fix duplicate documentation (#1001241) by not using %%doc magic
- Remove INSTALL instructions file
- Move _comedi.so Python module into base package
- chmod -x comedi.py Python module
- Don't exclude .pyc/.pyo files
- Remove %%defattr
- Add %%?_isa to base package dep

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.1-6
- disable static libs
- fix python macros

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan  7 2009 Marek Mahut <mmahut@fedoraproject.org> - 0.8.1-3
- RHBZ#473642 Unowned directories

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.1-2
- Rebuild for Python 2.6

* Wed Apr 23 2008 Marek Mahut <mmahut@fedoraproject.org> - 0.8.1-1
- Spec file rewrite
- Upstream release

* Mon Jun 03 2002 David Schleef <ds@schleef.org>
- update for new build system

* Thu Feb 21 2002 Tim Ousley <tim.ousley@ni.com>
- initial build of comedilib RPM

