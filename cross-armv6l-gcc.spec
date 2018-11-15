# Combined gcc / cross-armv*-gcc) specfile
Name: cross-armv6l-gcc
%define crossarch armv6l
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

%global gcc_version 4.9.4
%global gcc_release 1
%global _unpackaged_files_terminate_build 0
%global _performance_build 1
%global include_gappletviewer 0
%global build_cloog 1
%global build_libstdcxx_docs 0
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
%ifnarch mipsel aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%ifnarch aarch64
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch x86_64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch %{ix86} x86_64 %{arm}
%global build_libasan 0
%else
%global build_libasan 0
%endif


Summary: Various compilers (C, C++, Objective-C, Java, ...)
Version: %{gcc_version}
%if %{bootstrap}
Release: 0.%{bootstrap}.%{gcc_release}
%else
Release: %{gcc_release}
%endif
License: GPLv3+, GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
URL: https://releases.linaro.org/components/toolchain/gcc-linaro/
Source0: https://releases.linaro.org/components/toolchain/gcc-linaro/4.9-2017.01/gcc-linaro-4.9-2017.01.tar.xz
%global isl_version 0.12.2
Source1: ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-0.12.2.tar.bz2
%global cloog_version 0.18.1
Source2: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-0.18.1.tar.gz
Source3: README.libgcjwebplugin.so
Source100: gcc-rpmlintrc
Source200: baselibs.conf
Source300: precheckin.sh
Source301: aaa_README.PACKAGER

BuildRequires: binutils >= 2.25
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext,  bison, flex, texinfo
BuildRequires: mpc-devel
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.72
BuildRequires: libstdc++-devel

%if %{build_libstdcxx_docs}
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

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Obsoletes: gcc < %{version}-%{release}
Obsoletes: gcc43
AutoReq: true
# /!crossbuild
%endif

Patch0: gcc49-hack.patch
#Patch1: gcc48-java-nomulti.patch
Patch3: gcc49-rh330771.patch
#Patch4: gcc48-i386-libgomp.patch
Patch6: gcc49-libgomp-omp_h-multilib.patch
Patch7: gcc49-libtool-no-rpath.patch
Patch8: gcc49-cloog-dl.patch
Patch9: gcc49-cloog-dl2.patch
Patch10: gcc49-pr38757.patch
Patch11: gcc48-libstdc++-docs.patch
Patch12: gcc49-no-add-needed.patch
Patch17: gcc49-pr64336.patch

Patch20: gcc48-x86_64-nolib64.patch

#Patch42: gcc46-libiberty-conftest.patch
#Patch44: gcc-hash-style-gnu.diff
#Patch45: gcc46-MIPS-boehm-gc-stack-qemu.patch

#Patch50: fix-stable-debugtypes.patch
Patch51: use-lib-for-aarch64.patch

Patch9999: gcc44-ARM-boehm-gc-stack-qemu.patch

#We need -gnueabi indicator for ARM
%ifnarch %{arm} aarch64
%global _gnu %{nil}
%endif
%global gcc_target_platform %{_target_platform}

%description
The gcc package contains the GNU Compiler Collection version 4.9.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 4.9 shared support library
Group: System Environment/Libraries
Obsoletes: libgcc < %{version}-%{release}
Obsoletes: libgcc43
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
Obsoletes: gcc43-c++
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Obsoletes: libstdc++ < %{version}-%{release}
Obsoletes: libstdc++43
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
Obsoletes: libstdc++43-devel
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

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Obsoletes: libstdc++-docs < %{version}-%{release}
Obsoletes: libstdc++43-doc
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Obsoletes: gcc-objc < %{version}-%{release}
Obsoletes: gcc43-objc
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
Obsoletes: gcc43-obj-c++ gcc43-objc++
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Group: System Environment/Libraries
Obsoletes: libobjc < %{version}-%{release}
Obsoletes: libobjc43
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.


%package -n libgomp
Summary: GCC OpenMP v3.0 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Obsoletes: libgomp < %{version}-%{release}
Obsoletes: libgomp43

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.

%package -n libquadmath
Summary: GCC __float128 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

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
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

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
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libatomic-devel
Summary: The Atomic 
Group: Development/Libraries
Requires: libatomic = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libatomic-devel
This package contains headers and support files for the
GNU Atomic Library

%package -n libatomic-static
Summary: The GNU Atomic static library
Group: Development/Libraries
Requires: libatomic = %{version}-%{release}

%description -n libatomic-static
This package contains GNU Atomic static libraries.

