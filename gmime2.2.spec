%define	major 2
%define apiver 2.0
%define libname %mklibname gmime %{apiver} %{major}
%define develname %mklibname %{name} -d

%define _gtkdocdir	%{_datadir}/gtk-doc/html
%{expand:%%define _aclocaldir %(aclocal --print-ac-dir 2>/dev/null)}

%define _requires_exceptions libgmime
Summary:		The libGMIME library
Name:			gmime2.2
Version:		2.2.25
Release:		%mkrel 1
License:		LGPLv2+
Group:			System/Libraries
URL:			http://spruce.sourceforge.net/gmime
Source0:		ftp://ftp.gnome.org/pub/GNOME/sources/gmime/gmime-%{version}.tar.bz2
Patch: gmime-2.2.23-format-strings.patch
BuildRequires:		glib2-devel
BuildRequires:		libz-devel
Buildroot:		%{_tmppath}/%{name}-%{version}-buildroot

%description
This library allows you to manipulate MIME messages.

%package -n %{name}-utils
Summary:	Utilities using the libGMIME library
Group:		File tools
Requires:	%{libname} = %{version}-%{release}
Conflicts: gmime-utils

%description -n %{name}-utils
This package contains gmime-uudecode and gmime-uuencode and will 
allow you to manipulate MIME messages. These utilities can also be
used instead of uudecode and uuencode from the sharutils package. 

%package -n %{libname}
Summary:	The libGMIME library
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This library allows you to manipulate MIME messages.

%package -n %{develname}
Summary:	Development library and header files for the lib%{name} library
Group:		Development/C
Provides:	lib%{name}-devel = %version-%release
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
This package contains the lib%{name} development library and its header files.

%prep

%setup -q -n gmime-%version
%patch -p1

%build

%configure2_5x \
	--with-html-dir=%{_gtkdocdir} \
	--disable-mono

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
