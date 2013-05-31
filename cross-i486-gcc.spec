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
BuildRequires: -rpmlint-Moblin -rpmlint-mini -post-build-checks
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
%define crossextraconfig --with-float=hard --with-fpu=vfpv3-d16 --with-arch=armv7-a
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
%define crossextraconfig --disable-libstdcxx-pch --with-arch=i486 --with-gnu-as=/opt/cross/bin/i486-meego-linux-gnu-as --with-gnu-ld=/opt/cross/bin/i486-meego-linux-gnu-ld --with-as=/opt/cross/bin/i486-meego-linux-gnu-as --with-ld=/opt/cross/bin/i486-meego-linux-gnu-ld
%endif
%if "%{crossarch}" == "x86_64"
%define crossextraconfig --disable-libstdcxx-pch
%endif
# single target atm.
ExclusiveArch: %ix86
#
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
# end crossbuild / accelerator section
%endif

%global gcc_version 4.6.4
%global gcc_release 1
%global _unpackaged_files_terminate_build 0
%global include_gappletviewer 0
%if !%{crossbuild} 
%ifnarch mips mipsel
%global build_cloog 1
%else
%global build_cloog 0
%endif
%else
%global build_cloog 0
%endif
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

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Version: %{gcc_version}
%if %{bootstrap}
Release: 0.%{bootstrap}.%{gcc_release}
%else
Release: %{gcc_release}
%endif
License: GPLv3+, GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
URL: http://launchpad.net/gcc-linaro
Source0: https://launchpad.net/gcc-linaro/4.6/4.6-2013.01/+download/gcc-linaro-4.6-2013.01.tar.bz2
Source1: libgcc_post_upgrade.c
Source2: README.libgcjwebplugin.so
Source100: gcc-rpmlintrc
Source200: baselibs.conf
Source300: precheckin.sh
Source301: aaa_README.PACKAGER

BuildRequires: binutils >= 2.22
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext,  bison, flex, texinfo
BuildRequires: mpc-devel
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.72

%if %{build_cloog}
BuildRequires: ppl >= 0.10, ppl-devel >= 0.10, cloog-ppl >= 0.15, cloog-ppl-devel >= 0.15
%endif

%if %{build_libstdcxx_docs}
BuildRequires: doxygen
BuildRequires: graphviz
%endif

%if !%{crossbuild}
Requires: cpp = %{version}-%{release}
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
Requires: glibc-devel
Requires: binutils >= 2.22
%endif

%if !%{crossbuild} 

%if %{build_cloog}
Requires: cloog-ppl >= 0.15
%endif

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

Patch0: gcc46-hack.patch
Patch2: gcc46-c++-builtin-redecl.patch
Patch4: gcc46-java-nomulti.patch
Patch7: gcc46-rh330771.patch
Patch8: gcc46-i386-libgomp.patch
Patch10: gcc46-libgomp-omp_h-multilib.patch
Patch11: gcc46-libtool-no-rpath.patch
Patch12: gcc46-cloog-dl.patch
Patch14: gcc46-pr38757.patch
Patch15: gcc46-libstdc++-docs.patch
Patch18: gcc46-ppl-0.10.patch
Patch19: gcc46-pr47858.patch
Patch20: gcc46-x86_64-nolib64.patch

Patch40: gcc46-use-atom.patch
Patch41: libgcc_post_upgrade.c.arm.patch
Patch42: gcc46-libiberty-conftest.patch
Patch44: gcc-hash-style-gnu.diff
Patch45: gcc46-MIPS-boehm-gc-stack-qemu.patch
Patch46: gcc-4.6.0-mips_fix-1.patch
Patch47: gcc46-fuse-ld-gold.patch

Patch9999: gcc44-ARM-boehm-gc-stack-qemu.patch

#We need -gnueabi indicator for ARM
%ifnarch %{arm}
%global _gnu %{nil}
%endif
%global gcc_target_platform %{_target_platform}

%description
The gcc package contains the GNU Compiler Collection version 4.6.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 4.6 shared support library
Group: System Environment/Libraries
Obsoletes: libgcc < %{version}-%{release}
Obsoletes: libgcc43
Autoreq: false

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

