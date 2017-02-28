Name:           comedi
Version:        0.7.76.1
Release:        7%{?dist}
URL:            https://github.com/davidjkrause/comedi-contec-rpm
Summary:        Data Acquisition device kernel driver with Contec FiT driver addition
License:        GPLv3

%global commit0 1881165dd06542c56f7ad6f72022293562df3337
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Source0:        https://github.com/Linux-Comedi/%{name}/archive/%{commit0}/%{name}-%{version}.tar.gz
Patch0:         0001-Add-contec_fit-driver-to-comedi.patch

BuildRequires:  kernel-devel autoconf automake gcc make module-init-tools
Requires:       module-init-tools
Requires(pre):  shadow-utils

# Fedora is broken, it installs kernel-debug-devel when you try to install kernel-devel
# See https://bugzilla.redhat.com/show_bug.cgi?id=1228897
# Just deal with the mis-installed package by checking for kernel-devel
# If it's installed at this point, use it, otherwise use kernel-debug-devel

%if %(rpm -q --quiet kernel-devel && echo 1 || echo 0)
%global current_kernel $(rpm -q kernel-devel | sed -r 's/kernel-devel-(.*)/\\1/')
%else
%global current_kernel $(rpm -q kernel-debug-devel | sed -r 's/kernel-debug-devel-(.*)/\\1/')+debug
%endif

# There are no debug files associated with a kernel module, so don't generate debuginfo package
%global debug_package %{nil}


%description
Package from comedi.org for kernel driver, with added driver for
Contec FiT devices

%prep
%autosetup -n %{name}-%{commit0} -p1


# Add an iogroup
%pre
getent group iogroup >/dev/null || groupadd -r iogroup


%build
./autogen.sh
./configure \
   --with-rpm-target=x86_64 \
   --libdir=%{_usr}/%{_lib} \
   --with-linuxsrcdir=/usr/src/kernels/%{current_kernel} \
   --with-linuxdir=/usr/src/kernels/%{current_kernel}
make


%install
rm -rf $RPM_BUILD_ROOT
%make_install
# Remove /lib/modules/... files created by depmod, they are not useful in
# an RPM, and need to be re-created on the machine where the driver is 
# installed, which happens in the post step
rm $RPM_BUILD_ROOT/lib/modules/%{current_kernel}/modules.*


# Post-install, run depmod so comedi and related drivers can be modprobe'd
%post
depmod -a
if [ ! -e /dev/comedi0 ]; then
    mknod -m 660 /dev/comedi0 c 98 0
    chown root.iogroup /dev/comedi0
fi

# Post-uninstall, re-run depmod to not leave any dependencies
%postun
depmod -a


%files
/lib/modules/*/comedi/comedi.ko
/lib/modules/*/comedi/drivers/*
/lib/modules/*/comedi/kcomedilib/kcomedilib.ko

%changelog
* Tue Feb 28 2017 David Krause <david.krause@gmail.com> - 0.7.76.1-7
- Pull source from github
- Cleanups for rpmlint

* Fri Feb 10 2017 David Krause <david.krause@gmail.com> - 0.7.76.1-1
- First comedi package with contec_fit

