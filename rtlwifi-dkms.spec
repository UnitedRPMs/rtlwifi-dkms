# This spec file is based on other projects, Sources available from
# https://aur.archlinux.org/packages/rtlwifi_new-dkms/
# http://xmodulo.com/build-kernel-module-dkms-linux.html (great guide about how to make modules with dkms)


%define debug_package %{nil}
%global	realname rtlwifi
%global kname rtlwifi

%global commit0 0547b3634353a91369c6df0b4965739dd1ddacec
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Summary:	Nonfree Newest rtlwifi firmware files for the Linux kernel
Name:		rtlwifi-dkms
Version:	0.6%{?gver}%{dist}
Release:	1%{?dist}
Source0:	https://github.com/lwfinger/rtlwifi_new/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:	dkms.conf
Source2:	blacklist-rtlwifi_new-dkms.conf
Provides:	kmod(%{kname}.ko) = %{version}
Requires(post):		dkms
Requires(preun):	dkms

License:	Redistributable, no modification permitted
Group:		System/Kernel and hardware
URL:		https://github.com/lwfinger/rtlwifi_new

%description
This package contains all the Newest Realtek rtlwifi wireless firmware files.

%prep
%autosetup -n %{realname}_new-%{commit0}
	# Set version
  sed -i "s/@PKGVER@/%{version}/" %{S:1} 

%build

%install
rm -rf %{buildroot}

_pkgname=%{kname}
pkgver=%{version}
dest=%{buildroot}/usr/src/${_pkgname/-dkms/}-%{version}

  mkdir -p ${dest}

	cp -rf %{_builddir}/%{realname}_new-%{commit0}/* ${dest}
	install -D -m 644 %{S:1} ${dest}

        install -dm755 "%{buildroot}/etc/modprobe.d"
        install -m644 %{S:2} "%{buildroot}/etc/modprobe.d/"

        install -dm755 %{buildroot}/usr/share/licenses/%{name}

%post 

# rmmod can fail
/sbin/rmmod %{kname} >/dev/null 2>&1 ||:
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{realname} -v %{version} --all || :
# now kdms install
/usr/sbin/dkms --rpm_safe_upgrade add -m %{realname} -v %{version} 
/usr/sbin/dkms --rpm_safe_upgrade build -m %{realname} -v %{version} 
/usr/sbin/dkms --rpm_safe_upgrade install -m %{realname} -v %{version}

%preun 
# rmmod can fail
/sbin/rmmod %{kname} >/dev/null 2>&1 ||:
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{realname} -v %{version} --all || :

%posttrans 
if [ -z "$DURING_INSTALL" ] ; then
    /sbin/modprobe rtlwifi >/dev/null 2>&1 ||:
fi

%clean
rm -rf %{buildroot}

%files 
%doc firmware/rtlwifi/Realtek-Firmware-License.txt
%dir %{_usr}/src/%{realname}-%{version}
%{_usr}/src/%{realname}-%{version}/*
%config %{_sysconfdir}/modprobe.d/blacklist-%{realname}_new-dkms.conf

%changelog

* Mon Nov 06 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  0.6-1.git0547b36
- Initial build