%package -n libmudflap
Summary: GCC mudflap shared support library
Group: System Environment/Libraries

%description -n libmudflap
This package contains GCC shared support library which is needed
for mudflap support.

%package -n libmudflap-devel
Summary: GCC mudflap support
Group: Development/Libraries
Requires: libmudflap = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libmudflap-devel
This package contains headers and static libraries for building
mudflap-instrumented programs.

To instrument a non-threaded program, add -fmudflap
option to GCC and when linking add -lmudflap, for threaded programs
also add -fmudflapth and -lmudflapth.

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

%prep
%setup -q -n gcc-linaro-4.6-2013.01
%patch0 -p0 -b .hack~
%patch2 -p0 -b .c++-builtin-redecl~
%patch4 -p0 -b .java-nomulti~
%patch7 -p0 -b .rh341221~
%patch8 -p0 -b .i386-libgomp~
%patch10 -p0 -b .libgomp-omp_h-multilib~
%patch11 -p0 -b .libtool-no-rpath~
%if %{build_cloog}
%patch12 -p0 -b .cloog-dl~
%endif
%patch14 -p0 -b .pr38757~
%if %{build_libstdcxx_docs}
%patch15 -p0 -b .libstdc++-docs~
%endif
%patch18 -p0 -b .ppl-0.10~
%patch19 -p0 -b .pr47858~
%patch20 -p1

%ifarch i586
%patch40 -p0 -b .atom
%endif

%ifarch %arm
%patch42 -p1
%endif
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1

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
export OPT_FLAGS="$OPT_FLAGS --param ggc-min-expand=0 --param ggc-min-heapsize=65536" 
%endif

%ifarch %arm
# gcc 45 fails to bootstrap itself otherwise on insn-attrtab.o
# issue is bad interaction between ggc and qemu
export OPT_FLAGS="$OPT_FLAGS --param ggc-min-expand=0 --param ggc-min-heapsize=65536" 
# gcc 45 segfaults on O2g.gch generation. (cc1plus)
%define ARM_EXTRA_CONFIGURE --disable-libstdcxx-pch
# for armv7hl reset the gcc specs
%ifarch armv6l
%define ARM_EXTRA_CONFIGURE --disable-libstdcxx-pch --with-fpu=vfp --with-arch=armv6
%endif
%ifarch armv7l
%define ARM_EXTRA_CONFIGURE --disable-libstdcxx-pch --with-fpu=vfpv3-d16 --with-arch=armv7-a
%endif
%ifarch armv7hl
%define ARM_EXTRA_CONFIGURE --disable-libstdcxx-pch --with-float=hard --with-fpu=vfpv3-d16 --with-arch=armv7-a
%endif
# for armv7nhl reset the gcc specs
%ifarch armv7nhl
%define ARM_EXTRA_CONFIGURE --disable-libstdcxx-pch --with-float=hard --with-fpu=neon --with-arch=armv7-a
%endif
# for armv7thl reset the gcc specs
%ifarch armv7thl
%define ARM_EXTRA_CONFIGURE --disable-libstdcxx-pch --with-float=hard --with-fpu=vfpv3-d16 --with-arch=armv7-a --with-mode=thumb
%endif
%# for armv7tnhl reset the gcc specs
%ifarch armv7tnhl
%define ARM_EXTRA_CONFIGURE --disable-libstdcxx-pch --with-float=hard --with-fpu=neon --with-arch=armv7-a --with-mode=thumb
%endif
%endif

#export OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e "s/-O2/-O2 -fkeep-inline-functions/g"`
export OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e "s/-fstack-protector//g"`

%if %{crossbuild}
# cross build
export PATH=/opt/cross/bin:$PATH
# strip all after -march . no arch specific options in cross-compiler build .
# -march=core2 -mssse3 -mtune=atom -mfpmath=sse -fasynchronous-unwi
export OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e "s#\-march=.*##g"`
%endif

CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="`echo $OPT_FLAGS | sed 's/ -Wall / /g'`" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
        --disable-bootstrap \
	--with-bugurl=http://bugs.merproject.org/ \
	--build=%{gcc_target_platform} \
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
%ifarch %{arm}
	%ARM_EXTRA_CONFIGURE \
	--disable-sjlj-exceptions \
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch i586
	--with-arch=i686 \
%endif
%ifarch i486
	--with-arch=i486 \
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
	--disable-libmudflap \
	--disable-libquadmath \
%endif
%if %{bootstrap} == 2
	--enable-languages=c \
	--with-sysroot=%{crosssysroot} \
	--disable-libssp \
	--disable-libgomp \
	--disable-libmudflap \
	--disable-libquadmath \
%endif
	--disable-libgcj \
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
mkdir -p rpm.doc/changelogs/{gcc/cp,libstdc++-v3,libobjc,libmudflap,libgomp}
sed -e 's,@VERSION@,%{gcc_version},' %{SOURCE2} > rpm.doc/README.libgcjwebplugin.so

for i in {gcc,gcc/cp,libstdc++-v3,libobjc,libmudflap,libgomp}/ChangeLog*; do
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
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/stdc++.h.gch

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
ln -sf ../../../libobjc.so.3 libobjc.so
ln -sf ../../../libstdc++.so.6.* libstdc++.so
ln -sf ../../../libgomp.so.1.* libgomp.so
ln -sf ../../../libmudflap.so.0.* libmudflap.so
ln -sf ../../../libmudflapth.so.0.* libmudflapth.so
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.3 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.* libstdc++.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
ln -sf ../../../../%{_lib}/libmudflap.so.0.* libmudflap.so
ln -sf ../../../../%{_lib}/libmudflapth.so.0.* libmudflapth.so
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
fi
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.*a $FULLLPATH/
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif


%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.3 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.* | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflapth.so
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libsupc++.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflap.a 32/libmudflap.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflapth.a 32/libmudflapth.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libquadmath.a 32/libquadmath.a
%endif
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libobjc.a -o -name libgomp.a \
		    -o -name libmudflap.a -o -name libmudflapth.a \
		    -o -name libgcc.a -o -name libgcov.a -name libquadmath.a \) -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.3.*

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

mkdir -p %{buildroot}%{_prefix}/sbin
%ifarch %{arm}
patch %{SOURCE1} < %{PATCH41}
%endif
%ifnarch mipsel
gcc -static -Os %{SOURCE1} -o %{buildroot}%{_prefix}/sbin/libgcc_post_upgrade
strip %{buildroot}%{_prefix}/sbin/libgcc_post_upgrade
%endif

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
#set -x
rm -rRf %buildroot/%{_prefix}/lib/libiberty.a
rm -rRf %buildroot/%{_prefix}/share
#set +x
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

%ifnarch mipsel
%post -n libgcc -p %{_prefix}/sbin/libgcc_post_upgrade
%endif

%postun -n libgcc -p /sbin/ldconfig

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

%post -n libmudflap -p /sbin/ldconfig

%postun -n libmudflap -p /sbin/ldconfig

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

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%ifnarch %{arm} mipsel
%{_prefix}/bin/%{gcc_target_platform}-gcc
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
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
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
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/abmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%endif

# For ARM port
%ifarch %{arm}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed/README
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed/linux/a.out.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/ssp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/stdio.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/string.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp/unistd.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/install-tools
%endif

%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.so
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
%ifnarch mipsel
%{_prefix}/sbin/libgcc_post_upgrade
%endif
%doc gcc/COPYING.LIB

# For ARM port
%ifarch %{arm} mipsel
%{_prefix}/%{_lib}/libssp*
%endif

%files c++
%defattr(-,root,root,-)
%ifnarch %{arm} mipsel
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

%files -n libmudflap
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libmudflap.*
%{_prefix}/%{_lib}/libmudflapth.*

%files -n libmudflap-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mf-runtime.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a  
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a  
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so  
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so  
%doc rpm.doc/changelogs/libmudflap/ChangeLog*

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

