# Combined gcc / cross-armv*-gcc) specfile
Name: cross-i486-gcc
%define crossarch i486
# Keep Name on top !

%if "%{?bootstrap}" == ""
%define bootstrap 0
%else
%if "%{bootstrap}" != "0" && "%{bootstrap}" != "1" && "%{bootstrap}" != "2"
%{error:Bootstrap parameter should me one of: 0, 1, 2}
%endif
%endif

# crossbuild / accelerator section
# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
%define crossbuild 0
%if "%{name}" != "gcc"
# this is the ix86 -> arm cross compiler (cross-armv*-gcc)
#
# We set requires/provides by hand and disable post-build-checks.
# Captain Trunk: Sledge, you cannot disarm that nuclear bomb!
# Sledge Hammer: Trust me, I know what I'm doing. 
AutoReqProv: 0
AutoReq: false
#!BuildIgnore: rpmlint-Moblin
#!BuildIgnore: rpmlint-mini
#!BuildIgnore: post-build-checks
# cross platform
%if %(echo %{crossarch} | grep -q "^arm" && echo 1 || echo 0)
%define cross_gcc_target_platform %{crossarch}-%{_vendor}-linux-gnueabi
%else
%define cross_gcc_target_platform %{crossarch}-%{_vendor}-linux-gnu
%endif
# gcc_target_platform holds the host (executing the compiler)
# cross_gcc_target_platform holds the target (for which the compiler is producing binaries)
# prefix for cross compiler
%define _prefix /opt/cross
# strip of 'foreign arch' symbols fails
%define __strip /bin/true
# sysroot for cross-compiler
%define crosssysroot %{_prefix}/%{cross_gcc_target_platform}/sys-root
# flag
%define crossbuild 1
# macros in buildrequires is hard to expand for the scheduler (e.g. crossarch) which would make this easier.
%if %{bootstrap} == 2
%define cross_deps cross-%{crossarch}-glibc-headers cross-%{crossarch}-kernel-headers cross-%{crossarch}-binutils
%endif
%if %{bootstrap} == 0
%define cross_deps cross-%{crossarch}-glibc cross-%{crossarch}-glibc-devel cross-%{crossarch}-glibc-headers cross-%{crossarch}-kernel-headers cross-%{crossarch}-binutils
%endif
%if %{bootstrap} == 1
%define cross_deps cross-%{crossarch}-kernel-headers cross-%{crossarch}-binutils
%endif

BuildRequires: %{cross_deps}

# Fixme: find way to make this without listing every package
%if "%{crossarch}" == "armv5tel"
%define crossextraconfig %{nil}
%endif
%if "%{crossarch}" == "armv6l"
%define crossextraconfig --with-fpu=vfp --with-arch=armv6
%endif
%if "%{crossarch}" == "armv7l"
%define crossextraconfig --with-fpu=vfpv3-d16 --with-arch=armv7-a
%endif
%if "%{crossarch}" == "armv7hl"
%define crossextraconfig --with-float=hard --with-fpu=neon --with-arch=armv7-a --with-mode=thumb
%endif
%if "%{crossarch}" == "armv7nhl"
%define crossextraconfig --with-float=hard --with-fpu=neon --with-arch=armv7-a
%endif
%if "%{crossarch}" == "armv7thl"
%define crossextraconfig --with-float=hard --with-fpu=vfpv3-d16 --with-arch=armv7-a --with-mode=thumb
%endif
%if "%{crossarch}" == "armv7tnhl"
%define crossextraconfig --with-float=hard --with-fpu=neon --with-arch=armv7-a --with-mode=thumb
%endif
%if "%{crossarch}" == "mipsel"
%define crossextraconfig --disable-fixed-point --disable-ssp --disable-libstdcxx-pch --with-arch=mips32
%endif
%if "%{crossarch}" == "i486"
%define crossextraconfig --disable-libstdcxx-pch --with-arch=i686 --with-fpmatch=sse --with-gnu-as=/opt/cross/bin/i486-meego-linux-gnu-as --with-gnu-ld=/opt/cross/bin/i486-meego-linux-gnu-ld --with-as=/opt/cross/bin/i486-meego-linux-gnu-as --with-ld=/opt/cross/bin/i486-meego-linux-gnu-ld
%endif
%if "%{crossarch}" == "x86_64"
%define crossextraconfig --disable-libstdcxx-pch
%endif
%if "%{crossarch}" == "aarch64"
%define crossextraconfig --with-arch=armv8-a
%endif

