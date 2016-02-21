%global pkg_name geronimo-osgi-support
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global registry geronimo-osgi-registry
%global locator geronimo-osgi-locator

Name:             %{?scl_prefix}%{pkg_name}
Version:          1.0
Release:          15.12%{?dist}
Summary:          OSGI spec bundle support
License:          ASL 2.0 and W3C
URL:              http://geronimo.apache.org/

Source0:          http://repo2.maven.org/maven2/org/apache/geronimo/specs/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.tar.gz
# Use parent pom files instead of unavailable 'genesis-java5-flava'
Patch1:           use_parent_pom.patch
# Remove itests due to unavailable dependencies
Patch2:           remove-itests.patch
BuildArch:        noarch

BuildRequires:    %{?scl_prefix_java_common}javapackages-tools
BuildRequires:    %{?scl_prefix_java_common}maven-local
BuildRequires:    %{?scl_prefix}felix-osgi-core
BuildRequires:    %{?scl_prefix}felix-osgi-compendium
BuildRequires:    %{?scl_prefix}geronimo-parent-poms
BuildRequires:    %{?scl_prefix}maven-resources-plugin
BuildRequires:    %{?scl_prefix}maven-surefire-provider-junit


%description
This project is a set of bundles and integration tests for implementing
OSGi-specific lookup in the Geronimo spec projects.


%package javadoc
Summary:          Javadoc for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
iconv -f iso8859-1 -t utf-8 LICENSE > LICENSE.conv && mv -f LICENSE.conv LICENSE
sed -i 's/\r//' LICENSE NOTICE
%patch1 -p0
%patch2 -p0

%pom_xpath_inject "pom:plugin[pom:artifactId[text()='maven-bundle-plugin']]
                       /pom:configuration/pom:instructions" "
    <Export-Package>!*</Export-Package>" geronimo-osgi-locator

%mvn_file :%{registry} %{registry}
%mvn_file :%{locator} %{locator}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1.0-15.12
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.0-15.11
- maven33 rebuild

* Thu Jan 15 2015 Michal Srb <msrb@redhat.com> - 1.0-15.10
- Fix directory ownership

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.0-15.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.0-15.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-15.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-15.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-15.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-15.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-15.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-15.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-15.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0-15
- Mass rebuild 2013-12-27

* Fri Aug 23 2013 Michal Srb <msrb@redhat.com> - 1.0-14
- Migrate away from mvn-rpmbuild (Resolves: #997485)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-13
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-11
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Dec 07 2012 Jaromir Capik <jcapik@redhat.com> 1.0-10
- Depmap removed (not needed anymore)
- Removing EOL whitespaces in the spec file

* Thu Aug 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-9
- Fix license tag
- Install NOTICE files

* Mon Aug  6 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-8
- Add explicit OSGi export, resolves 812827

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-5
- Build with maven 3 - site-plugin no longer works with maven2.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 2 2010 Chris Spike <chris.spike@arcor.de> 1.0-3
- Removed W3C from 'License:' field (XMLSchema.dtd not existent)

* Thu Jul 29 2010 Chris Spike <chris.spike@arcor.de> 1.0-2
- Fixed wrong EOL encoding in LICENSE
- Fixed LICENSE file-not-utf8 
- Added W3C to 'License:' field
- Added patch explanations

* Mon Jul 26 2010 Chris Spike <chris.spike@arcor.de> 1.0-1
- Initial version of the package
