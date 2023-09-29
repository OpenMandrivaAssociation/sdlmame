# Better disable debug because with it's so greedy for resources
# that linkage fails
%define _enable_debug_packages 0
%define debugcflags %nil
%define debug_package %{nil}
%define _disable_lto 1

Summary:	SDL MAME is an arcade emulator
Name:		sdlmame
Version:	0.259
Release:	1
%define sversion	%(sed -r -e "s/\\.//" -e "s/(.*)u(.)/\\1/" <<<%{version})
License:	Freeware
Group:		Emulators
Url:		http://mamedev.org/
#http://mamedev.org/downloader.php?&file=mame%{sversion}s.zip
Source0:	https://github.com/mamedev/mame/archive/refs/tags/mame%{sversion}.tar.gz
Source1:	sdlmame-wrapper
Source2:	sdlmess-wrapper
#Source3:	sdlmame-extra.tar.bz2
# Repack from git and 0.146 as these files are no longer in sources zip
#Source4:	sdlmess-extra-0.147.tar.bz2

BuildRequires:	dos2unix
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_ttf)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  cmake(ECM)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Widgets)

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

%prep
%setup -qn mame-mame%{sversion}

#files missing : ui.bdf, keymaps
#tar xf %{SOURCE3}
#files missing : arkwork, sysinfo.dat
#tar xf %{SOURCE4}

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
 OPT_FLAGS="%{optflags}" \
 VERBOSE=1 \
 PYTHON_EXECUTABLE=python \
 TOOLS=1

%install
install -d -m 755 %{buildroot}%{_gamesbindir}
[ -f mame ] && install -m 755 mame %{buildroot}/%{_gamesbindir}/sdlmame.real
[ -f mame64 ] && install -m 755 mame64 %{buildroot}/%{_gamesbindir}/sdlmame.real

#tools
#useful to manage roms
install -m 755 chdman %{buildroot}%{_gamesbindir}/chdman-sdlmame
install -m 755 romcmp %{buildroot}%{_gamesbindir}/romcmp-sdlmame
#useful to create a new keymap
#install -m 755 testkeys %{buildroot}%{_gamesbindir}/testkeys-sdlmame
#other tools built:
#jedutils, makemeta, regrep, srcclean

#"support files" moved to sdlmame-extra-data
#but the directory is still owned by this package
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame

#ui font
install -m 644 uismall.bdf %{buildroot}/%{_gamesdatadir}/sdlmame/

#keymaps
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame/keymaps
install -m 644 keymaps/* %{buildroot}/%{_gamesdatadir}/sdlmame/keymaps/

#various directories and files
install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame/hash
install -m 644 hash/* %{buildroot}%{_gamesdatadir}/sdlmame/hash/

pushd artwork
    find -type d -exec install -d $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/artwork/{} \;
    find -type f -exec install -pm 644 {} $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/artwork/{} \;
popd
pushd bgfx
    find -type d -exec install -d $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/bgfx/{} \;
    find -type f -exec install -pm 644 {} $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/bgfx/{} \;
popd

#install wrapper
install -m 755 %{SOURCE1} %{buildroot}%{_gamesbindir}/sdlmame

