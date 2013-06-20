%define		realname	SDL_mixer
Summary:	Simple DirectMedia Layer - Sample Mixer Library - MinGW32 cross version
Summary(pl.UTF-8):	Simple DirectMedia Layer - biblioteka miksująca próbki dźwiękowe - wersja skrośna MinGW32
Name:		crossmingw32-%{realname}
Version:	1.2.12
Release:	1
License:	Zlib-like
Group:		Libraries
Source0:	http://www.libsdl.org/projects/SDL_mixer/release/%{realname}-%{version}.tar.gz
# Source0-md5:	e03ff73d77a55e3572ad0217131dc4a1
URL:		http://www.libsdl.org/projects/SDL_mixer/
BuildRequires:	crossmingw32-SDL >= 1.2.10
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-libvorbis >= 1.0
BuildRequires:	crossmingw32-w32api
Requires:	crossmingw32-SDL >= 1.2.10
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

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
Due to popular demand, here is a simple multi-channel audio mixer. It
supports 4 channels of 16 bit stereo audio, plus a single channel of
music, mixed by the popular MikMod MOD, Timidity MIDI and SMPEG MP3
libraries.

This package contains the cross version for Win32.

%description -l pl.UTF-8
SDL_mixer to prosty wielokanałowy mikser audio. Obsługuje 4 kanały
16-bitowego dźwięku stereo plus jeden kanał dla muzyki miksowanej
przez popularne biblioteki MikMod MOD, Timitity MIDI i SMPEG MP3.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static SDL_mixer library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka SDL_mixer (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SDL_mixer library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka SDL_mixer (wersja skrośna MinGW32).

%package dll
Summary:	SDL_mixer - DLL library for Windows
Summary(pl.UTF-8):	SDL_mixer - biblioteka DLL dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-SDL-dll >= 1.2.10
Requires:	wine

%description dll
SDL_mixer - DLL library for Windows.

%description dll -l pl.UTF-8
SDL_mixer - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%configure \
	--host=%{target} \
	--target=%{target} \
	--with-sdl-prefix=%{_prefix} \
	--disable-music-mp3 \
	--disable-music-mod

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
