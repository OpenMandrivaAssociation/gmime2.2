%define debug_package %{nil}
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define _gtkdocdir	%{_datadir}/gtk-doc/html
%{expand:%%define _aclocaldir %(aclocal --print-ac-dir 2>/dev/null)}

%define api	2.0
%define	major	2
%define libname %mklibname gmime %{api} %{major}
%define devname %mklibname %{name} -d

Summary:	The libGMIME library
Name:		gmime2.2
Version:	2.2.27
Release:	10
License:	LGPLv2+
Group:		System/Libraries
Url:		http://spruce.sourceforge.net/gmime
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/gmime/%{url_ver}/gmime-%{version}.tar.bz2
Patch0:		gmime-2.2.23-format-strings.patch
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(zlib)

%description
This library allows you to manipulate MIME messages.

%package -n %{name}-utils
Summary:	Utilities using the libGMIME library
Group:		File tools
Conflicts:	gmime-utils

%description -n %{name}-utils
This package contains gmime-uudecode and gmime-uuencode and will 
allow you to manipulate MIME messages. These utilities can also be
used instead of uudecode and uuencode from the sharutils package. 

%package -n %{libname}
Summary:	The libGMIME library
Group:		System/Libraries

%description -n %{libname}
This library allows you to manipulate MIME messages.

%package -n %{devname}
Summary:	Development library and header files for the lib%{name} library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains the lib%{name} development library and its header files.

%prep

%setup -qn gmime-%{version}
%autopatch -p1

%build
%configure2_5x \
	--disable-static \
	--with-html-dir=%{_gtkdocdir} \
	--disable-mono

#gw parallel build broken in 2.1.15
# (tpg) mono stuff doesn't like parallel build, this solves it
%(echo %make CFLAGS='-UG_DISABLE_DEPRECATED' |perl -pe 's/-j\d+/-j1/g')

%check
make check

%install
%makeinstall_std

# these are provided by sharutils, gotta rename them...
mv %{buildroot}%{_bindir}/uudecode %{buildroot}%{_bindir}/gmime-uudecode
mv %{buildroot}%{_bindir}/uuencode %{buildroot}%{_bindir}/gmime-uuencode

# cleanup
rm -f %{buildroot}%{_libdir}/gmimeConf.sh

#multiarch 
%multiarch_binaries %{buildroot}%{_bindir}/gmime-config

%files -n %{name}-utils
%{_bindir}/gmime-uudecode
%{_bindir}/gmime-uuencode

%files -n %{libname}
%{_libdir}/libgmime-%{api}.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog PORTING README TODO
%{multiarch_bindir}/gmime-config
%{_bindir}/gmime-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/gmime-2.0.pc
%{_includedir}/*
%doc %{_gtkdocdir}/*

