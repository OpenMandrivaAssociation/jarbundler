%define gcj_support 1
%define section free

Name:           jarbundler
Version:        1.9
Release:        %mkrel 0.0.2
Epoch:          0
Summary:        Mac OS X JarBundler ANT Task
License:        GPL
Group:          Development/Java
URL:            http://informagen.com/JarBundler/
Source0:        http://informagen.com/JarBundler/dist/jarbundler.tar.gz
BuildRequires:  ant
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  java-rpmbuild
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
How many times has this happened to you? You've written a little 
Java utility, or maybe even a more complex application, and you 
want to create Mac OS X application bundle for easy distribution.

You'd like to be able to do it automatically from your build 
process, but you're forced to go run the Apple Jar Bundler and 
tweak all the settings manually every time you build.

Well no more! JarBundler is a feature-rich Ant task which will 
create a Mac OS X application bundle from a list of Jar files and 
a main class name. You can add an Icon resource, set various Mac 
OS X native look-and-feel bells and whistles, and maintain your 
application bundles as part of your normal build and release 
cycle. It is free software licensed under the GNU General Public 
License.

This release is based on the earlier work of Seth Morabito.

%package javadoc
Summary:        Javadoc documentation for %{name}
Group:          Development/Java

%description javadoc
Javadoc documentation for %{name}.

%prep
%setup -q
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} jar javadocs

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a build/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc *.TXT example
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
