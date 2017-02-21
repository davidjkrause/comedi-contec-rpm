Name:           comedilib
Version:        0.11.0
Release:        2%{?dist}
Summary:        Comedilib user spaces tools for comedi kernel driver

License:        GPLv3
Source0:        comedilib-0.11.0.tar.gz
Patch0:         0001-Add-fit_demo-and-fit_demo2-to-comedilib.patch

BuildRequires:  autoconf automake libtool gcc make flex bison
Requires:       module-init-tools

%description
comedilib package from comedi.org git, with two added demo programs
to show usage of the contec_fit driver

%package devel
Group: Development/Libraries
Summary: Development files for comedilib

%description devel
Development files for comedilib, primarily header files and
man pages


%prep
%setup -q
%patch0 -p1


%pre


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
install -m755 %{_builddir}/comedilib-0.11.0/demo/.libs/fit_demo $RPM_BUILD_ROOT%{_sbindir}/fit_demo
install -m755 %{_builddir}/comedilib-0.11.0/demo/.libs/fit_demo2 $RPM_BUILD_ROOT%{_sbindir}/fit_demo2

# Post-install
%post


# Post-uninstall
%postun


%files
%{_bindir}/comedi_board_info
%{_bindir}/comedi_test
%{_libdir}/libcomedi*
%{_libdir}/pkgconfig/comedilib.pc
%{_sbindir}/comedi_*
%{_sbindir}/fit_demo
%{_sbindir}/fit_demo2
%{_mandir}/man7/*
%{_mandir}/man8/*
/lib/udev/rules.d/90-comedi.rules
/etc/pcmcia/*


%files devel
%{_includedir}/comedi*
%{_datarootdir}/doc/comedilib/*
%{_mandir}/man1/*


%changelog
* Mon Feb 13 2017 David Krause <david.krause@gmail.com> - 0.11.0-1
- First comedilib package with fit_demo and fit_demo2

