%define release %mkrel 1
%define major_ver 4.3
%define minor_ver 1
%define gmtversion %{major_ver}.%{minor_ver}
%define version %{gmtversion}

%define dataversion 1.10
%define dataepoch 1
%define dataevr %{dataepoch}:%{dataversion}-%{release}

%define requirever %gmtversion

%define libname %mklibname %name

Summary: Scientific graphic tool with maps
Name: gmt
Version: %{version}
Release: %{release}
License: GPL 
Group: Sciences/Geosciences
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_src.tar.bz2
Source1: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_scripts.tar.bz2
Source2: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_suppl.tar.bz2
Source4: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_pdf.tar.bz2
Source5: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_web.tar.bz2
Source6: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_tut.tar.bz2
Source7: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_share.tar.bz2
Source8: ftp://gmt.soest.hawaii.edu/pub/gmt/GSHHS%{dataversion}_coast.tar.bz2
Source9: ftp://gmt.soest.hawaii.edu/pub/gmt/GSHHS%{dataversion}_high.tar.bz2
Source10: ftp://gmt.soest.hawaii.edu/pub/gmt/GSHHS%{dataversion}_full.tar.bz2
Patch1: gmt-4.2.0-overflow.patch
Patch2: gmt-netcdf-location.patch
URL: http://gmt.soest.hawaii.edu/
BuildRequires: netcdf-devel >= 3.4
BuildRequires: X11-devel
Requires: gmt-coast = %dataevr

%package        coast
Summary:        GMT cartography data crude, low and intermediate resolution
Group:          Sciences/Geosciences
Requires:       %{name} >= %requirever
Conflicts:      gmt-data < %gmtversion
Version:        %{dataversion}
Epoch:          %{dataepoch}

%package 	highdata
Summary:	GMT cartography data High-Resolution
Group:		Sciences/Geosciences
Requires: 	%{name} >= %requirever
Version:        %{dataversion}
Epoch:          %{dataepoch}

%package 	fulldata
Summary:	GMT cartography data Full-Resolution (maximum)
Group:		Sciences/Geosciences
Requires: 	%{name} >= %requirever
Version:        %{dataversion}
Epoch:          %{dataepoch}

%package        doc
Summary:        GMT HTML and PDF Documentation
Group:          Books/Other

%package -n %libname
Summary:	Library from GMT
Group:		System/Libraries
Provides:	lib%name = %gmtversion-%release

%package -n %libname-devel
Summary:	Library from GMT
Group:		Development/Other
Provides:	lib%name-devel = %gmtversion-%release
Provides:	%name-devel = %gmtversion-%release
Requires:	%libname = %gmtversion-%release

%description
GMT is a free, open source collection of ~60 UNIX tools that allow users to 
manipulate (x,y) and (x,y,z) data sets (including filtering, trend fitting, 
gridding, projecting, etc.) and produce Encapsulated PostScript File (EPS) 
illustrations ranging from simple x-y plots through contour maps to 
artificially illuminated surfaces and 3-D perspective views in black and white,
gray tone, hachure patterns, and 24-bit color. GMT supports 25 common map 
projections plus linear, log, and power scaling, and comes with support data 
such as coastlines, rivers, and political boundaries.

GMT is developed and maintained by Paul Wessel and Walter H. F. Smith. 

GMT is partly supported by the National Science Foundation. 

%description coast 
GMT is a free, open source collection of mapping tools and cartography
GMT supports 25 common map projections plus linear, log, and power scaling,
and comes with support data such as coastlines, rivers, 
and political boundaries. This is crude,low and intermediate resolution 
data version

%description highdata 
GMT is a free, open source collection of mapping tools and cartography
GMT supports 25 common map projections plus linear, log, and power scaling,
and comes with support data such as coastlines, rivers, 
and political boundaries. This is High resolution data version

%description fulldata 
GMT is a free, open source collection of mapping tools and cartography
GMT supports 25 common map projections plus linear, log, and power scaling,
and comes with support data such as coastlines, rivers, 
and political boundaries. This is maximum resolution data version

%description doc
HTML, PDF documentation and examples for GMT.

