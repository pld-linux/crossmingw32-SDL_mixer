%define		realname	SDL_mixer
Summary:	Simple DirectMedia Layer - Sample Mixer Library - MinGW32 cross version
Name:		crossmingw32-%{realname}
Version:	1.2.12
Release:	1
License:	Zlib-like
Group:		Libraries
Source0:	http://www.libsdl.org/projects/SDL_mixer/release/%{realname}-%{version}.tar.gz
# Source0-md5:	e03ff73d77a55e3572ad0217131dc4a1
URL:		http://www.libsdl.org/projects/SDL_mixer/
BuildRequires:	crossmingw32-SDL
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-libvorbis
BuildRequires:	crossmingw32-w32api
Requires:	crossmingw32-SDL
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

# -z options are invalid for mingw linker
%define		filterout_ld		-Wl,-z,.*

%description
Due to popular demand, here is a simple multi-channel audio mixer. It
supports 4 channels of 16 bit stereo audio, plus a single channel of
music, mixed by the popular MikMod MOD, Timidity MIDI and SMPEG MP3
libraries.

This package contains the cross version for Win32.

%package static
Summary:	Static SDL_mixer libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SDL_mixer libraries (cross MinGW32 version).

%package dll
Summary:	SDL_mixer - DLL library for Windows
Group:		Applications/Emulators
Requires:	crossmingw32-SDL-dll >= 1.2.10
Requires:	wine

%description dll
SDL_mixer - DLL library for Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%configure \
	--host=%{target} \
	--target=%{target} \
	--with-sdl-prefix=%{_prefix}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING README
%{_libdir}/libSDL_mixer.dll.a
%{_libdir}/libSDL_mixer.la
%{_includedir}/SDL/SDL_mixer.h
%{_pkgconfigdir}/SDL_mixer.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libSDL_mixer.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/SDL_mixer.dll