%package -n libasan
Summary: The Address Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libasan
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n libasan-static
Summary: The Address Sanitizer static library
Group: Development/Libraries
Requires: libasan = %{version}-%{release}

%description -n libasan-static
This package contains Address Sanitizer static runtime library.

%package -n libasan-devel
Summary: The GNU Transactional Memory support
Group: Development/Libraries
Requires: libasan = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libasan-devel
This package contains headers and support files for the
Adress Sanitizer library

%package -n libtsan
Summary: The Thread Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n libtsan-static
Summary: The Thread Sanitizer static library
Group: Development/Libraries
Requires: libtsan = %{version}-%{release}

%description -n libtsan-static
This package contains Thread Sanitizer static runtime library.

%package -n cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: mpc
Obsoletes: cpp < %{version}-%{release}
Obsoletes: cpp43
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
%setup -q -n gcc-linaro-4.9-2017.01 -a 1 -a 2
%patch0 -p0 -b .hack~
#%patch1 -p0 -b .java-nomulti~
%patch3 -p0 -b .rh330771~
#%patch4 -p0 -b .i386-libgomp~
%patch6 -p0 -b .libgomp-omp_h-multilib~
%patch7 -p0 -b .libtool-no-rpath~
%if %{build_cloog}
%patch8 -p0 -b .cloog-dl~
%patch9 -p0 -b .cloog-dl2~
%endif
%patch10 -p0 -b .pr38757~
%if %{build_libstdcxx_docs}
%patch11 -p0 -b .libstdc++-docs~
%endif
%patch12 -p0 -b .no-add-needed~
%patch17 -p0 -b .pr64336~
%patch20 -p1

%ifarch %arm aarch64
#%patch42 -p1
%endif
#%patch44 -p1
#%patch45 -p1

#%patch50 -p1
%patch51 -p1

# This testcase doesn't compile.
rm libjava/testsuite/libjava.lang/PR35020*

%patch9999 -p1 -b .arm-boehm-gc~

echo 'Mer %{version}-%{gcc_release}' > gcc/DEV-PHASE

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

%if %{build_cloog}
mkdir isl-build isl-install
%ifarch s390 s390x
ISL_FLAG_PIC=-fPIC
%else
ISL_FLAG_PIC=-fpic
%endif
cd isl-build
../../isl-%{isl_version}/configure --disable-shared \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC" --prefix=`cd ..; pwd`/isl-install
make %{?_smp_mflags}
make install
cd ..

mkdir cloog-build cloog-install
cd cloog-build
cat >> ../../cloog-%{cloog_version}/source/isl/constraints.c << \EOF
#include <isl/flow.h>
static void __attribute__((used)) *s1 = (void *) isl_union_map_compute_flow;
static void __attribute__((used)) *s2 = (void *) isl_map_dump;
EOF
sed -i 's|libcloog|libgcc49privatecloog|g' \
  ../../cloog-%{cloog_version}/{,test/}Makefile.{am,in}
isl_prefix=`cd ../isl-install; pwd` \
../../cloog-%{cloog_version}/configure --with-isl=system \
  --with-isl-prefix=`cd ../isl-install; pwd` \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
   --prefix=`cd ..; pwd`/cloog-install
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
make %{?_smp_mflags} install
cd ../cloog-install/lib
rm libgcc49privatecloog-isl.so{,.4}
mv libgcc49privatecloog-isl.so.4.0.0 libcloog-isl.so.4
ln -sf libcloog-isl.so.4 libcloog-isl.so
ln -sf libcloog-isl.so.4 libcloog.so
cd ../..
%endif

CC=gcc
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
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
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
%if !%{crossbuild}
%if ! 0%{?qemu_user_space_build}
        --enable-bootstrap \
%else
	--disable-bootstrap \
%endif
%else
	--disable-bootstrap \
%endif
	--with-bugurl=http://bugs.merproject.org/ \
	--build=%{gcc_target_platform} \
%if %{build_cloog}
	--with-isl=`pwd`/isl-install --with-cloog=`pwd`/cloog-install \
%else
	--without-isl --without-cloog \
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
%ifarch %{arm} aarch64
	%ARM_EXTRA_CONFIGURE \
	--disable-sjlj-exceptions \
        --enable-gold \
        --enable-plugin \
        --with-plugin-ld=gold \
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
	--enable-gnu-unique-object --enable-lto \
	--enable-linker-build-id \
