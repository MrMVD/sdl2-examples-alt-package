Name: sdl2-examples
Version: 1.0.1
Release: alt1

Summary: examples of programs using sdl2
License: BSD-3-Clause license
Group: Graphics

Url: https://github.com/xyproto/sdl2-examples
Packager: Mikhail Golubev <saysuntruth@gmail.com>

BuildRequires(pre): rpm-macros-cmake
BuildRequires: cmake make gcc-c++ pkgconf
BuildRequires: libSDL2-devel
Requires:      desktop-file-utils

Source0: %name-%version.tar

%description
just some test programs for sld2

%global make_c_prog c++11 c++98 c11 c18 c2x c89 c99
%global cmake_c_prog c++11-cmake c++14-cmake c++17-cmake c++20-cmake c++23-cmake
%global c_programs %make_c_prog  %cmake_c_prog

%prep
%setup -q

%build
for prog in %make_c_prog; do
cd $prog 
%make_build
cd ..
done

for prog in %cmake_c_prog; do
cd $prog
%cmake_insource
%make_build # VERBOSE=1
cd ..
done


%install
mkdir -p \
  %buildroot%_bindir/
mkdir -p \
  %buildroot%_libdir/
mkdir -p \
  %buildroot%_libdir/sdl2-examples/

mkdir -p \
  %buildroot%_libdir/sdl2-examples/img/
install -Dm 0644 img/grumpy-cat.bmp %buildroot%_libdir/sdl2-examples/img/
install -Dm 0644 img/grumpy-cat.png %buildroot%_libdir/sdl2-examples/img/

mkdir -p \
  %buildroot%_libdir/sdl2-examples/bin

for prog in %c_programs; do
install -Dm0755 $prog/main %buildroot%_libdir/sdl2-examples/bin/
mv %buildroot%_libdir/sdl2-examples/bin/main \
  %buildroot%_libdir/sdl2-examples/bin/sdl2-$prog
done

mkdir -p \
  %buildroot%_datadir/ 
mkdir -p \
  %buildroot%_datadir/applications

for prog in %c_programs; do
cat > %buildroot%_datadir/applications/sdl2-$prog.desktop << EOF
[Desktop Entry]
Name=sdl2-$prog
Comment=sdl2 example by $prog
Exec=%_bindir/sdl2-$prog
Type=Application
Terminal=false
Categories=Utility;
EOF
done

cat > %buildroot%_libdir/sdl2-examples/launcher.sh << 'EOF'
#!/bin/bash
CALLED_NAME=$(basename "$0")
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
cd "$SCRIPT_DIR"/bin/ || exit 1
exec ./"$CALLED_NAME" "$@"
EOF
chmod 755 %buildroot%_libdir/sdl2-examples/launcher.sh

for prog in %c_programs; do
touch %buildroot%_bindir/sdl2-$prog
ln -sf %_libdir/sdl2-examples/launcher.sh \
  %buildroot%_bindir/sdl2-$prog
done

%post
# Обновление кэша меню
update-desktop-database &>/dev/null || :

%postun
# Обновление кэша меню после удаления
update-desktop-database &>/dev/null || :

%files
%_libdir/sdl2-examples/
%_bindir/
%_datadir/applications/