# single target atm.
ExclusiveArch: %ix86 x86_64
#
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
# end crossbuild / accelerator section
%endif

%global gcc_version 8.3.0
%global gcc_release 1
%global _unpackaged_files_terminate_build 0
%global _performance_build 1
%global build_ada 0
%global build_objc 0
%global build_go 0
%global build_d 0
%global include_gappletviewer 0
%global build_libstdcxx_doc 0
%global multilib_64_archs %{nil}
%ifarch x86_64
%global multilib_32_arch i686
%endif
%global build_64bit_multilib 0
%ifarch %{ix86} x86_64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64
%global build_liblsan 1
%else
%global build_liblsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_libubsan 1
%else
%global build_libubsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
#GCC Graphite needs isl
%global build_isl 1

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Version: %{gcc_version}
%if %{bootstrap}
Release: 0.%{bootstrap}.%{gcc_release}
%else
Release: %{gcc_release}
%endif
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
URL: https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a/downloads
Source0: https://developer.arm.com/-/media/Files/downloads/gnu-a/8.3-2019.03/srcrel/gcc-arm-src-snapshot-8.3-2019.03.tar.xz
Source2: README.libgcjwebplugin.so
Source3: gcc-rpmlintrc
Source4: baselibs.conf
Source5: precheckin.sh
Source6: aaa_README.PACKAGER
Patch0: gcc8-hack.patch
Patch2: gcc8-i386-libgomp.patch
Patch5: gcc8-libtool-no-rpath.patch
Patch6: gcc8-isl-dl.patch
Patch9: gcc8-foffload-default.patch
Patch10: gcc8-Wno-format-security.patch
#Enabling CET blows up on x86 atm, if we really want this then we need to debug the glibc/binutils etc issues.
#Patch12: gcc8-mcet.patch
Patch13: libcc1.patch

BuildRequires: binutils >= 2.31
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext,  bison, flex
BuildRequires: mpc-devel
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: libstdc++-devel
BuildRequires: libgomp

%if %{build_libstdcxx_doc}
BuildRequires: doxygen
BuildRequires: graphviz
%endif

%if !%{crossbuild}
Requires: cpp = %{version}-%{release}
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
Requires: glibc-devel
Requires: binutils >= 2.25
%endif

%if !%{crossbuild} 

%if %{build_64bit_multilib}
Requires: glibc64bit-helper
%endif

Obsoletes: gcc < %{version}-%{release}
AutoReq: true
# /!crossbuild
%endif

#We need -gnueabi indicator for ARM
%ifnarch %{arm} aarch64
%global _gnu %{nil}
%endif
%global gcc_target_platform %{_target_platform}

%description
The gcc package contains the GNU Compiler Collection version 4.9.
You'll need this package in order to compile C code.

%if !%{crossbuild}
%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man and info pages for %{name}.
%endif # !crossbuild

%package -n libgcc
Summary: GCC version 8.3 shared support library
Group: System Environment/Libraries
Obsoletes: libgcc < %{version}-%{release}
Autoreq: false
%if "%{version}" != "%{gcc_version}"
Provides: libgcc = %{gcc_provides}
%endif

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Obsoletes: gcc-c++ < %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Obsoletes: libstdc++ < %{version}-%{release}
Obsoletes: libstdc++6 < %{version}-%{release}
Autoreq: true
Requires: glibc 

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++ = %{version}-%{release}
Obsoletes: libstdc++-devel < %{version}-%{release}
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Group: Development/Libraries
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description -n libstdc++-static
Static libraries for the GNU standard C++ library.

%if !%{crossbuild}
%package -n libstdc++-doc
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Requires:  libstdc++ = %{version}-%{release}
Obsoletes: libstdc++-docs
Autoreq: true

%description -n libstdc++-doc
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.
%endif # !crossbuild

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Obsoletes: gcc-objc < %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Obsoletes: gcc-objc++ < %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Group: System Environment/Libraries
Obsoletes: libobjc < %{version}-%{release}
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.


%package -n libgomp
Summary: GCC OpenMP v4.5 shared support library
Group: System Environment/Libraries
Obsoletes: libgomp < %{version}-%{release}

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.

%package -n libquadmath
Summary: GCC __float128 shared support library
Group: System Environment/Libraries

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libquadmath-devel
Summary: GCC __float128 support
Group: Development/Libraries
Requires: libquadmath = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libquadmath-static
Summary: Static libraries for __float128 support
Group: Development/Libraries
Requires: libquadmath-devel = %{version}-%{release}

