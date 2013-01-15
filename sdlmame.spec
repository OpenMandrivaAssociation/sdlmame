# Better disable debug because with it's so greedy for resources
# that linkage fails
%define _enable_debug_packages %{nil}
%define debug_package %{nil}

Name:		sdlmame
Version:	0.148
Release:	1
%define sversion	%(sed -r -e "s/\\.//" -e "s/(.*)u(.)/\\1/" <<<%{version})
%define uversion	%(sed -r -e "s/(.*u)(.)/\\2/;t;c\\0" <<<%{version})

Summary:	SDL MAME is an arcade emulator
License:	Freeware
Group:		Emulators
URL:		http://mamedev.org/
#http://mamedev.org/downloader.php?&file=mame%{sversion}s.zip
Source0:	mame%{sversion}s.zip
Source1:	sdlmame-wrapper
Source2:	sdlmess-wrapper
Source3:	sdlmame-extra.tar.bz2
# Repack from git and 0.146 as these files are no longer in sources zip
Source4:	sdlmess-extra-0.147.tar.bz2

Patch0:		mame-verbosebuild.patch
# x86_64 build fails due to extra optimizations
Patch1:		sdlmame-0.148-dont-force-inline.patch
# We don't want 64 bit binaries to have extra suffix
Patch2:		sdlmame-0.147-no64suffix.patch

#Sources 10+ : u1, u2 etc zip files containing changelogs and patches (if any)
%if %{uversion}
%(for ((i=1 ; i<=%{uversion} ; i++)) ; do echo Source$((9+i)):	http://mamedev.org/updates/%{sversion}u${i}_diff.zip ;done)
%endif

BuildRequires:	SDL_ttf-devel
BuildRequires:	expat-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	perl
ExclusiveArch:	%{ix86} x86_64 ppc

%description
SDL MAME is an arcade emulator using SDL, and based on the Multiple Arcade
Machine Emulator (MAME).

You can find a some freeware and their description on http://mamedev.org/roms/

If you some tricks to finish a game, the cheat.zip file is now provided in a
other package named sdlmame-extra-data.

%package -n sdlmess
Summary:	SDL MESS emulates a large variety of different systems
Group:		Emulators

%description -n sdlmess
SDL MESS is a free emulator which emulates a large variety of different
systems (computers and home entertainment systems).
It uses SDL, and is based on MESS.

%prep
%setup -c -n %{name}-%{version} -q
unzip -qq mame.zip
%patch0 -p1
%patch1 -p1
%patch2 -p1

#files missing : ui.bdf, keymaps
tar xvjf %{SOURCE3}
#files missing : arkwork, sysinfo.dat
tar xvjf %{SOURCE4}
#fixes doc line endings, + needed before patching
find . -type f -not -name uismall.png | xargs perl -pi -e 's/\r\n?/\n/g'

#apply u1, u2, etc... patches (if any)
#fix line endings for mdv < 2010.1
%if %{uversion}
%(for ((i=1 ; i<=%{uversion} ; i++)) ; do echo "unzip -qq %{SOURCE$((9+i))}" ; echo "perl -pi -e 's/\r\n/\n/g' %{sversion}u${i}.diff" ; echo "patch -p0 -s --fuzz=0 -E < %{sversion}u${i}.diff" ; done)
%endif

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
 BUILD_ZLIB= \
 BUILD_EXPAT= \
 OPT_FLAGS="%{optflags}"

%make all TARGET=mess \
 PREFIX=sdl \
 NOWERROR=1 \
 BUILD_ZLIB= \
 BUILD_EXPAT= \
 OPT_FLAGS="%{optflags}"

%install
rm -rf %{buildroot}
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

%files
%defattr(0644,root,games,0755)
%doc docs/*
%attr(0755,root,games) %{_gamesbindir}/sdlmame*
%attr(0755,root,games) %{_gamesbindir}/*-sdlmame
%{_gamesdatadir}/sdlmame

%files -n sdlmess
%defattr(0644,root,games,0755)
%doc docs/*
%attr(0755,root,games) %{_gamesbindir}/sdlmess*
%attr(0755,root,games) %{_gamesbindir}/*-sdlmess
%{_gamesdatadir}/sdlmess

