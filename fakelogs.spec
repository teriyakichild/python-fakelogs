%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define module_name fakelogs

Name:           %{module_name}
Version:        0.1.0
Release:        1
Summary:        fakelogs - library to generate fake logs

License:        ASLv2
URL:            https://github.com/teriyakichild/python-fakelogs
Source0:        %{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools


%description

%prep
%setup -q -n %{module_name}-%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%doc README.md
%{python_sitelib}/*
%attr(0755,-,-) %{_bindir}/fakelogs

%changelog
* Fri Jul 12 2019 Tony Rogers <tony.rogers@logdna.com> - 0.1.0
- First kinda stable release
* Mon Jul 8 2019 Tony Rogers <tony.rogers@logdna.com> - 0.0.1
- Initial spec