%description -n libquadmath-static
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libitm-devel
Summary: The GNU Transactional Memory support
Group: Development/Libraries
Requires: libitm = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package -n libitm-static
Summary: The GNU Transactional Memory static library
Group: Development/Libraries
Requires: libitm-devel = %{version}-%{release}

%description -n libitm-static
This package contains GNU Transactional Memory static libraries.

%package -n libatomic
Summary: The GNU Atomic library
Group: System Environment/Libraries

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libatomic-static
Summary: The GNU Atomic static library
Group: Development/Libraries
Requires: libatomic = %{version}-%{release}

%description -n libatomic-static
This package contains GNU Atomic static libraries.

%package -n libasan
Summary: The Address Sanitizer runtime library
Group: System Environment/Libraries

%description -n libasan
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n libasan-static
Summary: The Address Sanitizer static library
Group: Development/Libraries
Requires: libasan = %{version}-%{release}

%description -n libasan-static
This package contains Address Sanitizer static runtime library.

%package -n libtsan
Summary: The Thread Sanitizer runtime library
Group: System Environment/Libraries

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n libtsan-static
Summary: The Thread Sanitizer static library
Group: Development/Libraries
Requires: libtsan = %{version}-%{release}

%description -n libtsan-static
This package contains Thread Sanitizer static runtime library.

%package -n libubsan
Summary: The Undefined Behavior Sanitizer runtime library

%description -n libubsan
This package contains the Undefined Behavior Sanitizer library
which is used for -fsanitize=undefined instrumented programs.

%package -n libubsan-static
Summary: The Undefined Behavior Sanitizer static library
Requires: libubsan = %{version}-%{release}

%description -n libubsan-static
This package contains Undefined Behavior Sanitizer static runtime library.

%package -n liblsan
Summary: The Leak Sanitizer runtime library

%description -n liblsan
This package contains the Leak Sanitizer library
which is used for -fsanitize=leak instrumented programs.

%package -n liblsan-static
Summary: The Leak Sanitizer static library
Requires: liblsan = %{version}-%{release}

%description -n liblsan-static
This package contains Leak Sanitizer static runtime library.

%package -n cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires: mpc
Obsoletes: cpp < %{version}-%{release}
Autoreq: true

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package -n gcc-multilib
Summary: for 64bit multilib support
Group: System Environment/Libraries
Autoreq: true

%description -n gcc-multilib
This is one set of libraries which support 64bit multilib on top of
32bit enviroment from compiler side.

%package plugin-devel
Summary: Support for compiling GCC plugins
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%prep
%setup -q -n gcc-arm-src-snapshot-8.3-2019.03
%patch0 -p0 -b .hack~
%patch2 -p0 -b .i386-libgomp~
%patch5 -p0 -b .libtool-no-rpath~
%if %{build_isl}
%patch6 -p0 -b .isl-dl~
%endif
%patch9 -p0 -b .foffload-default~
%patch10 -p0 -b .Wno-format-security~
#%patch12 -p0 -b .mcet~

# This is a patch which is put in place because libcc1 uses the current gcc
# to determine the lib path. As we're changing behaviour for aarch64, this
# temporary patch is needed.
%ifarch aarch64
%patch13 -p0
%endif

echo 'Sailfish OS gcc %{version}-%{gcc_release}' > gcc/DEV-PHASE

# Default to -gdwarf-4 rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(4)/' gcc/common.opt
sed -i 's/\(may be either 2 or 3 or 4; the default version is \)2\./\14./' gcc/doc/invoke.texi

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

# Hack to avoid building multilib libjava
perl -pi -e 's/^all: all-redirect/ifeq (\$(MULTISUBDIR),)\nall: all-redirect\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-redirect/ifeq (\$(MULTISUBDIR),)\ninstall: install-redirect\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-redirect/ifeq (\$(MULTISUBDIR),)\ncheck: check-redirect\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^all: all-recursive/ifeq (\$(MULTISUBDIR),)\nall: all-recursive\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-recursive/ifeq (\$(MULTISUBDIR),)\ninstall: install-recursive\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-recursive/ifeq (\$(MULTISUBDIR),)\ncheck: check-recursive\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%build

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_isl}
mkdir isl-build isl-install
%ifarch s390 s390x
ISL_FLAG_PIC=-fPIC
%else
ISL_FLAG_PIC=-fpic
%endif
cd isl-build
../../../isl/configure --disable-shared \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC" --prefix=`cd ..; pwd`/isl-install
make %{?_smp_mflags}
make %{?_smp_mflags} install
cd ..
%endif