%description -n %libname
GMT is a free, open source collection of mapping tools and cartography
GMT supports 25 common map projections plus linear, log, and power scaling,
and comes with support data such as coastlines, rivers, 
and political boundaries. This is High resolution data version.

This package contains library from gmt.

%description -n %libname-devel
GMT is a free, open source collection of mapping tools and cartography
GMT supports 25 common map projections plus linear, log, and power scaling,
and comes with support data such as coastlines, rivers, 
and political boundaries. This is High resolution data version.

This package contains development files from gmt.

%prep
%setup -q -n GMT%{gmtversion} -b 0 -b 1 -b 2 -b 4 -b 5 -b 6 -b 7 -a 8 -a 9 -a 10
%patch1 -p0 -b .overflow
%patch2 -p0 -b .netcdf-location

%build
# -fstack-protector make build failing
%define _ssp_cflags %{nil}

# workaround else if try to build mex, which need matlab
./configure

./configure \
	--prefix=%_prefix \
	--libdir=%_libdir \
	--enable-shared \
	--enable-mansect=1 \
    --disable-mex \
	--datadir=%{_datadir}/%{name}-%{gmtversion}/share \

# mex need matlab # TODO add a --with matlab
touch src/mex/.skip

make GMT_DEFAULT_PATH=%_datadir/gmt-%{gmtversion} CC_OPT="%optflags -fPIC" 

%install
%makeinstall install
%makeinstall install-man
%makeinstall suppldir=%buildroot%_datadir/gmt-%{gmtversion}/shareinstall-suppl
%makeinstall datadir=%buildroot%_datadir/gmt-%{gmtversion}/share install-data

