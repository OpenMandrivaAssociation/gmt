%define release %mkrel 3
%define version 4.1.3

%define requirever 4.1.3

%define libname %mklibname %name

Summary: Scientific graphic tool with maps
Name: gmt
Version: %{version}
Release: %{release}
License: GPL 
Group: Sciences/Geosciences
Source0: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_src.tar.bz2
Source1: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_scripts.tar.bz2
Source2: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_suppl.tar.bz2
Source3: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_man.tar.bz2
Source4: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_pdf.tar.bz2
Source5: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_web.tar.bz2
Source6: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_tut.tar.bz2
Source7: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT%{version}_share.tar.bz2
Source8: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT4.1_coast.tar.bz2
Source9: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT4.1_high.tar.bz2
Source10: ftp://gmt.soest.hawaii.edu/pub/gmt/GMT4.1_full.tar.bz2
URL: http://gmt.soest.hawaii.edu/
BuildRoot: %_tmppath/%name-%version-root
BuildRequires: netcdf-devel >= 3.4
BuildRequires: X11-devel
Requires: gmt-coast = %version-%release

%package        coast
Summary:        GMT cartography data crude, low and intermediate resolution
Group:          Sciences/Geosciences
Requires:       %{name} >= %requirever
Conflicts:      gmt-data < %version
BuildRoot:      %{_tmppath}/%{name}-%{version}

%package 	highdata
Summary:	GMT cartography data High-Resolution
Group:		Sciences/Geosciences
Requires: 	%{name} >= %requirever
BuildRoot:  %{_tmppath}/%{name}-%{version}

%package 	fulldata
Summary:	GMT cartography data Full-Resolution (maximum)
Group:		Sciences/Geosciences
Requires: 	%{name} >= %requirever
BuildRoot:  %{_tmppath}/%{name}-%{version}

%package        doc
Summary:        GMT HTML and PDF Documentation
Group:          Books/Other

%package -n %libname
Summary:	Library from GMT
Group:		System/Libraries
Provides:	lib%name = %version-%release

%package -n %libname-devel
Summary:	Library from GMT
Group:		Development/Other
Provides:	lib%name-devel = %version-%release
Provides:	%name-devel = %version-%release
Requires:	%libname = %version-%release

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
%setup -q -n GMT%{version} -b 0 -b 1 -b 2 -b 3 -b 4 -b 5 -b 6 -b 7 -a 8 -a 9 -a 10

%build
# workaround else if try to build mex, which need matlab
./configure

./configure \
	--prefix=%_prefix \
	--libdir=%_libdir \
	--enable-shared \
	--enable-mansect=1 \
        --disable-mex \
	--datadir=%{_datadir}/%{name}-%{version}/share/coast \

# mex need matlab # TODO add a --with matlab
touch src/mex/.skip

make GMT_DEFAULT_PATH=%_datadir/gmt-%{version} CC_OPT="%optflags -fPIC" 

%install
%makeinstall install
%makeinstall install-man
%makeinstall suppldir=%buildroot%_datadir/gmt-%{version}/shareinstall-suppl
%makeinstall datadir=%buildroot%_datadir/gmt-%{version}/share install-data

