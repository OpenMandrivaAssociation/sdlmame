Name:			sdlmame
Version:		0.146
%define sversion	%(sed -r -e "s/\\.//" -e "s/(.*)u(.)/\\1/" <<<%{version})
%define uversion	%(sed -r -e "s/(.*u)(.)/\\2/;t;c\\0" <<<%{version})
Release:		%mkrel 1

Summary:	SDL MAME is an arcade emulator
License:	Freeware
Group:		Emulators
URL:		http://mamedev.org/
#http://mamedev.org/downloader.php?&file=mame%{sversion}s.zip
Source0:        mame%{sversion}s.zip
Source1:	sdlmame-wrapper
Source2:	sdlmame-extra.tar.bz2

#Sources 10+ : u1, u2 etc zip files containing changelogs and patches (if any)
%if %{uversion}
%(for ((i=1 ; i<=%{uversion} ; i++)) ; do echo Source$((9+i)):	http://mamedev.org/updates/%{sversion}u${i}_diff.zip ;done)
%endif

BuildRequires:	SDL-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	expat-devel
BuildRequires:	zlib-devel
BuildRequires:	libxinerama-devel
BuildRequires:	gtk2-devel
BuildRequires:	libGConf2-devel
BuildRequires:	perl
# Workaround
BuildRequires:	libxrender-devel >= 0.9.6
ExclusiveArch:	%ix86 x86_64 ppc

%description
SDL MAME is an arcade emulator using SDL, and based on the Multiple Arcade 
Machine Emulator (MAME).

You can find a some freeware and their description on http://mamedev.org/roms/

If you some tricks to finish a game, the cheat.zip file is now provided in a 
other package named sdlmame-extra-data.

%prep
%setup -c -n %{name}-%{version} -q
unzip -qq mame.zip
#files missing : ui.bdf, keymaps
tar xvjf %{SOURCE2}
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
%make all PREFIX=sdl \
 NOWERROR=1 \
 BUILD_ZLIB= \
 BUILD_EXPAT= \
 OPT_FLAGS="%{optflags}"

%install
%__rm -rf %{buildroot}
%__install -d -m 755 %{buildroot}%{_gamesbindir}
%__install -m 755 %{name}* %{buildroot}/%{_gamesbindir}/sdlmame.real

#tools
#useful to manage roms
%__install -m 755 chdman %{buildroot}%{_gamesbindir}/chdman-sdlmame
%__install -m 755 romcmp %{buildroot}%{_gamesbindir}/romcmp-sdlmame
#useful to create a new keymap
%__install -m 755 testkeys %{buildroot}%{_gamesbindir}/testkeys-sdlmame
#other tools built:
#jedutils, makemeta, regrep, srcclean

#"support files" moved to sdlmame-extra-data
#but the directory is still owned by this package
%__install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame

#ui font
%__install -m 644 ui.bdf %{buildroot}/%{_gamesdatadir}/sdlmame/

#keymaps
%__install -d -m 755 %{buildroot}%{_gamesdatadir}/sdlmame/keymaps
%__install -m 644 keymaps/* %{buildroot}/%{_gamesdatadir}/sdlmame/keymaps/

#install wrapper
%__install -m 755 %{SOURCE1} %{buildroot}%{_gamesbindir}/sdlmame

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc whatsnew*.txt docs/*
%attr(0755,root,games) %{_gamesbindir}/sdlmame*
%attr(0755,root,games) %{_gamesbindir}/*-sdlmame
%{_gamesdatadir}/sdlmame