chmod 755 %buildroot%_libdir/*

mkdir -p %buildroot/%_sysconfdir/profile.d/
cat > %buildroot/%_sysconfdir/profile.d/%name.sh <<EOF
GMTHOME=%{_datadir}/gmt-%{gmtversion}
export GMTHOME

EOF

cat > %buildroot/%_sysconfdir/profile.d/%name.csh <<EOF
setenv GMTHOME %{_datadir}/gmt-%{gmtversion}

EOF

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*

%dir %{_datadir}/gmt-%{gmtversion}/share
%{_datadir}/gmt-%{gmtversion}/share/conf/gmt.conf
%{_datadir}/gmt-%{gmtversion}/share/conf/gmt_cpt.conf
%{_datadir}/gmt-%{gmtversion}/share/conf/gmt_custom_media.conf
%{_datadir}/gmt-%{gmtversion}/share/conf/gmt_custom_symbols.conf
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_drywet.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_cool.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_copper.cpt
%{_datadir}/gmt-%{gmtversion}/share/time/br.d
%{_datadir}/gmt-%{gmtversion}/share/time/cn1.d
%{_datadir}/gmt-%{gmtversion}/share/time/cn2.d
%{_datadir}/gmt-%{gmtversion}/share/time/de.d
%{_datadir}/gmt-%{gmtversion}/share/time/dk.d
%{_datadir}/gmt-%{gmtversion}/share/time/eh.d
%{_datadir}/gmt-%{gmtversion}/share/time/es.d
%{_datadir}/gmt-%{gmtversion}/share/time/fi.d
%{_datadir}/gmt-%{gmtversion}/share/time/fr.d
%{_datadir}/gmt-%{gmtversion}/share/time/gr.d
%{_datadir}/gmt-%{gmtversion}/share/time/hu.d
%{_datadir}/gmt-%{gmtversion}/share/time/ie.d
%{_datadir}/gmt-%{gmtversion}/share/time/il.d
%{_datadir}/gmt-%{gmtversion}/share/time/is.d
%{_datadir}/gmt-%{gmtversion}/share/time/it.d
%{_datadir}/gmt-%{gmtversion}/share/time/jp.d
%{_datadir}/gmt-%{gmtversion}/share/time/nl.d
%{_datadir}/gmt-%{gmtversion}/share/time/no.d
%{_datadir}/gmt-%{gmtversion}/share/time/pl.d
%{_datadir}/gmt-%{gmtversion}/share/time/pt.d
%{_datadir}/gmt-%{gmtversion}/share/time/ru.d
%{_datadir}/gmt-%{gmtversion}/share/time/se.d
%{_datadir}/gmt-%{gmtversion}/share/time/sg.d
%{_datadir}/gmt-%{gmtversion}/share/time/to.d
%{_datadir}/gmt-%{gmtversion}/share/time/tr.d
%{_datadir}/gmt-%{gmtversion}/share/time/uk.d
%{_datadir}/gmt-%{gmtversion}/share/time/us.d
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_gebco.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_globe.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_gray.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_haxby.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_hot.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_jet.cpt
#%{_datadir}/gmt-%{gmtversion}/share/gmtmedia.d
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_no_green.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_ocean.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_polar.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_rainbow.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_red2green.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_relief.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_sealand.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_seis.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_split.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_topo.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_wysiwyg.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_cyclic.cpt
%{_datadir}/gmt-%{gmtversion}/share/cpt/GMT_panoply.cpt

%{_datadir}/gmt-%{gmtversion}/share/dbase

%{_datadir}/gmt-%{gmtversion}/share/mgg/carter.d
%{_datadir}/gmt-%{gmtversion}/share/mgg/gmtfile_paths
%{_datadir}/gmt-%{gmtversion}/share/mgd77/mgd77_paths.txt
%dir %{_datadir}/gmt-%{gmtversion}/share/pslib
%{_datadir}/gmt-%{gmtversion}/share/pslib/PSL_text.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-1.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-10.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-13.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-14.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-15.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-2.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-3.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-4.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-5.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-6.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-7.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-8.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISO-8859-9.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISOLatin1+.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/ISOLatin1.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/PSL_label.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/PSL_prologue.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/PS_font_info.d
%{_datadir}/gmt-%{gmtversion}/share/pslib/Standard+.ps
%{_datadir}/gmt-%{gmtversion}/share/pslib/Standard.ps
%dir %{_datadir}/gmt-%{gmtversion}/share/pattern
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_01.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_02.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_03.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_04.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_05.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_06.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_07.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_08.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_09.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_10.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_11.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_12.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_13.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_14.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_15.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_16.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_17.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_18.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_19.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_20.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_21.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_22.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_23.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_24.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_25.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_26.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_27.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_28.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_29.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_30.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_31.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_32.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_33.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_34.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_35.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_36.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_37.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_38.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_39.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_40.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_41.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_42.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_43.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_44.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_45.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_46.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_47.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_48.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_49.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_50.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_51.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_52.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_53.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_54.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_55.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_56.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_57.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_58.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_59.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_60.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_61.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_62.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_63.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_64.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_65.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_66.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_67.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_68.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_69.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_70.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_71.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_72.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_73.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_74.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_75.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_76.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_77.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_78.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_79.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_80.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_81.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_82.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_83.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_84.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_85.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_86.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_87.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_88.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_89.ras
%{_datadir}/gmt-%{gmtversion}/share/pattern/ps_pattern_90.ras
%dir %{_datadir}/gmt-%{gmtversion}/share/x2sys
%{_datadir}/gmt-%{gmtversion}/share/x2sys/gmt.def
%{_datadir}/gmt-%{gmtversion}/share/x2sys/mgd77.def
%{_datadir}/gmt-%{gmtversion}/share/x2sys/xy.def
%{_datadir}/gmt-%{gmtversion}/share/x2sys/xyz.def
%{_datadir}/gmt-%{gmtversion}/share/x2sys/geo.def
%{_datadir}/gmt-%{gmtversion}/share/x2sys/geoz.def
%{_datadir}/gmt-%{gmtversion}/share/x2sys/mgd77+.def
%{_datadir}/gmt-%{gmtversion}/share/conf/gmtdefaults_SI
%{_datadir}/gmt-%{gmtversion}/share/conf/gmtdefaults_US
%{_datadir}/gmt-%{gmtversion}/share/custom/hurricane.def

%dir %{_datadir}/gmt-%{gmtversion}/share/custom
%{_datadir}/gmt-%{gmtversion}/share/custom/astroid.def
%{_datadir}/gmt-%{gmtversion}/share/custom/circle.def
%{_datadir}/gmt-%{gmtversion}/share/custom/crosshair.def
%{_datadir}/gmt-%{gmtversion}/share/custom/cross.def
%{_datadir}/gmt-%{gmtversion}/share/custom/diamond.def
%{_datadir}/gmt-%{gmtversion}/share/custom/deltoid.def
%{_datadir}/gmt-%{gmtversion}/share/custom/flash.def
%{_datadir}/gmt-%{gmtversion}/share/custom/hexagon.def
%{_datadir}/gmt-%{gmtversion}/share/custom/hlens.def
%{_datadir}/gmt-%{gmtversion}/share/custom/hlozenge.def
%{_datadir}/gmt-%{gmtversion}/share/custom/hneedle.def
%{_datadir}/gmt-%{gmtversion}/share/custom/invtriangle.def
%{_datadir}/gmt-%{gmtversion}/share/custom/lcrescent.def
%{_datadir}/gmt-%{gmtversion}/share/custom/lflag.def
%{_datadir}/gmt-%{gmtversion}/share/custom/ltriangle.def
%{_datadir}/gmt-%{gmtversion}/share/custom/meca.def
%{_datadir}/gmt-%{gmtversion}/share/custom/octagon.def
%{_datadir}/gmt-%{gmtversion}/share/custom/pacman.def
%{_datadir}/gmt-%{gmtversion}/share/custom/pentagon.def
%{_datadir}/gmt-%{gmtversion}/share/custom/rcrescent.def
%{_datadir}/gmt-%{gmtversion}/share/custom/rflag.def
%{_datadir}/gmt-%{gmtversion}/share/custom/rtriangle.def
%{_datadir}/gmt-%{gmtversion}/share/custom/sectoid.def
%{_datadir}/gmt-%{gmtversion}/share/custom/square.def
%{_datadir}/gmt-%{gmtversion}/share/custom/squaroid.def
%{_datadir}/gmt-%{gmtversion}/share/custom/star.def
%{_datadir}/gmt-%{gmtversion}/share/custom/star3.def
%{_datadir}/gmt-%{gmtversion}/share/custom/star4.def
%{_datadir}/gmt-%{gmtversion}/share/custom/starp.def
%{_datadir}/gmt-%{gmtversion}/share/custom/sun.def
%{_datadir}/gmt-%{gmtversion}/share/custom/triangle.def
%{_datadir}/gmt-%{gmtversion}/share/custom/vlens.def
%{_datadir}/gmt-%{gmtversion}/share/custom/vlozenge.def
%{_datadir}/gmt-%{gmtversion}/share/custom/vneedle.def
%{_datadir}/gmt-%{gmtversion}/share/custom/volcano.def
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%attr(0755, root, root) %{_sysconfdir}/profile.d/*

%files coast
%defattr(-,root,root)
%dir %{_datadir}/gmt-%{gmtversion}/share/coast
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_border_c.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_GSHHS_c.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_river_c.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_border_l.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_GSHHS_l.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_river_l.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_border_i.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_GSHHS_i.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_river_i.cdf

%files highdata
%defattr(-,root,root)
%dir %{_datadir}/gmt-%{gmtversion}/share/coast
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_border_h.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_GSHHS_h.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_river_h.cdf

%files fulldata
%defattr(-,root,root)
%dir %{_datadir}/gmt-%{gmtversion}/share/coast
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_border_f.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_GSHHS_f.cdf
%{_datadir}/gmt-%{gmtversion}/share/coast/binned_river_f.cdf

%files doc
%defattr(-,root,root)
%doc README COPYING tutorial examples www/gmt/* 

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libgmt.so.4
%{_libdir}/libgmtps.so.4
%{_libdir}/libmgd77.so
%{_libdir}/libmgd77.so.4
%{_libdir}/libpsl.so.4
%{_libdir}/libx2sys.so
%{_libdir}/libx2sys.so.4

%files -n %libname-devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_includedir}/*.h
%{_libdir}/libpsl.so
%{_libdir}/libgmt.so
%{_libdir}/libgmtps.so

%clean
[ %buildroot != '/' ] && rm -fr %buildroot