chmod 755 %buildroot%_libdir/*

mkdir -p %buildroot/%_sysconfdir/profile.d/
cat > %buildroot/%_sysconfdir/profile.d/%name.sh <<EOF
GMTHOME=%{_datadir}/gmt-%{version}
export GMTHOME

EOF

cat > %buildroot/%_sysconfdir/profile.d/%name.csh <<EOF
setenv GMTHOME %{_datadir}/gmt-%{version}

EOF

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/blockmean
%{_bindir}/blockmedian
%{_bindir}/blockmode
%{_bindir}/filter1d
%{_bindir}/fitcircle
%{_bindir}/grdfilter
%{_bindir}/gmt2rgb
%{_bindir}/gmtconvert
%{_bindir}/gmtdefaults
%{_bindir}/gmtmath
%{_bindir}/gmtselect
%{_bindir}/gmtset
%{_bindir}/grd2cpt
%{_bindir}/grd2xyz
%{_bindir}/grdcontour
%{_bindir}/grdblend
%{_bindir}/grdcut
%{_bindir}/grdclip
%{_bindir}/grdedit
%{_bindir}/grdfft
%{_bindir}/grdgradient
%{_bindir}/grdhisteq
%{_bindir}/grdimage
%{_bindir}/grdinfo
%{_bindir}/grdlandmask
%{_bindir}/grdmask
%{_bindir}/grdtrack
%{_bindir}/grdreformat
%{_bindir}/grdmath
%{_bindir}/grdpaste
%{_bindir}/grdproject
#%{_bindir}/grdrotater
%{_bindir}/grdsample
%{_bindir}/grdtrend
%{_bindir}/grdvector
%{_bindir}/grdview
%{_bindir}/grdvolume
%{_bindir}/makecpt
%{_bindir}/mapproject
#%{_bindir}/mgd77info
#%{_bindir}/mgd77list
#%{_bindir}/mgd77path
#%{_bindir}/mgd77sniffer
#%{_bindir}/mgd77track
%{_bindir}/minmax
%{_bindir}/nearneighbor
%{_bindir}/project
%{_bindir}/psbasemap
%{_bindir}/psclip
%{_bindir}/pscoast
%{_bindir}/pshistogram
%{_bindir}/psimage
%{_bindir}/pslegend
%{_bindir}/psmask
%{_bindir}/psrose
%{_bindir}/psscale
%{_bindir}/pstext
%{_bindir}/pscontour
%{_bindir}/pswiggle
%{_bindir}/psxy
%{_bindir}/psxyz
#%{_bindir}/rotconverter
%{_bindir}/sample1d
#%{_bindir}/segy2grd
%{_bindir}/spectrum1d
%{_bindir}/splitxyz
%{_bindir}/surface
%{_bindir}/trend1d
%{_bindir}/trend2d
%{_bindir}/triangulate
#%{_bindir}/x2sys_binlist
#%{_bindir}/x2sys_get
#%{_bindir}/x2sys_init
#%{_bindir}/x2sys_put
%{_bindir}/xyz2grd
%{_bindir}/GMT
#%{_bindir}/grdraster
#%{_bindir}/gshhs
#%{_bindir}/gshhs_dp
#%{_bindir}/img2mercgrd
#%{_bindir}/img2grd
#%{_bindir}/psmeca
#%{_bindir}/pscoupe
#%{_bindir}/pspolar
#%{_bindir}/psvelo
#%{_bindir}/binlegs
#%{_bindir}/gmt2bin
#%{_bindir}/gmt2dat
#%{_bindir}/dat2gmt
#%{_bindir}/gmtinfo
#%{_bindir}/gmtlegs
#%{_bindir}/gmtlist
#%{_bindir}/gmtpath
#%{_bindir}/gmttrack
#%{_bindir}/mgd77convert
#%{_bindir}/mgd77togmt
#%{_bindir}/mgd77manage
#%{_bindir}/psmegaplot
#%{_bindir}/makepattern
#%{_bindir}/nc2xy
#%{_bindir}/pssegyz
#%{_bindir}/pssegy
#%{_bindir}/ps2raster
#%{_bindir}/backtracker
#%{_bindir}/hotspotter
#%{_bindir}/originator
#%{_bindir}/x2sys_datalist
#%{_bindir}/x2sys_cross
#%{_bindir}/xgridedit
#%{_bindir}/x_edit
#%{_bindir}/x_init
#%{_bindir}/x_list
#%{_bindir}/x_over
#%{_bindir}/x_report
#%{_bindir}/x_remove
#%{_bindir}/x_setup
#%{_bindir}/x_solve_dc_drift
#%{_bindir}/x_update
%dir %{_datadir}/gmt-%{version}/share
%{_datadir}/gmt-%{version}/share/GMT_CustomSymbols.lis
#%{_datadir}/gmt-%{version}/share/dbase/grdraster.info
%{_datadir}/gmt-%{version}/share/.gmtdefaults_SI
%{_datadir}/gmt-%{version}/share/.gmtdefaults_US
%{_datadir}/gmt-%{version}/share/gmt.conf
%{_datadir}/gmt-%{version}/share/cpt/GMT_drywet.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_cool.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_copper.cpt
%{_datadir}/gmt-%{version}/share/GMT_CPT.lis
%{_datadir}/gmt-%{version}/share/gmtformats.d
%{_datadir}/gmt-%{version}/share/time/br.d
%{_datadir}/gmt-%{version}/share/time/cn1.d
%{_datadir}/gmt-%{version}/share/time/cn2.d
%{_datadir}/gmt-%{version}/share/time/de.d
%{_datadir}/gmt-%{version}/share/time/dk.d
%{_datadir}/gmt-%{version}/share/time/eh.d
%{_datadir}/gmt-%{version}/share/time/es.d
%{_datadir}/gmt-%{version}/share/time/fi.d
%{_datadir}/gmt-%{version}/share/time/fr.d
%{_datadir}/gmt-%{version}/share/time/gr.d
%{_datadir}/gmt-%{version}/share/time/hu.d
%{_datadir}/gmt-%{version}/share/time/ie.d
%{_datadir}/gmt-%{version}/share/time/il.d
%{_datadir}/gmt-%{version}/share/time/is.d
%{_datadir}/gmt-%{version}/share/time/it.d
%{_datadir}/gmt-%{version}/share/time/jp.d
%{_datadir}/gmt-%{version}/share/time/nl.d
%{_datadir}/gmt-%{version}/share/time/no.d
%{_datadir}/gmt-%{version}/share/time/pl.d
%{_datadir}/gmt-%{version}/share/time/pt.d
%{_datadir}/gmt-%{version}/share/time/ru.d
%{_datadir}/gmt-%{version}/share/time/se.d
%{_datadir}/gmt-%{version}/share/time/sg.d
%{_datadir}/gmt-%{version}/share/time/to.d
%{_datadir}/gmt-%{version}/share/time/tr.d
%{_datadir}/gmt-%{version}/share/time/uk.d
%{_datadir}/gmt-%{version}/share/time/us.d
%{_datadir}/gmt-%{version}/share/cpt/GMT_gebco.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_globe.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_gray.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_haxby.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_hot.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_jet.cpt
%{_datadir}/gmt-%{version}/share/gmtmedia.d
%{_datadir}/gmt-%{version}/share/cpt/GMT_no_green.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_ocean.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_polar.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_rainbow.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_red2green.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_relief.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_sealand.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_seis.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_split.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_topo.cpt
%{_datadir}/gmt-%{version}/share/cpt/GMT_wysiwyg.cpt

%{_datadir}/gmt-%{version}/share/dbase

%{_datadir}/gmt-%{version}/share/mgg/carter.d
%{_datadir}/gmt-%{version}/share/mgg/gmtfile_paths
%{_datadir}/gmt-%{version}/share/mgd77/mgd77_paths.txt
%dir %{_datadir}/gmt-%{version}/share/pslib
%{_datadir}/gmt-%{version}/share/pslib/PSL_text.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-1.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-10.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-13.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-14.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-15.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-2.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-3.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-4.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-5.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-6.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-7.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-8.ps
%{_datadir}/gmt-%{version}/share/pslib/ISO-8859-9.ps
%{_datadir}/gmt-%{version}/share/pslib/ISOLatin1+.ps
%{_datadir}/gmt-%{version}/share/pslib/ISOLatin1.ps
%{_datadir}/gmt-%{version}/share/pslib/PSL_label.ps
%{_datadir}/gmt-%{version}/share/pslib/PSL_prologue.ps
%{_datadir}/gmt-%{version}/share/pslib/PS_font_info.d
%{_datadir}/gmt-%{version}/share/pslib/Standard+.ps
%{_datadir}/gmt-%{version}/share/pslib/Standard.ps
%dir %{_datadir}/gmt-%{version}/share/pattern
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_01.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_02.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_03.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_04.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_05.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_06.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_07.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_08.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_09.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_10.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_11.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_12.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_13.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_14.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_15.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_16.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_17.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_18.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_19.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_20.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_21.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_22.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_23.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_24.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_25.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_26.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_27.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_28.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_29.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_30.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_31.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_32.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_33.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_34.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_35.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_36.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_37.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_38.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_39.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_40.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_41.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_42.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_43.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_44.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_45.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_46.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_47.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_48.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_49.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_50.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_51.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_52.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_53.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_54.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_55.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_56.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_57.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_58.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_59.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_60.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_61.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_62.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_63.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_64.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_65.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_66.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_67.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_68.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_69.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_70.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_71.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_72.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_73.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_74.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_75.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_76.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_77.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_78.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_79.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_80.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_81.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_82.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_83.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_84.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_85.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_86.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_87.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_88.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_89.ras
%{_datadir}/gmt-%{version}/share/pattern/ps_pattern_90.ras
#%{_datadir}/gmt-%{version}/share/x2sys/gmt.def
#%{_datadir}/gmt-%{version}/share/x2sys/mgd77.def
#%{_datadir}/gmt-%{version}/share/x2sys/xy.def
#%{_datadir}/gmt-%{version}/share/x2sys/xyz.def
#%{_datadir}/gmt-%{version}/share/x2sys/geo.def
#%{_datadir}/gmt-%{version}/share/x2sys/geoz.def
#%{_datadir}/gmt-%{version}/share/x2sys/mgd77+.def
%dir %{_datadir}/gmt-%{version}/share/custom
%{_datadir}/gmt-%{version}/share/custom/astroid.def
%{_datadir}/gmt-%{version}/share/custom/circle.def
%{_datadir}/gmt-%{version}/share/custom/crosshair.def
%{_datadir}/gmt-%{version}/share/custom/cross.def
%{_datadir}/gmt-%{version}/share/custom/diamond.def
%{_datadir}/gmt-%{version}/share/custom/deltoid.def
%{_datadir}/gmt-%{version}/share/custom/flash.def
%{_datadir}/gmt-%{version}/share/custom/hexagon.def
%{_datadir}/gmt-%{version}/share/custom/hlens.def
%{_datadir}/gmt-%{version}/share/custom/hlozenge.def
%{_datadir}/gmt-%{version}/share/custom/hneedle.def
%{_datadir}/gmt-%{version}/share/custom/invtriangle.def
%{_datadir}/gmt-%{version}/share/custom/lcrescent.def
%{_datadir}/gmt-%{version}/share/custom/lflag.def
%{_datadir}/gmt-%{version}/share/custom/ltriangle.def
%{_datadir}/gmt-%{version}/share/custom/meca.def
%{_datadir}/gmt-%{version}/share/custom/octagon.def
%{_datadir}/gmt-%{version}/share/custom/pacman.def
%{_datadir}/gmt-%{version}/share/custom/pentagon.def
%{_datadir}/gmt-%{version}/share/custom/rcrescent.def
%{_datadir}/gmt-%{version}/share/custom/rflag.def
%{_datadir}/gmt-%{version}/share/custom/rtriangle.def
%{_datadir}/gmt-%{version}/share/custom/sectoid.def
%{_datadir}/gmt-%{version}/share/custom/square.def
%{_datadir}/gmt-%{version}/share/custom/squaroid.def
%{_datadir}/gmt-%{version}/share/custom/star.def
%{_datadir}/gmt-%{version}/share/custom/star3.def
%{_datadir}/gmt-%{version}/share/custom/star4.def
%{_datadir}/gmt-%{version}/share/custom/starp.def
%{_datadir}/gmt-%{version}/share/custom/sun.def
%{_datadir}/gmt-%{version}/share/custom/triangle.def
%{_datadir}/gmt-%{version}/share/custom/vlens.def
%{_datadir}/gmt-%{version}/share/custom/vlozenge.def
%{_datadir}/gmt-%{version}/share/custom/vneedle.def
%{_datadir}/gmt-%{version}/share/custom/volcano.def
%{_mandir}/man1/*
%attr(0755, root, root) %{_sysconfdir}/profile.d/*

%files coast
%defattr(-,root,root)
%dir %{_datadir}/gmt-%{version}/share/coast
%{_datadir}/gmt-%{version}/share/coast/binned_border_c.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_GSHHS_c.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_river_c.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_border_l.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_GSHHS_l.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_river_l.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_border_i.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_GSHHS_i.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_river_i.cdf

%files highdata
%defattr(-,root,root)
%dir %{_datadir}/gmt-%{version}/share/coast
%{_datadir}/gmt-%{version}/share/coast/binned_border_h.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_GSHHS_h.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_river_h.cdf

%files fulldata
%defattr(-,root,root)
%dir %{_datadir}/gmt-%{version}/share/coast
%{_datadir}/gmt-%{version}/share/coast/binned_border_f.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_GSHHS_f.cdf
%{_datadir}/gmt-%{version}/share/coast/binned_river_f.cdf

%files doc
%defattr(-,root,root)
%doc README CHANGES COPYING tutorial examples www/gmt/* 

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libpsl.so
%{_libdir}/libgmt.so
%{_libdir}/libgmtps.so

%files -n %libname-devel
%defattr(-,root,root)
#%{_libdir}/libgmt_mgg.a
#%{_libdir}/libx2sys.a
%{_libdir}/libpsl.a
%{_libdir}/libgmt.a
#%{_libdir}/libmgd77.a
%{_libdir}/libgmtps.a
%{_includedir}/gmt.h
%{_includedir}/gmt_math.h
%{_includedir}/gmt_nan.h
%{_includedir}/gmt_map.h
%{_includedir}/gmt_boundcond.h
%{_includedir}/gmt_shore.h
%{_includedir}/gmt_project.h
%{_includedir}/gmt_grd.h
#%{_includedir}/gmt_funcnames.h
%{_includedir}/gmt_colors.h
%{_includedir}/gmt_grdio.h
%{_includedir}/gmt_customio.h
%{_includedir}/gmt_bcr.h
%{_includedir}/gmt_unique.h
%{_includedir}/gmt_keywords.h
%{_includedir}/gmt_io.h
%{_includedir}/gmt_notposix.h
%{_includedir}/gmt_calclock.h
%{_includedir}/gmt_contour.h
%{_includedir}/gmt_mgg_header2.h
%{_includedir}/gmt_symbol.h
%{_includedir}/gmt_notunix.h
%{_includedir}/gmt_time_systems.h
%{_includedir}/pslib.h
%{_includedir}/gmt_datums.h
%{_includedir}/gmt_ellipsoids.h
%{_includedir}/gmt_grdformats.h
%{_includedir}/gmt_version.h
%{_includedir}/gmt_common.h
%{_includedir}/gmt_init.h
%{_includedir}/gmt_keycases.h
%{_includedir}/gmt_plot.h
%{_includedir}/gmt_proj.h
%{_includedir}/gmt_stat.h
%{_includedir}/gmt_support.h
%{_includedir}/gmt_synopsis.h
%{_includedir}/gmt_vector.h
#%{_includedir}/mgd77.h
#%{_includedir}/mgd77defaults.h
%{_includedir}/pslib_inc.h

%clean
[ %buildroot != '/' ] && rm -fr %buildroot