CC=gcc
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo $OPT_FLAGS| sed -e 's/[[:blank:]]\+/ /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac

%ifarch mipsel
# Apply this in case you ever need to qemu bootstrap --cvm
#
# export OPT_FLAGS="$OPT_FLAGS --param ggc-min-expand=0 --param ggc-min-heapsize=65536" 
%endif

%ifarch %arm aarch64

%define ARM_EXTRA_CONFIGURE ""
# for armv7hl reset the gcc specs
%ifarch armv6l
%define ARM_EXTRA_CONFIGURE --with-fpu=vfp --with-arch=armv6
%endif
%ifarch armv7l
%define ARM_EXTRA_CONFIGURE --with-fpu=vfpv3-d16 --with-arch=armv7-a
%endif
%ifarch armv7hl
%define ARM_EXTRA_CONFIGURE --with-float=hard --with-fpu=neon --with-mode=thumb --with-arch=armv7-a
%endif
# for armv7nhl reset the gcc specs
%ifarch armv7nhl
%define ARM_EXTRA_CONFIGURE --with-float=hard --with-fpu=neon --with-arch=armv7-a
%endif
# for armv7thl reset the gcc specs
%ifarch armv7thl
%define ARM_EXTRA_CONFIGURE --with-float=hard --with-fpu=vfpv3-d16 --with-arch=armv7-a --with-mode=thumb
%endif
# for armv7tnhl reset the gcc specs
%ifarch armv7tnhl
%define ARM_EXTRA_CONFIGURE --with-float=hard --with-fpu=neon --with-arch=armv7-a --with-mode=thumb
%endif
# aarch64
%ifarch aarch64
%define ARM_EXTRA_CONFIGURE --with-arch=armv8-a
%endif
%endif

#export OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e "s/-O2/-O2 -fkeep-inline-functions/g"`
export OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e "s/-fstack-protector//g"`

%if %{crossbuild}
# cross build
export PATH=/opt/cross/bin:$PATH
# strip all after -march . no arch specific options in cross-compiler build .
# -march=core2 -mssse3 -mtune=atom -mfpmath=sse -fasynchronous-unwi
export OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e "s#\-march=.*##g" | sed -e 's#\-mtune=.*##g`
%endif

CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="`echo $OPT_FLAGS | sed 's/ -Wall / /g'`" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} \
%if !%{crossbuild}
%if ! 0%{?qemu_user_space_build}
        --enable-bootstrap \
%else
	--disable-bootstrap \
%endif
%else
	--disable-bootstrap \
%endif
	--with-bugurl=https://git.sailfishos.org/ \
	--build=%{gcc_target_platform} \
%if %{build_isl}
	--with-isl=`pwd`/isl-install \
%endif
%if %{crossbuild}
	--host=%{gcc_target_platform} \
	--target=%{cross_gcc_target_platform} \
        --with-sysroot=%{crosssysroot} \
	--disable-multilib \
%else
%ifarch mipsel
        --disable-fixed-point \
        --disable-ssp \
	--disable-libstdcxx-pch \
        --with-arch=mips32 \
%endif
        --enable-plugin --enable-initfini-array\
%ifarch %{arm} aarch64
	%ARM_EXTRA_CONFIGURE \
	--disable-sjlj-exceptions \
        --enable-gold \
        --with-plugin-ld=gold \
%endif
%ifarch aarch64
        --libdir=/usr/lib64 \
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch i586
	--with-arch=core2 --with-tune=atom --with-fpmath=sse \
%endif
%ifarch i486
	--with-arch=i686 --with-fpmath=sse  \
%endif
%ifarch x86_64
	--disable-libstdcxx-pch \
%endif
%endif
%if %{build_64bit_multilib}
	--enable-targets=all \
	--enable-multilib \
%else
	--disable-multilib \
%endif
	--enable-checking=release \
        --disable-fixed-point \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object \
        --enable-lto \
	--enable-linker-build-id \
%if %{bootstrap} == 0
	--enable-languages=c,c++,objc,obj-c++,lto \
	--enable-threads=posix \
	--enable-shared \
