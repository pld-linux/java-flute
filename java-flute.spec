#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		rel			1
%define		subver		OOo31
%define		srcname		flute
Summary:	Java CSS parser using SAC
Name:		java-%{srcname}
Version:	1.3.0
Release:	0.%{subver}.%{rel}
# The entire source code is W3C except ParseException.java which is LGPLv2+
License:	W3C and LGPL v2+
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/jfreereport/%{srcname}-%{version}-%{subver}.zip
# Source0-md5:	1209a788dff31ccb5304a82a35a80ad3
URL:		http://www.w3.org/Style/CSS/SAC/
BuildRequires:	ant
BuildRequires:	java-sac
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-sac
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Cascading Style Sheets parser using the Simple API for CSS, for
Java.

%package javadoc
Summary:	Javadoc for Flute
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for Flute.

%prep
%setup -qc
find -name "*.jar" | xargs -r rm -v

install -d lib

%build
build-jar-repository -s -p lib sac
%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc COPYRIGHT.html
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%doc COPYRIGHT.html
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
