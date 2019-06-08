Name:       xavs2
Version:    1.3
Release:    1%{?dist}
Summary:    An open-source encoder of AVS2-P2/IEEE1857.4 video coding standard
URL:        https://github.com/pkuvcl/%{name}
License:    GPLv2

Source0:    https://github.com/pkuvcl/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

#BuildRequires:  execstack
BuildRequires:  gcc
BuildRequires:  yasm

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
%autosetup -p1

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
    -e 's|-mpreferred-stack-boundary=5 ||g' \
    config.mak

%make_build

%install
cd build/linux
%make_install
execstack -c \
    %{buildroot}%{_libdir}/lib%{name}.so.* \
    %{buildroot}%{_bindir}/%{name}

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
* Sat Jun 08 2019 Simone Caronni <negativo17@gmail.com> - 1.3-1
- First build.