%endif
%if %{bootstrap} == 1
	--enable-languages=c \
	--without-headers \
	--with-newlib \
	--disable-decimal-float \
	--disable-fixed-point \
	--disable-threads \
	--disable-shared \
	--disable-libssp \
	--disable-libgomp \
	--disable-libquadmath \
%endif
%if %{bootstrap} == 2
	--enable-languages=c \
	--with-sysroot=%{crosssysroot} \
	--disable-libssp \
	--disable-libgomp \
	--disable-libquadmath \
%endif
	--disable-libgcj \
        --disable-libcilkrts \
%if %{attr_ifunc}
	--enable-gnu-indirect-function \
%endif
%if %{crossbuild}
	%{crossextraconfig} \
%endif
	--build=%{gcc_target_platform} || ( cat config.log ; exit 1 )

GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS"

# Make
#make -C gcc CC="./xgcc -B ./ -O2" all

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make %{?_smp_mflags} -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_doc}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc rpm.doc/gdc rpm.doc/libphobos
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer}

for i in {gcc,gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

sed -e 's,@VERSION@,%{gcc_version},' %{SOURCE2} > rpm.doc/README.libgcjwebplugin.so

%if %{build_objc}
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
%endif
%if %{build_d}
(cd gcc/d; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gdc/$i.gdc
done)
(cd libphobos; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libphobos/$i.libphobos
done
cp -a src/LICENSE*.txt libdruntime/LICENSE ../rpm.doc/libphobos/)
%endif
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif
%if %{build_go}
(cd gcc/go; for i in README* ChangeLog*; do
	cp -p $i ../../rpm.doc/go/$i
done)
(cd libgo; for i in LICENSE* PATENTS* README; do
	cp -p $i ../rpm.doc/libgo/$i.libgo
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -fr %{buildroot}

cd obj-%{gcc_target_platform}

%if !%{crossbuild}
# native
TARGET_PLATFORM=%{gcc_target_platform}
# There are some MP bugs in libstdc++ Makefiles
make %{?_smp_mflags} -C %{gcc_target_platform}/libstdc++-v3
%else
# cross build
export PATH=/opt/cross/bin:$PATH
# strip all after -march . no arch specific options in cross-compiler build .
# -march=core2 -mssse3 -mtune=atom -mfpmath=sse -fasynchronous-unwi
export OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e "s#\-march=.*##g"`
echo "$OPT_FLAGS"
TARGET_PLATFORM=%{cross_gcc_target_platform}
# There are some MP bugs in libstdc++ Makefiles
make %{?_smp_mflags} -C %{cross_gcc_target_platform}/libstdc++-v3
%endif

make %{?_smp_mflags} prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} libdir=%{buildroot}%{_libdir} \
  install

%if !%{crossbuild}
# native
# \/\/\/
FULLPATH=%{buildroot}%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

mkdir -p $FULLPATH
mkdir -p $FULLEPATH

ln -sf gcc %{buildroot}%{_prefix}/bin/cc
mkdir -p %{buildroot}/%{_lib}
ln -sf ..%{_prefix}/bin/cpp %{buildroot}/%{_lib}/cpp

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/stdc++.h.gch dirs
# 1) there is no bits/stdc++.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_doc}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
mv $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}
mv $libstdcxx_doc_builddir/man/man3 %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

#Debug
#set -x
#find %{buildroot}%{_prefix}/

FULLLSUBDIR=
%ifarch sparcv9 ppc
FULLLSUBDIR=lib32
%endif
%ifarch sparc64 ppc64 ppc64p7
FULLLSUBDIR=lib64
%endif
if [ -n "$FULLLSUBDIR" ]; then
  FULLLPATH=$FULLPATH/$FULLLSUBDIR
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f
%if %{build_d}
mv %{buildroot}%{_prefix}/%{_lib}/libgphobos.spec $FULLPATH/
%endif
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libasan}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}

mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}.so.1
ln -sf libgcc_s-%{gcc_version}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
#ln -sf /%{_lib}/libgcc_s.so.1 %{buildroot}/%{_libdir}/libgcc_s.so

%ifarch %{ix86} x86_64 ppc ppc64 ppc64p7 ppc64le %{arm}
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%else
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%endif
%ifarch sparcv9 ppc
%ifarch ppc
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -m64 -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /lib64/libgcc_s.so.1 libgcc.a )' > $FULLPATH/64/libgcc_s.so
%else
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%endif
%ifarch %{multilib_64_archs}
%ifarch x86_64 ppc64 ppc64p7
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -m32 -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%else
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -P -dD -xc /dev/null | grep '__LONG_MAX__.*\(2147483647\|0x7fffffff\($\|[LU]\)\)'; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
%if %{build_objc}
ln -sf ../../../libobjc.so.4 libobjc.so
%endif
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../libgo.so.14.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_d}
ln -sf ../../../libgdruntime.so.76.* libgdruntime.so
ln -sf ../../../libgphobos.so.76.* libgphobos.so
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../libasan.so.5.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../libubsan.so.1.* libubsan.so
%endif
else
%if %{build_objc}
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
%endif
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.14.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_d}
ln -sf ../../../../%{_lib}/libgdruntime.so.76.* libgdruntime.so
ln -sf ../../../../%{_lib}/libgphobos.so.76.* libgphobos.so
%endif
%if %{build_libitm}
ln -sf ../../../../%{_lib}/libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../../%{_lib}/libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../../%{_lib}/libasan.so.5.* libasan.so
mv ../../../../%{_lib}/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../../%{_lib}/libubsan.so.1.* libubsan.so
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libtsan.so.0.* | sed 's,^.*libt,libt,'`' )' > libtsan.so
mv ../../../../%{_lib}/libtsan_preinit.o libtsan_preinit.o
%endif
%if %{build_liblsan}
rm -f liblsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/liblsan.so.0.* | sed 's,^.*libl,libl,'`' )' > liblsan.so
mv ../../../../%{_lib}/liblsan_preinit.o liblsan_preinit.o
%endif
fi
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++fs.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_d}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgdruntime.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgphobos.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
%endif
%if %{build_libubsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libubsan.*a $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLPATH/
%endif
%if %{build_liblsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan.*a $FULLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgobegin.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgolibbegin.*a $FULLLPATH/
%endif


%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.4 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.* | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libsupc++.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libquadmath.a 32/libquadmath.a
%endif
%endif

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
for d in . $FULLLSUBDIR; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}/debug%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/$d
  for f in `find $d -maxdepth 1 -a \
		\( -name libasan.a -o -name libatomic.a \
		-o -name libcaf_single.a \
		-o -name libgcc.a -o -name libgcc_eh.a \
		-o -name libgcov.a \
		-o -name libgo.a -o -name libgobegin.a \
		-o -name libgolibbegin.a -o -name libgomp.a \
		-o -name libitm.a -o -name liblsan.a \
		-o -name libobjc.a -o -name libgdruntime.a -o -name libgphobos.a \
		-o -name libquadmath.a -o -name libstdc++.a \
		-o -name libstdc++fs.a -o -name libsupc++.a \
		-o -name libtsan.a -o -name libubsan.a \) -a -type f`; do
    cp -a $f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/debug%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/$d/
  done
done
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libobjc.a -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a -o -name libquadmath.a \) -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcc1.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%if %{build_d}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgdruntime.so.76.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgphobos.so.76.*
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.5.*
%endif
%if %{build_libubsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.1.*
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0.*
%endif
%if %{build_liblsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%endif
%if %{build_go}
# Avoid stripping these libraries and binaries.
chmod 644 %{buildroot}%{_prefix}/%{_lib}/libgo.so.14.*
chmod 644 %{buildroot}%{_prefix}/bin/go.gcc
chmod 644 %{buildroot}%{_prefix}/bin/gofmt.gcc
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cgo
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/buildid
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/test2json
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/vet
%endif
%if %{build_objc}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*
%endif

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a} || :
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gccgo || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcj || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ar || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-nm || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ranlib || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gdc || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/%{_lib}/go/%{gcc_version}/%{gcc_target_platform}
%ifnarch sparc64 ppc64 ppc64p7
ln -sf %{multilib_32_arch}-%{_vendor}-%{_target_os} %{buildroot}%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib64/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%endif

rm -f %{buildroot}%{mandir}/man3/ffi*
# /\/\/\
# native
%else
# cross
# \/\/\/
# additional install for cross
# remove some obsolete files
ln -sf %{cross_gcc_target_platform}-gcc %{buildroot}%{_prefix}/bin/%{cross_gcc_target_platform}-cc
set -x
rm -rRf %buildroot/%{_prefix}/lib/libiberty.a
rm -rRf %buildroot/%{_prefix}/share
set +x
# /\/\/\
# cross
%endif

%if !%{crossbuild}
#mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/{,cp,objc,libobjc}
#install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} \
#        gcc/README* rpm.doc/changelogs/gcc/ChangeLog*
#install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version}/cp \
#        rpm.doc/changelogs/gcc/cp/ChangeLog*
#install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version}/objc \
#        rpm.doc/objc/*
#install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version}/libobjc \
#        libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*
#
#mkdir -p %{buildroot}%{_docdir}/libstdc++-%{version}
#install -m0644 -t %{buildroot}%{_docdir}/libstdc++-%{version} \
#         rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*
#%if %{build_libstdcxx_doc}
#mv rpm.doc/libstdc++-v3/html %{buildroot}%{_docdir}/libstdc++-%{version}/html
#%endif
#
#mkdir -p %{buildroot}%{_docdir}/libgomp-%{version}
#install -m0644 -t %{buildroot}%{_docdir}/libgomp-%{version} \
#        rpm.doc/changelogs/libgomp/ChangeLog*
#
#%if %{build_libquadmath}
#mkdir -p %{buildroot}%{_docdir}/libquadmath-%{version}
#install -m0644 -t %{buildroot}%{_docdir}/libquadmath-%{version} \
#        rpm.doc/libquadmath/ChangeLog*
#%endif
%endif # !crossbuild

%if !%{crossbuild}
# checking and split packaging for native ...
# native
# \/\/\/

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

%check
%if 0
cd obj-%{gcc_target_platform}

# run the tests.
make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector-strong}'" || :
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats\|ada'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}
%endif

%clean
rm -rf %{buildroot}

# Don't add %post -p /sbin/ldconfig here, see comment below

%postun -p /sbin/ldconfig

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%postun -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%post -n libstdc++ -p /sbin/ldconfig

%postun -n libstdc++ -p /sbin/ldconfig

%post -n libobjc -p /sbin/ldconfig

%postun -n libobjc -p /sbin/ldconfig

%post -n libgomp -p /sbin/ldconfig

%postun -n libgomp -p /sbin/ldconfig

%post -n libquadmath -p /sbin/ldconfig

%postun -n libquadmath -p /sbin/ldconfig

%post -n libitm -p /sbin/ldconfig

%postun -n libitm -p /sbin/ldconfig

%post -n libatomic -p /sbin/ldconfig

%postun -n libatomic -p /sbin/ldconfig

%post -n libasan -p /sbin/ldconfig

%postun -n libasan -p /sbin/ldconfig

%post -n libubsan -p /sbin/ldconfig

%postun -n libubsan -p /sbin/ldconfig

%post -n liblsan -p /sbin/ldconfig

%postun -n liblsan -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcov-tool
%{_prefix}/bin/gcov-dump
%{_prefix}/bin/gcc-ar
%{_prefix}/bin/gcc-nm
%{_prefix}/bin/gcc-ranlib
#%ifnarch %{arm} aarch64 mipsel
#%{_prefix}/bin/%{gcc_target_platform}-gcc
#%{_prefix}/bin/%{gcc_target_platform}-gcc-ar
#%{_prefix}/bin/%{gcc_target_platform}-gcc-nm
#%{_prefix}/bin/%{gcc_target_platform}-gcc-ranlib
#%endif
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include

# Shouldn't include all files under this fold, split to diff pkgs
#%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/*
#%if !%{crossbuild}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_plugin.so*
#%endif

%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2

%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/include
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/include/*

# Shouldn't include all files under this fold, split to diff pkgs
#%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/*
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/rpmver
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/openacc.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint-gcc.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdalign.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdnoreturn.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdatomic.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/gcov.h
%ifarch %{ix86} x86_64
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmiintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/tbmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx2intrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmi2intrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/f16cintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/fmaintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/lzcntintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/rtmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/xtestintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/adxintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/prfchwintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/rdseedintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/fxsrintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveoptintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512cdintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512erintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512fintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512pfintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/shaintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512bwintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512dqintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512ifmaintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512ifmavlintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vbmiintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vbmivlintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vlbwintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vldqintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vlintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/clflushoptintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/clwbintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/mwaitxintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsavecintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsavesintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/clzerointrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/pkuintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx5124fmapsintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx5124vnniwintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vpopcntdqintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/sgxintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/gfniintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/cetintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/cet.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vbmi2intrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vbmi2vlintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vnniintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vnnivlintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/vaesintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/vpclmulqdqintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vpopcntdqvlintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512bitalgintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/pconfigintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/wbnoinvdintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/movdirintrin.h
%endif

# For ARM port
%ifarch %{arm}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed/README
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind-arm-common.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_acle.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_cmse.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_fp16.h
%endif
%ifarch aarch64
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_acle.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_fp16.h
%endif
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/ssp.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/stdio.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/string.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/unistd.h
%if %{build_libasan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/sanitizer
%endif

%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%if %{build_libitm}
%ifarch aarch64
%{_prefix}/lib64/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.spec
%else
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.spec
%endif
%endif
%if %{build_libasan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libsanitizer.spec
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%if %{build_libquadmath}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libubsan.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libubsan.so
%endif
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%if %{build_libquadmath}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libubsan.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libubsan.so
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%if %{build_libquadmath}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%if %{build_libitm}
%ifarch aarch64
%{_prefix}/lib64/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%{_prefix}/lib64/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
else
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%endif
%endif
%if %{build_libatomic}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.so
%endif
%else
%if %{build_libatomic}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.so
%endif
%endif
%if %{build_libtsan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan_preinit.o
%endif
%if %{build_liblsan}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan_preinit.o
%endif
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* 
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%if !%{crossbuild}
%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}
%{_mandir}/man1/cpp.1*
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/g++.1*
%{_mandir}/man7/*
%endif # !crossbuild

%files -n cpp -f cpplib.lang
%defattr(-,root,root,-)
/%{_lib}/cpp
%{_prefix}/bin/cpp
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc
%defattr(-,root,root,-)
/%{_lib}/libgcc_s-%{gcc_version}.so.1
/%{_lib}/libgcc_s.*
%license gcc/COPYING.LIB

%files c++
%defattr(-,root,root,-)
%ifnarch %{arm} aarch64 mipsel
%{_prefix}/bin/%{gcc_target_platform}-*++
%endif
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch %{multilib_64_archs}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++fs.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif

%files -n libstdc++
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libstdc++.so.6*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%dir %{_prefix}/share/gcc-%{gcc_version}
%{_prefix}/share/gcc-%{gcc_version}/python
%{_prefix}/share/gcc-%{gcc_version}/python/libstdcxx

%files -n libstdc++-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a  
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%ifnarch  %{multilib_64_archs}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++fs.a

%files -n libstdc++-static
%defattr(-,root,root,-)
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a

%if !%{crossbuild}
%if %{build_libstdcxx_doc}
%files -n libstdc++-doc
%defattr(-,root,root)
%{_mandir}/man3/*
%{_docdir}/libstdc++-%{version}
%endif
%endif # !crossbuild

%if %{build_objc}
%files objc
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1obj
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1objplus

%files -n libobjc
%{_prefix}/%{_lib}/libobjc.so.4*
%endif

%files -n libgomp
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgomp.*

%if %{build_64bit_multilib}
%files -n gcc-multilib
%defattr(-,root,root,-)
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%dir %{_prefix}/lib64
%{_prefix}/lib64/*
%endif

%if %{build_libquadmath}
%files -n libquadmath
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libquadmath.so.0*
%license rpm.doc/libquadmath/COPYING*

%files -n libquadmath-devel
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libquadmath.so
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath_weak.h
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so

%files -n libquadmath-static
%defattr(-,root,root,-)
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%endif

%if %{build_libitm}
%files -n libitm
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libitm.so.1*

%files -n libitm-devel
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/include
%doc rpm.doc/libitm/ChangeLog*

%files -n libitm-static
%defattr(-,root,root,-)
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%endif

%if %{build_libatomic}
%files -n libatomic
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic-static
%defattr(-,root,root,-)
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%endif

%if %{build_libasan}
%files -n libasan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libasan.so.5*

%files -n libasan-static
%defattr(-,root,root,-)
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%endif

%if %{build_libubsan}
%files -n libubsan
%{_prefix}/%{_lib}/libubsan.so.1*

%files -n libubsan-static
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libubsan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libubsan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.a
%endif
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libtsan.so.0*

%files -n libtsan-static
%defattr(-,root,root,-)
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_liblsan}
%files -n liblsan
%{_prefix}/%{_lib}/liblsan.so.0*

%files -n liblsan-static
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.a
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%files plugin-devel
%defattr(-,root,root,-)
%dir %{_prefix}/%{_lib}/gcc
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}
%dir %{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/%{_lib}/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/plugin

# /\/\/\
# native
%else
# cross
# \/\/\/
%files
%defattr(-,root,root,-)
%{_prefix}
# /\/\/\
# cross
%endif
