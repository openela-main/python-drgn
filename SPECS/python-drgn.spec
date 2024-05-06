# Created by pyp2rpm-3.3.5
%if 0%{?rhel}
%bcond_with docs
%else
%bcond_without docs
%endif
%bcond_without tests

%global pypi_name drgn

%global _description %{expand:
drgn (pronounced "dragon") is a debugger with an emphasis on programmability.
drgn exposes the types and variables in a program for easy, expressive
scripting in Python.}

Name:           python-%{pypi_name}
Version:        0.0.24
Release:        2%{?dist}
Summary:        Programmable debugger

License:        LGPL-2.1-or-later
URL:            https://github.com/osandov/drgn
Source0:        %{pypi_source}

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
%if %{with docs}
BuildRequires:  sed
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3-docs
%endif
%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  bzip2-devel
BuildRequires:  elfutils-devel
BuildRequires:  libkdumpfile-devel
BuildRequires:  zlib-devel
BuildRequires:  xz-devel
# These are needed when building from git snapshots
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%description %{_description}

%package -n     %{pypi_name}
Summary:        %{summary}

%description -n %{pypi_name} %{_description}

%if %{with docs}
%package -n %{pypi_name}-doc
Summary:        %{pypi_name} documentation
BuildArch:      noarch
Requires:       python3-docs

%description -n %{pypi_name}-doc %{_description}

This package contains additional documentation for %{pypi_name}.
%endif

%prep
%autosetup -n %{pypi_name}-%{version} -p1
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
%if %{with docs}
# Use local intersphinx inventory
sed -r \
    -e 's|https://docs.python.org/3|%{_docdir}/python3-docs/html|' \
    -i docs/conf.py
%endif
# Ensure version is always set, even when building from git snapshots
if [ ! -f drgn/internal/version.py ]; then
  echo '__version__ = "%{version}"' > drgn/internal/version.py
fi

%build
# verbose build
V=1 %py3_build

%if %{with docs}
# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py3_install
mkdir -p %{buildroot}%{_datadir}/drgn
cp -PR contrib tools %{buildroot}%{_datadir}/drgn

%if %{with tests}
%check
%pytest
%endif

%files -n %{pypi_name}
%license COPYING
%license LICENSES
%doc README.rst
%{_bindir}/drgn
%{_datadir}/drgn
%{python3_sitearch}/_%{pypi_name}.pyi
%{python3_sitearch}/_%{pypi_name}.cpython*.so
%{python3_sitearch}/%{pypi_name}
%{python3_sitearch}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%if %{with docs}
%files -n %{pypi_name}-doc
%license COPYING
%license LICENSES
%doc html
%endif

%changelog
* Mon Oct 23 2023 Davide Cavalca <dcavalca@centosproject.org> - 0.0.24-2
- Import changelog from the EPEL package
- Add gating.yaml to RHEL-9 python-drgn

* Tue Oct 10 2023 Tao Liu <ltao@redhat.com> - 0.0.24-1
- Import epel9 python-drgn to rhel9

* Fri Sep 08 2023 Omar Sandoval <osandov@osandov.com> - 0.0.24-1
- Update to 0.0.24; Fixes: RHBZ#2238043

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.23-2
- Rebuilt for Python 3.12; Fixes: RHBZ#2220199

* Wed Jun 28 2023 Omar Sandoval <osandov@osandov.com> - 0.0.23-1
- Update to 0.0.23; Fixes: RHBZ#2218383

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.0.22-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 06 2023 Omar Sandoval <osandov@osandov.com> - 0.0.22-1
- Update to 0.0.22

* Wed Oct 12 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.21-1
- Update to 0.0.21; Fixes: RHBZ#2134210

* Sat Aug 06 2022 Michel Alexandre Salim <michel@michel-slm.name> - 0.0.20-2
- Rebuilt for libkdumpfile.so.10

* Tue Jul 26 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.20-1
- Update to 0.0.20; Fixes: RHBZ#2110808

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.0.19-2
- Rebuilt for Python 3.11

* Wed May 18 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.19-1
- Update to 0.0.19; Fixes: RHBZ#2088180

* Thu Apr 21 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.0.18-3
- Rebuild for libkdumpfile 0.4.1

* Sun Mar 06 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.18-2
- Backport fix for armv7hl

* Sun Mar 06 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.18-1
- Update to 0.0.18; Fixes: RHBZ#2060295, RHBZ#2046872

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 09 2021 Omar Sandoval <osandov@osandov.com> - 0.0.16-1
- Update to 0.0.16

* Thu Dec 09 2021 Omar Sandoval <osandov@osandov.com> - 0.0.15-1
- Update to 0.0.15

* Tue Oct 26 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.14-2
- Add support for building from git snapshots for packit

* Thu Aug 12 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.14-1
- Update to 0.0.14; Fixes: RHBZ#1993354

* Thu Aug 12 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.13-6
- Update descriptions

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.13-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun  8 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.13-2
- Backport fix for s390x and drop the ExcludeArch

* Tue Jun  8 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.13-1
- Update to 0.0.13
- Drop no longer needed ExcludeArch for armv7hl and i686

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.0.11-3
- Rebuilt for Python 3.10

* Tue Apr  6 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.11-2
- Make doc subpackage noarch
- Add license file

* Tue Apr  6 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.0.11-1
- Initial package.
