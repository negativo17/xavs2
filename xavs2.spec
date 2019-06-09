%global commit0 f45c3407374ec8b8df221a049c42b3415ac8d3bb
%global date 20181229
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:       xavs2
Version:    1.3
Release:    2%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Summary:    An open-source encoder of AVS2-P2/IEEE1857.4 video coding standard
URL:        https://github.com/pkuvcl/%{name}
License:    GPLv2

%if %{?shortcommit0}
Source0:    https://github.com/pkuvcl/%{name}/archive/%{commit0}/%{name}-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%else
Source0:    https://github.com/pkuvcl/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  nasm >= 2.13

%description
xavs2 is an open-source encoder of AVS2-P2/IEEE1857.4 video coding standard.

This package contains the command line encoder.

%package libs
Summary:    AVS2-P2/IEEE1857.4 encoder library

%description libs
davs2 is an open-source encoder of AVS2-P2/IEEE1857.4 video coding standard.

This package contains the shared library.

%package devel
Summary:    AVS2-P2/IEEE1857.4 encoder library development files
Requires:   %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
davs2 is an open-source encoder of AVS2-P2/IEEE1857.4 video coding standard.

This package contains the shared library development files.

%prep
%autosetup %{?shortcommit0:-n %{name}-%{commit0}}

%build
cd build/linux
%configure \
    --bit-depth='8' \
    --chroma-format='all' \
    --disable-static \
    --enable-pic \
    --enable-shared

# Remove hardcoded CFLAGS on generated file containing variables
sed -i \
    -e 's|CFLAGS=.*%{optflags}|CFLAGS=%{optflags}|g' \
    config.mak

%make_build

%install
cd build/linux
%make_install

find %{buildroot} -name "*a" -delete

%ldconfig_scriptlets libs

%files
%{_bindir}/%{name}

%files libs
%license COPYING
%{_libdir}/lib%{name}.so.13

%files devel
%doc README.md
%{_includedir}/%{name}.h
%{_includedir}/%{name}_config.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sun Jun 09 2019 Simone Caronni <negativo17@gmail.com> - 1.3-2.20181229gitf45c340
- Update to latest snapshot to fix various bugs.

* Sat Jun 08 2019 Simone Caronni <negativo17@gmail.com> - 1.3-1
- First build.
