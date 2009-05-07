%define	major 2
%define apiver 2.0
%define libname %mklibname %{name} %{apiver} %{major}
%define develname %mklibname %{name} -d

%define _gtkdocdir	%{_datadir}/gtk-doc/html
%{expand:%%define _aclocaldir %(aclocal --print-ac-dir 2>/dev/null)}

%define _requires_exceptions libgmime
Summary:		The libGMIME library
Name:			gmime
Version:		2.2.23
Release:		%mkrel 1
License:		LGPLv2+
Group:			System/Libraries
URL:			http://spruce.sourceforge.net/gmime
Source0:		http://spruce.sourceforge.net/gmime/sources/v2.2/gmime-%{version}.tar.bz2
BuildRequires:		glib2-devel
BuildRequires:		gtk-doc
BuildRequires:		libz-devel
BuildRequires:		mono-devel
BuildRequires:		gtk-sharp2-devel
BuildRequires:		gtk-sharp2
Buildroot:		%{_tmppath}/%{name}-%{version}-buildroot

%description
This library allows you to manipulate MIME messages.

%package -n %{name}-utils
Summary:	Utilities using the libGMIME library
Group:		File tools
Requires:	%{libname} = %{version}-%{release}

%description -n %{name}-utils
This package contains gmime-uudecode and gmime-uuencode and will 
allow you to manipulate MIME messages. These utilities can also be
used instead of uudecode and uuencode from the sharutils package. 

%package -n %{libname}
Summary:	The libGMIME library
Group:		System/Libraries
Obsoletes:	%mklibname %{name} 2.0
Provides:	%mklibname %{name} 2.0
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This library allows you to manipulate MIME messages.

%package -n %{develname}
Summary:	Development library and header files for the lib%{name} library
Group:		Development/C
Provides:	lib%{name}-devel
Provides:	%{name}-devel
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname %{name} 2.0 -d
Provides:	%mklibname %{name} 2.0 -d

%description -n %{develname}
This package contains the lib%{name} development library and its header files.

%package sharp
Summary:	GMIME# bindings for mono
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description sharp
This library allows you to manipulate MIME messages.

%prep

%setup -q

%build
#libtoolize --copy --force; aclocal; autoconf; automake

%configure2_5x \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc

#gw parallel build broken in 2.1.15
# (tpg) mono stuff doesn't like parallel build, this solves it
%(echo %make|perl -pe 's/-j\d+/-j1/g')

%check
make check

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

# these are provided by sharutils, gotta rename them...
mv %{buildroot}%{_bindir}/uudecode %{buildroot}%{_bindir}/gmime-uudecode
mv %{buildroot}%{_bindir}/uuencode %{buildroot}%{_bindir}/gmime-uuencode

# cleanup
rm -f %{buildroot}%{_libdir}/gmimeConf.sh

#multiarch 
%multiarch_binaries %{buildroot}%{_bindir}/gmime-config


%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files -n %{name}-utils
%defattr(-,root,root)
%{_bindir}/gmime-uudecode
%{_bindir}/gmime-uuencode

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*%{apiver}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog PORTING README TODO
%multiarch %{multiarch_bindir}/gmime-config
%{_bindir}/gmime-config
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/gmime-2.0.pc
%{_includedir}/*
%doc %{_gtkdocdir}/*

%files sharp
%defattr(-,root,root)
%{_prefix}/lib/mono/gac/%{name}-sharp
%{_prefix}/lib/mono/%{name}-sharp
%{_libdir}/pkgconfig/%{name}-sharp.pc
%{_datadir}/gapi-2.0/gmime-api.xml