%if %{bootstrap} == 0
	--enable-languages=c,c++,objc,obj-c++ \
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
        --disable-libsanitizer \
        --disable-libcilkrts \
%if %{crossbuild}
	%{crossextraconfig} \
%endif
	--build=%{gcc_target_platform} || ( cat config.log ; exit 1 )

GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS"

# Make
#make -C gcc CC="./xgcc -B ./ -O2" all

%if %{build_cloog}
cp -a cloog-install/lib/libcloog-isl.so.4 gcc/
%endif

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc rpm.doc/libquadmath
mkdir -p rpm.doc/boehm-gc rpm.doc/fastjar rpm.doc/libffi
mkdir -p rpm.doc/changelogs/{gcc/cp,libstdc++-v3,libobjc,libgomp}
sed -e 's,@VERSION@,%{gcc_version},' %{SOURCE2} > rpm.doc/README.libgcjwebplugin.so

for i in {gcc,gcc/cp,libstdc++-v3,libobjc,libgomp}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd gcc/objc; for i in README*; do
	cp -p $i ../../rpm.doc/objc/$i.objc
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
(cd boehm-gc; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd fastjar-%{fastjar_ver}; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/fastjar/$i.fastjar
done)
(cd libffi; for i in ChangeLog* README* LICENSE; do
	cp -p $i ../rpm.doc/libffi/$i.libffi
done)
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
        cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
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
make -C %{gcc_target_platform}/libstdc++-v3
%else
# cross build
export PATH=/opt/cross/bin:$PATH
# strip all after -march . no arch specific options in cross-compiler build .
# -march=core2 -mssse3 -mtune=atom -mfpmath=sse -fasynchronous-unwi
export OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e "s#\-march=.*##g"`
#echo "$OPT_FLAGS"
#TARGET_PLATFORM=%{cross_gcc_target_platform}
# There are some MP bugs in libstdc++ Makefiles
#make -C %{cross_gcc_target_platform}/libstdc++-v3
%endif

make DESTDIR=%{buildroot} install
#prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
#  infodir=%{buildroot}%{_infodir} install

%if !%{crossbuild}
# native
# \/\/\/
FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

%if %{build_cloog}
cp -a cloog-install/lib/libcloog-isl.so.4 $FULLPATH/
%endif

ln -sf gcc %{buildroot}%{_prefix}/bin/cc
mkdir -p %{buildroot}/lib
ln -sf ..%{_prefix}/bin/cpp %{buildroot}/lib/cpp
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*

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

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
mv $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}
mv $libstdcxx_doc_builddir/man/man3 %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

if [ -n "$FULLLPATH" ]; then
   mkdir -p $FULLLPATH
else
   FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

mkdir -p %{buildroot}/%{_lib}

mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}.so.1
ln -sf libgcc_s-%{gcc_version}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 %{buildroot}/%{_libdir}/libgcc_s.so
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -dD -xc /dev/null | grep __LONG_MAX__.*2147483647; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.4 libobjc.so
ln -sf ../../../libstdc++.so.6.* libstdc++.so
ln -sf ../../../libgomp.so.1.* libgomp.so
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.* libstdc++.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../libasan.so.1.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
%endif
fi
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
#mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLLPATH/
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

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libobjc.a -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a -name libquadmath.a \) -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*

set -x
mkdir  %{buildroot}%{_prefix}/%{_lib}/bfd-plugins
ln -s %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_plugin.so %{buildroot}%{_prefix}/%{_lib}/bfd-plugins/
set +x

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
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a}
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
%ifarch %{ix86} x86_64
%if !%{crossbuild}
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
%endif
%endif
rm -f %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -f %{buildroot}%{_prefix}/bin/gnative2ascii
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-%{version} || :


%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
%endif

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
mkdir  -p %{buildroot}%{_prefix}/lib/bfd-plugins
ln -s %{_prefix}/libexec/gcc/%{cross_gcc_target_platform}/%{gcc_version}/liblto_plugin.so %{buildroot}%{_prefix}/lib/bfd-plugins/
mkdir  -p %{buildroot}/usr/lib/bfd-plugins
ln -s %{_prefix}/libexec/gcc/%{cross_gcc_target_platform}/%{gcc_version}/liblto_plugin.so %{buildroot}/usr/lib/bfd-plugins/
set +x
# /\/\/\
# cross
%endif

%if !%{crossbuild}
# checking and split packaging for native ...
# native
# \/\/\/

%check
%if 0
cd obj-%{gcc_target_platform}

# run the tests.
make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
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

%post
[ -e %{_infodir}/gcc.info.gz ] && /sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :

%postun -p /sbin/ldconfig

%preun
if [ $1 = 0 ]; then
  [ -e %{_infodir}/gcc.info.gz ] && /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%post -n cpp
[ -e %{_infodir}/cpp.info.gz ] && /sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :

%preun -n cpp
if [ $1 = 0 ]; then
  [ -e %{_infodir}/cpp.info.gz ] && /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

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

%post -n libgomp
/sbin/ldconfig
[ -e %{_infodir}/libgomp.info.gz ] && /sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :

%preun -n libgomp
if [ $1 = 0 ]; then
  [ -e %{_infodir}/libgomp.info.gz ] && /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%postun -n libgomp -p /sbin/ldconfig

%post -n libquadmath
/sbin/ldconfig
if [ -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%preun -n libquadmath
if [ $1 = 0 -a -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%postun -n libquadmath -p /sbin/ldconfig

%post -n libitm -p /sbin/ldconfig

%postun -n libitm -p /sbin/ldconfig

%post -n libatomic -p /sbin/ldconfig

%postun -n libatomic -p /sbin/ldconfig

%post -n libasan -p /sbin/ldconfig

%postun -n libasan -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcc-ar
%{_prefix}/bin/gcc-nm
%{_prefix}/bin/gcc-ranlib
%ifnarch %{arm} aarch64 mipsel
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_prefix}/bin/%{gcc_target_platform}-gcc-ar
%{_prefix}/bin/%{gcc_target_platform}-gcc-nm
%{_prefix}/bin/%{gcc_target_platform}-gcc-ranlib
%endif
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man7/*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include

# Shouldn't include all files under this fold, split to diff pkgs
#%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/*
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_plugin.so*

%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2

%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/include/*

# Shouldn't include all files under this fold, split to diff pkgs
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdatomic.h

%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%endif

# For ARM port
%ifarch %{arm}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed/README
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_acle.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_acle.h
%endif
%ifnarch mips mipsel aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/ssp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/stdio.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/string.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/unistd.h
%ifnarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdnoreturn.h

%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/install-tools

%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%if %{build_cloog}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcloog-isl.so.*
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.so
%endif
%endif
%dir %{_prefix}/libexec/getconf
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING*

%files -n cpp -f cpplib.lang
%defattr(-,root,root,-)
/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc
%defattr(-,root,root,-)
/%{_lib}/libgcc_s-%{gcc_version}.so.1
/%{_lib}/libgcc_s.*
/%{_libdir}/libgcc_s.*
%doc gcc/COPYING.LIB

# For ARM port
%ifarch %{arm} aarch64 mipsel
%{_prefix}/%{_lib}/libssp*
%endif

%files c++
%defattr(-,root,root,-)
%ifnarch %{arm} aarch64 mipsel
%{_prefix}/bin/%{gcc_target_platform}-*++
%endif
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libstdc++.*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%dir %{_prefix}/share/gcc-%{gcc_version}
%{_prefix}/share/gcc-%{gcc_version}/python

%files -n libstdc++-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a  
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%ifnarch  %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%defattr(-,root,root)
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%files objc
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/objc
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/objc/*.h
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.so
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%defattr(-,root,root,-)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libobjc.*

%files -n libgomp
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgomp.*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%if %{build_64bit_multilib}
%files -n gcc-multilib
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortranbegin.a
%dir %{_prefix}/lib64
%{_prefix}/lib64/*
%endif

%if %{build_libquadmath}
%files -n libquadmath
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%doc rpm.doc/libquadmath/COPYING*

%files -n libquadmath-devel
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libquadmath.so
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath_weak.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%doc rpm.doc/libquadmath/ChangeLog*

%files -n libquadmath-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%endif


%if %{build_libitm}
%files -n libitm
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm-devel
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libitm.so
%{_prefix}/%{_lib}/libitm.spec
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/itm.h
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/itm_weak.h
##%doc rpm.doc/libitm/ChangeLog*

%files -n libitm-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%endif

%if %{build_libatomic}
%files -n libatomic
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic-devel
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libatomic.so

%files -n libatomic-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
##%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libasan.so.0*

%files -n libasan-devel
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libasan.so

%files -n libasan-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
##%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libtsan.so.0*

%files -n libtsan-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
##%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%files plugin-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
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
%dir /usr/lib/bfd-plugins
/usr/lib/bfd-plugins/liblto_plugin.so
# /\/\/\
# cross
%endif

