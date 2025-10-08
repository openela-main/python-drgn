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
Version:        0.0.29
Release:        1%{?dist}
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
%{python3_sitearch}/_%{pypi_name}_util
%{python3_sitearch}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%if %{with docs}
%files -n %{pypi_name}-doc
%license COPYING
%license LICENSES
%doc html
%endif

%changelog
* Mon Nov 11 2024 Philipp Rudo <prudo@redhat.com> - 0.0.29-1
- Rebase to upstream v0.0.29
  Resolves: RHEL-61657

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 0.0.25-8
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Thu Aug 8 2024 Tao Liu <ltao@redhat.com> - 0.0.25-7
- Enable brew-build.tier0.functional test
- Remove autorelease and autochangelog

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 0.0.25-6
- Bump release for June 2024 mass rebuild

* Wed May 15 2024 Tao Liu <ltao@redhat.com> - 0.0.25-5
- Remove brew-build.tier0.functional test

* Thu May 02 2024 Philipp Rudo <prudo@redhat.com> - 0.0.25-4
- Add gating.yaml to RHEL-10 python-drgn

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Omar Sandoval <osandov@osandov.com> - 0.0.25-1
- Update to 0.0.25; Fixes: RHBZ#2252482

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
