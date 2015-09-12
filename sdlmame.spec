# Better disable debug because with it's so greedy for resources
# that linkage fails
%define _enable_debug_packages %{nil}
%define debug_package %{nil}

Summary:	SDL MAME is an arcade emulator
Name:		sdlmame
Version:	0.153
Release:	3
%define sversion	%(sed -r -e "s/\\.//" -e "s/(.*)u(.)/\\1/" <<<%{version})
License:	Freeware
Group:		Emulators
Url:		http://mamedev.org/
#http://mamedev.org/downloader.php?&file=mame%{sversion}s.zip
Source0:	mame%{sversion}s.zip
Source1:	sdlmame-wrapper
Source2:	sdlmess-wrapper
Source3:	sdlmame-extra.tar.bz2
# Repack from git and 0.146 as these files are no longer in sources zip
Source4:	sdlmess-extra-0.147.tar.bz2

Patch0:		sdlmame-0.151-verbose-build.patch
# x86_64 build fails due to extra optimizations
Patch1:		sdlmame-0.150-dont-force-inline.patch
# We don't want 64 bit binaries to have extra suffix
Patch2:		sdlmame-0.147-no64suffix.patch

BuildRequires:	dos2unix
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_ttf)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(zlib)
ExclusiveArch:	%{ix86} x86_64 ppc

%description
SDL MAME is an arcade emulator using SDL, and based on the Multiple Arcade
Machine Emulator (MAME).

You can find a some freeware and their description on http://mamedev.org/roms/

If you some tricks to finish a game, the cheat.zip file is now provided in a
other package named sdlmame-extra-data.

%files
%defattr(0644,root,games,0755)
%doc docs/*
%attr(0755,root,games) %{_gamesbindir}/sdlmame*
%attr(0755,root,games) %{_gamesbindir}/*-sdlmame
%{_gamesdatadir}/sdlmame

#----------------------------------------------------------------------------

%package -n sdlmess
Summary:	SDL MESS emulates a large variety of different systems
Group:		Emulators

%description -n sdlmess
SDL MESS is a free emulator which emulates a large variety of different
systems (computers and home entertainment systems).
It uses SDL, and is based on MESS.

%files -n sdlmess
%defattr(0644,root,games,0755)
%doc docs/*
%attr(0755,root,games) %{_gamesbindir}/sdlmess*
%attr(0755,root,games) %{_gamesbindir}/*-sdlmess
%{_gamesdatadir}/sdlmess

#----------------------------------------------------------------------------

%prep
%setup -c -n %{name}-%{version} -q
unzip -qq mame.zip
%patch0 -p1
%patch1 -p1
%patch2 -p1

#files missing : ui.bdf, keymaps
tar xf %{SOURCE3}
#files missing : arkwork, sysinfo.dat
tar xf %{SOURCE4}

find . -type f | xargs dos2unix

%build
#notes:
#fullname is prefix+name+suffix+suffix64+suffixdebug(+suffixexe)
#optimizing for specific processor adds suffixes:
#DEBUG=1 for the debugger
#SYMBOLS=1 to build a -debug package
#set ARCHOPTS for architecture-specific optimizations
#(-march=,-msse3,-mcpu=,...)
#Arch is auto-detected now, DRC options are set accordingly
#no need for PTR64=1, PPC=1, X86_MIPS3_DRC=, X86_PPC_DRC=, etc
%make all TARGET=mame \
 PREFIX=sdl \
 NOWERROR=1 \
 BUILD_EXPAT= \
 BUILD_FLAC= \
 BUILD_ZLIB= \
 NO_USE_QTDEBUG=1 \
 NO_DEBUGGER=1 \
 OPT_FLAGS="%{optflags}"

%make all TARGET=mess \
 PREFIX=sdl \
 NOWERROR=1 \
 BUILD_EXPAT= \
 BUILD_FLAC= \
 BUILD_ZLIB= \
 NO_USE_QTDEBUG=1 \
 NO_DEBUGGER=1 \
 OPT_FLAGS="%{optflags}"

%install
install -d -m 755 %{buildroot}%{_gamesbindir}
install -m 755 sdlmame %{buildroot}/%{_gamesbindir}/sdlmame.real
install -m 755 sdlmess* %{buildroot}/%{_gamesbindir}/sdlmess.real

#tools
#useful to manage roms
install -m 755 chdman %{buildroot}%{_gamesbindir}/chdman-sdlmame
install -m 755 chdman %{buildroot}%{_gamesbindir}/chdman-sdlmess
install -m 755 romcmp %{buildroot}%{_gamesbindir}/romcmp-sdlmame
install -m 755 romcmp %{buildroot}%{_gamesbindir}/romcmp-sdlmess
#useful to create a new keymap
install -m 755 testkeys %{buildroot}%{_gamesbindir}/testkeys-sdlmame
install -m 755 testkeys %{buildroot}%{_gamesbindir}/testkeys-sdlmess
#other tools built:
#jedutils, makemeta, regrep, srcclean

#"support files" moved to sdlmame-extra-data
#but the directory is still owned by this package
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmess

#ui font
install -m 644 ui.bdf %{buildroot}/%{_gamesdatadir}/sdlmame/
install -m 644 ui.bdf %{buildroot}/%{_gamesdatadir}/sdlmess/

#keymaps
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame/keymaps
install -m 644 keymaps/* %{buildroot}/%{_gamesdatadir}/sdlmame/keymaps/
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmess/keymaps
install -m 644 keymaps/* %{buildroot}/%{_gamesdatadir}/sdlmess/keymaps/

#various directories and files
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmess/artwork
install -m 644 artwork/* %{buildroot}%{_gamesdatadir}/sdlmess/artwork/
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame/hash
install -m 644 hash/* %{buildroot}%{_gamesdatadir}/sdlmame/hash/
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmess/hash
install -m 644 hash/* %{buildroot}%{_gamesdatadir}/sdlmess/hash/

#sysinfo.dat
install -m 644 sysinfo.dat %{buildroot}%{_gamesdatadir}/sdlmess/

#install wrapper
install -m 755 %{SOURCE1} %{buildroot}%{_gamesbindir}/sdlmame
install -m 755 %{SOURCE2} %{buildroot}%{_gamesbindir}/sdlmess

