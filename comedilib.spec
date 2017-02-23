Name:           comedilib
Version:        0.11.0
Release:        3%{?dist}
URL:            https://github.com/davidjkrause/comedi-contec-rpm
Summary:        User space tools for comedi kernel driver
License:        LGPLv2+

%global commit0 5a5a46b4eec5c8112d1b54406287f9cf7368cda7
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Source0:        https://github.com/Linux-Comedi/%{name}/archive/%{commit0}/%{name}-%{version}.tar.gz
Patch0:         0001-Add-fit_demo-and-fit_demo2-to-comedilib.patch

BuildRequires:  autoconf automake libtool gcc make flex bison
Requires:       module-init-tools

%description
Package from comedi.org git, with two added demo programs to show
usage of the contec_fit driver

%package devel
Group: Development/Libraries
Summary: Development files for user space tools for comedi kernel driver

%description devel
Development files - header files, static libraries, and man pages


%prep
%autosetup -n %{name}-%{commit0} -p1


%build
./autogen.sh
./configure \
   --with-udev-hotplug=/lib \
   --sysconfdir=%{_sysconfdir} \
   --disable-dependency-tracking \
   --prefix=%{_usr} \
   --libdir=%{_usr}/%{_lib}
make


%install
rm -rf $RPM_BUILD_ROOT
%make_install
# These files conflict with another package,so delete them rather than install
# Deleting them lets us have a clean RPM with no unpackaged files
rm $RPM_BUILD_ROOT/lib/firmware/usbdux_firmware.bin
rm $RPM_BUILD_ROOT/lib/firmware/usbduxfast_firmware.bin
rm $RPM_BUILD_ROOT/lib/firmware/usbduxsigma_firmware.bin
mkdir -p $RPM_BUILD_ROOT/usr/local/bin
install -m755 %{_builddir}/%{name}-%{commit0}/demo/.libs/fit_demo $RPM_BUILD_ROOT%{_sbindir}/fit_demo
install -m755 %{_builddir}/%{name}-%{commit0}/demo/.libs/fit_demo2 $RPM_BUILD_ROOT%{_sbindir}/fit_demo2

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/comedi_board_info
%{_bindir}/comedi_test
%{_libdir}/libcomedi.so
%{_libdir}/libcomedi.so.0
%{_libdir}/libcomedi.so.0.11.0
%{_sbindir}/comedi_*
%{_sbindir}/fit_demo
%{_sbindir}/fit_demo2
%{_mandir}/man7/*
%{_mandir}/man8/*
/lib/udev/rules.d/90-comedi.rules
/etc/pcmcia/comedi
%config(noreplace) /etc/pcmcia/comedi.conf
%config(noreplace) /etc/pcmcia/comedi.opts


%files devel
%{_includedir}/comedi*
%{_datarootdir}/doc/comedilib/*
%{_mandir}/man1/*
%{_libdir}/libcomedi.a
%{_libdir}/libcomedi.la
%{_libdir}/pkgconfig/comedilib.pc

%changelog
* Wed Feb 22 2017 David Krause <david.krause@gmail.com> - 0.11.0-3
- Correct license
- Add URL for .spec file
- Update summary to address rpmlint issue
- Move dev libraries to devel package
- Run ldconfig on install and uninstall
- Handle /etc/pcmcia files

* Mon Feb 13 2017 David Krause <david.krause@gmail.com> - 0.11.0-1
- First comedilib package with fit_demo and fit_demo2

